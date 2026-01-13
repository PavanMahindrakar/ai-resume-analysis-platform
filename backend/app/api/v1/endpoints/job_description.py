"""Job description endpoints."""
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas import (
    JobDescriptionCreateRequest,
    JobDescriptionResponse,
)
from app.core.dependencies import CurrentUserDep, DBSessionDep
from app.infrastructure.database.models import JobDescription

router = APIRouter(tags=["job_description"])


@router.post(
    "/job-description/create",
    response_model=JobDescriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create job description",
    description="Accepts job title and description text, stores it, and associates it with the authenticated user.",
)
async def create_job_description(
    payload: JobDescriptionCreateRequest,
    current_user: CurrentUserDep,
    db: DBSessionDep,
) -> JobDescriptionResponse:
    """Create a job description tied to the current user."""
    job_desc = JobDescription(
        user_id=current_user.id,
        title=payload.title,
        description=payload.description,
    )

    db.add(job_desc)
    db.commit()
    db.refresh(job_desc)

    return JobDescriptionResponse.model_validate(job_desc)


@router.get(
    "/job-descriptions",
    response_model=List[JobDescriptionResponse],
    summary="Get user's job descriptions",
    description="Get a list of all job descriptions created by the authenticated user",
)
async def get_job_descriptions(
    current_user: CurrentUserDep,
    db: DBSessionDep,
) -> List[JobDescriptionResponse]:
    """Get all job descriptions for the current user."""
    job_descriptions = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.id
    ).order_by(JobDescription.created_at.desc()).all()
    
    return [JobDescriptionResponse.model_validate(jd) for jd in job_descriptions]
