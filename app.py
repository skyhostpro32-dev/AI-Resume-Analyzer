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


# ---------------- LOAD CSS ----------------

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.title("🚀 AI Resume Analyzer & ATS Optimizer")

st.write("Upload your resume and analyze ATS score using AI")


# ---------------- SIDEBAR ----------------

st.sidebar.title("📂 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

job_description = st.sidebar.text_area(
    "Paste Job Description"
)
# ---------------- RESUME EXTRACTION ----------------

resume_text = ""

if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_pdf_text(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_docx_text(uploaded_file)


# ---------------- ANALYSIS ----------------
if resume_text:

    st.success("Resume Uploaded Successfully ✅")


    # Extract Skills
    skills_found = extract_skills(resume_text)


    # ATS Score
    ats_score = calculate_ats_score(resume_text, skills_found)


    # ---------------- TOP CARDS ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{ats_score}%")

    with col2:
        st.metric("Skills Found", len(skills_found))

    with col3:
        if job_description:
            st.metric("JD Match", "78%")
        else:
            st.metric("JD Match", "N/A")


    # ---------------- SKILLS ----------------
    st.subheader("🛠 Skills Found")
    
    for skill in skills_found:
        st.success(skill)


    # ---------------- CHART ----------------

    if skills_found:

        df = pd.DataFrame({
            "Skill": skills_found,
            "Value": [1] * len(skills_found)
        })

        fig = px.bar(df, x="Skill", y="Value")

        st.plotly_chart(fig, use_container_width=True)
 # ---------------- RESUME PREVIEW ----------------

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=300
    )


    # ---------------- AI SUGGESTIONS ----------------

    if st.button("✨ Generate AI Suggestions"):

        with st.spinner("Analyzing Resume..."):

            suggestions = get_ai_suggestions(
                resume_text,
                job_description
            )
            st.subheader("🤖 AI Suggestions")

            st.write(suggestions)
else:

    st.info("Upload Resume to Start Analysis")

st.title("🚀 AI Resume Analyzer & ATS Optimizer")
