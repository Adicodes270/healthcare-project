"""
pages/3_🔬_Symptom_Checker.py
AI-powered symptom checker and triage assistant.
"""
import streamlit as st
from utils.gemini_client import get_text_model, MEDICAL_SAFETY_DISCLAIMER

st.set_page_config(page_title="Symptom Checker | HealthAI", page_icon="🔬", layout="wide")

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.triage-urgent {
    background: linear-gradient(135deg, #4a0000, #8b0000);
    border: 1px solid #ff4444;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.triage-moderate {
    background: linear-gradient(135deg, #3a2500, #7a5000);
    border: 1px solid #ff9800;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.triage-mild {
    background: linear-gradient(135deg, #0a3a00, #1a6a00);
    border: 1px solid #4caf50;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.symptom-tag {
    background: rgba(100,200,255,0.15);
    border: 1px solid rgba(100,200,255,0.4);
    border-radius: 16px;
    padding: 0.25rem 0.7rem;
    display: inline-block;
    margin: 0.15rem;
    font-size: 0.82rem;
    color: #64c8ff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔬 Symptom Checker & Triage Assistant")
st.markdown("Describe your symptoms to receive **AI-powered guidance** on possible conditions and suggested next steps.")

st.divider()

# ─── Symptom Input ────────────────────────────────────────────────────────────
col1, col2 = st.columns([1.5, 1])

with col1:
    symptoms_text = st.text_area(
        "Describe your symptoms in detail",
        placeholder="e.g. I have had a persistent headache on the right side for 3 days, along with nausea and sensitivity to light. No fever.",
        height=130,
    )

    st.markdown("**Select common symptoms (optional):**")
    common_symptoms = [
        "Fever", "Headache", "Cough", "Fatigue", "Nausea", "Chest pain",
        "Shortness of breath", "Dizziness", "Abdominal pain", "Joint pain",
        "Rash", "Sore throat", "Vomiting", "Diarrhea", "Loss of appetite",
    ]
    selected_symptoms = []
    cols_s = st.columns(4)
    for i, sym in enumerate(common_symptoms):
        if cols_s[i % 4].checkbox(sym, key=f"sym_{i}"):
            selected_symptoms.append(sym)

with col2:
    st.markdown("**Patient details (optional, improves accuracy):**")
    age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
    sex = st.selectbox("Biological sex", ["Not specified", "Male", "Female"])
    duration = st.selectbox(
        "Symptom duration",
        ["Less than 24 hours", "1–3 days", "4–7 days", "1–2 weeks", "More than 2 weeks"],
    )
    severity = st.select_slider(
        "Overall severity",
        options=["Mild", "Moderate", "Severe", "Very Severe"],
        value="Moderate",
    )
    pre_conditions = st.multiselect(
        "Pre-existing conditions",
        ["Diabetes", "Hypertension", "Heart disease", "Asthma", "Thyroid disorder",
         "Kidney disease", "Pregnancy", "Immunocompromised", "None"],
        default=["None"],
    )

st.divider()

if st.button("🔍 Analyse Symptoms", type="primary", use_container_width=True):
    all_symptoms = symptoms_text.strip()
    if selected_symptoms:
        all_symptoms += (" Also experiencing: " + ", ".join(selected_symptoms) + ".") if all_symptoms else ", ".join(selected_symptoms)

    if not all_symptoms:
        st.warning("⚠️ Please describe at least one symptom before analysing.")
        st.stop()

    pre_cond_str = ", ".join([p for p in pre_conditions if p != "None"]) or "None reported"

    prompt = f"""You are an empathetic medical AI triage assistant helping a patient understand their symptoms.

Patient Profile:
- Age: {age}
- Sex: {sex}
- Symptoms: {all_symptoms}
- Duration: {duration}
- Severity: {severity}
- Pre-existing conditions: {pre_cond_str}

Provide a structured triage assessment:

## 🚨 Triage Level
Classify as one of: URGENT (seek emergency care now), MODERATE (see a doctor within 24–48 hours), or MILD (home care + monitor).
Explain your reasoning in 1–2 sentences.

## 🩺 Possible Conditions
List 3–5 possible conditions that match these symptoms, from most to least likely. For each:
- **Condition name**
- Brief explanation (1–2 sentences in plain language)
- Key distinguishing feature

## 🏠 Immediate Care Advice
What the patient can safely do right now at home (rest, hydration, OTC medications if safe).

## 🚨 Emergency Warning Signs
List specific symptoms that, if they appear, mean the patient should seek emergency care IMMEDIATELY.

## 👨‍⚕️ Recommended Next Steps
What type of healthcare professional to see and timeframe.

Be accurate, empathetic, and conservative — when in doubt, recommend medical consultation.
"""

    with st.spinner("🤖 Analysing symptoms…"):
        try:
            model = get_text_model()
            response = model.generate_content(prompt)
            result = response.text

            st.markdown("## 📋 Triage Assessment")
            st.markdown(result)
            st.markdown(MEDICAL_SAFETY_DISCLAIMER)
        except Exception as e:
            st.error(f"❌ Error: {e}")
