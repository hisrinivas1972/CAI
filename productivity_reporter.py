import streamlit as st
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Configure the Google Gemini API key
api_key = os.getenv("API_KEY")
if not api_key:
    st.warning("⚠️ Google API key not set. Please set it in your .env file or Streamlit secrets.")

genai.configure(api_key=api_key)

# Function to generate productivity report
def generate_productivity_report(description: str):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        Project Productivity Report  
        Date: {datetime.today().strftime('%B %d, %Y')}  
        Description: {description}

        Please generate a detailed productivity report in markdown format based on the above project description. Include:
        1. **Overall Summary**
        2. **Key Accomplishments**
        3. **Challenges/Blockers**
        4. **Plan for Next Period**
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate report: {e}")
        return None

# Streamlit App Layout
st.title("Productivity Reporter")
st.write("Generate a structured construction project productivity report using AI.")

# User input for project details
project_name = st.text_input("Project Name", "Mixed-Use Development Phase 1")
reporting_period = st.text_input("Reporting Period", "Week of August 7 - August 13, 2025")
description = st.text_area("Project Progress Description", placeholder="E.g., Completed foundation pouring for Block A. Started steel framing for Block B...")

if st.button("Generate Productivity Report"):
    if not description:
        st.warning("⚠️ Please enter a project progress description.")
    else:
        with st.spinner('Generating report...'):
            report = generate_productivity_report(description)
            if report:
                st.subheader("🏗️ Generated Productivity Report")
                st.markdown(report)
