import streamlit as st
import pandas as pd

from database.db import init_db

from services.application_service import (
    add_application,
    get_all_applications,
    delete_application,
    update_application
)

# Initialize database
init_db()

st.title("Applications")

# Add Application
st.header("Add New Application")

company = st.text_input("Company")
position = st.text_input("Position")

status = st.selectbox(
    "Status",
    ["Applied", "Interview", "Rejected", "Offer"]
)

date_applied = st.date_input("Date Applied")
deadline = st.date_input("Application Deadline")
notes = st.text_area("Notes")

job_description = st.text_area(
    "Job Description",
    height=250
)

if st.button("Add Application"):

    if company and position:

        add_application(
            company,
            position,
            status,
            str(date_applied),
            str(deadline),
            notes,
            job_description
        )

        st.success("Application added!")
        st.rerun()

    else:
        st.error("Company and Position required")

st.divider()

# Applications Dashboard
st.header("Applications Dashboard")

# Search
search_term = st.text_input(
    "Search by company or position"
)

# Status Filter
selected_status = st.selectbox(
    "Filter by Status",
    ["All", "Applied", "Interview", "Rejected", "Offer"]
)

# Sorting
sort_by = st.selectbox(
    "Sort By",
    ["Date Applied", "Company", "Status", "Deadline"]
)

# Deadline Filter
deadline_filter = st.selectbox(
    "Deadline Filter",
    ["All", "Due Today", "Due Soon", "Overdue"]
)

# Get Applications
data = get_all_applications()

# Filter Applications
filtered_data = []

for app in data:

    company_name = app[1]
    position_name = app[2]
    status_value = app[3]
    deadline_value = app[5]

    matches_search = (
        search_term.lower() in company_name.lower()
        or search_term.lower() in position_name.lower()
    )

    matches_status = (
        selected_status == "All"
        or status_value == selected_status
    )

    days_remaining = (
        pd.to_datetime(deadline_value)
        - pd.Timestamp.today().normalize()
    ).days

    matches_deadline = (
        deadline_filter == "All"
        or (
            deadline_filter == "Due Today"
            and days_remaining == 0
        )
        or (
            deadline_filter == "Due Soon"
            and 1 <= days_remaining <= 7
        )
        or (
            deadline_filter == "Overdue"
            and days_remaining < 0
        )
    )

    if (
        matches_search
        and matches_status
        and matches_deadline
    ):
        filtered_data.append(app)

# Sort
if sort_by == "Company":

    filtered_data.sort(
        key=lambda x: x[1]
    )

elif sort_by == "Status":

    filtered_data.sort(
        key=lambda x: x[3]
    )

elif sort_by == "Deadline":

    filtered_data.sort(
        key=lambda x: x[5]
    )

else:

    filtered_data.sort(
        key=lambda x: x[4],
        reverse=True
    )

# Display Applications
if not filtered_data:

    st.info("No matching applications found.")

else:

    df = pd.DataFrame(
        filtered_data,
        columns=[
            "ID",
            "Company",
            "Position",
            "Status",
            "Date Applied",
            "Deadline",
            "Notes",
            "Job Description"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # CSV Export
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Applications as CSV",
        data=csv,
        file_name="applications.csv",
        mime="text/csv"
    )

    st.divider()

    # Manage Applications
    st.subheader("Manage Applications")

    for app in filtered_data:

        app_id = app[0]
        company_name = app[1]
        position_name = app[2]
        status_value = app[3]
        date_value = app[4]
        deadline_value = app[5]
        notes_value = app[6]

        days_remaining = (
            pd.to_datetime(deadline_value)
            - pd.Timestamp.today().normalize()
        ).days

        col1, col2, col3 = st.columns(
            [4, 1, 1]
        )

        with col1:

            st.write(
                f"**{company_name}** | "
                f"{position_name} | "
                f"{status_value}"
            )

            if days_remaining < 0:

                st.error(
                    f"Deadline passed "
                    f"({abs(days_remaining)} days ago)"
                )

            elif days_remaining <= 7:

                st.warning(
                    f"{days_remaining} days remaining"
                )

            else:

                st.success(
                    f"{days_remaining} days remaining"
                )

            st.caption(
                f"Applied: {date_value} | "
                f"Deadline: {deadline_value}"
            )

            with st.expander("Notes"):
                st.write(notes_value)

        with col2:

            if st.button(
                "Edit",
                key=f"edit_{app_id}"
            ):

                st.session_state.edit_id = app_id
                st.rerun()

        with col3:

            if st.button(
                "Delete",
                key=f"delete_{app_id}"
            ):

                delete_application(app_id)
                st.rerun()

# Edit Form
if "edit_id" in st.session_state:

    st.divider()

    st.subheader("Edit Application")

    edit_id = st.session_state.edit_id

    record = [
        a for a in data
        if a[0] == edit_id
    ][0]

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

    status_options = [
        "Applied",
        "Interview",
        "Rejected",
        "Offer"
    ]

    status_edit = st.selectbox(
        "Status",
        status_options,
        index=status_options.index(record[3]),
        key=f"status_edit_{edit_id}"
    )

    date_edit = st.date_input(
        "Date Applied",
        value=pd.to_datetime(record[4]),
        key=f"date_edit_{edit_id}"
    )

    deadline_edit = st.date_input(
        "Application Deadline",
        value=pd.to_datetime(record[5]),
        key=f"deadline_edit_{edit_id}"
    )

    notes_edit = st.text_area(
        "Notes",
        record[6],
        key=f"notes_edit_{edit_id}"
    )

    job_description_edit = st.text_area(
    "Job Description",
    record[7],
    height=300,
    key=f"job_description_edit_{edit_id}"
)

    if st.button(
        "Save Changes",
        key=f"save_{edit_id}"
    ):

        update_application(
            edit_id,
            company_edit,
            position_edit,
            status_edit,
            str(date_edit),
            str(deadline_edit),
            notes_edit,
            job_description_edit
        )

        st.success("Application updated!")

        del st.session_state.edit_id

        st.rerun()