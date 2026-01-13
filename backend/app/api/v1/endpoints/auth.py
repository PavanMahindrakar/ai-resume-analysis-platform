"""Authentication endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.schemas import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.core.dependencies import DBSessionDep
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import get_settings
from app.infrastructure.database.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])

settings = get_settings()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password",
)
async def register(
    user_data: UserRegisterRequest,
    db: DBSessionDep,
) -> UserResponse:
    """Register a new user.
    
    Flow:
    1. Check if user with email already exists
    2. Hash the password securely
    3. Create new user in database
    4. Return user information (without password)
    
    Args:
        user_data: Registration data (email, password)
        db: Database session
        
    Returns:
        UserResponse: Created user information
        
    Raises:
        HTTPException: If email already exists
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Hash password before storing
        hashed_password = hash_password(user_data.password)
        
        # Create new user
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            is_active=new_user.is_active,
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like email already exists)
        raise
    except Exception as e:
        # Log unexpected errors and return a generic error message
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again later.",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    description="Authenticate user and receive JWT access token",
)
async def login(
    credentials: UserLoginRequest,
    db: DBSessionDep,
) -> TokenResponse:
    """Login user and return JWT access token.
    
    Token Flow:
    1. User provides email and password
    2. Server finds user by email
    3. Server verifies password against hashed password in database
    4. Server generates JWT token containing user identity
    5. Token is returned to client
    6. Client uses token in Authorization header for subsequent requests
    
    Args:
        credentials: Login credentials (email, password)
        db: Database session
        
    Returns:
        TokenResponse: JWT access token and metadata
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Create JWT token with user identity
    # "sub" (subject) claim contains user ID
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # Calculate expiration time in seconds
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
    )
