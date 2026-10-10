"""
recommender.py — Project Recommendation Engine
Recommends practical projects based on the user's missing skills
to help them build their portfolio while learning.
"""

import pandas as pd


def load_projects(path: str) -> pd.DataFrame:
    """Load and return the projects dataset from a CSV file."""
    df = pd.read_csv(path)
    return df


def _normalize(skill: str) -> str:
    return skill.strip().lower()


def _parse_skills(skills_str: str) -> list:
    """Parse a comma-separated skills string into a cleaned list."""
    if pd.isna(skills_str) or not str(skills_str).strip():
        return []
    return [_normalize(s) for s in str(skills_str).split(",") if s.strip()]


def recommend_projects(
    missing_skills: list,
    current_skills: list,
    projects_df: pd.DataFrame,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Recommend projects based on the user's missing and current skills.

    Strategy:
    1. Prioritize projects that teach at least one missing skill.
    2. Among those, prefer projects that also leverage current skills.
    3. Sort by missing-skill coverage descending, then difficulty ascending.

    Parameters
    ----------
    missing_skills : list
        Skills the user needs to develop.
    current_skills : list
        Skills the user already has.
    projects_df : pd.DataFrame
        The projects dataset.
    top_n : int
        Maximum number of recommendations to return.

    Returns
    -------
    pd.DataFrame with columns including 'relevance_score'.
    """
    if projects_df.empty:
        return pd.DataFrame()

    missing_set = set([_normalize(s) for s in missing_skills])
    current_set = set([_normalize(s) for s in current_skills])

    # Difficulty ordering for secondary sort
    difficulty_order = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

    rows = []
    for _, project in projects_df.iterrows():
        project_skills = set(_parse_skills(project.get("Skills", "")))

        # How many missing skills does this project address?
        missing_covered = len(project_skills & missing_set)
        # How many current skills does it reinforce?
        current_covered = len(project_skills & current_set)
        total_covered = missing_covered + current_covered

        # Only include if it covers at least one missing skill
        # or if we have very few missing skills, also show starter projects
        if missing_covered == 0 and len(missing_set) > 0:
            continue

        rows.append({
            **project.to_dict(),
            "missing_covered": missing_covered,
            "current_covered": current_covered,
            "total_covered": total_covered,
            "difficulty_order": difficulty_order.get(project.get("Difficulty", ""), 99),
        })

    if not rows:
        # Fallback: return beginner projects
        fallback = projects_df[projects_df["Difficulty"] == "Beginner"].head(top_n)
        return fallback.copy()

    result_df = pd.DataFrame(rows)
    result_df = result_df.sort_values(
        ["missing_covered", "current_covered", "difficulty_order"],
        ascending=[False, False, True],
    ).head(top_n)

    return result_df.reset_index(drop=True)
