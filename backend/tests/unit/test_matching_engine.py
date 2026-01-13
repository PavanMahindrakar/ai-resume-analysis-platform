"""Unit tests for the matching engine."""
import pytest

from app.infrastructure.ai.matching_engine import MatchingEngine


class TestMatchingEngine:
    """Test the explainable matching engine."""
    
    @pytest.fixture
    def engine(self):
        """Create a matching engine instance."""
        return MatchingEngine()
    
    def test_preprocess_text(self, engine: MatchingEngine):
        """Test text preprocessing."""
        text = "Hello World! This is a TEST."
        processed = engine.preprocess_text(text)
        
        assert processed == "hello world this is a test"
        assert "!" not in processed
        assert processed.islower()
    
    def test_preprocess_text_empty(self, engine: MatchingEngine):
        """Test preprocessing empty text."""
        assert engine.preprocess_text("") == ""
        assert engine.preprocess_text("   ") == ""
    
    def test_extract_keywords(self, engine: MatchingEngine):
        """Test keyword extraction from text."""
        text = "Python developer with experience in Django and React. Strong skills in SQL and PostgreSQL."
        keywords = engine.extract_keywords(text)
        
        assert isinstance(keywords, dict)
        assert len(keywords) > 0
        # Should extract technical terms
        assert any("python" in k.lower() or "django" in k.lower() or "react" in k.lower() 
                  for k in keywords.keys())
    
    def test_extract_keywords_empty(self, engine: MatchingEngine):
        """Test keyword extraction from empty text."""
        keywords = engine.extract_keywords("")
        assert keywords == {}
    
    def test_normalize_keyword(self, engine: MatchingEngine):
        """Test keyword normalization."""
        assert engine.normalize_keyword("Python") == "python"
        assert engine.normalize_keyword("Python3") == "python"
        assert engine.normalize_keyword("JavaScript") == "javascript"
        assert engine.normalize_keyword("  React  ") == "react"
    
    def test_match_keywords_exact_match(self, engine: MatchingEngine):
        """Test exact keyword matching."""
        resume_keywords = {"python": 0.8, "django": 0.7, "react": 0.6}
        job_keywords = {"python": 0.9, "django": 0.8, "sql": 0.7}
        
        matched, missing, extra = engine.match_keywords(resume_keywords, job_keywords)
        
        # Should match python and django
        assert "python" in matched
        assert "django" in matched
        # sql should be missing
        assert "sql" in missing
        # react should be extra
        assert "react" in extra
    
    def test_match_keywords_partial_match(self, engine: MatchingEngine):
        """Test partial keyword matching."""
        resume_keywords = {"python": 0.8, "javascript": 0.7}
        job_keywords = {"python3": 0.9, "js": 0.8}
        
        matched, missing, extra = engine.match_keywords(resume_keywords, job_keywords)
        
        # Should have partial matches
        assert len(matched) > 0
    
    def test_calculate_match_score(self, engine: MatchingEngine):
        """Test match score calculation."""
        matched_keywords = {
            "python": {"score": 0.8, "match_type": "exact"},
            "django": {"score": 0.7, "match_type": "exact"},
        }
        total_job_keywords = 5
        
        score = engine.calculate_match_score(matched_keywords, total_job_keywords)
        
        assert 0 <= score <= 100
        assert isinstance(score, float)
    
    def test_calculate_match_score_no_matches(self, engine: MatchingEngine):
        """Test match score with no matches."""
        matched_keywords = {}
        total_job_keywords = 5
        
        score = engine.calculate_match_score(matched_keywords, total_job_keywords)
        
        assert score == 0.0
    
    def test_generate_explanation(self, engine: MatchingEngine):
        """Test explanation generation."""
        matched_keywords = {
            "python": {"score": 0.8, "match_type": "exact", "resume_keyword": "python"},
            "django": {"score": 0.7, "match_type": "exact", "resume_keyword": "django"},
        }
        missing_keywords = {"sql", "postgresql"}
        match_score = 65.5
        
        explanation = engine.generate_explanation(matched_keywords, missing_keywords, match_score)
        
        assert isinstance(explanation, str)
        assert "65.5" in explanation or "65" in explanation
        assert "python" in explanation.lower() or "django" in explanation.lower()
        assert "sql" in explanation.lower() or "missing" in explanation.lower()
    
    def test_analyze_complete_flow(self, engine: MatchingEngine):
        """Test complete analysis flow."""
        resume_text = """
        Software Engineer with 5 years of experience in Python and Django.
        Strong background in web development using React and JavaScript.
        Experience with PostgreSQL and SQL databases.
        """
        
        job_text = """
        We are looking for a Python developer with Django experience.
        Must have knowledge of SQL and database design.
        Experience with React is a plus.
        """
        
        result = engine.analyze(resume_text, job_text)
        
        assert "match_score" in result
        assert "matched_keywords" in result
        assert "missing_keywords" in result
        assert "explanation" in result
        
        assert 0 <= result["match_score"] <= 100
        assert isinstance(result["matched_keywords"], dict)
        assert isinstance(result["missing_keywords"], list)
        assert isinstance(result["explanation"], str)
        
        # Should have some matches
        assert len(result["matched_keywords"]) > 0
    
    def test_analyze_no_matches(self, engine: MatchingEngine):
        """Test analysis with completely different texts."""
        resume_text = "Chef with experience in French cuisine and pastry."
        job_text = "Software engineer needed for Python development."
        
        result = engine.analyze(resume_text, job_text)
        
        assert result["match_score"] < 50  # Should be low match
        assert len(result["matched_keywords"]) == 0 or result["match_score"] < 20
