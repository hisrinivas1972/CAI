import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def app():
    st.header("🏠 3D Floor Plan Visualizer")
    st.write("Generate clean, realistic 3D floor plan images from your architectural descriptions using AI.")

    # API Key Input
    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        api_key = st.text_input("🔑 Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if api_key.strip():
                st.session_state["google_api_key"] = api_key.strip()
                st.session_state["api_key_saved"] = True
                st.success("✅ API key saved!")
            else:
                st.error("⚠️ Please enter a valid API key.")
        return  # Exit until key is entered

    # Configure Gemini client
    genai.configure(api_key=st.session_state["google_api_key"])
    client = genai.GenerativeModel("gemini-1.5-flash")

    # ✅ Now show the prompt input
    st.subheader("📝 Describe your floor plan:")
    prompt = st.text_area("e.g. Modern 2-bedroom apartment with balcony and open kitchen", height=100)

    aspect = st.selectbox("Aspect Ratio", ["Any", "Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"])
    img_format = st.selectbox("Output Format", ["PNG", "JPEG"])

    if st.button("🎨 Generate 3D Floor Plan"):
        if not prompt.strip():
            st.warning("Please enter a description.")
            return

        full_prompt = f"{prompt.strip()}, 3D Render, isometric view, clean layout, no text, no labels"
        if aspect != "Any":
            full_prompt += f", aspect ratio {aspect}"

        with st.spinner("Generating image..."):
            try:
                response = client.generate_content(
                    contents=[full_prompt],
                    generation_config=types.GenerationConfig(response_mime_type="image/png")
                )

                image_data = response.parts[0].inline_data.data
                image = Image.open(BytesIO(image_data))

                st.image(image, caption="Generated 3D Floor Plan", use_container_width=True)

                # Download button
                img_bytes = BytesIO()
                fmt = img_format.upper()
                if fmt == "JPG":
                    fmt = "JPEG"
                image.save(img_bytes, format=fmt)
                img_bytes.seek(0)

                st.download_button(
                    label="📥 Download Image",
                    data=img_bytes,
                    file_name=f"floorplan.{img_format.lower()}",
                    mime=f"image/{img_format.lower()}"
                )

            except Exception as e:
                st.error(f"⚠️ Error generating image: {e}")

if __name__ == "__main__":
    app()
