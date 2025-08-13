import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Initialize Gemini client with API key from environment variable
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("🏠 Clean 3D Floor Plan Image Generator")

def enhance_prompt(user_prompt, style, aspect):
    base_prompt = user_prompt.strip()
    if not base_prompt:
        return ""

    floorplan_keywords = ["floor plan", "apartment", "house", "bedroom", "living room", "kitchen"]
    if any(word in base_prompt.lower() for word in floorplan_keywords):
        style_hint = "3D Render"
        clean_hints = "no text, no labels, clean architectural render"
    else:
        style_hint = style if style != "Any" else ""
        clean_hints = ""

    aspect_hint = f"aspect ratio {aspect}" if aspect != "Any" else ""

    hints = ", ".join(filter(None, [style_hint, clean_hints, aspect_hint]))
    full_prompt = f"{base_prompt}, {hints}" if hints else base_prompt
    return full_prompt

# User inputs
prompt = st.text_area("Enter your floor plan or image prompt here:", height=150)
style = st.selectbox(
    "Choose Artistic Style",
    ["Any", "Photorealistic", "Pixel Art", "Vector Art", "3D Render", "Isometric",
     "Cartoon", "Fantasy Art", "Cyberpunk", "Steampunk", "Watercolor", "Oil Painting",
     "Concept Art", "Low Poly", "Line Art", "Ink Drawing", "Pencil Drawing",
     "Minimalist", "Surrealism", "Abstract", "Neon Glow", "Flat Design"]
)
aspect = st.selectbox(
    "Choose Aspect Ratio Hint",
    ["Any", "Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"]
)
img_format = st.selectbox("Choose Output Format", ["PNG", "JPEG"])

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        full_prompt = enhance_prompt(prompt, style, aspect)
        st.markdown(f"**Using prompt:** `{full_prompt}`")

        with st.spinner("Generating image..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[full_prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

                found_image = False
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image, caption="Generated Image", use_container_width=True)

                        img_bytes = BytesIO()
                        file_format = img_format.upper()
                        if file_format == "JPG":
                            file_format = "JPEG"
                        image.save(img_bytes, format=file_format)
                        img_bytes.seek(0)

                        st.download_button(
                            label="Download Image",
                            data=img_bytes,
                            file_name=f"generated_image.{img_format.lower()}",
                            mime=f"image/{img_format.lower()}"
                        )
                        st.success("✅ Image generated and ready for download!")
                        found_image = True
                    elif part.text:
                        st.info(f"Model says:\n{part.text}")

                if not found_image:
                    st.error("❌ No image found in the response. Try simplifying the prompt.")
            except Exception as e:
                st.error(f"Error generating image: {e}")

st.markdown("---")
st.markdown("""
### 💡 Prompt Writing Tips
- Be descriptive but concise.
- For floor plans, mention "3D Render", "no text", "clean architectural render" for best results.
- Example prompt: *"Modern two-bedroom apartment floor plan, 3D Render, no text, isometric view"*
""")
