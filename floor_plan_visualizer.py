import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Function to generate image using Gemini
def generate_floor_plan_image(description, style, aspect, client):
    # Style + aspect hints
    style_hint = f"{style} style" if style != "Any" else "3D render"
    aspect_hint = f"{aspect} aspect ratio" if aspect != "Any" else ""

    # Prompt engineered to encourage image generation
    prompt = (
        f"Isometric 3D render of a floor plan: {description}, "
        f"{style_hint}, {aspect_hint}, realistic lighting, white background, architectural visualization"
    ).strip(", ")

    # Make Gemini request
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
    )

    # Extract image
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return Image.open(BytesIO(part.inline_data.data))

    # If no image found
    return "❌ No image returned. Try rephrasing the description."

# Streamlit app
def app():
    st.set_page_config(page_title="3D Floor Plan Generator", layout="centered")
    st.title("🏠 3D Floor Plan Generator (Google Gemini)")

    # API key handling
    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("🔐 Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                st.session_state["google_api_key"] = key.strip()
                st.session_state["api_key_saved"] = True
                st.success("✅ API key saved! You're ready to generate images.")
            else:
                st.error("⚠️ Please enter a valid API key.")
        return

    # Prompt input
    description = st.text_area(
        "📝 Describe your floor plan:",
        height=150,
        placeholder="E.g., 'Modern 3-bedroom house with large windows, open kitchen, and garage'"
    )

    # Style, aspect, format selection
    style = st.selectbox(
        "🎨 Choose Style",
        ["Any", "Photorealistic", "3D Render", "Isometric", "Line Art", "Fantasy Art", "Minimalist", "Oil Painting"]
    )

    aspect = st.selectbox(
        "📐 Choose Aspect Ratio",
        ["Any", "Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"]
    )

    img_format = st.selectbox("🖼️ Output Format", ["PNG", "JPEG"])

    if st.button("🚀 Generate Floor Plan Image"):
        if not description.strip():
            st.warning("Please enter a floor plan description.")
            return

        with st.spinner("Generating image using Gemini..."):
            try:
                client = genai.Client(api_key=st.session_state["google_api_key"])
                result = generate_floor_plan_image(description, style, aspect, client)

                if isinstance(result, Image.Image):
                    st.image(result, caption="🖼️ Generated Floor Plan", use_container_width=True)

                    # Image download
                    img_bytes = BytesIO()
                    result.save(img_bytes, format=img_format.upper())
                    img_bytes.seek(0)

                    st.download_button(
                        label="⬇️ Download Image",
                        data=img_bytes,
                        file_name=f"floor_plan_3d.{img_format.lower()}",
                        mime=f"image/{img_format.lower()}"
                    )
                    st.success("✅ Image generated successfully!")

                elif isinstance(result, str):
                    st.warning("⚠️ The model returned text instead of an image.")
                    st.info(result)
                else:
                    st.error("❌ No valid response from model.")

            except Exception as e:
                st.error(f"🔥 Error generating image: {e}")

# Run app
if __name__ == "__main__":
    app()
