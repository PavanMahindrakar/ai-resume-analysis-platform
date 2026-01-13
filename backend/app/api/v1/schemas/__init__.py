"""API schemas."""
from app.api.v1.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.api.v1.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.api.v1.schemas.dashboard import (
    AnalysisHistoryItem,
    DashboardHistoryResponse,
    DashboardSummaryResponse,
    MissingSkillStat,
)
from app.api.v1.schemas.resume import ResumeUploadResponse
from app.api.v1.schemas.job_description import (
    JobDescriptionCreateRequest,
    JobDescriptionResponse,
)

__all__ = [
    "UserRegisterRequest",
    "UserLoginRequest",
    "TokenResponse",
    "UserResponse",
    "ResumeUploadResponse",
    "JobDescriptionCreateRequest",
    "JobDescriptionResponse",
    "AnalysisRequest",
    "AnalysisResponse",
    "DashboardSummaryResponse",
    "DashboardHistoryResponse",
    "AnalysisHistoryItem",
    "MissingSkillStat",
]
