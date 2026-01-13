"""API v1 endpoints."""
from app.api.v1.endpoints import analysis, auth, dashboard, health, job_description, resume

__all__ = ["health", "auth", "resume", "job_description", "analysis", "dashboard"]
