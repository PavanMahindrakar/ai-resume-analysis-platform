"""Dependency injection for FastAPI."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.security import get_user_id_from_token
from app.infrastructure.database.database import get_db
from app.infrastructure.database.models import User


def get_settings_dependency() -> Settings:
    """Dependency to get settings.
    
    Returns:
        Settings: Application settings instance
    """
    return get_settings()


# Re-export for convenience
SettingsDep = Annotated[Settings, Depends(get_settings_dependency)]

# Database session dependency
DBSessionDep = Annotated[Session, Depends(get_db)]

# HTTP Bearer token security scheme
security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: DBSessionDep,
) -> User:
    """Dependency to get current authenticated user from JWT token.
    
    Token Flow:
    1. Extract token from Authorization header (Bearer <token>)
    2. Decode and verify token signature
    3. Check token expiration
    4. Extract user_id from token payload
    5. Load user from database
    6. Return user object
    
    This dependency can be used in any endpoint that requires authentication.
    
    Args:
        credentials: HTTP Bearer token credentials from Authorization header
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid, expired, or user not found
    """
    token = credentials.credentials
    
    # Extract user ID from token
    user_id = get_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Load user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    return user


# Convenience type alias for current user dependency
CurrentUserDep = Annotated[User, Depends(get_current_user)]
