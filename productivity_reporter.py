import streamlit as st
import google.generativeai as genai

def generate_productivity_report(description: str) -> str:
    """Call Gemini API to generate productivity report."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    You are a construction project manager AI assistant. Based on the following progress description, 
    generate a formal and structured productivity report. The report should be well-formatted 
    using Markdown and include these sections:
    1. **Overall Summary:** A brief overview of the project status.
    2. **Key Accomplishments:** A bulleted list of completed tasks and milestones.
    3. **Identified Challenges/Blockers:** A bulleted list of any issues hindering progress.
    4. **Plan for Next Period:** A bulleted list of upcoming tasks and goals.

    Here is the progress description:
    ---
    {description}
    ---
    """
    response = model.generate_content(prompt)
    return response.text

def app():
    st.title("Productivity Reporter")
    st.write("Generate a structured productivity report for your construction project using Gemini AI.")

    # Get API key from session state (set on Dashboard or initial input)
    google_api_key = st.session_state.get("google_api_key", "")
    if not google_api_key:
        google_api_key = st.text_input("Enter your Google API key", type="password")
        if google_api_key:
            st.session_state["google_api_key"] = google_api_key
        else:
            st.warning("Please enter your Google API key to continue.")
            return

    # Configure Google Generative AI
    try:
        genai.configure(api_key=google_api_key)
    except Exception as e:
        st.error(f"API Key configuration error: {e}")
        return

    st.success("✅ API key loaded. Gemini AI is ready.")

    description = st.text_area(
        "Project Progress Description",
        placeholder="e.g., Completed foundation pouring for Block A. Started steel framing for Block B..."
    )

    if st.button("Generate Report"):
        if not description.strip():
            st.warning("Please enter a progress description.")
            return
        with st.spinner("Generating productivity report..."):
            try:
                report = generate_productivity_report(description)
                st.markdown(report)
            except Exception as e:
                st.error(f"Failed to generate report: {e}")

if __name__ == "__main__":
    app()
