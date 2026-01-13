"""Job description schemas."""
from uuid import UUID

from pydantic import BaseModel, Field


class JobDescriptionCreateRequest(BaseModel):
    """Request body for creating a job description."""

    title: str = Field(..., min_length=2, max_length=255, description="Job title")
    description: str = Field(..., min_length=10, description="Job description text")


class JobDescriptionResponse(BaseModel):
    """Response model for job description."""

    id: UUID = Field(..., description="Job description ID")
    title: str = Field(..., description="Job title")
    description: str = Field(..., description="Job description text")

    class Config:
        from_attributes = True
