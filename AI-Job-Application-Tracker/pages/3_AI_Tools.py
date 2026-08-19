import streamlit as st
from PyPDF2 import PdfReader

from services.ai_service import (
    analyze_job_description,
    analyze_resume_match,
    generate_cover_letter
)

st.title("AI Tools")

st.write(
    "Use AI to analyze job descriptions and compare "
    "your resume against specific job opportunities."
)

st.divider()

# Job Description Analyzer

st.header("Job Description Analyzer")

job_description = st.text_area(
    "Paste a job description",
    height=300,
    key="job_description"
)

if st.button("Analyze Job Description"):

    if job_description.strip():

        with st.spinner("Analyzing job description..."):

            analysis = analyze_job_description(
                job_description
            )

        st.subheader("AI Analysis")

        st.write(analysis)

    else:

        st.warning(
            "Please paste a job description first."
        )

st.divider()

# Resume Upload

st.header("Resume")

uploaded_resume = st.file_uploader(
    "Upload your resume as a PDF",
    type=["pdf"]
)

resume_text = ""

if uploaded_resume is not None:

    reader = PdfReader(uploaded_resume)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    # Clean extracted PDF text
    resume_text = resume_text.replace("\n", " ")
    resume_text = " ".join(resume_text.split())

    st.success("Resume uploaded successfully.")

    with st.expander("View Extracted Resume Text"):

        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )

st.divider()

# Resume Match Analyzer

st.header("Resume Match Analyzer")

if st.button("Analyze Resume Match"):

    if not resume_text.strip():

        st.warning(
            "Please upload your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste a job description above first."
        )

    else:

        with st.spinner(
            "Comparing resume with job description..."
        ):

            analysis = analyze_resume_match(
                resume_text,
                job_description
            )

        st.subheader("Resume Match Analysis")

        st.write(analysis)

st.divider()

# Cover Letter Generator

st.header("Cover Letter Generator")

if st.button("Generate Cover Letter"):

    if not resume_text.strip():

        st.warning(
            "Please upload your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste a job description above first."
        )

    else:

        with st.spinner(
            "Generating tailored cover letter..."
        ):

            cover_letter = generate_cover_letter(
                resume_text,
                job_description
            )

        st.subheader("Generated Cover Letter")

        st.text_area(
            "Cover Letter",
            cover_letter,
            height=500
        )