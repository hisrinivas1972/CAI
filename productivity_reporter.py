import streamlit as st
import google.generativeai as genai
from datetime import datetime

def app():
    st.title("Productivity Reporter")
    st.write("Generate a structured construction project productivity report using AI.")

    google_api_key = st.session_state.get("google_api_key", "")
    if not google_api_key:
        st.warning("⚠️ Please enter your Google API key on the Dashboard first.")
        return

    try:
        genai.configure(api_key=google_api_key)
    except Exception as e:
        st.error(f"API Key Error: {e}")
        return

    st.success("✅ API key loaded. Gemini AI is ready.")

    project_name = st.text_input("Project Name", "Mixed-Use Development Phase 1")
    reporting_period = st.text_input("Reporting Period", "Week of August 7 - August 13, 2025")
    description = st.text_area(
        "Enter progress description",
        placeholder="E.g., Completed foundation pouring for Block A. Started steel framing for Block B..."
    )

    if st.button("Generate Productivity Report"):
        if not description:
            st.warning("Please enter a progress description to generate the report.")
            return

        today_str = datetime.today().strftime("%B %d, %Y")

        prompt = f"""
Project Productivity Report  
Date: {today_str}  
Project: {project_name}  
Reporting Period: {reporting_period}

1. Overall Summary  
The project continues to demonstrate good progress, with significant structural milestones achieved across multiple blocks. The foundation work for Block A has been successfully completed, and critical steel framing operations have commenced on Block B, indicating advancement into subsequent construction phases.

2. Key Accomplishments  
Completed Foundation Pouring for Block A: The entire foundation system for Block A has been successfully poured, cured, and is now ready for subsequent structural work. This marks a major milestone for Block A.  
Initiated Steel Framing for Block B: Steel erection activities for Block B have commenced as scheduled. The initial structural members are being set, laying the groundwork for the vertical construction of this block.

3. Identified Challenges/Blockers  
No significant challenges or blockers were explicitly reported during this reporting period that are impeding critical path progress. Material deliveries and labor availability remain consistent with current demands.

4. Plan for Next Period  
Continue Steel Framing for Block B: Focus on the efficient erection of steel columns, beams, and bracing for Block B, aiming to complete [specify a floor/section if known, otherwise keep general, e.g., the first two levels].  
Initiate Vertical Construction for Block A: Begin preparations and, where applicable, commence vertical construction activities for Block A, following the successful completion of the foundation. This may include formwork, rebar installation, or initial concrete pours for walls/columns.  
Coordinate Material Deliveries: Ensure timely delivery and staging of steel members for Block B and concrete/formwork materials for Block A.  
Safety Adherence: Maintain vigilant oversight on all construction activities, particularly during steel erection and concrete pouring, to ensure strict adherence to safety protocols.

Here is the progress description:  
---  
{description}  
---
"""

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            st.subheader("🏗️ Generated Productivity Report")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")
