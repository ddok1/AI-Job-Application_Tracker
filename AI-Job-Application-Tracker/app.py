import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import init_db

from services.application_service import (
    add_application,
    get_all_applications,
    delete_application,
    update_application
)

# Initialize database
init_db()

# Page Configuration
st.set_page_config(page_title="AI Job Tracker", layout="wide")

st.title("📊 AI Job Application Tracker")

# Add Application
st.header("➕ Add New Application")

company = st.text_input("Company")
position = st.text_input("Position")

status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
date_applied = st.date_input("Date Applied")
deadline = st.date_input("Application Deadline")
notes = st.text_area("Notes")

if st.button("Add Application"):
    if company and position:
        add_application(
            company,
            position,
            status,
            str(date_applied),
            str(deadline),
            notes
        )
        st.success("Application added!")
        st.rerun()
    else:
        st.error("Company and Position required")
st.divider()

# AI Job Description Analyzer
st.divider()

st.header("AI Job Description Analyzer")

job_description = st.text_area(
    "Paste a job description",
    height=250,
    key="job_description"
)

if st.button("Analyze Job Description"):
    if job_description.strip():
        with st.spinner("Analyzing job description..."):
            from services.ai_service import analyze_job_description

            analysis = analyze_job_description(job_description)

        st.subheader("AI Analysis")
        st.write(analysis)
    else:
        st.warning("Please paste a job description first.")

# Dashboard
st.header("📋 Applications Dashboard")

# Search Bar
search_term = st.text_input("🔍 Search by company or position")

# Status Filter
selected_status = st.selectbox(
    "Filter by Status",
    ["All", "Applied", "Interview", "Rejected", "Offer"]
)

# Sorting (Status Filter)
sort_by = st.selectbox(
    "Sort By",
    ["Date Applied", "Company", "Status", "Deadline"]
)

# Deadline Filter
deadline_filter = st.selectbox(
    "Deadline Filter",
    ["All", "Due Today", "Due Soon", "Overdue"]
)

# Retrieves Data
data = get_all_applications()

# Analytics
total_count = len(data)
applied_count = sum(1 for app in data if app[3] == "Applied")
interview_count = sum(1 for app in data if app[3] == "Interview")
rejected_count = sum(1 for app in data if app[3] == "Rejected")
offer_count = sum(1 for app in data if app[3] == "Offer")

# Rates
interview_rate = 0
offer_rate = 0

if total_count > 0:
    interview_rate = round(interview_count / total_count * 100, 1)
    offer_rate = round(offer_count / total_count * 100, 1)

# Deadline Analytics
overdue_count = 0
due_today_count = 0
due_soon_count = 0
upcoming_count = 0

for app in data:
    deadline_value = app[5]

    days_remaining = (
        pd.to_datetime(deadline_value)
        - pd.Timestamp.today().normalize()
    ).days

    if days_remaining < 0:
        overdue_count += 1
    elif days_remaining == 0:
        due_today_count += 1
    elif days_remaining <= 7:
        due_soon_count += 1
    else:
        upcoming_count += 1

# Analytic Cards
st.subheader("📈 Analytics")

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

with col1:
    st.metric("Total", total_count)
with col2:
    st.metric("Applied", applied_count)
with col3:
    st.metric("Interview", interview_count)
with col4:
    st.metric("Rejected", rejected_count)
with col5:
    st.metric("Offer", offer_count)
with col6:
    st.metric("Interview %", f"{interview_rate}%")
with col7:
    st.metric("Offer %", f"{offer_rate}%")
with col8:
    st.metric("Overdue", overdue_count)
with col9:
    st.metric("Due Today", due_today_count)
with col10:
    st.metric("Due Soon", due_soon_count)
st.divider()

status_counts = {
    "Applied": applied_count,
    "Interview": interview_count,
    "Rejected": rejected_count,
    "Offer": offer_count
}

# Charts
chart_df = pd.DataFrame(
    status_counts.items(),
    columns=["Status", "Count"]
)

# Distribution of Application Statuses
fig = px.pie(
    chart_df,
    values="Count",
    names="Status",
    title="Applications by Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Data Frame from all applications
company_df = pd.DataFrame(
    data,
    columns=[
        "ID",
        "Company",
        "Position",
        "Status",
        "Date Applied",
        "Deadline",
        "Notes"
    ]
)

# Number of applications sent to each company
company_counts = (
    company_df["Company"]
    .value_counts()
    .reset_index()
)

company_counts.columns = [
    "Company",
    "Applications"
]
# Bar Chart
company_fig = px.bar(
    company_counts,
    x="Company",
    y="Applications",
    title="Top Companies Applied To"
)

st.plotly_chart(
    company_fig,
    use_container_width=True
)

# Convert date strings into dateime objects
company_df["Date Applied"] = pd.to_datetime(
    company_df["Date Applied"]
)

# Extract month and year from each application date
company_df["Month"] = (
    company_df["Date Applied"]
    .dt.strftime("%Y-%m")
)

# Counts applications sumbitted each month
monthly_counts = (
    company_df.groupby("Month")
    .size()
    .reset_index(name="Applications")
)

# Line Chart showing application activity
trend_fig = px.line(
    monthly_counts,
    x="Month",
    y="Applications",
    title="Monthly Application Trend"
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)

# Bar chart displaying number of application per status
bar_fig = px.bar(
    chart_df,
    x="Status",
    y="Count",
    title="Application Status Distribution"
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

st.divider()

# Search and Filters
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
    # Calculate Deadline Status
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
    
    if matches_search and matches_status and matches_deadline:
        filtered_data.append(app)

# Sort Applications
if sort_by == "Company":
    filtered_data.sort(key=lambda x: x[1])
elif sort_by == "Status":
    filtered_data.sort(key=lambda x: x[3])
elif sort_by == "Deadline":
    filtered_data.sort(key=lambda x: x[5])
else:
    filtered_data.sort(key=lambda x: x[4], reverse=True)
    
# Display table
if not filtered_data:
    st.info("No matching applications found.")
else:
    # Table View
    df = pd.DataFrame(
    filtered_data,
    columns=[
        "ID",
        "Company",
        "Position",
        "Status",
        "Date Applied",
        "Deadline",
        "Notes"
    ]
)

    st.dataframe(df, use_container_width=True)
    
    # Export applications to CSV
    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Applications as CSV",
        data=csv,
        file_name="applications.csv",
        mime="text/csv"
    )

    st.divider()

    # Row Action (Edit + Delete)
    st.subheader("Manage Applications")

    for app in filtered_data:

        app_id = app[0]
        company_name = app[1]
        position_name = app[2]
        status_value = app[3]
        date_value = app[4]
        deadline_value = app[5]
        notes_value = app[6]

        # Calculate days until deadline
        days_remaining = (
            pd.to_datetime(deadline_value)
            - pd.Timestamp.today().normalize()
        ).days

        col1, col2, col3 = st.columns([4, 1, 1])

        # Display Info
        with col1:
            st.write(
                f"**{company_name}** | "
                f"{position_name} | "
                f"{status_value}"
            )

            if days_remaining < 0:
                st.error(
                    f"Deadline passed ({abs(days_remaining)} days ago)"
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
                f"Applied: {date_value} | Deadline: {deadline_value}"
            )

            with st.expander("Notes"):
                st.write(notes_value)

        # Edit button
        with col2:
            if st.button("Edit", key=f"edit_{app_id}"):
                st.session_state.edit_id = app_id

        # Delete button
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

    # Find record
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
            notes_edit
        )

        st.success("Application updated!")

        del st.session_state.edit_id
        st.rerun()