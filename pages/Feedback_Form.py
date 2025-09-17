import streamlit as st
from database import initialize_database, insert_submission

# Initialize the database and table
initialize_database()

st.set_page_config(page_title="Feedback Form", layout="centered")

st.title("Feedback Form: AI for Educators")
st.markdown("We value your feedback! Please take a moment to fill out this form.")

with st.form("feedback_form", clear_on_submit=True):
    # --- Part 1: Your Information ---
    st.subheader("Part 1: Your Information")
    q1_name = st.text_input("Name", key="q1")
    q2_grade = st.text_input("Grade Level(s) you teach", key="q2")
    q3_subject = st.text_input("Subject(s) you teach", key="q3")

    # --- Part 2: Overall Impressions ---
    st.subheader("Part 2: Overall Impressions")
    likert_options = list(range(1, 6))
    q4_satisfaction = st.radio("Overall, I was satisfied with this seminar.", likert_options, horizontal=True, key="q4")
    q5_expectations = st.radio("The seminar met my expectations based on its description.", likert_options, horizontal=True, key="q5")
    q6_duration = st.radio("The 1-hour time frame was an effective length for this session.", likert_options, horizontal=True, key="q6")
    q7_recommend = st.radio("I would recommend this seminar to other educators.", likert_options, horizontal=True, key="q7")
    st.caption("Scale: 1 = Strongly Disagree, 5 = Strongly Agree")

    # --- Part 3: Content and Delivery ---
    st.subheader("Part 3: Content and Delivery")
    q8_relevance = st.radio("The content presented was relevant to my work as an educator.", likert_options, horizontal=True, key="q8")
    q9_clarity = st.radio("The speaker presented the information in a clear and understandable way.", likert_options, horizontal=True, key="q9")
    q10_pace = st.radio("The pace of the seminar was just right.", likert_options, horizontal=True, key="q10")
    q11_theory_focus = st.radio("The session's focus on theory and concepts, without a live demo, was a valuable use of time.", likert_options, horizontal=True, key="q11")
    q12_perspectives = st.radio("The seminar presented ideas that challenged my current thinking about AI in education.", likert_options, horizontal=True, key="q12")
    st.caption("Scale: 1 = Strongly Disagree, 5 = Strongly Agree")
    
    q13_takeaway = st.text_area("What was your biggest takeaway from the seminar?", key="q13")
    q14_ideas = st.text_area("Which of the challenging ideas presented stood out to you most, and why?", key="q14")
    q15_unclear = st.text_area("Was any part of the seminar unclear, confusing, or something you disagreed with? Please briefly explain.", key="q15")

    # --- Part 4: Suggestions for the Future ---
    st.subheader("Part 4: Suggestions for the Future")
    q16_changes = st.text_area("Besides adding a live demo, what one thing would you change about this seminar?", key="q16")
    q17_topics = st.text_area("What other AI topics for educators would you be interested in learning about in the future?", key="q17")
    q18_comments = st.text_area("Any other comments or feedback?", key="q18")

    # --- Submission Button ---
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        # Validation
        if not q1_name:
            st.warning("Name is a required field.")
        else:
            # Collate data into a tuple in the correct order for the database
            data = (
                q1_name, q2_grade, q3_subject, q4_satisfaction, q5_expectations,
                q6_duration, q7_recommend, q8_relevance, q9_clarity, q10_pace,
                q11_theory_focus, q12_perspectives, q13_takeaway, q14_ideas,
                q15_unclear, q16_changes, q17_topics, q18_comments
            )
            # Insert data into the database
            insert_submission(data)
            st.success("Thank you for your feedback! Your submission has been recorded.")
