from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, scans, recon, vulnerability
from app.core.config import settings
from app.core.database import engine
from app.models import models
import uvicorn

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Web Auditor",
    description="Comprehensive Web Security Auditing Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(recon.router, prefix="/api/recon", tags=["reconnaissance"])
app.include_router(vulnerability.router, prefix="/api/vulnerability", tags=["vulnerability"])

@app.get("/")
async def root():
    return {"message": "Web Auditor API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)