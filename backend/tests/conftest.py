"""Pytest configuration and shared fixtures."""
import os
from pathlib import Path
from typing import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.database import Base, get_db
from app.infrastructure.database.models import User
from app.main import create_application
from app.core.security import hash_password

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app = create_application()
    app.dependency_overrides[get_db] = override_get_db
    
    # Set test upload directory
    test_upload_dir = Path("/tmp/test_uploads")
    test_upload_dir.mkdir(exist_ok=True)
    os.environ["UPLOAD_DIR"] = str(test_upload_dir)
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    # Clean up test uploads
    if test_upload_dir.exists():
        for file in test_upload_dir.glob("*"):
            if file.is_file():
                file.unlink()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_token(client: TestClient, test_user: User) -> str:
    """Get an access token for the test user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def authenticated_client(client: TestClient, test_user_token: str, test_user, db_session) -> TestClient:
    """Create a test client with authentication headers."""
    from app.core.dependencies import get_current_user
    
    # Override the get_current_user dependency to return test_user
    # This bypasses JWT verification for testing
    # FastAPI's dependency override system handles parameter matching
    def override_get_current_user(*args, **kwargs):
        return test_user
    
    client.app.dependency_overrides[get_current_user] = override_get_current_user
    client.headers.update({"Authorization": f"Bearer {test_user_token}"})
    return client
