# app.py
# PURPOSE: Main Streamlit app — Career Path Intelligence System
# RUN WITH: streamlit run app.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Import our three utility modules
from utils.matcher import match_roles
from utils.gap_detector import detect_gaps
from utils.recommender import generate_roadmap

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# Must be the very first Streamlit command
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Career Path Intelligence",
    page_icon="🧭",
    layout="wide"
)

# ─────────────────────────────────────────
# CUSTOM CSS — cleaner look
# ─────────────────────────────────────────
st.markdown("""
    <style>
        .main { padding-top: 1rem; }
        .match-card {
            background-color: #1e1e2e;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #7c3aed;
        }
        .skill-badge-green {
            display: inline-block;
            background-color: #166534;
            color: #bbf7d0;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            margin: 3px;
        }
        .skill-badge-red {
            display: inline-block;
            background-color: #7f1d1d;
            color: #fecaca;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            margin: 3px;
        }
        .priority-high   { color: #f87171; font-weight: bold; }
        .priority-medium { color: #fbbf24; font-weight: bold; }
        .priority-low    { color: #34d399; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🧭 Career Path Intelligence System")
st.markdown("#### Discover the best-fit roles for your skills — and exactly how to close the gap.")
st.divider()


# ─────────────────────────────────────────
# SIDEBAR — Controls
# ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    top_n = st.slider(
        "Number of roles to show",
        min_value=1,
        max_value=10,
        value=5,
        help="How many top matching job roles to display"
    )

    show_roadmap = st.toggle(
        "Show Learning Roadmap",
        value=True,
        help="Show courses and resources for missing skills"
    )

    st.divider()
    st.markdown("**About**")
    st.caption(
        "Built with Python, Scikit-learn, and Streamlit. "
        "Matches your skills to 42 real job roles using "
        "TF-IDF + Cosine Similarity."
    )


# ─────────────────────────────────────────
# SKILL INPUT
# ─────────────────────────────────────────
st.subheader("📝 Enter Your Skills")

user_input = st.text_area(
    label="Type your skills below (comma-separated or plain text):",
    placeholder="e.g. Python, SQL, Machine Learning, Data Analysis, Pandas, Scikit-learn",
    height=100,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    analyse_clicked = st.button("🔍 Analyse My Skills", type="primary", use_container_width=True)
with col2:
    clear_clicked = st.button("🗑️ Clear", use_container_width=True)

if clear_clicked:
    st.rerun()


# ─────────────────────────────────────────
# EXAMPLE SKILL SETS — Quick start buttons
# ─────────────────────────────────────────
st.markdown("**Or try an example:**")
ex1, ex2, ex3 = st.columns(3)

with ex1:
    if st.button("💻 Data Science Profile"):
        user_input = "python machine learning data analysis sql pandas numpy scikit-learn"
        analyse_clicked = True

with ex2:
    if st.button("🌐 Web Dev Profile"):
        user_input = "html css javascript react node.js frontend web development"
        analyse_clicked = True

with ex3:
    if st.button("📣 Marketing Profile"):
        user_input = "marketing social media brand strategy google analytics seo content"
        analyse_clicked = True


# ─────────────────────────────────────────
# MAIN ANALYSIS — runs when button clicked
# ─────────────────────────────────────────
if analyse_clicked and user_input.strip():

    st.divider()

    # Show a spinner while processing
    with st.spinner("Analysing your skills against 42 job roles..."):
        matches = match_roles(user_input.strip(), top_n=top_n)

    if not matches:
        st.warning("No strong matches found. Try adding more skills.")
        st.stop()

    # ─────────────────────────────────────
    # SECTION 1 — Match Score Chart
    # ─────────────────────────────────────
    st.subheader("🎯 Your Top Career Matches")

    roles_list  = [m['role'].title() for m in matches]
    scores_list = [m['score'] for m in matches]

    fig = go.Figure(go.Bar(
        x=scores_list,
        y=roles_list,
        orientation='h',
        marker=dict(
            color=scores_list,
            colorscale='Viridis',
            showscale=False
        ),
        text=[f"{s}%" for s in scores_list],
        textposition='outside'
    ))

    fig.update_layout(
        xaxis_title="Match Score (%)",
        yaxis=dict(autorange="reversed"),
        height=80 + (len(matches) * 55),
        margin=dict(l=10, r=60, t=10, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # ─────────────────────────────────────
    # SECTION 2 — Role Cards with Gap Analysis
    # ─────────────────────────────────────
    st.subheader("🔍 Detailed Role Analysis")

    for i, match in enumerate(matches):
        role_name  = match['role'].title()
        score      = match['score']
        role_skills = match['skills']

        # Run gap detection for this role
        gap_result = detect_gaps(user_input.strip(), role_skills)
        matched_skills  = gap_result['matched']
        missing_skills  = gap_result['missing']
        coverage        = gap_result['coverage']

        # Expandable card per role
        with st.expander(f"{'🥇' if i==0 else '🔹'} {role_name}  —  {score}% Match", expanded=(i == 0)):

            # Coverage progress bar
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**Skill Coverage:** {coverage}%")
                st.progress(int(coverage) / 100)
            with col_b:
                st.metric("Match Score", f"{score}%")

            st.markdown("---")

            # Skills you have
            if matched_skills:
                st.markdown("**✅ Skills You Already Have:**")
                badges_html = " ".join([
                    f'<span class="skill-badge-green">{s}</span>'
                    for s in matched_skills[:10]  # cap display at 10
                ])
                st.markdown(badges_html, unsafe_allow_html=True)

            st.markdown("")

            # Skills you're missing
            if missing_skills:
                st.markdown("**❌ Skills You're Missing:**")
                badges_html = " ".join([
                    f'<span class="skill-badge-red">{s}</span>'
                    for s in missing_skills[:10]
                ])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.success("You have strong coverage for this role!")

            # ─────────────────────────────
            # ROADMAP SECTION
            # ─────────────────────────────
            if show_roadmap and missing_skills:
                st.markdown("---")
                st.markdown("**📚 Your Learning Roadmap:**")

                roadmap = generate_roadmap(missing_skills, match['role'])

                if roadmap:
                    roadmap_df = pd.DataFrame([{
                        "Priority": step['priority'],
                        "Skill": step['skill'].title(),
                        "Course": step['resource']['title'],
                        "Platform": step['resource']['platform'],
                        "Duration": step['resource']['duration'],
                        "Link": step['resource']['url']
                    } for step in roadmap])

                    # Color priority column
                    st.dataframe(
                        roadmap_df,
                        column_config={
                            "Link": st.column_config.LinkColumn("Link")
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No specific resources found. Search Coursera or YouTube for these skills.")

    # ─────────────────────────────────────
    # SECTION 3 — Skills Gap Summary Chart
    # ─────────────────────────────────────
    st.divider()
    st.subheader("📊 Skills Coverage Overview")

    # Build coverage data for all roles
    coverage_data = []
    for match in matches:
        gap = detect_gaps(user_input.strip(), match['skills'])
        coverage_data.append({
            'Role': match['role'].title(),
            'You Have': gap['coverage'],
            'Gap': round(100 - gap['coverage'], 1)
        })

    cov_df = pd.DataFrame(coverage_data)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Skills You Have",
        x=cov_df['Role'],
        y=cov_df['You Have'],
        marker_color='#10b981'
    ))
    fig2.add_trace(go.Bar(
        name="Skills Gap",
        x=cov_df['Role'],
        y=cov_df['Gap'],
        marker_color='#ef4444'
    ))

    fig2.update_layout(
        barmode='stack',
        yaxis_title="Coverage (%)",
        height=400,
        margin=dict(l=10, r=10, t=10, b=80),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )

    st.plotly_chart(fig2, use_container_width=True)


elif analyse_clicked and not user_input.strip():
    st.warning("Please enter at least a few skills before analysing.")