import streamlit as st
import google.generativeai as genai
from datetime import datetime

def set_google_api_key():
    # Using 'password' type to mask the API key input
    google_api_key = st.text_input("Enter Google API Key", type='password')
    if st.button("Save API Key"):
        if google_api_key:
            st.session_state["google_api_key"] = google_api_key
            st.success("✅ Google API Key saved successfully.")
            # Set a flag to show that the API key has been saved
            st.session_state["api_key_saved"] = True
        else:
            st.error("⚠️ Please enter a valid API key.")

def app():
    st.title("Productivity Reporter")
    st.write("Generate a structured construction project productivity report using AI.")
    
    google_api_key = st.session_state.get("google_api_key", "")
    
    # If no API key exists, show the input field and wait for the key to be entered
    if not google_api_key:
        set_google_api_key()  # Ask user to input API key
        return  # Stop further processing until API key is saved

    # Check if the API key is saved and proceed with the app
    if st.session_state.get("api_key_saved", False):
        try:
            genai.configure(api_key=google_api_key)
            st.success("✅ API key loaded. Gemini AI is ready.")
        except Exception as e:
            st.error(f"API Key Error: {e}")
            return

        # Project Name input (same as your previous `text_input` setup)
        project_name = st.text_input("Enter Project Name", placeholder="Enter project name here...")

        # If project name is empty, ask the user to input one
        if not project_name:
            st.warning("⚠️ Please enter a project name.")

        reporting_period = st.text_input("Reporting Period", "Week of August 7 - August 13, 2025")
        description = st.text_area(
            "Enter progress description",
            placeholder="E.g., Completed foundation pouring for Block A. Started steel framing for Block B..."
        )

        if st.button("Generate Productivity Report"):
            if not description:
                st.warning("⚠️ Please enter a progress description to generate the report.")
                return

            # Proceed with generating the report as usual
            today_str = datetime.today().strftime("%B %d, %Y")
            prompt = f"""
            Project Productivity Report  
            Date: {today_str}  
            Project: {project_name}  
            Reporting Period: {reporting_period}
            
            1. Overall Summary
            The project continues to demonstrate good progress...
            2. Key Accomplishments
            Completed foundation pouring for Block A. Steel framing for Block B.
            3. Challenges/Blockers
            No major blockers identified during this period.
            4. Plan for Next Period
            Continue with the vertical construction for Block A and proceed with the steel framing for Block B.
            """
            
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                st.subheader("🏗️ Generated Productivity Report")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

if __name__ == "__main__":
    app()
