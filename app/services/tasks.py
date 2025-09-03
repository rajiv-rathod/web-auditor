from celery import current_app as celery_app
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import Scan, ScanStatus
from app.services.recon_service import ReconService
from app.services.vulnerability_service import SQLInjectionService
import json
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@celery_app.task
def subdomain_scan(scan_id: int, domain: str):
    """Celery task for subdomain enumeration"""
    db = SessionLocal()
    try:
        # Update scan status
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return {"error": "Scan not found"}
        
        scan.status = ScanStatus.RUNNING
        db.commit()
        
        # Perform subdomain enumeration
        recon_service = ReconService()
        results = recon_service.enumerate_subdomains_sync(domain, ["subfinder"])
        
        # Update scan with results
        scan.results = json.dumps(results)
        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.utcnow()
        db.commit()
        
        return results
        
    except Exception as e:
        # Update scan with error
        scan.status = ScanStatus.FAILED
        scan.error_message = str(e)
        db.commit()
        return {"error": str(e)}
    finally:
        db.close()

@celery_app.task
def port_scan(scan_id: int, target: str):
    """Celery task for port scanning"""
    db = SessionLocal()
    try:
        # Update scan status
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return {"error": "Scan not found"}
        
        scan.status = ScanStatus.RUNNING
        db.commit()
        
        # Perform port scan
        recon_service = ReconService()
        results = recon_service.port_scan_sync(target, "fast")
        
        # Update scan with results
        scan.results = json.dumps(results)
        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.utcnow()
        db.commit()
        
        return results
        
    except Exception as e:
        # Update scan with error
        scan.status = ScanStatus.FAILED
        scan.error_message = str(e)
        db.commit()
        return {"error": str(e)}
    finally:
        db.close()

@celery_app.task
def tech_stack_scan(scan_id: int, url: str):
    """Celery task for technology stack detection"""
    db = SessionLocal()
    try:
        # Update scan status
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return {"error": "Scan not found"}
        
        scan.status = ScanStatus.RUNNING
        db.commit()
        
        # Perform tech stack detection
        recon_service = ReconService()
        results = recon_service.detect_tech_stack_sync(url)
        
        # Update scan with results
        scan.results = json.dumps(results)
        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.utcnow()
        db.commit()
        
        return results
        
    except Exception as e:
        # Update scan with error
        scan.status = ScanStatus.FAILED
        scan.error_message = str(e)
        db.commit()
        return {"error": str(e)}
    finally:
        db.close()

@celery_app.task
def sql_injection_scan(scan_id: int, url: str):
    """Celery task for SQL injection testing"""
    db = SessionLocal()
    try:
        # Update scan status
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return {"error": "Scan not found"}
        
        scan.status = ScanStatus.RUNNING
        db.commit()
        
        # Perform SQL injection scan
        sql_service = SQLInjectionService()
        results = sql_service.scan_sync(url)
        
        # Update scan with results
        scan.results = json.dumps(results)
        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.utcnow()
        db.commit()
        
        return results
        
    except Exception as e:
        # Update scan with error
        scan.status = ScanStatus.FAILED
        scan.error_message = str(e)
        db.commit()
        return {"error": str(e)}
    finally:
        db.close()