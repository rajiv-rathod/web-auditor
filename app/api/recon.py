from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import (
    SubdomainScanRequest, 
    PortScanRequest, 
    DNSLookupRequest
)
from app.services.recon_service import (
    ReconService,
    DNSService,
    WhoisService
)

router = APIRouter()

@router.post("/subdomain")
async def subdomain_enumeration(
    request: SubdomainScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Perform subdomain enumeration"""
    
    try:
        recon_service = ReconService()
        results = await recon_service.enumerate_subdomains(
            domain=request.domain,
            tools=request.tools
        )
        
        return {
            "domain": request.domain,
            "tools_used": request.tools,
            "subdomains": results.get("subdomains", []),
            "total_found": len(results.get("subdomains", [])),
            "live_subdomains": results.get("live_subdomains", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/port-scan")
async def port_scanning(
    request: PortScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Perform port scanning"""
    
    try:
        recon_service = ReconService()
        results = await recon_service.port_scan(
            target=request.target,
            scan_type=request.scan_type,
            ports=request.ports
        )
        
        return {
            "target": request.target,
            "scan_type": request.scan_type,
            "open_ports": results.get("open_ports", []),
            "services": results.get("services", {}),
            "total_ports_scanned": results.get("total_scanned", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dns-lookup")
async def dns_lookup(
    request: DNSLookupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Perform DNS lookup"""
    
    try:
        dns_service = DNSService()
        results = await dns_service.lookup(
            domain=request.domain,
            record_type=request.record_type
        )
        
        return {
            "domain": request.domain,
            "record_type": request.record_type,
            "records": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/whois/{domain}")
async def whois_lookup(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Perform WHOIS lookup"""
    
    try:
        whois_service = WhoisService()
        results = await whois_service.lookup(domain)
        
        return {
            "domain": domain,
            "whois_data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tech-stack/{url}")
async def tech_stack_detection(
    url: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Detect technology stack"""
    
    try:
        recon_service = ReconService()
        results = await recon_service.detect_tech_stack(url)
        
        return {
            "url": url,
            "technologies": results.get("technologies", []),
            "cms": results.get("cms", None),
            "web_server": results.get("web_server", None),
            "programming_languages": results.get("programming_languages", []),
            "frameworks": results.get("frameworks", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))