import streamlit as st

from database.db import init_db

init_db()

st.set_page_config(
    page_title="AI Job Application Tracker",
    layout="wide"
)

st.title("AI Job Application Tracker")

st.write(
    "Welcome to your AI-powered job application assistant."
)

st.info(
    "Select a page from the sidebar to get started."
)