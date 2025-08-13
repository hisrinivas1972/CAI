import streamlit as st
import google.generativeai as genai

def generate_floor_plan_image(description):
    genai.configure(api_key=st.session_state["google_api_key"])
    model = genai.GenerativeModel("gemini-2.0-flash-exp-image-generation")

    prompt = f"Generate a realistic 3D rendered floor plan image based on the description:\n{description}"

    response = model.generate_content({"prompt": prompt})

    return response.text

def app():
    st.title("Floor Plan Visualizer - 3D Image Generation")

    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                st.session_state["google_api_key"] = key.strip()
                st.session_state["api_key_saved"] = True
                st.success("✅ API key saved!")
            else:
                st.error("⚠️ Please enter a valid API key.")
        return

    description = st.text_area(
        "Describe your floor plan:",
        height=200,
        placeholder="E.g., 'Modern 3-bedroom house with large windows and garage'"
    )

    if st.button("Generate 3D Floor Plan Image"):
        if not description.strip():
            st.warning("Please enter a floor plan description.")
        else:
            with st.spinner("Generating 3D floor plan image..."):
                try:
                    image_data = generate_floor_plan_image(description)
                    if image_data.startswith("http"):
                        st.image(image_data, caption="3D Floor Plan Image")
                    elif image_data.startswith("data:image"):
                        st.image(image_data, caption="3D Floor Plan Image")
                    else:
                        st.text("Model response:\n" + image_data)
                except Exception as e:
                    st.error(f"Failed to generate 3D image: {e}")

if __name__ == "__main__":
    app()
