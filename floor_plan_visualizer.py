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

def generate_3d_floor_plan_image(description):
    prompt = f"""
    Generate a detailed description or prompt for a 3D rendered image of a floor plan with the following layout:
    {description}

    The image should be realistic with walls, doors, windows, and furniture visible from an isometric perspective.
    Return either an image URL or a detailed prompt for a 3D rendering.
    """
    genai.configure(api_key=st.session_state["google_api_key"])
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text  # Could be a URL or prompt for a 3D image

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
        placeholder="e.g., 'A 20ft by 30ft rectangular workshop with a large garage door on the north wall...'"
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
        if st.button("Generate 3D Floor Plan Image Prompt"):
            if not description.strip():
                st.warning("Please enter a floor plan description.")
            else:
                with st.spinner("Generating 3D floor plan prompt..."):
                    try:
                        result = generate_3d_floor_plan_image(description)
                        st.info("Here’s a prompt or URL for a 3D floor plan image:")
                        st.write(result)
                        # If this is an image URL, you can also display it:
                        if result.startswith("http"):
                            st.image(result, caption="3D Floor Plan Image")
                    except Exception as e:
                        st.error(f"Failed to generate 3D floor plan image: {e}")
