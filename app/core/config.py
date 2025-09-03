from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./webauditor.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys for external services
    DEHASHED_API_KEY: Optional[str] = None
    VIRUSTOTAL_API_KEY: Optional[str] = None
    
    # File paths
    SCAN_RESULTS_PATH: str = "/scans"
    REPORTS_PATH: str = "/reports"
    WORDLISTS_PATH: str = "/wordlists"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()