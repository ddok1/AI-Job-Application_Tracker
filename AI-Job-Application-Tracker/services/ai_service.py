import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_ai_response(prompt):
    """
    Sends a prompt to OpenAI and returns the AI response.
    """

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI request failed: {e}"
    
def analyze_job_description(job_description):
    prompt = f"""
    Analyze the following software engineering job description.

    Provide:
    1. Required technical skills
    2. Preferred technical skills
    3. Programming languages and technologies
    4. Key responsibilities
    5. Experience requirements
    6. Important keywords
    7. Three recommendations for a student applying to this position

    Job Description:
    {job_description}
    """

    return generate_ai_response(prompt)

def analyze_resume_match(resume_text, job_description):
    prompt = f"""
    Compare the following resume against the job description.

    Provide the following:

    1. Overall match score from 0-100
    2. Technical skills that match
    3. Technical skills that are missing or weak
    4. Relevant experience from the resume
    5. Education relevance
    6. Important job requirements the candidate does not currently demonstrate
    7. Three specific recommendations for improving the candidate's chances

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    return generate_ai_response(prompt)