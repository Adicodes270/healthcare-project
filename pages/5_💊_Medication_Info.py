"""
pages/5_💊_Medication_Info.py
AI-powered medication information and drug interaction checker.
"""
import streamlit as st
from utils.gemini_client import get_text_model, MEDICAL_SAFETY_DISCLAIMER

st.set_page_config(page_title="Medication Info | HealthAI", page_icon="💊", layout="wide")

st.markdown("""
<style>
.med-card {
    background: linear-gradient(135deg, #0a1628, #162040);
    border: 1px solid rgba(100,200,255,0.2);
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.5rem 0;
}
.interaction-warning {
    background: linear-gradient(135deg, #3a1500, #7a3000);
    border: 1px solid #ff6600;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.interaction-safe {
    background: linear-gradient(135deg, #0a2a00, #1a4a00);
    border: 1px solid #44bb44;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 💊 Medication Information & Interaction Checker")
st.markdown("Look up **detailed medication information** or check for **potential drug interactions** between multiple medicines.")

tab1, tab2 = st.tabs(["📖 Medication Lookup", "⚠️ Drug Interaction Checker"])

# ─── Tab 1: Medication Lookup ─────────────────────────────────────────────────
with tab1:
    st.markdown("### 🔍 Search for a Medication")
    med_name = st.text_input(
        "Medication name (brand or generic)",
        placeholder="e.g. Metformin, Lisinopril, Amoxicillin, Paracetamol…",
    )
    patient_age_group = st.selectbox(
        "Patient age group (for dosage context)",
        ["Adult (18–64 yrs)", "Elderly (65+)", "Paediatric (2–12 yrs)", "Adolescent (13–17 yrs)", "Infant (<2 yrs)"],
    )

    if st.button("📋 Get Medication Info", type="primary", use_container_width=True, key="med_lookup"):
        if not med_name.strip():
            st.warning("Please enter a medication name.")
            st.stop()

        prompt = f"""You are a clinical pharmacist AI. Provide comprehensive information about the medication: "{med_name}"
Patient age group context: {patient_age_group}

Structure your response as:

## 💊 {med_name.title()} — Drug Information Sheet

### 🧬 Drug Class & Mechanism
What class of drug this is and how it works in the body (plain language).

### ✅ Approved Uses (Indications)
What conditions it is prescribed for.

### 📏 Typical Dosage
Standard dosing for {patient_age_group}. State that individual dosing must be determined by a doctor.

### ⚠️ Common Side Effects
List the most frequently reported side effects (bullet points).

### 🚨 Serious/Rare Side Effects
Side effects requiring immediate medical attention.

### 🚫 Contraindications
Who should NOT take this medication.

### 💊 Drug Interactions
Most important known drug interactions to be aware of.

### 🍎 Food & Lifestyle Interactions
Foods, alcohol, or activities to avoid.

### 💡 Patient Tips
Practical advice for taking this medication correctly.

Keep language clear and accessible. Emphasise that dosing/treatment decisions must involve a healthcare professional.
"""
        with st.spinner(f"🔍 Looking up {med_name}…"):
            try:
                model = get_text_model()
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.markdown(MEDICAL_SAFETY_DISCLAIMER)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ─── Tab 2: Drug Interaction Checker ─────────────────────────────────────────
with tab2:
    st.markdown("### ⚠️ Check Drug Interactions")
    st.info("Enter up to 5 medications to check for known interactions between them.")

    meds = []
    cols = st.columns(2)
    for i in range(5):
        m = cols[i % 2].text_input(f"Medication {i+1}", placeholder=f"e.g. {'Aspirin' if i==0 else 'Warfarin' if i==1 else ''}…", key=f"drug_{i}")
        if m.strip():
            meds.append(m.strip())

    if st.button("🔬 Check Interactions", type="primary", use_container_width=True, key="interaction_check"):
        if len(meds) < 2:
            st.warning("⚠️ Please enter at least 2 medications to check interactions.")
            st.stop()

        meds_str = ", ".join(meds)
        prompt = f"""You are a clinical pharmacist AI expert. Analyse drug interactions for the following medications: {meds_str}

Structure your response as:

## ⚠️ Drug Interaction Report: {meds_str}

### 📊 Interaction Summary Table
For each pair of medications, rate the interaction:
🔴 CONTRAINDICATED | 🟠 MAJOR | 🟡 MODERATE | 🟢 MINOR | ⚪ NO KNOWN INTERACTION

### 🔍 Detailed Interaction Analysis
For each significant interaction found (moderate or above):
- **Drugs involved**: 
- **Severity**: 
- **Mechanism**: (how they interact)
- **Clinical effect**: (what can happen to the patient)
- **Management**: (what to do — avoid, monitor, dose adjust, etc.)

### ✅ Safe Combinations
List any pairs with no significant interactions.

### 👨‍⚕️ Clinical Recommendation
Overall assessment and recommendation.

Be precise and clinically conservative. Flag uncertainty when interaction data is limited.
"""
        with st.spinner("🔬 Checking drug interactions…"):
            try:
                model = get_text_model()
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.markdown(MEDICAL_SAFETY_DISCLAIMER)
            except Exception as e:
                st.error(f"❌ Error: {e}")
