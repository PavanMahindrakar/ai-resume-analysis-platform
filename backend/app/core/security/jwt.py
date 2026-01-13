"""JWT token utilities for authentication.

Token Flow Explanation:
======================

1. USER REGISTRATION/LOGIN:
   - User provides credentials (email + password)
   - Server validates credentials
   - Server generates JWT access token containing user identity
   - Token is returned to client

2. TOKEN STRUCTURE:
   - Header: Algorithm and token type (e.g., HS256, JWT)
   - Payload: Claims (user_id, email, expiration time, etc.)
   - Signature: HMAC signature using SECRET_KEY

3. CLIENT USAGE:
   - Client stores token (typically in localStorage or httpOnly cookie)
   - Client includes token in Authorization header: "Bearer <token>"
   - Token is sent with every authenticated request

4. TOKEN VERIFICATION:
   - Server extracts token from Authorization header
   - Server verifies signature using SECRET_KEY
   - Server checks expiration time
   - Server extracts user identity from payload
   - Server loads user from database

5. TOKEN EXPIRATION:
   - Tokens have expiration time (default: 30 minutes)
   - Expired tokens are rejected
   - Client must refresh/login again when token expires
"""
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.
    
    The token contains user identity claims and expiration time.
    It's signed with SECRET_KEY to prevent tampering.
    
    Args:
        data: Dictionary containing claims (typically user_id, email)
        expires_delta: Optional custom expiration time. If None, uses default from settings.
        
    Returns:
        str: Encoded JWT token
        
    Example:
        >>> token = create_access_token({"sub": str(user_id), "email": user.email})
        >>> # Token can be used in Authorization header: "Bearer {token}"
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration claim
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # Encode and sign token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT access token.
    
    Verifies the token signature and expiration time.
    Returns None if token is invalid or expired.
    
    Args:
        token: JWT token string (without "Bearer " prefix)
        
    Returns:
        Optional[dict]: Decoded token payload if valid, None otherwise
        
    Example:
        >>> payload = decode_access_token(token)
        >>> if payload:
        ...     user_id = payload.get("sub")
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None


def get_user_id_from_token(token: str) -> Optional[UUID]:
    """Extract user ID from JWT token.
    
    Convenience function to get user_id from token payload.
    
    Args:
        token: JWT token string
        
    Returns:
        Optional[UUID]: User ID if token is valid, None otherwise
    """
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    # "sub" (subject) claim typically contains user identifier
    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None
    
    try:
        return UUID(user_id_str)
    except (ValueError, TypeError):
        return None
