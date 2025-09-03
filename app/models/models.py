from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ScanType(str, enum.Enum):
    SUBDOMAIN = "subdomain"
    PORT_SCAN = "port_scan"
    VULNERABILITY = "vulnerability"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    DIRECTORY_BRUTEFORCE = "directory_bruteforce"
    CMS_SCAN = "cms_scan"
    TECH_STACK = "tech_stack"

class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    scans = relationship("Scan", back_populates="user")

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, index=True)
    scan_type = Column(Enum(ScanType))
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING)
    task_id = Column(String, unique=True, index=True)
    results = Column(Text)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="scans")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    vulnerability_type = Column(String)
    severity = Column(String)
    description = Column(Text)
    payload = Column(Text)
    url = Column(String)
    parameter = Column(String)
    cvss_score = Column(String)
    recommendation = Column(Text)
    
    scan = relationship("Scan")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    report_type = Column(String)  # PDF, HTML, JSON
    file_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    scan = relationship("Scan")