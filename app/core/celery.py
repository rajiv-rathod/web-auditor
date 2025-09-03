from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "web-auditor",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.services.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.services.tasks.subdomain_scan": {"queue": "recon"},
        "app.services.tasks.port_scan": {"queue": "recon"},
        "app.services.tasks.vulnerability_scan": {"queue": "vuln"},
        "app.services.tasks.sql_injection_scan": {"queue": "vuln"},
    }
)