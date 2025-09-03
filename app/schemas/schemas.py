from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.models import ScanType, ScanStatus

# User schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Scan schemas
class ScanBase(BaseModel):
    target: str
    scan_type: ScanType

class ScanCreate(ScanBase):
    pass

class ScanResponse(ScanBase):
    id: int
    status: ScanStatus
    task_id: str
    results: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    user_id: int
    
    class Config:
        from_attributes = True

# Vulnerability schemas
class VulnerabilityBase(BaseModel):
    vulnerability_type: str
    severity: str
    description: str
    url: str
    recommendation: str

class VulnerabilityCreate(VulnerabilityBase):
    scan_id: int
    payload: Optional[str] = None
    parameter: Optional[str] = None
    cvss_score: Optional[str] = None

class Vulnerability(VulnerabilityBase):
    id: int
    scan_id: int
    payload: Optional[str] = None
    parameter: Optional[str] = None
    cvss_score: Optional[str] = None
    
    class Config:
        from_attributes = True

# Recon schemas
class SubdomainScanRequest(BaseModel):
    domain: str
    tools: List[str] = ["subfinder", "amass"]

class PortScanRequest(BaseModel):
    target: str
    scan_type: str = "fast"  # fast, full, custom
    ports: Optional[str] = None

class DNSLookupRequest(BaseModel):
    domain: str
    record_type: str = "A"  # A, AAAA, MX, TXT, NS, CNAME

# Vulnerability scan schemas
class SQLInjectionScanRequest(BaseModel):
    url: str
    parameters: Optional[List[str]] = None
    cookie: Optional[str] = None
    user_agent: Optional[str] = None

class XSSScanRequest(BaseModel):
    url: str
    parameters: Optional[List[str]] = None
    payloads: Optional[List[str]] = None

class DirectoryBruteforceRequest(BaseModel):
    url: str
    wordlist: str = "common"
    extensions: List[str] = ["php", "html", "js", "txt"]
    threads: int = 10

# Results schemas
class ScanResult(BaseModel):
    scan_id: int
    results: Dict[str, Any]
    vulnerabilities: List[Vulnerability] = []

class ReportRequest(BaseModel):
    scan_id: int
    format: str = "pdf"  # pdf, html, json

# NPM Security schemas
class NPMAuditRequest(BaseModel):
    package_json_content: str

class DependencyCheckRequest(BaseModel):
    dependencies: List[str]

class LicenseScanRequest(BaseModel):
    package_json_content: str

class OutdatedPackagesRequest(BaseModel):
    package_json_content: str

class NPMPackageInfo(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = None
    homepage: Optional[str] = None
    repository: Optional[Dict[str, Any]] = None
    keywords: List[str] = []
    dependencies: Dict[str, str] = {}
    devDependencies: Dict[str, str] = {}
    downloads: Optional[int] = None
    last_modified: Optional[str] = None
    maintainers: List[Dict[str, Any]] = []