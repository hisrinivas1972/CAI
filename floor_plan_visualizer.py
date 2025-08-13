import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def app():
    st.header("🏠 3D Floor Plan Visualizer")

    # Step 1: Get API key if not saved
    if "google_api_key" not in st.session_state or not st.session_state.get("api_key_saved", False):
        key = st.text_input("🔑 Enter your Google API Key", type="password")
        if st.button("Save API Key"):
            if key.strip():
                st.session_state["google_api_key"] = key.strip()
                st.session_state["api_key_saved"] = True
                st.success("✅ API key saved! You can now generate images.")
                try:
                    st.experimental_rerun()  # Immediately rerun so UI updates
                except Exception as e:
                    st.error(f"Failed to rerun app: {e}")
        return  # Stop here until API key is saved

    # Step 2: Initialize Gemini client
    try:
        client = genai.Client(api_key=st.session_state["google_api_key"])
    except Exception as e:
        st.error(f"🔒 Failed to initialize client: {e}")
        return

    # Step 3: Prompt input
    prompt = st.text_area(
        "📝 Describe your floor plan:",
        height=150,
        placeholder="e.g. Modern 2-bedroom apartment with balcony and open kitchen"
    )

    if st.button("🎨 Generate 3D Floor Plan"):
        if not prompt.strip():
            st.warning("⚠️ Please enter a description.")
        else:
            full_prompt = f"{prompt.strip()}, 3D Render, clean architectural floor plan, no text, isometric view"
            with st.spinner("Generating image..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-exp-image-generation",
                        contents=[full_prompt],
                        config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
                    )

                    image_found = False
                    for part in response.candidates[0].content.parts:
                        # Check if part has image data
                        if hasattr(part, "inline_data") and part.inline_data:
                            image = Image.open(BytesIO(part.inline_data.data))
                            st.image(image, caption="🏡 Generated 3D Floor Plan", use_container_width=True)

                            # Download button
                            img_bytes = BytesIO()
                            image.save(img_bytes, format="PNG")
                            img_bytes.seek(0)
                            st.download_button("⬇️ Download Image", data=img_bytes, file_name="floor_plan.png", mime="image/png")

                            image_found = True
                            break
                        elif hasattr(part, "text") and part.text:
                            st.info(f"🧠 Model Text Response:\n\n{part.text}")

                    if not image_found:
                        st.error("❌ No image returned. Try rewording the description or simplifying it.")

                except Exception as e:
                    st.error(f"🚨 Error generating image: {e}")

if __name__ == "__main__":
    app()
