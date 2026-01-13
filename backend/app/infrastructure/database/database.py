"""Database connection and session management."""
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    # Connection pool settings
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_reset_on_return="commit",  # Reset connections on return
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all models (Alembic-ready)
Base = declarative_base()


def get_db():
    """Dependency function to get database session.
    
    Yields:
        Session: Database session instance
        
    Note:
        This function should be used as a FastAPI dependency.
        It automatically closes the session after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: Add connection pool event listeners for monitoring
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Optional: Set database-specific connection parameters."""
    # PostgreSQL-specific settings can be added here if needed
    pass
