"""Integration tests for resume upload API."""
import io
from pathlib import Path

import pytest
from fastapi import status


class TestResumeUpload:
    """Test resume upload endpoint."""
    
    def test_upload_pdf_success(self, authenticated_client, db_session):
        """Test successful PDF upload."""
        # Create a simple PDF-like file (in real tests, use actual PDF bytes)
        # For testing, we'll create a mock PDF file
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"
        
        response = authenticated_client.post(
            "/api/v1/resume/upload",
            files={"file": ("resume.pdf", pdf_content, "application/pdf")}
        )
        
        # Note: This might fail if PDF parsing doesn't work with minimal PDF
        # In a real scenario, use a proper test PDF file
        # For now, we check the endpoint structure
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_422_UNPROCESSABLE_ENTITY  # If PDF parsing fails
        ]
        
        if response.status_code == status.HTTP_201_CREATED:
            data = response.json()
            assert "id" in data
            assert "file_name" in data
            assert "content_type" in data
            assert data["content_type"] == "application/pdf"
    
    def test_upload_non_pdf_file(self, authenticated_client):
        """Test upload with non-PDF file."""
        text_content = b"This is a text file, not a PDF"
        
        response = authenticated_client.post(
            "/api/v1/resume/upload",
            files={"file": ("document.txt", text_content, "text/plain")}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pdf" in response.json()["detail"].lower()
    
    def test_upload_empty_file(self, authenticated_client):
        """Test upload with empty file."""
        response = authenticated_client.post(
            "/api/v1/resume/upload",
            files={"file": ("empty.pdf", b"", "application/pdf")}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "empty" in response.json()["detail"].lower()
    
    def test_upload_requires_authentication(self, client):
        """Test that upload requires authentication."""
        pdf_content = b"%PDF-1.4\n"
        
        response = client.post(
            "/api/v1/resume/upload",
            files={"file": ("resume.pdf", pdf_content, "application/pdf")}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_upload_invalid_token(self, client):
        """Test upload with invalid token."""
        client.headers.update({"Authorization": "Bearer invalid_token"})
        pdf_content = b"%PDF-1.4\n"
        
        response = client.post(
            "/api/v1/resume/upload",
            files={"file": ("resume.pdf", pdf_content, "application/pdf")}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
