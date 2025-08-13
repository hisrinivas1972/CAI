import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def generate_floor_plan_image(description, client):
    prompt = f"Generate a realistic 3D rendered floor plan image based on the description:\n{description}"

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
    )

    # Extract image from response
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return Image.open(BytesIO(part.inline_data.data))
        elif part.text:
            # fallback text output
            return part.text
    return "No image found in response."

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
                    client = genai.Client(api_key=st.session_state["google_api_key"])
                    image_or_text = generate_floor_plan_image(description, client)

                    if isinstance(image_or_text, Image.Image):
                        st.image(image_or_text, caption="3D Floor Plan Image", use_container_width=True)
                    else:
                        st.text(f"Model response:\n{image_or_text}")

                except Exception as e:
                    st.error(f"Failed to generate 3D image: {e}")

if __name__ == "__main__":
    app()
