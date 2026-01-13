"""Analysis request and response schemas."""
from uuid import UUID

from pydantic import BaseModel, Field


class MatchedKeywordDetail(BaseModel):
    """Details of a matched keyword."""
    
    resume_keyword: str = Field(..., description="Keyword found in resume")
    score: float = Field(..., description="Importance score of the match")
    match_type: str = Field(..., description="Type of match: 'exact' or 'partial'")


class AnalysisRequest(BaseModel):
    """Request schema for running resume analysis.
    
    Flow:
    1. User selects resume (resume_id)
    2. User selects job description (job_description_id)
    3. System runs AI matching engine
    4. Results are stored in database
    5. Response includes score, missing skills, and explanation
    """
    
    resume_id: UUID = Field(
        ...,
        description="ID of the resume to analyze (must belong to authenticated user)"
    )
    job_description_id: UUID = Field(
        ...,
        description="ID of the job description to match against (must belong to authenticated user)"
    )


class AnalysisResponse(BaseModel):
    """Response schema for analysis results.
    
    Contains the complete analysis result including:
    - Overall match score (0-100%)
    - Matched keywords with details
    - Missing keywords from job description
    - Human-readable explanation
    """
    
    id: UUID = Field(..., description="Analysis result ID (for future reference)")
    resume_id: UUID = Field(..., description="Resume ID that was analyzed")
    job_description_id: UUID = Field(..., description="Job description ID used for matching")
    match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Match score as percentage (0-100). Higher is better."
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the match, including matched skills, "
                    "missing skills, and recommendations"
    )
    matched_keywords: dict[str, MatchedKeywordDetail] = Field(
        ...,
        description="Dictionary of matched keywords. Key is job keyword, value contains "
                    "resume keyword, score, and match type."
    )
    missing_keywords: list[str] = Field(
        ...,
        description="List of keywords from job description that were not found in resume. "
                    "These represent skills/requirements the candidate may be missing."
    )
    
    class Config:
        from_attributes = True
