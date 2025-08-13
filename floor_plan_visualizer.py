import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

def generate_floor_plan_image(description):
    prompt = f"Generate a realistic 3D rendered floor plan image based on the description:\n{description}"
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
    )
    return response

def app():
    st.title("Floor Plan Visualizer - 3D Image Generation")

    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                # You must set environment variable or configure API key here
                import os
                os.environ["GOOGLE_API_KEY"] = key.strip()
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
                    response = generate_floor_plan_image(description)
                    found_image = False
                    for part in response.candidates[0].content.parts:
                        if part.text:
                            st.write(part.text)
                        elif part.inline_data:
                            image = Image.open(BytesIO(part.inline_data.data))
                            st.image(image, caption="3D Floor Plan Image", use_container_width=True)

                            # Optional: allow download in PNG
                            img_bytes = BytesIO()
                            image.save(img_bytes, format="PNG")
                            img_bytes.seek(0)

                            st.download_button(
                                label="Download Image (PNG)",
                                data=img_bytes,
                                file_name="floor_plan.png",
                                mime="image/png"
                            )
                            found_image = True

                    if not found_image:
                        st.error("❌ No image found in the response. Try simplifying the description.")
                except Exception as e:
                    st.error(f"Failed to generate 3D image: {e}")

if __name__ == "__main__":
    app()
