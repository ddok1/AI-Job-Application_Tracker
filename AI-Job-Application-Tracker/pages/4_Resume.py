import streamlit as st
from PyPDF2 import PdfReader

st.title("Resume")

st.write(
    "Upload your resume as a PDF to extract and review "
    "your resume text."
)

st.divider()

# Resume Upload

st.header("Upload Resume")

uploaded_resume = st.file_uploader(
    "Choose a PDF resume",
    type=["pdf"]
)

if uploaded_resume is not None:

    reader = PdfReader(uploaded_resume)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    # Clean extracted text
    resume_text = resume_text.replace(
        "\n",
        " "
    )

    resume_text = " ".join(
        resume_text.split()
    )

    st.success("Resume uploaded successfully.")

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=500
    )

else:

    st.info(
        "Upload a PDF resume to extract its text."
    )