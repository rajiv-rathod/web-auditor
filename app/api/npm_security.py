from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import requests
import json
import subprocess
import os
import tempfile

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import ScanResponse, ScanCreate, NPMAuditRequest, DependencyCheckRequest, LicenseScanRequest, OutdatedPackagesRequest

router = APIRouter()

@router.post("/npm-audit")
async def npm_security_audit(
    request: NPMAuditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Perform npm security audit on package.json content"""
    
    try:
        # Create temporary directory for npm audit
        with tempfile.TemporaryDirectory() as temp_dir:
            package_json_path = os.path.join(temp_dir, "package.json")
            
            # Write package.json content to temporary file
            with open(package_json_path, 'w') as f:
                f.write(request.package_json_content)
            
            # Run npm audit command
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            audit_output = {}
            if result.stdout:
                try:
                    audit_output = json.loads(result.stdout)
                except json.JSONDecodeError:
                    audit_output = {"error": "Failed to parse npm audit output"}
            
            return {
                "status": "completed",
                "audit_results": audit_output,
                "vulnerabilities_found": audit_output.get("metadata", {}).get("vulnerabilities", {}).get("total", 0),
                "summary": audit_output.get("metadata", {})
            }
            
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="npm audit timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"npm audit failed: {str(e)}")

@router.post("/dependency-check")
async def dependency_vulnerability_check(
    request: DependencyCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Check specific dependencies for known vulnerabilities"""
    
    try:
        results = []
        
        for dependency in request.dependencies:
            # Use npm view to get package information
            result = subprocess.run(
                ["npm", "view", dependency, "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    package_info = json.loads(result.stdout)
                    results.append({
                        "package": dependency,
                        "latest_version": package_info.get("version"),
                        "description": package_info.get("description"),
                        "author": package_info.get("author"),
                        "license": package_info.get("license"),
                        "last_modified": package_info.get("time", {}).get("modified"),
                        "status": "found"
                    })
                except json.JSONDecodeError:
                    results.append({
                        "package": dependency,
                        "status": "error",
                        "error": "Failed to parse package information"
                    })
            else:
                results.append({
                    "package": dependency,
                    "status": "not_found"
                })
        
        return {
            "status": "completed",
            "checked_packages": len(request.dependencies),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dependency check failed: {str(e)}")

@router.post("/license-scan")
async def license_compliance_scan(
    request: LicenseScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Scan dependencies for license compliance issues"""
    
    try:
        # Parse package.json
        package_data = json.loads(request.package_json_content)
        dependencies = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
        
        license_results = []
        
        for package_name, version in dependencies.items():
            # Get package license information
            result = subprocess.run(
                ["npm", "view", package_name, "license", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    license_info = json.loads(result.stdout) if result.stdout.strip() != '""' else "Unknown"
                    
                    # Classify license risk
                    risk_level = "low"
                    if license_info in ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]:
                        risk_level = "high"
                    elif license_info in ["LGPL-2.1", "LGPL-3.0"]:
                        risk_level = "medium"
                    
                    license_results.append({
                        "package": package_name,
                        "version": version,
                        "license": license_info,
                        "risk_level": risk_level
                    })
                except json.JSONDecodeError:
                    license_results.append({
                        "package": package_name,
                        "version": version,
                        "license": "Unknown",
                        "risk_level": "unknown"
                    })
        
        # Summarize results
        risk_summary = {
            "high": sum(1 for r in license_results if r["risk_level"] == "high"),
            "medium": sum(1 for r in license_results if r["risk_level"] == "medium"),
            "low": sum(1 for r in license_results if r["risk_level"] == "low"),
            "unknown": sum(1 for r in license_results if r["risk_level"] == "unknown")
        }
        
        return {
            "status": "completed",
            "total_packages": len(license_results),
            "risk_summary": risk_summary,
            "license_details": license_results
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid package.json content")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"License scan failed: {str(e)}")

@router.post("/outdated-packages")
async def check_outdated_packages(
    request: OutdatedPackagesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Check for outdated packages in package.json"""
    
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            package_json_path = os.path.join(temp_dir, "package.json")
            
            # Write package.json content
            with open(package_json_path, 'w') as f:
                f.write(request.package_json_content)
            
            # Run npm outdated command
            result = subprocess.run(
                ["npm", "outdated", "--json"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            outdated_packages = {}
            if result.stdout:
                try:
                    outdated_packages = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass
            
            # Format results
            formatted_results = []
            for package_name, info in outdated_packages.items():
                formatted_results.append({
                    "package": package_name,
                    "current": info.get("current"),
                    "wanted": info.get("wanted"),
                    "latest": info.get("latest"),
                    "location": info.get("location", "")
                })
            
            return {
                "status": "completed",
                "outdated_count": len(formatted_results),
                "outdated_packages": formatted_results
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outdated packages check failed: {str(e)}")

@router.get("/package-info/{package_name}")
async def get_package_info(
    package_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get detailed information about a specific npm package"""
    
    try:
        # Get package information from npm
        result = subprocess.run(
            ["npm", "view", package_name, "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=404, detail=f"Package '{package_name}' not found")
        
        package_info = json.loads(result.stdout)
        
        # Extract relevant information
        return {
            "name": package_info.get("name"),
            "version": package_info.get("version"),
            "description": package_info.get("description"),
            "author": package_info.get("author"),
            "license": package_info.get("license"),
            "homepage": package_info.get("homepage"),
            "repository": package_info.get("repository"),
            "keywords": package_info.get("keywords", []),
            "dependencies": package_info.get("dependencies", {}),
            "devDependencies": package_info.get("devDependencies", {}),
            "downloads": package_info.get("dist", {}).get("npm-download-count"),
            "last_modified": package_info.get("time", {}).get("modified"),
            "maintainers": package_info.get("maintainers", [])
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse package information")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get package info: {str(e)}")