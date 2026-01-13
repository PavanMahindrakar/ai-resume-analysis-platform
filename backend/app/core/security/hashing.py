"""Password hashing utilities using bcrypt."""
import bcrypt

# Use direct bcrypt to avoid passlib compatibility issues with newer bcrypt versions
# bcrypt is a secure password hashing algorithm that automatically handles salt generation


def hash_password(password: str) -> str:
    """Hash a plain text password.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password (includes salt and algorithm info)
        
    Example:
        >>> hashed = hash_password("my_password")
        >>> verify_password("my_password", hashed)
        True
    """
    # Use direct bcrypt to avoid passlib compatibility issues
    # Ensure password is encoded as bytes and limit to 72 bytes (bcrypt limit)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
        
    Example:
        >>> verify_password("my_password", "$2b$12$...")
        True
    """
    # Use direct bcrypt to avoid passlib compatibility issues
    # Ensure password is encoded as bytes and limit to 72 bytes (bcrypt limit)
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
