"""
roadmap.py — Personalized Career Roadmap Generator
Builds a step-by-step learning roadmap from the user's missing skills
and their chosen career target.
"""


# Skill categorization helps order the roadmap logically
SKILL_ORDER = {
    # Foundational programming
    "python": 1,
    "java": 1,
    "c++": 1,
    "javascript": 1,
    "html": 1,
    "css": 1,
    "dart": 1,
    "kotlin": 1,
    "swift": 1,
    # Core data/math
    "sql": 2,
    "excel": 2,
    "statistics": 2,
    "numpy": 2,
    "pandas": 2,
    "data structures": 2,
    "algorithms": 2,
    "oop": 2,
    # Tools and frameworks
    "git": 3,
    "django": 3,
    "flask": 3,
    "react": 3,
    "node.js": 3,
    "rest apis": 3,
    "apis": 3,
    "testing": 3,
    # Visualization and analysis
    "data visualization": 4,
    "tableau": 4,
    "power bi": 4,
    "matplotlib": 4,
    # ML / AI
    "scikit-learn": 5,
    "machine learning": 5,
    "deep learning": 5,
    "nlp": 5,
    "tensorflow": 5,
    "pytorch": 5,
    "computer vision": 5,
    # Infrastructure / Cloud
    "linux": 6,
    "docker": 6,
    "kubernetes": 6,
    "aws": 6,
    "azure": 6,
    "gcp": 6,
    "ci/cd": 6,
    "networking": 6,
    "cloud platforms": 6,
    "terraform": 6,
    "apache spark": 6,
    "airflow": 6,
    "big data": 6,
    "etl": 6,
    # Security
    "security protocols": 7,
    "ethical hacking": 7,
    "firewalls": 7,
    "siem": 7,
    "risk assessment": 7,
    # Design / Product
    "figma": 4,
    "adobe xd": 4,
    "wireframing": 4,
    "prototyping": 4,
    "user research": 4,
    # Soft/business
    "communication": 3,
    "requirements gathering": 3,
    "a/b testing": 4,
    "product management": 4,
}

STAGE_LABELS = {
    1: "🏗️ Build Core Programming Foundation",
    2: "📊 Strengthen Data & Math Skills",
    3: "🔧 Learn Frameworks & Dev Tools",
    4: "📈 Master Visualization & Analysis",
    5: "🤖 Explore AI / Machine Learning",
    6: "☁️ Learn Infrastructure & Cloud",
    7: "🔒 Study Security Specializations",
    8: "🌐 Other Specialized Skills",
}


def _get_skill_stage(skill: str) -> int:
    """Return the learning stage index for a skill (lower = earlier)."""
    key = skill.strip().lower()
    return SKILL_ORDER.get(key, 8)


def generate_roadmap(missing_skills: list, career_name: str, current_skills: list) -> dict:
    """
    Generate an ordered career roadmap from missing skills.

    Parameters
    ----------
    missing_skills : list
        Skills the user needs to learn (from skill gap analysis).
    career_name : str
        The target career name.
    current_skills : list
        Skills the user already has.

    Returns
    -------
    dict with keys:
        'career'    — target career
        'stages'    — list of dicts { 'label': str, 'skills': list }
        'summary'   — short guidance note
    """
    if not missing_skills:
        return {
            "career": career_name,
            "stages": [],
            "summary": (
                f"You already have the core skills needed for {career_name}! "
                "Focus on building projects and gaining practical experience."
            ),
        }

    # Sort missing skills by their stage number
    sorted_skills = sorted(missing_skills, key=lambda s: _get_skill_stage(s))

    # Group skills by stage
    stages_dict = {}
    for skill in sorted_skills:
        stage = _get_skill_stage(skill)
        label = STAGE_LABELS.get(stage, STAGE_LABELS[8])
        if label not in stages_dict:
            stages_dict[label] = []
        stages_dict[label].append(skill)

    stages = [{"label": label, "skills": skills} for label, skills in stages_dict.items()]

    # After learning stages, add final project and career step
    stages.append({
        "label": "🛠️ Build Hands-On Projects",
        "skills": [f"Apply your skills in a real project relevant to {career_name}"],
    })
    stages.append({
        "label": f"🎯 Apply for {career_name} Roles",
        "skills": ["Build your portfolio", "Update your resume", "Start applying!"],
    })

    summary = (
        f"You need to develop {len(missing_skills)} skill(s) to be ready for {career_name}. "
        "Follow the roadmap stages below in order for the most efficient learning path."
    )

    return {
        "career": career_name,
        "stages": stages,
        "summary": summary,
    }
