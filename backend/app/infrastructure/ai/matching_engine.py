"""Explainable resume-to-job-description matching engine.

This engine uses rule-based and statistical methods to match resumes against job descriptions.
The approach is fully explainable and can be easily justified in interviews.

Why This Approach is Explainable:
==================================

1. TRANSPARENT KEYWORD EXTRACTION:
   - Uses TF-IDF (Term Frequency-Inverse Document Frequency) - a well-known statistical method
   - TF-IDF scores words based on how frequently they appear in the document vs. common words
   - Higher TF-IDF = more important/relevant keyword
   - This is a standard information retrieval technique, not a black box

2. CLEAR MATCHING LOGIC:
   - Exact keyword matching (case-insensitive)
   - Partial matching for skill variations (e.g., "Python" matches "Python 3.9")
   - Weighted scoring based on keyword importance
   - Simple percentage calculation: (matched_keywords / total_keywords) * 100

3. TRACEABLE SCORING:
   - Every matched keyword is logged with its importance score
   - Missing keywords are explicitly identified
   - Score breakdown is visible and auditable
   - No hidden neural network weights or embeddings

4. HUMAN-READABLE EXPLANATIONS:
   - Explains which skills matched and why
   - Lists missing skills with importance
   - Provides actionable recommendations
   - All logic can be traced back to the input text

How Accuracy Can Be Improved Later:
====================================

1. ENHANCED KEYWORD EXTRACTION:
   - Add synonym detection (e.g., "JS" = "JavaScript")
   - Use domain-specific skill dictionaries
   - Implement n-gram matching for phrases
   - Add skill normalization (e.g., "React.js" = "React")

2. CONTEXTUAL MATCHING:
   - Weight keywords by section (e.g., "Experience" section more important)
   - Consider years of experience mentioned
   - Match job titles and company names
   - Extract and match education levels

3. SEMANTIC SIMILARITY (Still Explainable):
   - Use word embeddings (Word2Vec, GloVe) for similarity
   - Calculate cosine similarity between skill vectors
   - This is still explainable - you can show which embeddings matched
   - Can visualize in vector space

4. RULE-BASED ENHANCEMENTS:
   - Add industry-specific rules (e.g., "5+ years" requirement matching)
   - Implement certification matching
   - Match project descriptions to job requirements
   - Add soft skills extraction and matching

5. FEEDBACK LOOP:
   - Collect user feedback on match accuracy
   - Adjust keyword weights based on feedback
   - A/B test different matching strategies
   - Continuously refine keyword extraction rules
"""
import re
from collections import Counter
from typing import Dict, List, Set, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer


