import streamlit as st
import google.generativeai as genai
from datetime import datetime

def app():
    st.title("Productivity Reporter")
    st.write("Generate a structured construction project productivity report using AI.")

    # Get API key from session state
    google_api_key = st.session_state.get("google_api_key", "")
    if not google_api_key:
        st.warning("⚠️ Please enter your Google API key on the Dashboard first.")
        return

    # Configure Google Generative AI
    try:
        genai.configure(api_key=google_api_key)
    except Exception as e:
        st.error(f"API Key Error: {e}")
        return

    st.success("✅ API key loaded. Gemini AI is ready.")

    project_name = st.text_input("Project Name", "Mixed-Use Development Phase 1")
    reporting_period_start = st.date_input("Reporting Period Start")
    reporting_period_end = st.date_input("Reporting Period End")
    description = st.text_area(
        "Enter progress description",
        placeholder="E.g., Completed foundation pouring for Block A. Started steel framing for Block B..."
    )

    if st.button("Generate Productivity Report"):
        if not description:
            st.warning("Please enter a progress description to generate the report.")
            return
        if reporting_period_start > reporting_period_end:
            st.warning("Reporting period start date must be before end date.")
            return

        # Format dates as strings
        start_date_str = reporting_period_start.strftime("%B %d, %Y")
        end_date_str = reporting_period_end.strftime("%B %d, %Y")
        today_str = datetime.today().strftime("%B %d, %Y")

        prompt = f"""
        You are a construction project manager AI assistant. Based on the following progress description, generate a formal productivity report with the following sections:

        Construction Project Productivity Report  
        Date: {today_str}  
        Project: {project_name}  
        Reporting Period: {start_date_str} - {end_date_str}

        1. Overall Summary  
        Provide a brief overview of the project status.

        2. Key Accomplishments  
        Provide a bulleted list of completed tasks and milestones.

        3. Identified Challenges/Blockers  
        Provide a bulleted list of any issues hindering progress.

        4. Plan for Next Period  
        Provide a bulleted list of upcoming tasks and goals.

        Here is the progress description:  
        ---  
        {description}  
        ---
        """

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")  # Use your correct model
            response = model.generate_content(prompt)
            st.subheader("🏗️ Generated Productivity Report")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")
