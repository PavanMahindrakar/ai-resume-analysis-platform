"""Integration tests for analysis API."""
import pytest
from fastapi import status

from app.infrastructure.database.models import Resume, JobDescription


class TestAnalysisAPI:
    """Test analysis endpoint."""
    
    @pytest.fixture
    def test_resume(self, db_session, test_user):
        """Create a test resume."""
        resume = Resume(
            user_id=test_user.id,
            file_name="test_resume.pdf",
            file_path="/tmp/test_resume.pdf",
            content_type="application/pdf",
            text_content="Python developer with 5 years experience. Strong skills in Django, React, and PostgreSQL.",
        )
        db_session.add(resume)
        db_session.commit()
        db_session.refresh(resume)
        return resume
    
    @pytest.fixture
    def test_job_description(self, db_session, test_user):
        """Create a test job description."""
        job = JobDescription(
            user_id=test_user.id,
            title="Senior Python Developer",
            description="Looking for a Python developer with Django experience. Must know SQL and PostgreSQL. React experience is a plus.",
        )
        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)
        return job
    
    def test_run_analysis_success(self, authenticated_client, test_resume, test_job_description):
        """Test successful analysis run."""
        response = authenticated_client.post(
            "/api/v1/analysis/run",
            json={
                "resume_id": str(test_resume.id),
                "job_description_id": str(test_job_description.id),
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert "id" in data
        assert "match_score" in data
        assert "explanation" in data
        assert "matched_keywords" in data
        assert "missing_keywords" in data
        
        assert 0 <= data["match_score"] <= 100
        assert isinstance(data["matched_keywords"], dict)
        assert isinstance(data["missing_keywords"], list)
        assert len(data["explanation"]) > 0
    
    def test_run_analysis_resume_not_found(self, authenticated_client, test_job_description):
        """Test analysis with non-existent resume."""
        from uuid import uuid4
        
        response = authenticated_client.post(
            "/api/v1/analysis/run",
            json={
                "resume_id": str(uuid4()),
                "job_description_id": str(test_job_description.id),
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "resume" in response.json()["detail"].lower()
    
    def test_run_analysis_job_not_found(self, authenticated_client, test_resume):
        """Test analysis with non-existent job description."""
        from uuid import uuid4
        
        response = authenticated_client.post(
            "/api/v1/analysis/run",
            json={
                "resume_id": str(test_resume.id),
                "job_description_id": str(uuid4()),
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "job" in response.json()["detail"].lower()
    
    def test_run_analysis_resume_no_text(self, authenticated_client, db_session, test_user, test_job_description):
        """Test analysis with resume that has no text content."""
        resume_no_text = Resume(
            user_id=test_user.id,
            file_name="empty_resume.pdf",
            file_path="/tmp/empty_resume.pdf",
            content_type="application/pdf",
            text_content=None,  # No text content
        )
        db_session.add(resume_no_text)
        db_session.commit()
        db_session.refresh(resume_no_text)
        
        response = authenticated_client.post(
            "/api/v1/analysis/run",
            json={
                "resume_id": str(resume_no_text.id),
                "job_description_id": str(test_job_description.id),
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "text content" in response.json()["detail"].lower()
    
    def test_run_analysis_requires_authentication(self, client, test_resume, test_job_description):
        """Test that analysis requires authentication."""
        response = client.post(
            "/api/v1/analysis/run",
            json={
                "resume_id": str(test_resume.id),
                "job_description_id": str(test_job_description.id),
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_run_analysis_other_user_resume(self, authenticated_client, db_session, test_user):
        """Test that users can't analyze other users' resumes."""
        from app.core.security import hash_password
        from app.infrastructure.database.models import User
        
        # Create another user
        other_user = User(
            email="other@example.com",
            hashed_password=hash_password("password123"),
            is_active=True,
        )
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        
        # Create resume for other user
        other_resume = Resume(
            user_id=other_user.id,
            file_name="other_resume.pdf",
            file_path="/tmp/other_resume.pdf",
            content_type="application/pdf",
            text_content="Some resume text",
        )
        db_session.add(other_resume)
        
        # Create job for current user
        job = JobDescription(
            user_id=test_user.id,
            title="Test Job",
            description="Test description",
        )
        db_session.add(job)
        db_session.commit()
        db_session.refresh(other_resume)
        db_session.refresh(job)
        
        response = authenticated_client.post(
            "/api/v1/analysis/run",
            json={
                "resume_id": str(other_resume.id),
                "job_description_id": str(job.id),
            }
        )
        
        # Should fail because resume belongs to different user
        assert response.status_code == status.HTTP_404_NOT_FOUND
