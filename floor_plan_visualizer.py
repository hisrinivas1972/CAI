import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Floor Plan Visualizer", layout="wide")

def save_api_key():
    key = st.text_input("Enter your Google API Key", type="password")
    if st.button("Save API Key"):
        if key.strip():
            st.session_state["google_api_key"] = key.strip()
            st.success("✅ Google API Key saved")
            st.session_state["api_key_saved"] = True
        else:
            st.error("⚠️ Please enter a valid API key")

def generate_svg_floor_plan(description):
    prompt = f"""
    Generate a simple SVG code for a floor plan based on the following description.
    The SVG should be 600x400 pixels, showing walls as black lines, doors as arcs, windows as blue rectangles.
    Description: {description}

    Only output valid SVG code starting with <svg> and ending with </svg>.
    """
    genai.configure(api_key=st.session_state["google_api_key"])
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)
    return response.text

def app():
    st.title("Floor Plan Visualizer")

    # Check for saved API key
    if "google_api_key" not in st.session_state:
        save_api_key()
        return

    description = st.text_area(
        "Describe your floor plan (e.g. room sizes, doors, windows):",
        height=200,
        placeholder="e.g., 'A 20ft by 30ft rectangular workshop with a large garage door on the north wall...'"
    )

    if st.button("Generate Floor Plan SVG"):
        if not description.strip():
            st.warning("Please enter a floor plan description")
            return

        with st.spinner("Generating SVG floor plan..."):
            try:
                svg_code = generate_svg_floor_plan(description)
                # Render SVG safely in Streamlit
                st.markdown(svg_code, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate SVG: {e}")

if __name__ == "__main__":
    app()
