"""
Quick script to create database tables directly.
Run this if migrations aren't working.
"""
from app.infrastructure.database.database import engine, Base
from app.infrastructure.database.models import User, Resume, JobDescription, AnalysisResult

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
    print("\nCreated tables:")
    print("  - users")
    print("  - resumes")
    print("  - job_descriptions")
    print("  - analysis_results")
