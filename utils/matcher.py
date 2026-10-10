"""
matcher.py — Career Matching Engine
Uses TF-IDF vectorization and cosine similarity to match a user profile
against curated career roles in the dataset.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def load_careers(path: str) -> pd.DataFrame:
    """Load and return the careers dataset from a CSV file."""
    df = pd.read_csv(path)
    return df


def _normalize_skill(skill: str) -> str:
    """Lowercase and strip a single skill string."""
    return skill.strip().lower()


def _skills_to_list(skills_str: str) -> list:
    """Convert a comma-separated skills string into a cleaned list."""
    if pd.isna(skills_str) or not skills_str:
        return []
    return [_normalize_skill(s) for s in skills_str.split(",") if s.strip()]


def _build_profile_text(skills: list, interests: str, branch: str) -> str:
    """
    Combine user skills, interests, and branch into a single text blob
    that can be compared with career descriptions via TF-IDF.
    """
    parts = skills + [interests, branch]
    return " ".join([p.lower() for p in parts if p])


def _build_career_text(row: pd.Series) -> str:
    """
    Combine career metadata into a single text blob for TF-IDF.
    We repeat Required Skills to give them higher weight.
    """
    skills_text = row["Required Skills"].lower() if pd.notna(row["Required Skills"]) else ""
    description = row["Description"].lower() if pd.notna(row["Description"]) else ""
    category = row["Category"].lower() if pd.notna(row["Category"]) else ""
    # Repeat skills twice to boost their weight in TF-IDF
    return f"{skills_text} {skills_text} {description} {category}"


def compute_matches(
    user_skills: list,
    user_interests: str,
    user_branch: str,
    careers_df: pd.DataFrame,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Compute cosine-similarity-based compatibility scores between the user
    profile and each career in the dataset.

    Returns the top_n careers sorted by compatibility score (descending),
    with an additional 'Compatibility' column (0-100 float).
    """
    if careers_df.empty:
        return pd.DataFrame()

    # Build text representations
    profile_text = _build_profile_text(user_skills, user_interests, user_branch)
    career_texts = careers_df.apply(_build_career_text, axis=1).tolist()

    if not profile_text.strip():
        # No profile info — return empty
        return pd.DataFrame()

    # Fit TF-IDF on all documents (profile + careers)
    all_texts = [profile_text] + career_texts
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),  # unigrams and bigrams
        min_df=1,
    )
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Profile vector is the first row; career vectors are the rest
    profile_vec = tfidf_matrix[0:1]
    career_vecs = tfidf_matrix[1:]

    # Cosine similarity scores: shape (1, n_careers)
    scores = cosine_similarity(profile_vec, career_vecs).flatten()

    # Attach scores and sort
    result_df = careers_df.copy()
    result_df["raw_score"] = scores

    # Scale to 0-100 percentage (purely model-based, not employment probability)
    max_score = scores.max() if scores.max() > 0 else 1.0
    result_df["Compatibility"] = (scores / max_score * 100).round(1)

    # Also compute a secondary "skill overlap" boost
    user_skill_set = set(user_skills)
    def _skill_overlap(row):
        career_skills = set(_skills_to_list(row["Required Skills"]))
        if not career_skills:
            return 0.0
        overlap = len(user_skill_set & career_skills) / len(career_skills)
        return overlap

    result_df["skill_overlap"] = result_df.apply(_skill_overlap, axis=1)

    # Blend TF-IDF score (70%) with skill overlap (30%) for final score
    result_df["Compatibility"] = (
        0.70 * result_df["Compatibility"] + 0.30 * result_df["skill_overlap"] * 100
    ).round(1)

    # Clip to [0, 100]
    result_df["Compatibility"] = result_df["Compatibility"].clip(0, 100)

    # Get matching skills for display
    def _matching_skills(row):
        career_skills = set(_skills_to_list(row["Required Skills"]))
        matched = sorted(user_skill_set & career_skills)
        return ", ".join([s.title() for s in matched]) if matched else "—"

    result_df["Matching Skills"] = result_df.apply(_matching_skills, axis=1)

    # Return top_n sorted by Compatibility
    top = result_df.sort_values("Compatibility", ascending=False).head(top_n)
    return top.reset_index(drop=True)


def get_career_by_name(name: str, careers_df: pd.DataFrame) -> pd.Series:
    """Return the first career row matching the given name (case-insensitive)."""
    match = careers_df[careers_df["Career"].str.lower() == name.lower()]
    if match.empty:
        return None
    return match.iloc[0]
