"""Health check endpoints."""
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.core.dependencies import SettingsDep

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(settings: Annotated[Settings, SettingsDep]) -> dict:
    """Health check endpoint.
    
    Args:
        settings: Application settings
        
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
