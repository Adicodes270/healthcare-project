"""
pages/1_📋_Report_Summariser.py
Plain-language summarisation of medical reports.
Supports: PDF upload (text-based & scanned), direct text paste, and OpenAI vision OCR for image-only PDFs.
"""
import streamlit as st
from utils.openai_client import get_text_model, get_vision_model, MEDICAL_SAFETY_DISCLAIMER
from utils.pdf_reader import extract_text_from_pdf

st.set_page_config(page_title="Medical Report Summariser | HealthAI", page_icon="📋", layout="wide")

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

.report-card {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    border: 1px solid rgba(100,200,255,0.2);
}
.metric-pill {
    background: rgba(100,200,255,0.1);
    border: 1px solid rgba(100,200,255,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    display: inline-block;
    margin: 0.2rem;
    font-size: 0.85rem;
    color: #64c8ff;
}
.tab-desc {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(100,200,255,0.12);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    color: rgba(180,210,235,0.65);
    margin-bottom: 1rem;
}
.word-count-badge {
    display: inline-block;
    background: rgba(0,229,160,0.12);
    border: 1px solid rgba(0,229,160,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    color: #00e5a0;
    margin: 0.3rem 0;
}
.scanned-notice {
    background: linear-gradient(135deg, rgba(255,165,0,0.08), rgba(255,100,0,0.05));
    border: 1px solid rgba(255,165,0,0.35);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 📋 Medical Report Summariser")
st.markdown(
    "Upload a PDF, paste text directly, or use AI Vision for scanned reports — "
    "and receive a **clear, plain-language summary** with no medical jargon."
)
st.divider()

# ─── Shared settings (sidebar-style column) ───────────────────────────────────
col_settings, col_info = st.columns([1.3, 1])

with col_settings:
    reading_level = st.select_slider(
        "📖 Explain at the level of…",
        options=["Child (8–12 yrs)", "High-School Student", "General Adult", "Science Graduate"],
        value="General Adult",
    )
    focus_areas = st.multiselect(
        "🎯 Focus on these areas (optional)",
        ["Key Diagnoses", "Test Results & Values", "Medications Prescribed",
         "Recommended Follow-ups", "Risk Factors", "Lifestyle Recommendations"],
        default=["Key Diagnoses", "Test Results & Values", "Recommended Follow-ups"],
    )

with col_info:
    st.markdown("""
    <div class='report-card'>
    <b>💡 Three ways to analyse</b><br><br>
    <span class='metric-pill'>📄 PDF Upload</span> — text-based PDFs<br>
    <span class='metric-pill'>✏️ Paste Text</span> — copy-paste any report text<br>
    <span class='metric-pill'>🔬 Vision OCR</span> — scanned / image PDFs<br><br>
    <small>Nothing is stored. All processing is in-memory via the OpenAI API.</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─── Input tabs ───────────────────────────────────────────────────────────────
tab_pdf, tab_text, tab_vision = st.tabs(["📄 PDF Upload", "✏️ Paste Text", "🔬 Vision / Scanned PDF"])

report_text = None      # text-based content
vision_images = None    # PIL images for vision path
input_source = None     # label for UI messages

# ── Tab 1: PDF Upload ─────────────────────────────────────────────────────────
with tab_pdf:
    st.markdown("<div class='tab-desc'>Upload a <b>text-selectable PDF</b> (lab reports, discharge summaries, clinical notes). If the PDF is scanned/image-only, switch to the <b>Vision / Scanned PDF</b> tab.</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload medical report (PDF)",
        type=["pdf"],
        key="pdf_uploader",
        help="Lab reports, clinical notes, discharge summaries, radiology reports",
    )

    if uploaded_file:
        with st.spinner("🔍 Extracting text from PDF…"):
            try:
                result = extract_text_from_pdf(uploaded_file)
            except RuntimeError as e:
                st.error(str(e))
                st.stop()

        pages = result["pages"]
        strategy = result["strategy"]

        if result["is_scanned"] or not result["text"]:
            st.markdown(f"""
            <div class='scanned-notice'>
            ⚠️ <b>No selectable text found in this PDF</b> ({pages} page{'s' if pages != 1 else ''}).<br>
            This PDF appears to be <b>scanned / image-based</b>.<br>
            👉 Please switch to the <b>🔬 Vision / Scanned PDF</b> tab and upload it there for AI Vision analysis.
            </div>
            """, unsafe_allow_html=True)
        else:
            word_count = len(result["text"].split())
            st.markdown(f"<span class='word-count-badge'>✅ Extracted {word_count:,} words from {pages} page{'s' if pages != 1 else ''} &nbsp;·&nbsp; method: {strategy}</span>", unsafe_allow_html=True)
            report_text = result["text"]
            input_source = "PDF"

# ── Tab 2: Paste Text ─────────────────────────────────────────────────────────
with tab_text:
    st.markdown("<div class='tab-desc'>Paste any medical report, lab result, clinical note, or health document text directly into the box below.</div>", unsafe_allow_html=True)

    pasted_text = st.text_area(
        "Paste your medical report text here",
        placeholder=(
            "Example:\n\n"
            "Patient: John Doe, Age 45\n"
            "Date: 28-Sep-2026\n\n"
            "COMPLETE BLOOD COUNT:\n"
            "Haemoglobin: 11.2 g/dL (Low) [Normal: 13.5–17.5]\n"
            "WBC: 9,800 /µL [Normal: 4,500–11,000]\n"
            "Platelets: 142,000 /µL (Low) [Normal: 150,000–400,000]\n\n"
            "IMPRESSION: Mild anaemia. Recommend dietary iron supplementation and follow-up in 6 weeks.\n"
            "..."
        ),
        height=280,
        key="text_input_area",
    )

    if pasted_text and pasted_text.strip():
        word_count = len(pasted_text.split())
        if word_count < 10:
            st.warning("⚠️ Please enter more text — at least a few sentences are needed for a meaningful summary.")
        else:
            st.markdown(f"<span class='word-count-badge'>✅ {word_count:,} words ready for analysis</span>", unsafe_allow_html=True)
            report_text = pasted_text.strip()
            input_source = "pasted text"

# ── Tab 3: Vision / Scanned PDF ───────────────────────────────────────────────
with tab_vision:
    st.markdown("<div class='tab-desc'>Upload a <b>scanned PDF or medical image</b> (JPG/PNG). OpenAI's vision model will read the content visually and generate a summary — no selectable text required.</div>", unsafe_allow_html=True)

    vision_upload = st.file_uploader(
        "Upload scanned report (PDF, JPG, PNG)",
        type=["pdf", "jpg", "jpeg", "png", "webp"],
        key="vision_uploader",
        help="Works with scanned PDFs and photographed reports",
    )

    if vision_upload:
        from PIL import Image
        import io as _io

        file_type = vision_upload.type

        if "pdf" in file_type:
            # Try to convert PDF pages to images
            pdf_bytes = vision_upload.read()
            images_list = []
            try:
                import pypdfium2 as pdfium
                pdf_doc = pdfium.PdfDocument(pdf_bytes)
                st.info(f"📄 PDF has {len(pdf_doc)} page(s). Converting first 5 pages for Vision analysis…")
                for i in range(min(len(pdf_doc), 5)):
                    page = pdf_doc[i]
                    bitmap = page.render(scale=2.0)
                    pil_img = bitmap.to_pil()
                    images_list.append(pil_img)
                    st.image(pil_img, caption=f"Page {i+1}", use_container_width=True)
                vision_images = images_list
                input_source = "scanned PDF (Vision)"
            except ImportError:
                st.warning("⚠️ `pypdfium2` is not installed. Cannot convert PDF pages to images. Please install it: `pip install pypdfium2`")
                st.info("💡 Alternatively, export your PDF pages as PNG/JPG images and upload them here.")
            except Exception as e:
                st.error(f"❌ Could not process PDF: {e}")
        else:
            # Direct image upload
            img = Image.open(vision_upload)
            st.image(img, caption="Uploaded medical document", use_container_width=True)
            vision_images = [img]
            input_source = "image (Vision)"

        if vision_images:
            st.markdown(f"<span class='word-count-badge'>✅ {len(vision_images)} image(s) ready for Vision analysis</span>", unsafe_allow_html=True)

st.divider()

# ─── Shared prompt builder ────────────────────────────────────────────────────
focus_str = ", ".join(focus_areas) if focus_areas else "everything relevant"

SUMMARY_PROMPT_TEMPLATE = """You are a compassionate medical AI assistant helping a patient understand their medical report.

Reading level: {reading_level}
Focus on: {focus_str}

Medical Report Content:
\"\"\"
{content}
\"\"\"

Please provide a comprehensive, empathetic summary structured as follows:

## 🩺 Overview
A brief 2–3 sentence plain-language overview of what this report is about.

## 📊 Key Findings
Bullet-point list of the most important findings, results, or diagnoses. For every medical term or abbreviation, add a plain-language explanation in parentheses immediately after it.
For lab values, clearly state: value | normal range | whether it is High / Low / Normal.

## 💊 Medications / Treatments (if mentioned)
List any prescribed medications, dosages, and what they are for.

## 📅 Next Steps & Follow-ups
What the patient should do next — appointments, tests, lifestyle changes.

## ⚠️ Important Alerts
Highlight any values or findings that are abnormal or require urgent attention. Use ⚠️ symbol for each alert item.

## ❓ Questions to Ask Your Doctor
Suggest 3–5 specific questions the patient might want to ask their healthcare provider based on this report.

Tone: Warm, clear, reassuring. Avoid unnecessary jargon. Explain every medical term in simple language.
"""

# ─── Generate Summary button ──────────────────────────────────────────────────
if report_text or vision_images:
    if st.button("✨ Generate Summary", type="primary", use_container_width=True):
        # ── Text path (PDF extract or pasted text) ────────────────────────────
        if report_text:
            # Limit to ~12,000 chars but keep full content for short reports
            content_snippet = report_text[:14000]
            prompt = SUMMARY_PROMPT_TEMPLATE.format(
                reading_level=reading_level,
                focus_str=focus_str,
                content=content_snippet,
            )
            with st.spinner(f"🤖 OpenAI is analysing your {input_source}…"):
                try:
                    model = get_text_model()
                    response = model.generate_content(prompt)
                    summary = response.text

                    st.markdown("---")
                    st.markdown("## 📄 Your Report Summary")
                    st.markdown(summary)
                    st.markdown(MEDICAL_SAFETY_DISCLAIMER)

                    st.download_button(
                        "⬇️ Download Summary",
                        data=summary + "\n\n" + MEDICAL_SAFETY_DISCLAIMER,
                        file_name="medical_report_summary.txt",
                        mime="text/plain",
                    )
                except Exception as e:
                    st.error(f"❌ OpenAI API error: {e}")

        # ── Vision path (scanned PDF / image) ────────────────────────────────
        elif vision_images:
            vision_prompt = f"""You are a compassionate medical AI assistant. The following image(s) show a scanned medical report or document.

Reading level: {reading_level}
Focus on: {focus_str}

Please:
1. First, carefully read ALL text visible in the image(s) — including handwritten notes, printed values, headers, and tables.
2. Then provide a comprehensive, empathetic summary structured as follows:

## 🩺 Overview
A brief 2–3 sentence plain-language overview of what this report is about.

## 📊 Key Findings
Bullet-point list of findings/results. For lab values: state value | normal range | High / Low / Normal.
Explain every medical term in plain language in parentheses.

## 💊 Medications / Treatments (if mentioned)
List any prescribed medications, dosages, and what they are for.

## 📅 Next Steps & Follow-ups
What the patient should do next.

## ⚠️ Important Alerts
Abnormal values or urgent findings (prefix each with ⚠️).

## ❓ Questions to Ask Your Doctor
3–5 specific questions based on this report.

Tone: Warm, clear, reassuring.
"""
            with st.spinner("🔬 OpenAI vision is reading your scanned document…"):
                try:
                    model = get_vision_model()
                    # Pass all images with the prompt for multimodal analysis.
                    content_parts = [vision_prompt] + vision_images
                    response = model.generate_content(content_parts)
                    summary = response.text

                    st.markdown("---")
                    st.markdown("## 📄 Your Report Summary (Vision Analysis)")
                    st.markdown(summary)
                    st.markdown(MEDICAL_SAFETY_DISCLAIMER)

                    st.download_button(
                        "⬇️ Download Summary",
                        data=summary + "\n\n" + MEDICAL_SAFETY_DISCLAIMER,
                        file_name="medical_report_summary_vision.txt",
                        mime="text/plain",
                    )
                except Exception as e:
                    st.error(f"❌ OpenAI vision error: {e}")
else:
    st.info("👆 Choose an input method above: upload a PDF, paste text, or use Vision for scanned documents.")
