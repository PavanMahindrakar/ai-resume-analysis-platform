"""Resume upload schemas."""
from uuid import UUID

from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume."""

    id: UUID = Field(..., description="Resume ID")
    file_name: str = Field(..., description="Stored file name")
    content_type: str = Field(..., description="MIME type of uploaded file")
    text_length: int = Field(..., description="Length of extracted text")

    class Config:
        from_attributes = True
