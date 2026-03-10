import streamlit as st
import requests
import pandas as pd



import streamlit as st
import requests
import pandas as pd

# Custom CSS for sidebar hover effects
st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

/* Default menu style */
section[data-testid="stSidebar"] label {
    color: #E2E8F0 !important;
    padding: 10px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

/* Hover effect */
section[data-testid="stSidebar"] label:hover {
    background: linear-gradient(90deg, #6366F1, #3B82F6);
    color: white !important;
    transform: translateX(5px);
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

/* Selected menu item */
section[data-testid="stSidebar"] input:checked + div {
    background: linear-gradient(90deg, #4F46E5, #2563EB);
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)



API = "http://127.0.0.1:8000"

st.title("🏠 Gharpayy CRM System")

st.sidebar.title("CRM Menu")

menu = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "View Leads",
        "Create Lead",
        "Update Lead Pipeline",
        "Schedule Visit",
        "Update Visit Outcome",
        "Follow-up Reminders",
        "Lead Activity Timeline",
        "Agent Leaderboard"
    ]
)
# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.header("CRM Dashboard")

    total_leads = requests.get(f"{API}/total-leads").json()
    visits = requests.get(f"{API}/total-visits").json()
    bookings = requests.get(f"{API}/bookings").json()
    pipeline = requests.get(f"{API}/pipeline-stats").json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leads", total_leads["total_leads"])
    col2.metric("Visits Scheduled", visits["visits"])
    col3.metric("Bookings Confirmed", bookings["bookings"])

    st.subheader("Leads by Pipeline Stage")

    df = pd.DataFrame(list(pipeline.items()), columns=["Stage", "Count"])

    st.dataframe(df)

    st.bar_chart(df.set_index("Stage"))

# ---------------- VIEW LEADS ----------------

elif menu == "View Leads":

    st.header("All Leads")

    data = requests.get(f"{API}/leads").json()

    df = pd.DataFrame(data)

    st.dataframe(df)
# ---------------- CREATE LEAD ----------------

elif menu == "Create Lead":

    st.header("Create Lead")

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    source = st.selectbox(
        "Lead Source",
        ["Website", "Google Form", "WhatsApp"]
    )

    if st.button("Create Lead"):

        requests.post(
            f"{API}/create-lead",
            json={
                "name": name,
                "phone": phone,
                "email": email,
                "source": source
            }
        )

        st.success("Lead Created Successfully")

# ---------------- UPDATE PIPELINE ----------------

elif menu == "Update Lead Pipeline":

    st.header("Update Lead Pipeline")

    lead_id_pipeline = st.number_input("Lead ID", key="pipeline")

    status = st.selectbox(
        "Move Lead To Stage",
        [
            "New Lead",
            "Contacted",
            "Requirement Collected",
            "Property Suggested",
            "Visit Scheduled",
            "Visit Completed",
            "Booked",
            "Lost"
        ]
    )

    if st.button("Update Status"):

        requests.put(
            f"{API}/update-status/{lead_id_pipeline}",
            params={"status": status}
        )

        st.success("Lead Pipeline Updated")

# ---------------- SCHEDULE VISIT ----------------

elif menu == "Schedule Visit":

    st.header("Schedule Property Visit")

    lead_id_visit = st.number_input("Lead ID", key="visit")

    property_name = st.selectbox(
        "Select Property",
        [
            "Gharpayy PG Whitefield",
            "Gharpayy PG Marathahalli",
            "Gharpayy PG Electronic City"
        ]
    )

    visit_date = st.date_input("Visit Date")

    visit_time = st.time_input("Visit Time")

    if st.button("Schedule Visit"):

        requests.post(
            f"{API}/schedule-visit",
            json={
                "lead_id": lead_id_visit,
                "property_name": property_name,
                "visit_date": str(visit_date),
                "visit_time": str(visit_time)
            }
        )

        st.success("Visit Scheduled Successfully")

# ---------------- UPDATE VISIT OUTCOME ----------------

elif menu == "Update Visit Outcome":

    st.header("Update Visit Outcome")

    lead_id = st.number_input("Lead ID", key="visit_outcome")
   

    outcome = st.selectbox(
        "Visit Outcome",
        [
            "Interested",
            "Needs More Options",
            "Not Interested",
            "Booked"
        ]
    )

    if st.button("Update Outcome"):

        requests.put(
    f"{API}/update-visit-outcome",
    params={
        "lead_id": lead_id,
        "outcome": outcome
    }
)

        st.success("Visit Outcome Updated")

# ---------------- FOLLOW-UP REMINDERS ----------------

elif menu == "Follow-up Reminders":

    st.header("Leads Requiring Follow-up")

    response = requests.get(f"{API}/followups")

    data = response.json()

    if len(data) == 0:

        st.success("No pending follow-ups")

    else:

        df = pd.DataFrame(data)

        st.warning("These leads require follow-up today")

        st.dataframe(df)
        



elif menu == "Lead Activity Timeline":

    st.header("📜 Lead Activity Timeline")

    lead_id = st.number_input("Enter Lead ID", key="timeline")

    if st.button("Load Timeline"):

        data = requests.get(f"{API}/lead-activity/{lead_id}").json()

        if len(data) == 0:
            st.warning("No activity found for this lead")

        else:
            for activity in data:

                st.markdown(f"""
                <div style="
                border-left:4px solid #6366F1;
                padding:10px;
                margin-bottom:10px;
                background:#f8fafc;
                border-radius:8px">

                <b>{activity['activity']}</b><br>
                <small style="color:gray">{activity['created_at']}</small>

                </div>
                """, unsafe_allow_html=True)
        
        
        
        
        
elif menu == "Agent Leaderboard":

    st.header("🏆 Agent Performance Leaderboard")

    # Call API
    response = requests.get(f"{API}/agent-leaderboard")

    # Check response
    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No agent data available")
        else:

            # Leaderboard table
            st.subheader("Leaderboard Table")
            st.dataframe(df)

            # Chart
            st.subheader("Bookings Performance")
            chart = df.set_index("Agent")
            st.bar_chart(chart["Bookings"])

            # Rank cards
            st.subheader("Top Performers")

            cols = st.columns(len(df))

            for i, row in df.iterrows():

                cols[i].metric(
                    label=row["Agent"],
                    value=f"{row['Bookings']} Bookings",
                    delta=f"{row['Leads Handled']} Leads"
                )

    else:
        st.error("Error fetching leaderboard data from backend")