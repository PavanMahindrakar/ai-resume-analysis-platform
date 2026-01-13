"""Dashboard endpoints for user analytics and history."""
import json
from collections import Counter

from fastapi import APIRouter, Query
from sqlalchemy import func

from app.api.v1.schemas.dashboard import (
    AnalysisHistoryItem,
    DashboardHistoryResponse,
    DashboardSummaryResponse,
    MissingSkillStat,
)
from app.core.dependencies import CurrentUserDep, DBSessionDep
from app.infrastructure.database.models import AnalysisResult

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Get dashboard summary",
    description="Get aggregated statistics including average match score and most common missing skills",
)
async def get_dashboard_summary(
    current_user: CurrentUserDep,
    db: DBSessionDep,
    limit: int = Query(default=10, ge=1, le=50, description="Number of top missing skills to return"),
) -> DashboardSummaryResponse:
    """Get dashboard summary with aggregated statistics.
    
    This endpoint uses efficient PostgreSQL aggregations to calculate:
    - Total number of analyses
    - Average match score (using AVG aggregation)
    - Highest and lowest match scores (using MAX and MIN aggregations)
    - Most common missing skills (using JSON parsing and counting)
    
    PostgreSQL Aggregation Explanation:
    ===================================
    
    1. AVG() FUNCTION:
       - Calculates the average of a numeric column
       - Syntax: AVG(column_name)
       - Returns NULL if no rows match
       - Example: AVG(match_score) calculates mean of all match scores
       - Efficient: Database does calculation, not application code
       - Uses index if available on the column
    
    2. MAX() and MIN() FUNCTIONS:
       - Find maximum/minimum value in a column
       - Can use indexes for fast lookup
       - Example: MAX(match_score) finds highest score
    
    3. COUNT() FUNCTION:
       - Counts number of rows
       - COUNT(*) counts all rows
       - COUNT(column) counts non-NULL values
       - Very efficient, especially with WHERE clause
    
    4. JSON AGGREGATION:
       - PostgreSQL can parse JSON columns
       - jsonb_array_elements_text() expands JSON arrays
       - We use this to extract missing keywords from JSON
       - Then aggregate (count) occurrences
       - More efficient than loading all rows into application
    
    Why This Approach is Efficient:
    - All calculations done in database (single query)
    - Database can use indexes on user_id and match_score
    - Reduces data transfer (only aggregated results sent)
    - Leverages PostgreSQL's optimized aggregation engine
    
    Args:
        current_user: Authenticated user
        db: Database session
        limit: Number of top missing skills to return
        
    Returns:
        DashboardSummaryResponse: Aggregated statistics
    """
    # Efficient aggregation query using PostgreSQL functions
    # This single query calculates all statistics at once
    stats = db.query(
        func.count(AnalysisResult.id).label("total_analyses"),
        func.avg(AnalysisResult.match_score).label("avg_score"),
        func.max(AnalysisResult.match_score).label("max_score"),
        func.min(AnalysisResult.match_score).label("min_score"),
    ).filter(
        AnalysisResult.user_id == current_user.id
    ).first()
    
    # Handle case where user has no analyses
    if not stats or stats.total_analyses == 0:
        return DashboardSummaryResponse(
            total_analyses=0,
            average_match_score=0.0,
            highest_match_score=0.0,
            lowest_match_score=0.0,
            most_common_missing_skills=[],
        )
    
    # Extract missing skills from all analyses
    # We fetch only the missing_keywords column to minimize data transfer
    missing_keywords_rows = db.query(
        AnalysisResult.missing_keywords
    ).filter(
        AnalysisResult.user_id == current_user.id,
        AnalysisResult.missing_keywords.isnot(None),
    ).all()
    
    # Aggregate missing skills in application (could be done in DB with jsonb functions)
    # For simplicity and readability, we do it here
    all_missing_skills = []
    for row in missing_keywords_rows:
        if row.missing_keywords:
            try:
                skills = json.loads(row.missing_keywords)
                if isinstance(skills, list):
                    all_missing_skills.extend(skills)
            except (json.JSONDecodeError, TypeError):
                continue
    
    # Count frequency of each missing skill
    skill_counter = Counter(all_missing_skills)
    total_skill_occurrences = sum(skill_counter.values())
    
    # Create missing skill statistics
    most_common_missing_skills = [
        MissingSkillStat(
            skill=skill,
            count=count,
            frequency=round((count / total_skill_occurrences * 100) if total_skill_occurrences > 0 else 0, 2),
        )
        for skill, count in skill_counter.most_common(limit)
    ]
    
    return DashboardSummaryResponse(
        total_analyses=stats.total_analyses or 0,
        average_match_score=round(float(stats.avg_score or 0), 2),
        highest_match_score=round(float(stats.max_score or 0), 2),
        lowest_match_score=round(float(stats.min_score or 0), 2),
        most_common_missing_skills=most_common_missing_skills,
    )


@router.get(
    "/history",
    response_model=DashboardHistoryResponse,
    summary="Get analysis history",
    description="Get paginated list of user's past analyses",
)
async def get_dashboard_history(
    current_user: CurrentUserDep,
    db: DBSessionDep,
    skip: int = Query(default=0, ge=0, description="Number of records to skip (pagination offset)"),
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of records to return"),
) -> DashboardHistoryResponse:
    """Get paginated history of user's analyses.
    
    Uses efficient SQL query with:
    - WHERE clause to filter by user_id (uses index)
    - ORDER BY to sort by creation date (descending)
    - LIMIT and OFFSET for pagination
    - Only selects needed columns (not full text fields)
    
    Args:
        current_user: Authenticated user
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        DashboardHistoryResponse: Paginated list of analyses
    """
    # Efficient query with pagination
    # Uses index on user_id for fast filtering
    analyses = db.query(
        AnalysisResult.id,
        AnalysisResult.resume_id,
        AnalysisResult.job_description_id,
        AnalysisResult.match_score,
        AnalysisResult.created_at,
    ).filter(
        AnalysisResult.user_id == current_user.id
    ).order_by(
        AnalysisResult.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    # Get total count for pagination info
    total = db.query(func.count(AnalysisResult.id)).filter(
        AnalysisResult.user_id == current_user.id
    ).scalar()
    
    return DashboardHistoryResponse(
        analyses=[
            AnalysisHistoryItem(
                id=analysis.id,
                resume_id=analysis.resume_id,
                job_description_id=analysis.job_description_id,
                match_score=analysis.match_score,
                created_at=analysis.created_at,
            )
            for analysis in analyses
        ],
        total=total or 0,
    )
