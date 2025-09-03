from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.models import User, Scan, ScanStatus
from app.schemas.schemas import ScanCreate, ScanResponse
from app.services.tasks import subdomain_scan, port_scan, tech_stack_scan

router = APIRouter()

@router.post("/", response_model=ScanResponse)
async def create_scan(
    scan: ScanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new scan job"""
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Create scan record
    db_scan = Scan(
        target=scan.target,
        scan_type=scan.scan_type,
        task_id=task_id,
        user_id=current_user.id,
        status=ScanStatus.PENDING
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    
    # Start appropriate background task
    if scan.scan_type == "subdomain":
        subdomain_scan.delay(db_scan.id, scan.target)
    elif scan.scan_type == "port_scan":
        port_scan.delay(db_scan.id, scan.target)
    elif scan.scan_type == "tech_stack":
        tech_stack_scan.delay(db_scan.id, scan.target)
    else:
        # Update scan status to failed
        db_scan.status = ScanStatus.FAILED
        db_scan.error_message = f"Unsupported scan type: {scan.scan_type}"
        db.commit()
        raise HTTPException(status_code=400, detail=f"Unsupported scan type: {scan.scan_type}")
    
    return db_scan

@router.get("/", response_model=List[ScanResponse])
async def get_scans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's scans"""
    scans = db.query(Scan).filter(
        Scan.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return scans

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific scan by ID"""
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.user_id == current_user.id
    ).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan

@router.delete("/{scan_id}")
async def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a scan"""
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.user_id == current_user.id
    ).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(scan)
    db.commit()
    
    return {"message": "Scan deleted successfully"}