import streamlit as st
import pandas as pd
import openai
from database import initialize_database, get_all_submissions

# Initialize the database and table
initialize_database()

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🔒 Admin Dashboard")

# --- Password Protection ---
# In deployment, use st.secrets. For local, you can fall back to a default.
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123")
password = st.text_input("Enter password to access the dashboard:", type="password")

if password == ADMIN_PASSWORD:
    st.success("Access Granted!")

    # --- OpenAI API Key Input ---
    st.subheader("OpenAI Configuration")
    # In deployment, use st.secrets.
    api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Enter your OpenAI API Key:", type="password", key="api_key_input", help="Your API key is not stored. It is used only for this session.")

    # --- Display Raw Data ---
    st.subheader("All Feedback Submissions")
    try:
        records = get_all_submissions()
        if records:
            # Define column names based on the database schema
            column_names = [
                "ID", "Timestamp", "Name", "Grade", "Subject", "Satisfaction", 
                "Expectations", "Duration", "Recommend", "Relevance", "Clarity",
                "Pace", "Theory Focus", "Perspectives", "Takeaway", "Challenging Ideas",
                "Unclear Points", "Suggested Changes", "Future Topics", "Comments"
            ]
            df = pd.DataFrame(records, columns=column_names)
            st.dataframe(df)
        else:
            st.info("No submissions have been recorded yet.")
            df = pd.DataFrame() # Create an empty dataframe
    except Exception as e:
        st.error(f"Failed to load data from the database: {e}")
        df = pd.DataFrame() # Create an empty dataframe on error

    # --- AI Analysis Section ---
    st.subheader("AI-Powered Feedback Summary")

    # The button is disabled if no API key is provided or no data is available
    if st.button("Generate AI Summary", disabled=(not api_key or df.empty)):
        with st.spinner("Analyzing feedback... This may take a moment."):
            try:
                # 1. Collate open-ended feedback
                open_ended_cols = [
                    "Takeaway", "Challenging Ideas", "Unclear Points", 
                    "Suggested Changes", "Future Topics", "Comments"
                ]
                
                # Filter out empty feedback to send a cleaner prompt
                all_feedback_text = []
                for index, row in df.iterrows():
                    feedback_entry = []
                    for col in open_ended_cols:
                        if pd.notna(row[col]) and row[col].strip():
                            feedback_entry.append(f"- {col}: {row[col]}")
                    if feedback_entry:
                         all_feedback_text.append(f"Feedback from {row['Name']}:\n" + "\n".join(feedback_entry))

                if not all_feedback_text:
                    st.warning("No open-ended feedback available to analyze.")
                else:
                    compiled_text = "\n\n---\n\n".join(all_feedback_text)

                    # 2. Call OpenAI API
                    client = openai.OpenAI(api_key=api_key)
                    system_prompt = """
                    You are an expert in analyzing professional development feedback. Summarize the following feedback from an 'AI for Educators' seminar. Identify 3-4 key positive themes, 3-4 key areas for improvement, and a list of specific, actionable suggestions mentioned by the attendees. Format your output using clear headings and bullet points.
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": compiled_text}
                        ]
                    )
                    
                    summary = response.choices[0].message.content
                    
                    # 3. Display summary
                    st.markdown(summary)

            except openai.AuthenticationError:
                 st.error("Authentication failed. Please check if your OpenAI API key is correct and active. You may need to configure it in the deployment secrets.")
            except Exception as e:
                st.error(f"An error occurred during AI analysis: {e}")

elif password and password != ADMIN_PASSWORD:
    st.error("Incorrect password. Please try again.")


