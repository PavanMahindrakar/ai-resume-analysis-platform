"""Unit tests for authentication logic."""
import pytest
from fastapi import HTTPException

from app.core.security import hash_password, verify_password
from app.core.security.jwt import create_access_token, decode_access_token


class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_hash_password_creates_different_hash(self):
        """Test that hashing the same password twice creates different hashes (due to salt)."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different (bcrypt uses random salt)
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "my_secret_password"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "my_secret_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_hash_password_empty_string(self):
        """Test hashing empty password."""
        hashed = hash_password("")
        assert hashed is not None
        assert verify_password("", hashed) is True


class TestJWTToken:
    """Test JWT token creation and decoding."""
    
    def test_create_access_token(self):
        """Test creating an access token."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_access_token(self):
        """Test decoding a valid access token."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "user123"
        assert decoded["email"] == "test@example.com"
    
    def test_decode_invalid_token(self):
        """Test decoding an invalid token raises exception."""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(Exception):  # JWT decode will raise an exception
            decode_access_token(invalid_token)
    
    def test_token_contains_user_data(self):
        """Test that token contains expected user data."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        email = "user@example.com"
        
        token = create_access_token({"sub": user_id, "email": email})
        decoded = decode_access_token(token)
        
        assert decoded["sub"] == user_id
        assert decoded["email"] == email
