import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def generate_floor_plan_image(description, client):
    prompt = f"Create a detailed, realistic 3D rendered floor plan image ONLY based on this description:\n{description}"

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            # Optional: specify image size or other image generation configs here
            image_generation_config=types.ImageGenerationConfig(
                # image_size="1024x768"  # optional
            ),
        )
    )

    # Parse response to find image inline data
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image = Image.open(BytesIO(part.inline_data.data))
            return image
        elif part.text:
            return part.text  # fallback text if no image

    return "No image found in the response."

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
            return

        with st.spinner("Generating 3D floor plan image..."):
            try:
                client = genai.Client(api_key=st.session_state["google_api_key"])
                result = generate_floor_plan_image(description, client)

                if isinstance(result, Image.Image):
                    st.image(result, caption="3D Floor Plan Image", use_container_width=True)
                else:
                    # Text fallback (likely description or error)
                    st.text(result)

            except Exception as e:
                st.error(f"Failed to generate 3D image: {e}")

if __name__ == "__main__":
    app()
