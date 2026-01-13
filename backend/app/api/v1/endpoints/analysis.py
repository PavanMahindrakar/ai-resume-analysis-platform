"""Analysis endpoints for resume-to-job-description matching."""
import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas import AnalysisRequest, AnalysisResponse
from app.api.v1.schemas.analysis import MatchedKeywordDetail
from app.core.dependencies import CurrentUserDep, DBSessionDep
from app.infrastructure.ai.matching_engine import MatchingEngine
from app.infrastructure.database.models import AnalysisResult, JobDescription, Resume

router = APIRouter(prefix="/analysis", tags=["analysis"])

# Initialize matching engine
matching_engine = MatchingEngine()


@router.post(
    "/run",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Run resume analysis",
    description="Analyze a resume against a job description using explainable matching logic",
)
async def run_analysis(
    request: AnalysisRequest,
    current_user: CurrentUserDep,
    db: DBSessionDep,
) -> AnalysisResponse:
    """Run analysis of resume against job description.
    
    This endpoint:
    1. Validates that resume and job description belong to the user
    2. Extracts text from both documents
    3. Runs the explainable matching engine
    4. Stores results in database
    5. Returns analysis results
    
    Args:
        request: Analysis request with resume_id and job_description_id
        current_user: Authenticated user
        db: Database session
        
    Returns:
        AnalysisResponse: Analysis results with match score and explanation
        
    Raises:
        HTTPException: If resume/job not found or doesn't belong to user
    """
    # Fetch resume and validate ownership
    resume = db.query(Resume).filter(
        Resume.id == request.resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access denied",
        )
    
    if not resume.text_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has no text content to analyze",
        )
    
    # Fetch job description and validate ownership
    job_description = db.query(JobDescription).filter(
        JobDescription.id == request.job_description_id,
        JobDescription.user_id == current_user.id
    ).first()
    
    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access denied",
        )
    
    # Run matching engine (this is CPU-bound, but fast enough for async)
    # In production, you might want to run this in a background task
    analysis_result = matching_engine.analyze(
        resume_text=resume.text_content,
        job_description_text=job_description.description
    )
    
    # Store results in database
    db_result = AnalysisResult(
        resume_id=resume.id,
        job_description_id=job_description.id,
        user_id=current_user.id,
        match_score=analysis_result["match_score"],
        matched_keywords=json.dumps(analysis_result["matched_keywords"]),
        missing_keywords=json.dumps(analysis_result["missing_keywords"]),
        explanation=analysis_result["explanation"],
    )
    
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    # Parse stored JSON back for response
    matched_keywords_dict = json.loads(db_result.matched_keywords or "{}")
    
    # Convert matched keywords to proper format with validation
    formatted_matched_keywords = {}
    for job_keyword, match_info in matched_keywords_dict.items():
        if isinstance(match_info, dict):
            formatted_matched_keywords[job_keyword] = MatchedKeywordDetail(
                resume_keyword=match_info.get("resume_keyword", job_keyword),
                score=float(match_info.get("score", 0.0)),
                match_type=match_info.get("match_type", "exact")
            )
    
    return AnalysisResponse(
        id=db_result.id,
        resume_id=db_result.resume_id,
        job_description_id=db_result.job_description_id,
        match_score=db_result.match_score,
        explanation=db_result.explanation or "",
        matched_keywords=formatted_matched_keywords,
        missing_keywords=json.loads(db_result.missing_keywords or "[]"),
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
    summary="Get analysis result",
    description="Retrieve a specific analysis result by ID",
)
async def get_analysis(
    analysis_id: UUID,
    current_user: CurrentUserDep,
    db: DBSessionDep,
) -> AnalysisResponse:
    """Get a specific analysis result by ID.
    
    Args:
        analysis_id: UUID of the analysis result
        current_user: Authenticated user
        db: Database session
        
    Returns:
        AnalysisResponse: Analysis results
        
    Raises:
        HTTPException: If analysis not found or doesn't belong to user
    """
    # Fetch analysis result and validate ownership
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.id == analysis_id,
        AnalysisResult.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis result not found or access denied",
        )
    
    # Parse stored JSON back for response
    matched_keywords_dict = json.loads(analysis.matched_keywords or "{}")
    
    # Convert matched keywords to proper format with validation
    formatted_matched_keywords = {}
    for job_keyword, match_info in matched_keywords_dict.items():
        if isinstance(match_info, dict):
            formatted_matched_keywords[job_keyword] = MatchedKeywordDetail(
                resume_keyword=match_info.get("resume_keyword", job_keyword),
                score=float(match_info.get("score", 0.0)),
                match_type=match_info.get("match_type", "exact")
            )
    
    return AnalysisResponse(
        id=analysis.id,
        resume_id=analysis.resume_id,
        job_description_id=analysis.job_description_id,
        match_score=analysis.match_score,
        explanation=analysis.explanation or "",
        matched_keywords=formatted_matched_keywords,
        missing_keywords=json.loads(analysis.missing_keywords or "[]"),
    )
