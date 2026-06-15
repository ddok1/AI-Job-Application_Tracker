import streamlit as st
import pandas as pd

from services.application_service import (
    add_application,
    get_all_applications,
    delete_application,
    update_application
)

# Page Configuration
st.set_page_config(page_title="AI Job Tracker", layout="wide")

st.title("📊 AI Job Application Tracker")

# Add Application
st.header("➕ Add New Application")

company = st.text_input("Company")
position = st.text_input("Position")

status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
date_applied = st.text_input("Date Applied (YYYY-MM-DD)")
notes = st.text_area("Notes")

if st.button("Add Application"):
    if company and position:
        add_application(company, position, status, date_applied, notes)
        st.success("Application added!")
        st.rerun()
    else:
        st.error("Company and Position required")
st.divider()

# Dashboard
st.header("📋 Applications Dashboard")

data = get_all_applications()

if not data:
    st.info("No applications yet.")
else:
    # Table View
    df = pd.DataFrame(
        data,
        columns=["ID", "Company", "Position", "Status", "Date Applied", "Notes"]
    )

    st.dataframe(df, use_container_width=True)

    st.divider()

    # Row Action (Edit + Delete)
    st.subheader("Manage Applications")

    for app in data:

        app_id = app[0]
        company_name = app[1]
        position_name = app[2]
        status_value = app[3]
        date_value = app[4]
        notes_value = app[5]

        col1, col2, col3 = st.columns([4, 1, 1])

        # Display Info
        with col1:
            st.write(f"**{company_name}** | {position_name} | {status_value} | {date_value}")
            st.caption(notes_value)

        # Edit button
        with col2:
            if st.button("Edit", key=f"edit_{app_id}"):
                st.session_state.edit_id = app_id

        # Delete Button
        with col3:
            if st.button("Delete", key=f"delete_{app_id}"):
                delete_application(app_id)
                st.success(f"Deleted {company_name}")
                st.rerun()

# Edit Form
if "edit_id" in st.session_state:

    st.divider()
    st.subheader("✏️ Edit Application")

    edit_id = st.session_state.edit_id

    # finds record
    record = [a for a in data if a[0] == edit_id][0]

    company_edit = st.text_input(
    "Company",
    record[1],
    key=f"company_edit_{edit_id}"
    )

    position_edit = st.text_input(
    "Position",
    record[2],
    key=f"position_edit_{edit_id}"
    )

    status_edit = st.selectbox(
    "Status",
    ["Applied", "Interview", "Rejected", "Offer"],
    index=["Applied", "Interview", "Rejected", "Offer"].index(record[3]),
    key=f"status_edit_{edit_id}"
    )

    date_edit = st.text_input(
    "Date Applied",
    record[4],
    key=f"date_edit_{edit_id}"
    )

    notes_edit = st.text_area(
    "Notes",
    record[5],
    key=f"notes_edit_{edit_id}"
    )  
     
if st.button("Save Changes"):
        update_application(
            edit_id,
            company_edit,
            position_edit,
            status_edit,
            date_edit,
            notes_edit
        )

        st.success("Application updated!")

        del st.session_state.edit_id
        st.rerun()