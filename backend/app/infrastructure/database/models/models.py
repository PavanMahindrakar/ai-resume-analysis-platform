"""Database models for the application."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.infrastructure.database.database import Base


class User(Base):
    """User model.
    
    Represents a user in the system.
    """
    
    __tablename__ = "users"
    
    # Primary key
    id: UUID = Column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    
    # Authentication fields
    email: str = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password: str = Column(
        String(255),
        nullable=False,
    )
    is_active: bool = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    # Table constraints
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )


class Resume(Base):
    """Resume model.
    
    Represents a resume document uploaded by a user.
    """
    
    __tablename__ = "resumes"
    
    # Primary key
    id: UUID = Column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    
    # Foreign key
    user_id: Optional[UUID] = Column(
        PostgresUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    # File metadata
    file_name: str = Column(String(255), nullable=False)
    file_path: str = Column(String(512), nullable=False)
    content_type: str = Column(String(128), nullable=False, default="application/pdf")

    # Extracted text content
    text_content: str = Column(Text, nullable=True)
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    # TODO: Add resume fields (file_path, content, parsed_data, etc.)


class JobDescription(Base):
    """Job description model.
    
    Represents a job description for analysis.
    """
    
    __tablename__ = "job_descriptions"
    
    # Primary key
    id: UUID = Column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    
    # Foreign key
    user_id: Optional[UUID] = Column(
        PostgresUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    # Job details
    title: str = Column(String(255), nullable=False)
    description: str = Column(Text, nullable=False)
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    # TODO: Add job description fields (title, company, description, requirements, etc.)


class AnalysisResult(Base):
    """Analysis result model.
    
    Represents the result of analyzing a resume against a job description.
    """
    
    __tablename__ = "analysis_results"
    
    # Primary key
    id: UUID = Column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    
    # Foreign keys
    resume_id: Optional[UUID] = Column(
        PostgresUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    job_description_id: Optional[UUID] = Column(
        PostgresUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    user_id: Optional[UUID] = Column(
        PostgresUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    
    # Analysis results
    match_score: float = Column(
        Float,
        nullable=False,
        default=0.0,
        comment="Overall match score as percentage (0-100)",
    )
    matched_keywords: str = Column(
        Text,
        nullable=True,
        comment="JSON string of matched keywords with details",
    )
    missing_keywords: str = Column(
        Text,
        nullable=True,
        comment="JSON string of missing keywords",
    )
    explanation: str = Column(
        Text,
        nullable=True,
        comment="Human-readable explanation of the match",
    )
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
