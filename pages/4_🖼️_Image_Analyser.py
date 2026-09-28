"""
pages/4_🖼️_Image_Analyser.py
Multimodal Gemini vision analysis of medical images (X-rays, skin conditions, etc.)
"""
import streamlit as st
from PIL import Image
from utils.gemini_client import get_vision_model, MEDICAL_SAFETY_DISCLAIMER

st.set_page_config(page_title="Medical Image Analyser | HealthAI", page_icon="🖼️", layout="wide")

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.image-card {
    background: linear-gradient(135deg, #0a1628, #162040);
    border: 1px solid rgba(100,200,255,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}
.analysis-section {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #64c8ff;
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin: 0.8rem 0;
}
.confidence-bar {
    background: rgba(100,200,255,0.1);
    border-radius: 4px;
    height: 8px;
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🖼️ Medical Image Analyser")
st.markdown("Upload a medical image for **AI-powered visual analysis** using Gemini's multimodal capabilities.")

st.warning("⚠️ This tool provides AI-generated observations only. It is **not a diagnostic tool** and must not replace professional radiological or clinical assessment.")

st.divider()

col1, col2 = st.columns([1, 1.2])

with col1:
    image_type = st.selectbox(
        "Image type",
        [
            "General / Unknown",
            "X-Ray (Chest)",
            "X-Ray (Bone / Joint)",
            "MRI Scan",
            "CT Scan",
            "Skin Condition / Dermatology",
            "Eye / Fundus Image",
            "Wound / Injury Photo",
            "Ultrasound",
            "ECG / EKG Strip",
        ],
    )

    clinical_context = st.text_area(
        "Clinical context (optional)",
        placeholder="e.g. Patient is a 55-year-old male with chest pain and shortness of breath for 2 days.",
        height=90,
    )

    analysis_focus = st.multiselect(
        "What should the AI focus on?",
        ["Abnormalities / Lesions", "Anatomical structures", "Symmetry & alignment",
         "Density / Texture variations", "Comparison to normal baseline", "Possible pathology"],
        default=["Abnormalities / Lesions", "Possible pathology"],
    )

with col2:
    uploaded_image = st.file_uploader(
        "Upload medical image",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        help="Supports JPEG, PNG, WebP, BMP",
    )
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded image", use_container_width=True)

st.divider()

if uploaded_image and st.button("🔍 Analyse Image", type="primary", use_container_width=True):
    focus_str = ", ".join(analysis_focus) if analysis_focus else "general findings"
    context_str = clinical_context.strip() if clinical_context.strip() else "No additional clinical context provided."

    prompt = f"""You are an expert AI medical imaging assistant with knowledge equivalent to a radiologist/dermatologist/specialist.

Image type: {image_type}
Clinical context: {context_str}
Analysis focus: {focus_str}

Analyse this medical image and provide a structured report:

## 🔎 Image Quality Assessment
Comment on image quality, positioning, and any limitations affecting analysis.

## 📐 Anatomical Overview
Describe the key anatomical structures visible in the image.

## 🔍 Key Observations
List your observations systematically. For each finding:
- Location / region
- Appearance / characteristics
- Clinical significance (normal / abnormal / uncertain)

## ⚠️ Potential Concerns
Highlight any features that may warrant clinical attention. Be specific but appropriately cautious.

## ✅ Normal Findings
Note structures that appear within normal limits.

## 📋 Summary & Recommendations
A 2–3 sentence clinical summary and recommendation for next steps (additional imaging, specialist referral, etc.).

Use clear, structured language. Flag uncertainty explicitly. Do not over-diagnose.
"""

    with st.spinner("🤖 Analysing image with Gemini Vision…"):
        try:
            model = get_vision_model()
            image_pil = Image.open(uploaded_image)
            response = model.generate_content([prompt, image_pil])
            result = response.text

            st.markdown("## 🏥 AI Image Analysis Report")
            st.markdown(result)
            st.markdown(MEDICAL_SAFETY_DISCLAIMER)

            st.download_button(
                "⬇️ Download Report",
                data=result + "\n\n" + MEDICAL_SAFETY_DISCLAIMER,
                file_name="image_analysis_report.txt",
                mime="text/plain",
            )
        except Exception as e:
            st.error(f"❌ Error analysing image: {e}")
elif not uploaded_image:
    st.info("👆 Upload a medical image above to begin analysis.")
