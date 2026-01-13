"""Application settings and configuration."""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = Field(default="AI Resume Intelligence API", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow CORS credentials")
    CORS_METHODS: List[str] = Field(
        default=["*"],
        description="Allowed CORS methods"
    )
    CORS_HEADERS: List[str] = Field(
        default=["*"],
        description="Allowed CORS headers"
    )
    
    # API
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/ai_resume_intelligence",
        description="PostgreSQL database URL"
    )
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries (for debugging)")
    DB_POOL_SIZE: int = Field(default=5, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Maximum overflow connections")
    DB_POOL_PRE_PING: bool = Field(default=True, description="Enable connection health checks")
    
    # JWT Authentication
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT token signing"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )

    # File storage
    UPLOAD_DIR: str = Field(
        default="storage/resumes",
        description="Directory where uploaded resumes are stored",
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()
