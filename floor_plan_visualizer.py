import streamlit as st
import google.generativeai as genai

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

def generate_base64_png_image(description):
    prompt = f"""
    Generate a base64 encoded PNG image data URI of a 3D rendered floor plan image
    with the following description:

    {description}

    Only output the image as a data URI string starting with "data:image/png;base64,".
    """
    genai.configure(api_key=st.session_state["google_api_key"])
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

def app():
    st.title("Floor Plan Visualizer")

    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                st.session_state["google_api_key"] = key.strip()
                st.session_state["api_key_saved"] = True
                st.success("API key saved!")
            else:
                st.error("Please enter a valid API key.")
        return

    description = st.text_area(
        "Describe your floor plan (e.g. room sizes, doors, windows):",
        height=200,
        placeholder="e.g., 'A modern 3-bedroom house with garage and garden...'"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate 2D SVG Floor Plan"):
            if not description.strip():
                st.warning("Please enter a floor plan description.")
            else:
                with st.spinner("Generating SVG floor plan..."):
                    try:
                        svg_code = generate_svg_floor_plan(description)
                        st.markdown(svg_code, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed to generate SVG: {e}")

    with col2:
        if st.button("Generate 3D Floor Plan Image (Base64 PNG)"):
            if not description.strip():
                st.warning("Please enter a floor plan description.")
            else:
                with st.spinner("Generating 3D floor plan image..."):
                    try:
                        base64_img = generate_base64_png_image(description)
                        if base64_img.startswith("data:image/png;base64,"):
                            st.image(base64_img, caption="3D Floor Plan Image")
                        else:
                            st.warning("Model did not return a valid image data URI. Here's the output:")
                            st.text(base64_img)
                    except Exception as e:
                        st.error(f"Failed to generate 3D image: {e}")

if __name__ == "__main__":
    app()
