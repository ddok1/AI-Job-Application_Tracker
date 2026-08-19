import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import init_db
from services.application_service import get_all_applications

# Initialize database
init_db()

st.title("Dashboard")

# Get Applications
data = get_all_applications()

# Analytics
total_count = len(data)

applied_count = sum(
    1 for app in data
    if app[3] == "Applied"
)

interview_count = sum(
    1 for app in data
    if app[3] == "Interview"
)

rejected_count = sum(
    1 for app in data
    if app[3] == "Rejected"
)

offer_count = sum(
    1 for app in data
    if app[3] == "Offer"
)

# Rates
interview_rate = 0
offer_rate = 0

if total_count > 0:

    interview_rate = round(
        interview_count / total_count * 100,
        1
    )

    offer_rate = round(
        offer_count / total_count * 100,
        1
    )

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

# Analytics Section
st.subheader("Analytics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total", total_count)

with col2:
    st.metric("Applied", applied_count)

with col3:
    st.metric("Interviews", interview_count)

with col4:
    st.metric("Rejected", rejected_count)

with col5:
    st.metric("Offers", offer_count)

col6, col7, col8, col9, col10 = st.columns(5)

with col6:
    st.metric(
        "Interview Rate",
        f"{interview_rate}%"
    )

with col7:
    st.metric(
        "Offer Rate",
        f"{offer_rate}%"
    )

with col8:
    st.metric(
        "Overdue",
        overdue_count
    )

with col9:
    st.metric(
        "Due Today",
        due_today_count
    )

with col10:
    st.metric(
        "Due Soon",
        due_soon_count
    )

st.divider()

# Status Data
status_counts = {
    "Applied": applied_count,
    "Interview": interview_count,
    "Rejected": rejected_count,
    "Offer": offer_count
}

chart_df = pd.DataFrame(
    status_counts.items(),
    columns=["Status", "Count"]
)

# Status Pie Chart
st.subheader("Application Status")

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

# Stop here if there are no applications
if not data:

    st.info(
        "Add applications to see additional analytics."
    )

    st.stop()

# Application DataFrame
company_df = pd.DataFrame(
    data,
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

# Applications by Company
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
    title="Applications by Company"
)

st.plotly_chart(
    company_fig,
    use_container_width=True
)

# Convert Date Applied
company_df["Date Applied"] = pd.to_datetime(
    company_df["Date Applied"]
)

# Extract Month
company_df["Month"] = (
    company_df["Date Applied"]
    .dt.strftime("%Y-%m")
)

# Monthly Applications
monthly_counts = (
    company_df
    .groupby("Month")
    .size()
    .reset_index(
        name="Applications"
    )
)

trend_fig = px.line(
    monthly_counts,
    x="Month",
    y="Applications",
    title="Monthly Application Trend",
    markers=True
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)

# Status Bar Chart
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