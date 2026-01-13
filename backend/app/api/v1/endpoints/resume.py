"""Resume upload endpoints."""
from pathlib import Path
from uuid import uuid4
from typing import List

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.api.v1.schemas import ResumeUploadResponse
from app.core.dependencies import CurrentUserDep, DBSessionDep, SettingsDep
from app.infrastructure.database.models import Resume
from app.infrastructure.storage.pdf import extract_text_from_pdf_bytes

router = APIRouter(tags=["resume"])


@router.post(
    "/resume/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a resume PDF",
    description="Accepts a PDF file, stores it, extracts text, and associates it with the authenticated user.",
)
async def upload_resume(
    current_user: CurrentUserDep,
    db: DBSessionDep,
    settings: SettingsDep,
    file: UploadFile = File(..., description="PDF resume file"),
) -> ResumeUploadResponse:
    """Upload a PDF resume and store extracted text."""
    # Validate file type
    if not file.content_type or "pdf" not in file.content_type.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    # Prepare storage directory
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file with unique name
    stored_name = f"{uuid4()}_{file.filename}"
    stored_path = upload_dir / stored_name
    async with aiofiles.open(stored_path, "wb") as out_file:
        await out_file.write(file_bytes)

    # Extract text from PDF (blocking parse done in threadpool)
    try:
        extracted_text = await extract_text_from_pdf_bytes(file_bytes)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failed to extract text from PDF.",
        ) from exc

    # Persist resume record
    resume = Resume(
        user_id=current_user.id,
        file_name=stored_name,
        file_path=str(stored_path),
        content_type=file.content_type or "application/pdf",
        text_content=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeUploadResponse(
        id=resume.id,
        file_name=resume.file_name,
        content_type=resume.content_type,
        text_length=len(resume.text_content or ""),
    )


# GET endpoint for listing resumes (without prefix to match frontend expectation)
@router.get(
    "/resumes",
    response_model=List[ResumeUploadResponse],
    summary="Get user's resumes",
    description="Get a list of all resumes uploaded by the authenticated user",
    include_in_schema=True,
)
async def get_resumes(
    current_user: CurrentUserDep,
    db: DBSessionDep,
) -> List[ResumeUploadResponse]:
    """Get all resumes for the current user."""
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(Resume.created_at.desc()).all()
    
    return [
        ResumeUploadResponse(
            id=resume.id,
            file_name=resume.file_name,
            content_type=resume.content_type,
            text_length=len(resume.text_content or ""),
        )
        for resume in resumes
    ]
