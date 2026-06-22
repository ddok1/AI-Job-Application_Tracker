import streamlit as st
import pandas as pd
import plotly.express as px

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
date_applied = st.date_input("Date Applied")
notes = st.text_area("Notes")

if st.button("Add Application"):
    if company and position:
        add_application(company, position, status, str(date_applied), notes)
        st.success("Application added!")
        st.rerun()
    else:
        st.error("Company and Position required")
st.divider()

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
    ["Date Applied", "Company", "Status"]
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

# Analytic Cards
st.subheader("📈 Analytics")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

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
company_df = pd.DataFrame(
    data,
    columns=[
        "ID",
        "Company",
        "Position",
        "Status",
        "Date Applied",
        "Notes"
    ]
)

company_counts = (
    company_df["Company"]
    .value_counts()
    .reset_index()
)

company_counts.columns = [
    "Company",
    "Applications"
]

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

company_df["Date Applied"] = pd.to_datetime(
    company_df["Date Applied"]
)

company_df["Month"] = (
    company_df["Date Applied"]
    .dt.strftime("%Y-%m")
)

monthly_counts = (
    company_df.groupby("Month")
    .size()
    .reset_index(name="Applications")
)

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

    matches_search = (
        search_term.lower() in company_name.lower()
        or search_term.lower() in position_name.lower()
    )
    matches_status = (
        selected_status == "All"
        or status_value == selected_status
    )
    if matches_search and matches_status:
        filtered_data.append(app)

# Sort Applications
if sort_by == "Company":
    filtered_data.sort(key=lambda x: x[1])
elif sort_by == "Status":
    filtered_data.sort(key=lambda x: x[3])
else:
    filtered_data.sort(key=lambda x: x[4], reverse=True)
    
# Display table
if not filtered_data:
    st.info("No matching applications found.")
else:
    # Table View
    df = pd.DataFrame(
        filtered_data,
        columns=["ID", "Company", "Position", "Status", "Date Applied", "Notes"]
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
        notes_value = app[5]

        col1, col2, col3 = st.columns([4, 1, 1])

        # Display Info
        with col1:
            st.write(f"**{company_name}** | {position_name} | {status_value} | {date_value}")
            with st.expander("Notes"):
                st.write(notes_value)

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

    date_edit = st.date_input(
    "Date Applied",
    value=pd.to_datetime(record[4]),
    key=f"date_edit_{edit_id}"
    )

    notes_edit = st.text_area(
    "Notes",
    record[5],
    key=f"notes_edit_{edit_id}"
    )  
     
    if st.button("Save Changes",
                 key=f"save_{edit_id}"):
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