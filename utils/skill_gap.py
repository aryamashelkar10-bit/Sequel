"""
skill_gap.py — Skill Gap Analysis
Compares a user's skills against the required skills for a selected career
and returns three categories: have, need, and missing.
"""

import pandas as pd


def _normalize(skill: str) -> str:
    """Lowercase and strip a skill string."""
    return skill.strip().lower()


def _parse_skills(skills_str: str) -> list:
    """Parse a comma-separated skills string into a cleaned list."""
    if pd.isna(skills_str) or not str(skills_str).strip():
        return []
    return [_normalize(s) for s in str(skills_str).split(",") if s.strip()]


def analyze_skill_gap(user_skills_raw: str, career_row: pd.Series) -> dict:
    """
    Compare user skills against career required skills.

    Parameters
    ----------
    user_skills_raw : str
        Comma-separated skills entered by the user.
    career_row : pd.Series
        A single row from the careers DataFrame.

    Returns
    -------
    dict with keys:
        'have'    — list of skills the user already has
        'missing' — list of required skills the user is missing
        'all_required' — full list of required skills for this career
        'career'  — career name
        'match_pct' — percentage of required skills the user has
    """
    user_skills = _parse_skills(user_skills_raw)
    required_skills = _parse_skills(career_row.get("Required Skills", ""))

    user_set = set(user_skills)
    required_set = set(required_skills)

    have = sorted(user_set & required_set)
    missing = sorted(required_set - user_set)

    match_pct = 0.0
    if required_set:
        match_pct = round(len(have) / len(required_set) * 100, 1)

    return {
        "career": career_row.get("Career", "Unknown"),
        "have": [s.title() for s in have],
        "missing": [s.title() for s in missing],
        "all_required": [s.title() for s in sorted(required_skills)],
        "match_pct": match_pct,
    }
