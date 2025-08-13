import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Google Gemini AI Image Generator", layout="centered")

# API Key input with password field saved in session state
if "google_api_key" not in st.session_state:
    st.session_state["google_api_key"] = ""

if not st.session_state["google_api_key"]:
    st.title("🔐 Enter your Google API Key")
    key_input = st.text_input("Google API Key", type="password")
    if st.button("Save API Key"):
        if key_input.strip():
            st.session_state["google_api_key"] = key_input.strip()
            st.success("API Key saved! Reloading app...")
            st.experimental_rerun()
        else:
            st.error("Please enter a valid API Key.")
    st.stop()  # Stop execution until key is entered

# Initialize Gemini client with provided API key
client = genai.Client(api_key=st.session_state["google_api_key"])

st.title("🎨 Google Gemini AI Image Generator")

# User inputs
prompt = st.text_area("Enter your image prompt here", height=150)

style = st.selectbox(
    "Choose Artistic Style",
    ["Any", "Photorealistic", "Pixel Art", "Vector Art", "3D Render", "Isometric",
     "Cartoon", "Fantasy Art", "Cyberpunk", "Steampunk", "Watercolor", "Oil Painting", "Concept Art", "Low Poly",
     "Line Art", "Ink Drawing", "Pencil Drawing", "Minimalist", "Surrealism", "Abstract", "Neon Glow", "Flat Design"]
)

aspect = st.selectbox(
    "Choose Aspect Ratio Hint",
    ["Any", "Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"]
)

img_format = st.selectbox("Choose Output Format", ["PNG", "JPEG"])

style_hint = f"in {style} style" if style != "Any" else ""
aspect_hint = f"aspect ratio {aspect}" if aspect != "Any" else ""

full_prompt = f"{prompt.strip()}, {style_hint}, {aspect_hint}".strip(", ")

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
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
                    if part.text:
                        st.write(part.text)
                    elif part.inline_data:
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
                            file_name=f"gemini_generated_image.{img_format.lower()}",
                            mime=f"image/{img_format.lower()}"
                        )
                        st.success("✅ Image generated and ready for download!")
                        found_image = True

                if not found_image:
                    st.error("❌ No image found in the response. Try simplifying the prompt.")

            except Exception as e:
                st.error(f"Error generating image: {e}")

# Prompt writing tips section
st.markdown("---")
st.markdown("""
### 💡 Prompt Writing Tips & Hints

**Be descriptive!** Mention:
- **Subjects**, **actions**, **colors**, **art style**, **mood**, **lighting**, and **composition**.

**Example Prompt:**
> *"A serene bioluminescent mushroom forest at night, glowing flora, mystical atmosphere"*
> *"A cute baby sea otter floating on its back, holding a small colorful shell"*

---

**Artistic Style Options:**
Photorealistic, Pixel Art, Vector Art, 3D Render, Isometric, Cartoon, Fantasy Art, Cyberpunk, Steampunk, Watercolor, Oil Painting

**Output Format:**
PNG, JPEG, etc.

**Aspect Ratio Hint:**
- Square (1:1)
- Portrait (9:16)
- Landscape (16:9)
- Any (Default)

*Note: These are only hints for the AI. Results may vary depending on prompt complexity.*
""")
