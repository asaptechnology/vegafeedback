import streamlit as st

st.set_page_config(
    page_title="AI for Educators Feedback",
    page_icon="🤖",
    layout="centered"
)

st.title("Welcome! 👋")
st.markdown(
    """
    This application is designed to collect and analyze feedback for the **AI for Educators** seminar.

    **👈 Please select a page from the sidebar to get started:**

    - **Feedback Form:** For seminar attendees to submit their feedback.
    - **Admin Dashboard:** For the seminar organizer to view and analyze submissions.
    """
)

