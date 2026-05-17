import streamlit as st
import pandas as pd
import plotly.express as px

from utils.pdf_reader import extract_pdf_text
from utils.docx_reader import extract_docx_text
from utils.skill_extractor import extract_skills
from utils.ats_score import calculate_ats_score
from utils.openai_helper import get_ai_suggestions


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🚀 AI Resume Analyzer & ATS Optimizer")

st.write("Upload your resume and analyze ATS score using AI.")

# ---------------- SIDEBAR ----------------

st.sidebar.title("📂 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

job_description = st.sidebar.text_area(
    "Paste Job Description"
)

analyze_button = st.sidebar.button("Analyze Resume")

# ---------------- RESUME TEXT ----------------

resume_text = ""

# ---------------- FILE EXTRACTION ----------------

if uploaded_file:

    try:

        # PDF
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_pdf_text(uploaded_file)

        # DOCX
        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_docx_text(uploaded_file)

    except Exception as e:
        st.error(f"Error reading file: {e}")

# ---------------- MAIN ANALYSIS ----------------

if analyze_button and resume_text:

    st.success("✅ Resume Uploaded Successfully")

    # ---------------- DEFAULT JD ----------------

    if not job_description:
        job_description = "General AI Engineer role"

    # ---------------- SKILL EXTRACTION ----------------

    skills_found = extract_skills(resume_text)

    # ---------------- ATS SCORE ----------------

    ats_score = calculate_ats_score(
        resume_text,
        skills_found
    )

    # ---------------- MATCH SCORE ----------------

    match_score = min(
        50 + len(skills_found) * 5,
        100
    )

    # ---------------- TOP METRICS ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{ats_score}%")

    with col2:
        st.metric("Skills Found", len(skills_found))

    with col3:
        st.metric("JD Match", f"{match_score}%")

    # ---------------- SKILLS SECTION ----------------

    st.subheader("🛠 Skills Found")

    if skills_found:

        skill_cols = st.columns(4)

        for index, skill in enumerate(skills_found):

            with skill_cols[index % 4]:
                st.success(skill)

    else:
        st.warning("No skills detected.")

    # ---------------- CHART ----------------

    if skills_found:

        df = pd.DataFrame({
            "Skill": skills_found,
            "Value": [1] * len(skills_found)
        })

        fig = px.bar(
            df,
            x="Skill",
            y="Value",
            title="Detected Skills"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------- RESUME PREVIEW ----------------

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=300
    )

    # ---------------- AI SUGGESTIONS ----------------

    st.subheader("🤖 AI Suggestions")

    if st.button("Generate AI Suggestions"):

        with st.spinner("Analyzing Resume using AI..."):

            try:

                suggestions = get_ai_suggestions(
                    resume_text,
                    job_description
                )

                st.success("AI Analysis Completed ✅")

                st.write(suggestions)

            except Exception as e:

                st.error(f"OpenAI Error: {e}")

else:

    st.info("📌 Upload a Resume and Click 'Analyze Resume'")

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "Built with ❤️ using Python, Streamlit & OpenAI"
)
