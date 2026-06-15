import streamlit as st
import pandas as pd
from services.application_service import add_application, get_all_applications

st.title("📊 AI Job Application Tracker")

# Add Application
st.header("Add New Application")

company = st.text_input("Company")
position = st.text_input("Position")

status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
date_applied = st.text_input("Date Applied (YYYY-MM-DD)")
notes = st.text_area("Notes")

if st.button("Add Application"):
    if company and position:
        add_application(company, position, status, date_applied, notes)
        st.success("Application added!")
    else:
        st.error("Company and Position required")

# View Application
st.header("Applications Dashboard")

data = get_all_applications()

# Convert to clean table
df = pd.DataFrame(
    data,
    columns=["ID", "Company", "Position", "Status", "Date Applied", "Notes"]
)

st.dataframe(df)