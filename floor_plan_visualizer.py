import streamlit as st
import google.generativeai as genai
from google.generativeai.types import content_types
from PIL import Image
from io import BytesIO

# --------------------
# Helper: Configure Gemini client
# --------------------
def configure_client(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini client: {e}")
        return None

# --------------------
# Main Streamlit App
# --------------------
def app():
    st.set_page_config(page_title="3D Floor Plan Visualizer", page_icon="🏠")
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
        return  # Stop app until API key is saved

    # Step 2: Configure client
    genai = configure_client(st.session_state["google_api_key"])
    if not genai:
        return

    # Step 3: Get user input
    prompt = st.text_area("📝 Describe your floor plan:", height=150,
                          placeholder="e.g. Modern 2-bedroom apartment with balcony and open kitchen")

    if st.button("🎨 Generate 3D Floor Plan"):
        if not prompt.strip():
            st.warning("⚠️ Please enter a description.")
            return

        full_prompt = f"{prompt.strip()}, 3D Render, clean architectural floor plan, no text, isometric view"

        with st.spinner("🛠️ Generating image..."):
            try:
                # Use the correct image generation model
                model = genai.GenerativeModel("gemini-1.5-flash")  # or use your preferred model
                response = model.generate_content(
                    full_prompt,
                    generation_config={"response_mime_type": "image/png"}
                )

                image_data = None

                for part in response.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        image_data = part.inline_data.data
                        break

                if image_data:
                    image = Image.open(BytesIO(image_data))
                    st.image(image, caption="🏡 Generated 3D Floor Plan", use_container_width=True)

                    # Download button
                    img_bytes = BytesIO()
                    image.save(img_bytes, format="PNG")
                    img_bytes.seek(0)
                    st.download_button("⬇️ Download Image", data=img_bytes, file_name="floor_plan.png", mime="image/png")
                else:
                    st.error("❌ No image returned. Try simplifying your description.")

            except Exception as e:
                st.error(f"🚨 Error generating image: {e}")

# --------------------
# Entry point
# --------------------
if __name__ == "__main__":
    app()