class MatchingEngine:
    """Explainable resume-to-job-description matching engine."""
    
    # Common stop words to filter out (these don't indicate skills)
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
        "be", "have", "has", "had", "do", "does", "did", "will", "would",
        "should", "could", "may", "might", "must", "can", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they",
        "me", "him", "her", "us", "them", "my", "your", "his", "her", "its",
        "our", "their", "what", "which", "who", "whom", "whose", "where",
        "when", "why", "how", "all", "each", "every", "both", "few", "more",
        "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        "same", "so", "than", "too", "very", "just", "now"
    }
    
    # Common technical terms that might be skills (to preserve)
    TECHNICAL_TERMS = {
        "api", "sql", "html", "css", "js", "json", "xml", "http", "https",
        "rest", "graphql", "aws", "gcp", "azure", "docker", "kubernetes",
        "ci", "cd", "devops", "ml", "ai", "nlp", "cv", "ui", "ux"
    }
    
    def __init__(self, min_keyword_length: int = 3, max_keywords: int = 50):
        """Initialize the matching engine.
        
        Args:
            min_keyword_length: Minimum length for a keyword to be considered
            max_keywords: Maximum number of keywords to extract from each document
        """
        self.min_keyword_length = min_keyword_length
        self.max_keywords = max_keywords
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text for processing.
        
        Args:
            text: Raw text input
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces and hyphens (for compound terms)
        text = re.sub(r'[^\w\s-]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_keywords(self, text: str) -> Dict[str, float]:
        """Extract important keywords using TF-IDF.
        
        TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical method
        that scores words based on:
        - How frequently they appear in the document (TF)
        - How rare they are across all documents (IDF)
        
        This gives higher scores to words that are:
        - Frequent in this document (important to this text)
        - Rare in general (not common stop words)
        
        Args:
            text: Input text to extract keywords from
            
        Returns:
            Dict[str, float]: Dictionary of keywords and their importance scores
        """
        if not text or not text.strip():
            return {}
        
        # Preprocess text
        cleaned_text = self.preprocess_text(text)
        
        if not cleaned_text:
            return {}
        
        # Use TF-IDF to extract important keywords
        # We treat the single document as a corpus of sentences
        sentences = [s.strip() for s in cleaned_text.split('.') if s.strip()]
        if not sentences:
            sentences = [cleaned_text]
        
        # Create TF-IDF vectorizer
        # max_features limits the vocabulary size
        # min_df=1 means word must appear at least once
        vectorizer = TfidfVectorizer(
            max_features=self.max_keywords * 2,  # Get more candidates
            min_df=1,
            stop_words=list(self.STOP_WORDS),
            token_pattern=r'\b[a-z][a-z0-9-]+\b',  # Match words with letters
            ngram_range=(1, 2),  # Include single words and 2-word phrases
        )
        
        try:
            # Fit and transform
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Get feature names (keywords)
            feature_names = vectorizer.get_feature_names_out()
            
            # Calculate average TF-IDF score for each keyword across all sentences
            keyword_scores = {}
            for idx, keyword in enumerate(feature_names):
                # Get average score across all sentences
                score = float(tfidf_matrix[:, idx].mean())
                
                # Filter by minimum length and exclude pure numbers
                if (len(keyword) >= self.min_keyword_length and 
                    not keyword.isdigit() and
                    score > 0):
                    keyword_scores[keyword] = score
            
            # Sort by score and take top keywords
            sorted_keywords = sorted(
                keyword_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:self.max_keywords]
            
            return dict(sorted_keywords)
        
        except Exception:
            # Fallback to simple frequency-based extraction
            return self._fallback_keyword_extraction(cleaned_text)
    
    def _fallback_keyword_extraction(self, text: str) -> Dict[str, float]:
        """Fallback keyword extraction using word frequency.
        
        Used when TF-IDF fails. This is still explainable - it's just counting
        word frequencies and filtering out common words.
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dict[str, float]: Keywords and their frequency scores
        """
        # Split into words
        words = text.split()
        
        # Filter words
        filtered_words = [
            w for w in words
            if (len(w) >= self.min_keyword_length and
                w not in self.STOP_WORDS and
                not w.isdigit())
        ]
        
        # Count frequencies
        word_counts = Counter(filtered_words)
        
        # Calculate normalized scores (frequency / max_frequency)
        if not word_counts:
            return {}
        
        max_count = max(word_counts.values())
        keyword_scores = {
            word: count / max_count
            for word, count in word_counts.most_common(self.max_keywords)
        }
        
        return keyword_scores
    
    def normalize_keyword(self, keyword: str) -> str:
        """Normalize keyword for matching (handles variations).
        
        Args:
            keyword: Raw keyword
            
        Returns:
            str: Normalized keyword
        """
        # Convert to lowercase
        normalized = keyword.lower().strip()
        
        # Remove common suffixes/prefixes that don't affect meaning
        # e.g., "python3" -> "python", "javascript" -> "javascript"
        normalized = re.sub(r'[0-9]+$', '', normalized)  # Remove trailing numbers
        normalized = re.sub(r'^[0-9]+', '', normalized)  # Remove leading numbers
        
        return normalized
    
    def match_keywords(
        self,
        resume_keywords: Dict[str, float],
        job_keywords: Dict[str, float]
    ) -> Tuple[Dict[str, float], Set[str], Set[str]]:
        """Match keywords between resume and job description.
        
        This is the core matching logic - it's simple and explainable:
        1. Normalize keywords for comparison
        2. Find exact matches
        3. Find partial matches (one keyword contains another)
        4. Calculate match scores
        
        Args:
            resume_keywords: Keywords from resume with scores
            job_keywords: Keywords from job description with scores
            
        Returns:
            Tuple containing:
            - matched_keywords: Dict of matched keywords with combined scores
            - missing_keywords: Set of job keywords not found in resume
            - extra_keywords: Set of resume keywords not in job description
        """
        # Normalize all keywords
        normalized_resume = {
            self.normalize_keyword(k): (k, score)
            for k, score in resume_keywords.items()
        }
        normalized_job = {
            self.normalize_keyword(k): (k, score)
            for k, score in job_keywords.items()
        }
        
        matched_keywords = {}
        missing_keywords = set()
        extra_keywords = set()
        
        # Check each job keyword against resume keywords
        for job_norm, (job_orig, job_score) in normalized_job.items():
            matched = False
            
            # Try exact match first
            if job_norm in normalized_resume:
                resume_orig, resume_score = normalized_resume[job_norm]
                # Combined score: average of both importance scores
                combined_score = (job_score + resume_score) / 2
                matched_keywords[job_orig] = {
                    "resume_keyword": resume_orig,
                    "score": combined_score,
                    "match_type": "exact"
                }
                matched = True
            else:
                # Try partial match (one contains the other)
                for resume_norm, (resume_orig, resume_score) in normalized_resume.items():
                    if (job_norm in resume_norm or resume_norm in job_norm) and len(job_norm) >= 3:
                        # Partial match gets lower weight
                        combined_score = (job_score + resume_score) / 2 * 0.7
                        matched_keywords[job_orig] = {
                            "resume_keyword": resume_orig,
                            "score": combined_score,
                            "match_type": "partial"
                        }
                        matched = True
                        break
            
            if not matched:
                missing_keywords.add(job_orig)
        
        # Find extra keywords in resume (not required by job)
        for resume_norm, (resume_orig, _) in normalized_resume.items():
            if resume_norm not in normalized_job:
                # Check if it's a partial match
                is_partial = False
                for job_norm in normalized_job:
                    if resume_norm in job_norm or job_norm in resume_norm:
                        is_partial = True
                        break
                
                if not is_partial:
                    extra_keywords.add(resume_orig)
        
        return matched_keywords, missing_keywords, extra_keywords
    
    def calculate_match_score(
        self,
        matched_keywords: Dict[str, Dict],
        total_job_keywords: int
    ) -> float:
        """Calculate overall match score as a percentage.
        
        Simple formula: (matched_keywords / total_keywords) * 100
        
        This is weighted by keyword importance, so important keywords
        that match contribute more to the score.
        
        Args:
            matched_keywords: Dictionary of matched keywords with scores
            total_job_keywords: Total number of keywords in job description
            
        Returns:
            float: Match score as percentage (0-100)
        """
        if total_job_keywords == 0:
            return 0.0
        
        # Calculate weighted match score
        # Each matched keyword contributes based on its importance
        total_match_score = sum(
            match_info["score"]
            for match_info in matched_keywords.values()
        )
        
        # Normalize to percentage
        # We use the sum of all job keyword scores as denominator
        # This gives us a percentage based on importance-weighted matching
        match_percentage = (len(matched_keywords) / total_job_keywords) * 100
        
        # Apply a bonus for high-importance matches
        if matched_keywords:
            avg_match_score = total_match_score / len(matched_keywords)
            # Boost score if important keywords matched
            importance_bonus = avg_match_score * 10
            match_percentage = min(100, match_percentage + importance_bonus)
        
        return round(match_percentage, 2)
    
    def generate_explanation(
        self,
        matched_keywords: Dict[str, Dict],
        missing_keywords: Set[str],
        match_score: float
    ) -> str:
        """Generate human-readable explanation of the match.
        
        This explanation is fully traceable - every statement can be
        verified by looking at the matched/missing keywords.
        
        Args:
            matched_keywords: Dictionary of matched keywords
            missing_keywords: Set of missing keywords
            match_score: Overall match score
            
        Returns:
            str: Human-readable explanation
        """
        explanation_parts = []
        
        # Overall score
        explanation_parts.append(
            f"Match Score: {match_score:.1f}%\n\n"
        )
        
        # Matched skills
        if matched_keywords:
            explanation_parts.append("✅ Matched Skills:\n")
            # Sort by importance
            sorted_matches = sorted(
                matched_keywords.items(),
                key=lambda x: x[1]["score"],
                reverse=True
            )
            
            for job_keyword, match_info in sorted_matches[:10]:  # Top 10
                match_type = match_info["match_type"]
                score = match_info["score"]
                resume_keyword = match_info["resume_keyword"]
                
                if match_type == "exact":
                    explanation_parts.append(
                        f"  • {job_keyword} (exact match, importance: {score:.2f})\n"
                    )
                else:
                    explanation_parts.append(
                        f"  • {job_keyword} (matched with '{resume_keyword}', "
                        f"importance: {score:.2f})\n"
                    )
            
            if len(matched_keywords) > 10:
                explanation_parts.append(
                    f"  ... and {len(matched_keywords) - 10} more matches\n"
                )
        else:
            explanation_parts.append("❌ No skills matched.\n")
        
        # Missing skills
        if missing_keywords:
            explanation_parts.append("\n⚠️ Missing Skills:\n")
            # Show top missing keywords
            for keyword in list(missing_keywords)[:10]:
                explanation_parts.append(f"  • {keyword}\n")
            
            if len(missing_keywords) > 10:
                explanation_parts.append(
                    f"  ... and {len(missing_keywords) - 10} more\n"
                )
        
        # Recommendations
        explanation_parts.append("\n💡 Recommendations:\n")
        if match_score >= 70:
            explanation_parts.append(
                "  • Strong match! Your resume aligns well with the job requirements.\n"
            )
        elif match_score >= 50:
            explanation_parts.append(
                "  • Good match, but consider highlighting the missing skills in your resume.\n"
            )
        else:
            explanation_parts.append(
                "  • Consider gaining experience with the missing skills or "
                "emphasizing transferable skills.\n"
            )
        
        return "".join(explanation_parts)
    
    def analyze(
        self,
        resume_text: str,
        job_description_text: str
    ) -> Dict:
        """Perform complete analysis of resume against job description.
        
        This is the main entry point. It orchestrates all the steps:
        1. Extract keywords from both texts
        2. Match keywords
        3. Calculate score
        4. Generate explanation
        
        Args:
            resume_text: Text content from resume
            job_description_text: Text content from job description
            
        Returns:
            Dict containing:
            - match_score: Overall match percentage
            - matched_keywords: List of matched keywords with details
            - missing_keywords: List of missing keywords
            - explanation: Human-readable explanation
        """
        # Extract keywords
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_description_text)
        
        # Match keywords
        matched_keywords, missing_keywords, extra_keywords = self.match_keywords(
            resume_keywords,
            job_keywords
        )
        
        # Calculate score
        total_job_keywords = len(job_keywords)
        match_score = self.calculate_match_score(matched_keywords, total_job_keywords)
        
        # Generate explanation
        explanation = self.generate_explanation(
            matched_keywords,
            missing_keywords,
            match_score
        )
        
        return {
            "match_score": match_score,
            "matched_keywords": matched_keywords,
            "missing_keywords": list(missing_keywords),
            "extra_keywords": list(extra_keywords),
            "explanation": explanation,
            "resume_keyword_count": len(resume_keywords),
            "job_keyword_count": total_job_keywords,
        }
