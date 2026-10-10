# SEQUEL — AI-Powered Career Pathway & Employability Navigator

> **Your skills. Your next step. Your future.**

---

## Project Description

SEQUEL is an AI-powered career guidance and employability platform built for college students, recent graduates, and beginners exploring technology careers.

Unlike a simple job board, SEQUEL takes your current skills and walks you through a complete career pathway:

**Current Skills → Career Matches → Skill Gap Analysis → Personalized Roadmap → What-If Simulation → Project Recommendations**

---

## Problem Statement

Many students and graduates struggle to answer:
- *"Which career fits my current skills?"*
- *"What skills am I missing?"*
- *"What should I learn next?"*
- *"What projects can I build to improve?"*

Generic career websites list hundreds of jobs but provide no personalized guidance. Students are left guessing.

---

## Solution

SEQUEL solves this with an AI pipeline:

1. The user enters their profile (skills, education, interests).
2. A **TF-IDF + Cosine Similarity** engine computes compatibility between the user profile and 20 curated tech career roles.
3. A **Skill Gap Analysis** module identifies exactly which skills are missing.
4. A **Roadmap Generator** builds an ordered learning plan from the missing skills.
5. A **What-If Simulator** lets users see how adding a skill would change their career compatibility.
6. A **Project Recommender** suggests hands-on portfolio projects based on skill gaps.

---

## Features

| Feature | Description |
|---|---|
| 👤 User Profile | Enter skills, education, experience, interests |
| 💼 Career Matches | Top 5 AI-matched careers with compatibility scores |
| 🔍 Skill Gap Analysis | Visual breakdown of skills you have vs. need |
| 🗺️ Career Roadmap | Step-by-step learning path based on your gaps |
| 🧪 What-If Simulator | Simulate adding a skill and see the impact |
| 📁 Project Recommendations | Curated projects to fill your skill gaps |

---

## AI / ML Methodology

### Career Matching
- Text preprocessing: user skills, interests, and branch are combined into a profile text string.
- Career roles are represented as text (required skills + description + category).
- **TF-IDF vectorization** (unigrams + bigrams, English stop words removed) converts all texts to feature vectors.
- **Cosine similarity** scores profile vs. each career vector.
- A **skill overlap ratio** (proportion of required skills present in user profile) is blended with the TF-IDF score (70% TF-IDF, 30% skill overlap) to produce the final **Estimated Compatibility** percentage.
- Scores are model-based estimates — **not** employment probability predictions.

### What-If Simulator
- Recomputes the full matching pipeline with an augmented skill set.
- No hard-coded score changes — every number comes from the same algorithm.

### Project Recommender
- Matches project skills against missing skill gaps.
- Prioritizes projects that cover the most missing skills, then leverages current skills.
- Secondary sort by difficulty (Beginner first).

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Streamlit | Web UI framework |
| Pandas | Data loading and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF vectorization, cosine similarity |
| CSV files | Career and project datasets |

No paid APIs. No API keys required. Fully local.

---

## Project Structure

```
SEQUEL/
│
├── app.py                  # Main Streamlit application
│
├── data/
│   ├── careers.csv         # 20 curated tech career roles
│   └── projects.csv        # 25 practical learning projects
│
├── utils/
│   ├── __init__.py
│   ├── matcher.py          # TF-IDF + cosine similarity career matching
│   ├── skill_gap.py        # Skill gap analysis logic
│   ├── roadmap.py          # Personalized roadmap generator
│   └── recommender.py      # Project recommendation engine
│
├── requirements.txt
├── README.md
├── AGENTS.md
└── .gitignore
```

---

## Installation

### Prerequisites
- Python 3.9 or later
- pip

### Steps

```bash
# 1. Clone or download the project
cd SEQUEL

# 2. (Recommended) Create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## How the Matching Algorithm Works

```
User Profile
    ↓  (skills + interests + branch → single text string)
TF-IDF Vectorizer
    ↓  (fits on profile + all 20 career texts)
Cosine Similarity
    ↓  (profile vector vs. each career vector)
TF-IDF Score (0–1)  ×  0.70
    +
Skill Overlap Ratio  ×  0.30
    ↓
Estimated Compatibility %  (clipped to 0–100)
```

---

## SDG Connection

SEQUEL is aligned with **SDG 1 — No Poverty**.

By helping individuals identify relevant career pathways and develop in-demand skills, SEQUEL supports employability and access to income-generating opportunities. SEQUEL does not claim to directly solve poverty — it is a career guidance tool.

---

## Future Scope

- Resume upload and automated skill extraction (NLP)
- Integration with real job listings APIs
- Course recommendations (Coursera, YouTube)
- User accounts and progress tracking
- Interview preparation module
- Industry-specific career tracks (Finance, Healthcare, etc.)
- Multi-language support

---

## Disclaimer

SEQUEL is a prototype that uses a curated dataset of 20 technology career roles. Compatibility scores are model-based estimates reflecting skill alignment — they are **not** predictions of employment probability or hiring likelihood. SEQUEL does not guarantee employment.
