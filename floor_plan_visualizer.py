import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Function to generate the floor plan image
def generate_floor_plan_image(description, style, aspect, client):
    # Build a visual-style prompt
    style_hint = f"{style} style" if style != "Any" else ""
    aspect_hint = f"aspect ratio {aspect}" if aspect != "Any" else ""

    prompt = f"{description}, 3D render, isometric view, architectural drawing, {style_hint}, {aspect_hint}".strip(", ")

    # Generate response
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
            return part.text  # Fallback: model returns only text

    return None

# Streamlit app
def app():
    st.set_page_config(page_title="3D Floor Plan Generator", layout="centered")
    st.title("🏠 3D Floor Plan Image Generator")

    # API key setup
    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("🔐 Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                st.session_state["google_api_key"] = key.strip()
                st.session_state["api_key_saved"] = True
                st.success("✅ API key saved!")
            else:
                st.error("⚠️ Please enter a valid API key.")
        return

    # Floor plan description input
    description = st.text_area(
        "📝 Describe your floor plan:",
        height=150,
        placeholder="E.g., 'Modern 3-bedroom house with large windows, open kitchen, and garage'"
    )

    # Style and aspect selections
    style = st.selectbox(
        "🎨 Choose Art Style",
        ["Any", "Photorealistic", "3D Render", "Isometric", "Line Art", "Fantasy Art", "Oil Painting", "Minimalist"]
    )

    aspect = st.selectbox(
        "📐 Choose Aspect Ratio Hint",
        ["Any", "Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"]
    )

    img_format = st.selectbox("🖼️ Output Format", ["PNG", "JPEG"])

    if st.button("🚀 Generate 3D Floor Plan Image"):
        if not description.strip():
            st.warning("Please enter a floor plan description.")
            return

        with st.spinner("Generating image..."):
            try:
                client = genai.Client(api_key=st.session_state["google_api_key"])
                result = generate_floor_plan_image(description, style, aspect, client)

                if isinstance(result, Image.Image):
                    st.image(result, caption="🖼️ Generated 3D Floor Plan", use_container_width=True)

                    # Convert and offer download
                    img_bytes = BytesIO()
                    file_format = img_format.upper()
                    if file_format == "JPG":
                        file_format = "JPEG"
                    result.save(img_bytes, format=file_format)
                    img_bytes.seek(0)

                    st.download_button(
                        label="⬇️ Download Image",
                        data=img_bytes,
                        file_name=f"floor_plan_3d.{img_format.lower()}",
                        mime=f"image/{img_format.lower()}"
                    )

                elif isinstance(result, str):
                    st.warning("⚠️ The model returned a description instead of an image.")
                    st.info("Model Response:")
                    st.write(result)

                else:
                    st.error("❌ No image or text returned by the model.")

            except Exception as e:
                st.error(f"🔥 Error generating image: {e}")

# Run the app
if __name__ == "__main__":
    app()
