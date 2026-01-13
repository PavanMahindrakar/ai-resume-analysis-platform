"""Dashboard request and response schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MissingSkillStat(BaseModel):
    """Statistics for a missing skill."""
    
    skill: str = Field(..., description="Missing skill keyword")
    count: int = Field(..., description="Number of times this skill was missing")
    frequency: float = Field(..., description="Frequency as percentage (0-100)")


class DashboardSummaryResponse(BaseModel):
    """Summary statistics for user's dashboard."""
    
    total_analyses: int = Field(..., description="Total number of analyses performed")
    average_match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Average match score across all analyses (0-100)"
    )
    highest_match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Highest match score achieved"
    )
    lowest_match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Lowest match score achieved"
    )
    most_common_missing_skills: list[MissingSkillStat] = Field(
        ...,
        description="Top missing skills across all analyses, ordered by frequency"
    )


class AnalysisHistoryItem(BaseModel):
    """Single analysis result in history."""
    
    id: UUID = Field(..., description="Analysis result ID")
    resume_id: UUID = Field(..., description="Resume ID used in analysis")
    job_description_id: UUID = Field(..., description="Job description ID used in analysis")
    match_score: float = Field(..., description="Match score (0-100)")
    created_at: datetime = Field(..., description="When the analysis was performed")
    
    class Config:
        from_attributes = True


class DashboardHistoryResponse(BaseModel):
    """History of user's analyses."""
    
    analyses: list[AnalysisHistoryItem] = Field(..., description="List of past analyses")
    total: int = Field(..., description="Total number of analyses")

