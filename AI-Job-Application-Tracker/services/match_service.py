"""
services/match_service.py

Core logic for comparing a resume's text against a job description's text
and producing a keyword-based match score.

This module has NO dependency on Streamlit or SQLite by design — it's pure
Python so it can be tested and reused independently of the UI or database.
"""

import re
from dataclasses import dataclass


# Standard English stopwords — small hardcoded list to avoid pulling in
# a heavy NLP dependency (e.g. NLTK) for something this simple.
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "so",
    "to", "of", "in", "on", "at", "for", "with", "as", "by", "from",
    "is", "are", "was", "were", "be", "been", "being", "this", "that",
    "these", "those", "it", "its", "you", "your", "we", "our", "they",
    "their", "he", "she", "his", "her", "will", "shall", "can", "could",
    "should", "would", "may", "might", "must", "have", "has", "had",
    "do", "does", "did", "not", "no", "nor", "up", "out", "about",
    "into", "over", "after", "before", "between", "through", "during",
    "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "only", "own", "same", "too", "very", "just",
}

# Filler words common in job postings/resumes that carry little
# distinguishing signal — nearly every resume says "experience".
FILLER_WORDS = {
    "experience", "experienced", "required", "requirements", "responsibility",
    "responsibilities", "years", "year", "work", "working", "team", "role",
    "job", "position", "candidate", "candidates", "skills", "skill",
    "ability", "including", "etc", "strong", "excellent", "preferred",
    "plus", "using", "used", "use", "knowledge", "understanding", "field",
    "environment", "opportunity", "company",
}

IGNORED_WORDS = STOPWORDS | FILLER_WORDS


@dataclass
class MatchResult:
    """Container for the outcome of a resume/job-description comparison."""
    score: float
    matched_keywords: list
    missing_keywords: list
    resume_keyword_count: int
    job_keyword_count: int


def extract_keywords(text: str) -> set:
    """
    Convert raw text into a normalized set of keywords.

    Steps:
      1. Lowercase the text.
      2. Strip anything that isn't a letter or space (punctuation, digits).
      3. Split into words.
      4. Drop very short words (<=2 chars) — rarely meaningful, mostly noise.
      5. Remove stopwords and filler words.
    """
    if not text:
        return set()

    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    words = text.split()

    return {
        word for word in words
        if len(word) > 2 and word not in IGNORED_WORDS
    }


def calculate_match(resume_text: str, job_description_text: str) -> MatchResult:
    """
    Compare a resume against a job description and return a MatchResult.

    Score = (keywords appearing in BOTH texts) / (unique keywords in the
    job description) * 100.

    This answers a specific, actionable question — "what percentage of the
    terms this job cares about appear in my resume?" — rather than a vague
    similarity score between two blobs of text.
    """
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description_text)

    if not job_keywords:
        return MatchResult(
            score=0.0,
            matched_keywords=[],
            missing_keywords=[],
            resume_keyword_count=len(resume_keywords),
            job_keyword_count=0,
        )

    matched = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords
    score = round((len(matched) / len(job_keywords)) * 100, 1)

    return MatchResult(
        score=score,
        matched_keywords=sorted(matched),
        missing_keywords=sorted(missing),
        resume_keyword_count=len(resume_keywords),
        job_keyword_count=len(job_keywords),
    )