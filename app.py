"""
SEQUEL — AI-Powered Career Pathway & Employability Navigator
============================================================
Main Streamlit application.

Run with:
    streamlit run app.py
"""

import os
import sys
import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Path setup — ensure utils/ is importable
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from utils.matcher import load_careers, compute_matches, get_career_by_name, _skills_to_list
from utils.skill_gap import analyze_skill_gap
from utils.roadmap import generate_roadmap
from utils.recommender import load_projects, recommend_projects

# ---------------------------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SEQUEL — Career Navigator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — clean, professional, minimal
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main background */
    .main { background-color: #f9fafb; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #cbd5e1 !important;
        font-size: 0.95rem;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
    }

    /* Cards */
    .card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .card-accent {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .skill-have {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .skill-missing {
        display: inline-block;
        background: #fee2e2;
        color: #991b1b;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .badge {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-left: 6px;
    }
    .roadmap-step {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0.6rem;
    }
    .step-dot {
        width: 12px;
        height: 12px;
        background: #3b82f6;
        border-radius: 50%;
        margin-top: 5px;
        margin-right: 12px;
        flex-shrink: 0;
    }
    .disclaimer {
        background: #fefce8;
        border: 1px solid #fde68a;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.82rem;
        color: #92400e;
        margin-top: 0.5rem;
    }
    h1, h2, h3, h4 { color: #1e293b; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data loading (cached so it only happens once)
# ---------------------------------------------------------------------------
@st.cache_data
def get_careers():
    return load_careers(os.path.join(BASE_DIR, "data", "careers.csv"))

@st.cache_data
def get_projects():
    return load_projects(os.path.join(BASE_DIR, "data", "projects.csv"))

careers_df = get_careers()
projects_df = get_projects()

# ---------------------------------------------------------------------------
# Session state — persist user profile across pages
# ---------------------------------------------------------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "",
        "education": "",
        "branch": "",
        "skills": "",
        "experience": "Student / No experience",
        "interests": "",
        "target": "",
    }

if "selected_career" not in st.session_state:
    st.session_state.selected_career = None

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("# 🎯 SEQUEL")
    st.markdown("*AI Career Navigator*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "👤 My Profile",
            "💼 Career Matches",
            "🔍 Skill Gap",
            "🗺️ Career Roadmap",
            "🧪 What-If Simulator",
            "📁 Project Recommendations",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#94a3b8'>Uses a curated dataset of 20 tech career roles.<br>"
        "This is a prototype for career guidance.</small>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Helper: parse user skills into a list
# ---------------------------------------------------------------------------
def parse_skills(raw: str) -> list:
    if not raw or not raw.strip():
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]

# ---------------------------------------------------------------------------
# Helper: profile completeness check
# ---------------------------------------------------------------------------
def profile_filled() -> bool:
    p = st.session_state.profile
    return bool(p["skills"].strip())

# ---------------------------------------------------------------------------
# PAGE: Home
# ---------------------------------------------------------------------------
if page == "🏠 Home":
    st.title("🎯 SEQUEL")
    st.markdown("### AI-Powered Career Pathway & Employability Navigator")
    st.markdown("*Your skills. Your next step. Your future.*")
    st.markdown("---")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(
            """
            <div class="card">
            <h4>What is SEQUEL?</h4>
            <p>
            SEQUEL is an AI-powered career guidance platform designed for college students,
            recent graduates, and beginners exploring tech careers.
            </p>
            <p>
            SEQUEL does <b>not</b> simply show you a list of jobs.
            It takes your current skills and guides you through a complete pathway:
            </p>
            <ul>
                <li>🔍 Discover the best-fitting career roles for your current skills</li>
                <li>📊 Understand exactly which skills you're missing</li>
                <li>🗺️ Get a personalized step-by-step learning roadmap</li>
                <li>🧪 Simulate "what if I learn this skill?" scenarios</li>
                <li>📁 Get hands-on project recommendations to build your portfolio</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card-accent">
            <b>🌍 SDG Connection</b><br>
            SEQUEL is aligned with <b>SDG 1 — No Poverty</b>. By helping individuals
            identify relevant career pathways and develop in-demand skills, SEQUEL
            supports employability and access to income-generating opportunities.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
            <h4>How It Works</h4>
            <ol>
                <li><b>Enter your profile</b> — skills, education, interests</li>
                <li><b>AI matches careers</b> using TF-IDF + Cosine Similarity</li>
                <li><b>Review skill gaps</b> for your chosen career</li>
                <li><b>Follow your roadmap</b> — step-by-step plan</li>
                <li><b>Simulate skill additions</b> to see their impact</li>
                <li><b>Build projects</b> to strengthen your portfolio</li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="disclaimer">
            ⚠️ <b>Disclaimer:</b> Compatibility scores are model-based estimates.
            They reflect skill alignment with career roles — not predictions of
            employment probability or hiring likelihood.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("👉 **Start here:** Go to **My Profile** in the sidebar to enter your details.")

# ---------------------------------------------------------------------------
# PAGE: My Profile
# ---------------------------------------------------------------------------
elif page == "👤 My Profile":
    st.title("👤 My Profile")
    st.markdown("Tell SEQUEL about yourself. Your skills are the most important input.")
    st.markdown("---")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", value=st.session_state.profile["name"])
            education = st.selectbox(
                "Education Level",
                ["", "High School", "Diploma", "Bachelor's", "Master's", "PhD", "Self-taught"],
                index=["", "High School", "Diploma", "Bachelor's", "Master's", "PhD", "Self-taught"].index(
                    st.session_state.profile["education"]
                ) if st.session_state.profile["education"] in ["", "High School", "Diploma", "Bachelor's", "Master's", "PhD", "Self-taught"] else 0,
            )
            branch = st.text_input(
                "Branch / Field of Study",
                value=st.session_state.profile["branch"],
                placeholder="e.g. Computer Science, Electronics, Commerce",
            )
        with col2:
            experience = st.selectbox(
                "Experience Level",
                [
                    "Student / No experience",
                    "0-1 years",
                    "1-2 years",
                    "2-4 years",
                    "4+ years",
                ],
                index=[
                    "Student / No experience", "0-1 years", "1-2 years", "2-4 years", "4+ years"
                ].index(st.session_state.profile["experience"])
                if st.session_state.profile["experience"] in ["Student / No experience", "0-1 years", "1-2 years", "2-4 years", "4+ years"]
                else 0,
            )
            interests = st.text_input(
                "Your Interests",
                value=st.session_state.profile["interests"],
                placeholder="e.g. Data Science, Web Development, AI",
            )
            target = st.text_input(
                "Target Career (optional)",
                value=st.session_state.profile["target"],
                placeholder="e.g. Data Scientist",
            )

        skills = st.text_area(
            "Your Skills (comma-separated) *",
            value=st.session_state.profile["skills"],
            placeholder="e.g. Python, SQL, Excel, Pandas, HTML, CSS",
            height=80,
            help="Enter all the technologies, tools, and languages you know.",
        )

        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)

    if submitted:
        if not skills.strip():
            st.error("Please enter at least one skill.")
        else:
            st.session_state.profile.update({
                "name": name,
                "education": education,
                "branch": branch,
                "skills": skills,
                "experience": experience,
                "interests": interests,
                "target": target,
            })
            # Clear cached matches when profile changes
            if "matches" in st.session_state:
                del st.session_state["matches"]
            st.success("✅ Profile saved! Navigate to Career Matches to see your results.")

    # Preview saved profile
    if profile_filled():
        st.markdown("---")
        st.markdown("#### 📋 Saved Profile")
        p = st.session_state.profile
        skill_list = parse_skills(p["skills"])
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {p['name'] or '—'}")
            st.markdown(f"**Education:** {p['education'] or '—'}")
            st.markdown(f"**Branch:** {p['branch'] or '—'}")
        with col2:
            st.markdown(f"**Experience:** {p['experience']}")
            st.markdown(f"**Interests:** {p['interests'] or '—'}")
            st.markdown(f"**Target Career:** {p['target'] or '—'}")
        st.markdown(f"**Skills ({len(skill_list)}):** " + " ".join([f"`{s}`" for s in skill_list]))

# ---------------------------------------------------------------------------
# PAGE: Career Matches
# ---------------------------------------------------------------------------
elif page == "💼 Career Matches":
    st.title("💼 Career Matches")
    st.markdown("AI-powered career compatibility based on your profile.")
    st.markdown("---")

    if not profile_filled():
        st.warning("⚠️ Please complete your profile first. Go to **My Profile**.")
        st.stop()

    p = st.session_state.profile
    user_skills = parse_skills(p["skills"])

    # Compute matches (cache in session state so we don't recompute every render)
    if "matches" not in st.session_state:
        with st.spinner("Running career matching algorithm…"):
            matches = compute_matches(
                user_skills=user_skills,
                user_interests=p["interests"],
                user_branch=p["branch"],
                careers_df=careers_df,
                top_n=5,
            )
            st.session_state["matches"] = matches
    else:
        matches = st.session_state["matches"]

    if matches.empty:
        st.error("Could not compute matches. Please check your profile.")
        st.stop()

    st.markdown(
        '<div class="disclaimer">ℹ️ Scores below are <b>estimated model-based compatibility</b> '
        '(TF-IDF + cosine similarity + skill overlap). They are <b>not</b> predictions of '
        'employment probability or hiring likelihood.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    for i, row in matches.iterrows():
        score = row["Compatibility"]
        color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        with st.container():
            st.markdown(
                f"""
                <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:1.15rem; font-weight:700; color:#1e293b;">
                            #{i+1}  {row['Career']}
                        </span>
                        <span class="badge">{row['Category']}</span>
                    </div>
                    <div style="font-size:1.4rem; font-weight:800; color:{color};">
                        {score}%
                    </div>
                </div>
                <div style="color:#57606a; margin:6px 0; font-size:0.9rem;">{row['Description']}</div>
                <div style="font-size:0.85rem;">
                    <b>Matching Skills:</b> {row['Matching Skills']}<br>
                    <b>Experience:</b> {row['Experience']} &nbsp;|&nbsp; <b>Education:</b> {row['Education']}
                </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("**Next step:** Select a career for Skill Gap analysis → go to **Skill Gap** in the sidebar.")
    career_options = matches["Career"].tolist()
    selected = st.selectbox("Select a career to analyze further:", career_options)
    if st.button("Set as Target Career", use_container_width=True):
        st.session_state.selected_career = selected
        st.success(f"✅ Target career set to: **{selected}**. Now explore Skill Gap, Roadmap, and Projects.")

# ---------------------------------------------------------------------------
# PAGE: Skill Gap
# ---------------------------------------------------------------------------
elif page == "🔍 Skill Gap":
    st.title("🔍 Skill Gap Analysis")
    st.markdown("See exactly which skills you have and which you need to develop.")
    st.markdown("---")

    if not profile_filled():
        st.warning("⚠️ Please complete your profile first.")
        st.stop()

    # Career selector
    all_career_names = careers_df["Career"].tolist()
    default_career = st.session_state.get("selected_career") or all_career_names[0]
    default_idx = all_career_names.index(default_career) if default_career in all_career_names else 0

    career_choice = st.selectbox("Choose a career to analyze:", all_career_names, index=default_idx)
    st.session_state.selected_career = career_choice

    career_row = get_career_by_name(career_choice, careers_df)
    if career_row is None:
        st.error("Career not found in dataset.")
        st.stop()

    gap = analyze_skill_gap(st.session_state.profile["skills"], career_row)

    # Summary bar
    st.markdown(
        f"""
        <div class="card-accent">
        <b>Skill Match for {gap['career']}:</b>
        You have <b>{len(gap['have'])}</b> of <b>{len(gap['all_required'])}</b> required skills
        &nbsp;|&nbsp; Coverage: <b>{gap['match_pct']}%</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Skills You Have")
        if gap["have"]:
            pills = " ".join([f'<span class="skill-have">✓ {s}</span>' for s in gap["have"]])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("None of the required skills matched your profile yet.")

    with col2:
        st.markdown("#### 🔴 Skills to Develop")
        if gap["missing"]:
            pills = " ".join([f'<span class="skill-missing">○ {s}</span>' for s in gap["missing"]])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.success("🎉 You already have all the required skills for this career!")

    st.markdown("---")
    st.markdown("#### 📋 All Required Skills for " + career_choice)
    all_pills = []
    for skill in gap["all_required"]:
        if skill in gap["have"]:
            all_pills.append(f'<span class="skill-have">✓ {skill}</span>')
        else:
            all_pills.append(f'<span class="skill-missing">○ {skill}</span>')
    st.markdown(" ".join(all_pills), unsafe_allow_html=True)

    st.markdown(
        '<div class="disclaimer" style="margin-top:1rem;">This analysis compares your stated skills '
        'against the curated required-skills list for this career role. It is a guideline, not an '
        'exhaustive requirement checklist.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# PAGE: Career Roadmap
# ---------------------------------------------------------------------------
elif page == "🗺️ Career Roadmap":
    st.title("🗺️ Career Roadmap")
    st.markdown("Your personalized learning path to reach your target career.")
    st.markdown("---")

    if not profile_filled():
        st.warning("⚠️ Please complete your profile first.")
        st.stop()

    all_career_names = careers_df["Career"].tolist()
    default_career = st.session_state.get("selected_career") or all_career_names[0]
    default_idx = all_career_names.index(default_career) if default_career in all_career_names else 0

    career_choice = st.selectbox("Generate roadmap for:", all_career_names, index=default_idx)
    st.session_state.selected_career = career_choice

    career_row = get_career_by_name(career_choice, careers_df)
    gap = analyze_skill_gap(st.session_state.profile["skills"], career_row)

    current_skills = parse_skills(st.session_state.profile["skills"])
    roadmap = generate_roadmap(
        missing_skills=gap["missing"],
        career_name=career_choice,
        current_skills=current_skills,
    )

    st.markdown(
        f'<div class="card-accent"><b>Target:</b> {roadmap["career"]}<br>{roadmap["summary"]}</div>',
        unsafe_allow_html=True,
    )

    if not gap["missing"]:
        st.success("🎉 You already have the required skills! Focus on projects and experience.")
    else:
        st.markdown("---")
        # Starting point
        st.markdown(
            """
            <div style="display:flex; align-items:center; margin-bottom:0.5rem;">
                <div style="background:#3b82f6; color:white; border-radius:8px; padding:6px 14px; font-weight:600;">
                    📍 Current Profile
                </div>
            </div>
            <div style="margin-left:18px; border-left:3px dashed #cbd5e1; padding-left:12px; margin-bottom:0.5rem; color:#64748b; font-size:0.88rem;">
                Skills: """ + (", ".join(current_skills[:6]) + ("..." if len(current_skills) > 6 else "")) + """
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i, stage in enumerate(roadmap["stages"]):
            is_final = i == len(roadmap["stages"]) - 1
            bg = "#1e293b" if is_final else "#f8fafc"
            color = "#f1f5f9" if is_final else "#1e293b"
            border = "#1e293b" if is_final else "#e2e8f0"
            skills_text = " · ".join(stage["skills"])
            st.markdown(
                f"""
                <div style="margin-left:18px; border-left:3px dashed #cbd5e1;">
                    <div style="margin-left:-8px; margin-bottom:4px; color:#3b82f6; font-size:1.2rem;">↓</div>
                </div>
                <div style="background:{bg}; color:{color}; border:1px solid {border}; 
                            border-radius:10px; padding:10px 16px; margin-bottom:2px; margin-left:6px;">
                    <div style="font-weight:700; font-size:0.95rem;">{stage['label']}</div>
                    <div style="font-size:0.85rem; margin-top:4px; opacity:0.85;">{skills_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# PAGE: What-If Simulator
# ---------------------------------------------------------------------------
elif page == "🧪 What-If Simulator":
    st.title("🧪 Career What-If Simulator")
    st.markdown("Explore how adding a new skill would change your career compatibility.")
    st.markdown("---")

    if not profile_filled():
        st.warning("⚠️ Please complete your profile first.")
        st.stop()

    st.markdown(
        '<div class="disclaimer">⚠️ All scores are <b>estimated model-based compatibility scores</b> '
        'produced by the same TF-IDF + cosine similarity system. They are <b>not</b> employment '
        'predictions. Use them as a relative guide only.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    p = st.session_state.profile
    current_skills = parse_skills(p["skills"])

    col1, col2 = st.columns([2, 1])
    with col1:
        additional_skill = st.text_input(
            "Skill you are considering learning:",
            placeholder="e.g. Machine Learning, Docker, React",
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        simulate_btn = st.button("🔬 Simulate", use_container_width=True)

    if simulate_btn:
        if not additional_skill.strip():
            st.error("Please enter a skill to simulate.")
        else:
            new_skill = additional_skill.strip()
            if new_skill.lower() in [s.lower() for s in current_skills]:
                st.info(f"**{new_skill}** is already in your profile. Try a different skill.")
            else:
                with st.spinner("Calculating before and after compatibility…"):
                    # BEFORE
                    before_matches = compute_matches(
                        user_skills=current_skills,
                        user_interests=p["interests"],
                        user_branch=p["branch"],
                        careers_df=careers_df,
                        top_n=5,
                    )
                    # AFTER
                    updated_skills = current_skills + [new_skill]
                    after_matches = compute_matches(
                        user_skills=updated_skills,
                        user_interests=p["interests"],
                        user_branch=p["branch"],
                        careers_df=careers_df,
                        top_n=5,
                    )

                st.markdown(f"### Results: Adding **{new_skill}**")
                st.markdown("---")

                # Merge on Career for side-by-side comparison
                before_dict = dict(zip(before_matches["Career"], before_matches["Compatibility"]))
                after_dict = dict(zip(after_matches["Career"], after_matches["Compatibility"]))

                # Show union of top careers
                all_careers = list(
                    dict.fromkeys(
                        list(before_matches["Career"]) + list(after_matches["Career"])
                    )
                )

                any_gain = False
                for career in all_careers[:6]:
                    b_score = before_dict.get(career, 0.0)
                    a_score = after_dict.get(career, 0.0)
                    delta = round(a_score - b_score, 1)
                    delta_color = "#22c55e" if delta > 0 else "#ef4444" if delta < 0 else "#64748b"
                    delta_icon = "▲" if delta > 0 else "▼" if delta < 0 else "►"
                    if delta > 0:
                        any_gain = True

                    st.markdown(
                        f"""
                        <div class="card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:700; font-size:1rem;">{career}</div>
                            <div style="font-size:0.95rem; color:{delta_color}; font-weight:700;">
                                {delta_icon} {delta:+.1f}%
                            </div>
                        </div>
                        <div style="display:flex; gap:2rem; margin-top:8px; font-size:0.9rem;">
                            <div>
                                <span style="color:#64748b;">Before</span><br>
                                <span style="font-size:1.3rem; font-weight:700; color:#475569;">{b_score:.1f}%</span>
                            </div>
                            <div style="display:flex; align-items:center; color:#94a3b8; font-size:1.3rem;">→</div>
                            <div>
                                <span style="color:#64748b;">After adding {new_skill}</span><br>
                                <span style="font-size:1.3rem; font-weight:700; color:#1d4ed8;">{a_score:.1f}%</span>
                            </div>
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                if any_gain:
                    st.success(
                        f"✅ Learning **{new_skill}** improves your compatibility with at least one career role."
                    )
                else:
                    st.info(
                        f"ℹ️ Adding **{new_skill}** does not significantly change compatibility with these careers. "
                        "Consider a skill more directly aligned with your target role."
                    )

# ---------------------------------------------------------------------------
# PAGE: Project Recommendations
# ---------------------------------------------------------------------------
elif page == "📁 Project Recommendations":
    st.title("📁 Project Recommendations")
    st.markdown("Hands-on projects to help you build your portfolio and fill your skill gaps.")
    st.markdown("---")

    if not profile_filled():
        st.warning("⚠️ Please complete your profile first.")
        st.stop()

    all_career_names = careers_df["Career"].tolist()
    default_career = st.session_state.get("selected_career") or all_career_names[0]
    default_idx = all_career_names.index(default_career) if default_career in all_career_names else 0

    career_choice = st.selectbox(
        "Show projects relevant to my gaps for:", all_career_names, index=default_idx
    )
    st.session_state.selected_career = career_choice

    career_row = get_career_by_name(career_choice, careers_df)
    gap = analyze_skill_gap(st.session_state.profile["skills"], career_row)
    current_skills = parse_skills(st.session_state.profile["skills"])

    recs = recommend_projects(
        missing_skills=gap["missing"],
        current_skills=current_skills,
        projects_df=projects_df,
        top_n=5,
    )

    if recs.empty:
        st.info("No specific project recommendations found. Try updating your skill gaps.")
    else:
        diff_colors = {
            "Beginner": ("#dcfce7", "#166534"),
            "Intermediate": ("#fef9c3", "#854d0e"),
            "Advanced": ("#fee2e2", "#991b1b"),
        }

        for _, proj in recs.iterrows():
            diff = proj.get("Difficulty", "")
            bg, fg = diff_colors.get(diff, ("#f1f5f9", "#475569"))
            proj_skills = proj.get("Skills", "—")
            st.markdown(
                f"""
                <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="font-size:1.05rem; font-weight:700; color:#1e293b;">
                        📂 {proj['Project Name']}
                    </div>
                    <span style="background:{bg}; color:{fg}; border-radius:12px; 
                                 padding:2px 10px; font-size:0.78rem; font-weight:600; white-space:nowrap;">
                        {diff}
                    </span>
                </div>
                <div style="color:#57606a; font-size:0.9rem; margin:6px 0;">
                    {proj['Description']}
                </div>
                <div style="font-size:0.83rem; color:#475569;">
                    <b>Skills practiced:</b> {proj_skills}
                </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="disclaimer" style="margin-top:1rem;">Projects are selected from a curated dataset '
        'based on your skill gaps. They are intended as learning exercises and portfolio builders.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:0.78rem;'>"
    "SEQUEL — AI-Powered Career Navigator · Prototype · Uses curated career data · "
    "Not an employment prediction tool"
    "</div>",
    unsafe_allow_html=True,
)
