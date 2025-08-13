import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def app():
    st.header("🏠 3D Floor Plan Visualizer")
    st.write("Create clean, text-free 3D floor plan renderings from descriptive prompts.")

    # Step 1: Get API key
    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("🔑 Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                st.session_state["google_api_key"] = key.strip()
                st.session_state["api_key_saved"] = True
                st.success("✅ API key saved! You can now generate images.")
            else:
                st.error("❌ Please enter a valid API key.")
        return  # Exit until key is entered

    # Step 2: Configure Gemini client
    genai.configure(api_key=st.session_state["google_api_key"])
    client = genai.GenerativeModel("gemini-1.5-flash")

    # Step 3: Get user input
    prompt = st.text_area("📝 Describe your floor plan:", height=150,
                          placeholder="e.g. Modern 2-bedroom apartment with balcony and open kitchen")

    if st.button("🎨 Generate 3D Floor Plan"):
        if not prompt.strip():
            st.warning("⚠️ Please enter a description.")
        else:
            full_prompt = f"{prompt.strip()}, 3D Render, clean architectural floor plan, no text, isometric view"

            with st.spinner("Generating image..."):
                try:
                    response = client.generate_content(
                        contents=[full_prompt],
                        generation_config=types.GenerationConfig(response_mime_type="image/png")
                    )

                    image = Image.open(BytesIO(response.parts[0].inline_data.data))
                    st.image(image, caption="🏡 Generated 3D Floor Plan", use_container_width=True)

                    # Download option
                    img_bytes = BytesIO()
                    image.save(img_bytes, format="PNG")
                    img_bytes.seek(0)
                    st.download_button("⬇️ Download Image", data=img_bytes, file_name="floor_plan.png", mime="image/png")

                except Exception as e:
                    st.error(f"🚨 Error generating image: {e}")

if __name__ == "__main__":
    app()
