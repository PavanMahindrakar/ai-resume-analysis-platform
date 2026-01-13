"""API v1 router."""
from fastapi import APIRouter

from app.api.v1.endpoints import analysis, auth, dashboard, health, job_description, resume
from app.core.config import get_settings

settings = get_settings()

api_router = APIRouter(prefix=settings.API_V1_PREFIX)

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(resume.router)
api_router.include_router(job_description.router)
api_router.include_router(analysis.router)
api_router.include_router(dashboard.router)