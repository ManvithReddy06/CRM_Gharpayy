import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("Lead Capture Form")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

source = st.selectbox(
    "Lead Source",
    ["Website Form", "Google Form", "Visit Booking"]
)

if st.button("Submit"):

    requests.post(
        f"{API}/capture-lead",
        params={
            "name": name,
            "phone": phone,
            "source": source
        }
    )

    st.success("Lead Captured Successfully!")