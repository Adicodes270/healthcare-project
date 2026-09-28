"""
app.py — Main entry point for HealthAI
 A Generative AI-based healthcare application powered by OpenAI.
"""
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthAI — Generative AI Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "HealthAI: An ethical Generative AI healthcare assistant powered by OpenAI.",
    },
)

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Global resets */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background override */
.stApp {
    background: linear-gradient(135deg, #050d1a 0%, #0a1628 40%, #0d1f3a 70%, #061020 100%);
    min-height: 100vh;
}

/* Hide default Streamlit header decorations */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Hero section ── */
.hero-container {
    text-align: center;
    padding: 3rem 1rem 2rem 1rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, rgba(100,200,255,0.15), rgba(100,255,200,0.15));
    border: 1px solid rgba(100,200,255,0.4);
    border-radius: 30px;
    padding: 0.4rem 1.2rem;
    font-size: 0.82rem;
    color: #64c8ff;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #64c8ff 40%, #00e5a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 1.2rem;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: rgba(200,220,240,0.75);
    max-width: 660px;
    margin: 0 auto 2.5rem auto;
    line-height: 1.7;
    font-weight: 400;
}

/* ── Feature cards ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.2rem;
    padding: 0.5rem 0;
}
.feature-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(100,200,255,0.03));
    border: 1px solid rgba(100,200,255,0.15);
    border-radius: 20px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: default;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #64c8ff, transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(100,200,255,0.12);
    border-color: rgba(100,200,255,0.35);
}
.feature-card:hover::before { opacity: 1; }

.feature-icon {
    font-size: 2.6rem;
    margin-bottom: 1rem;
    display: block;
}
.feature-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e8f4fd;
    margin-bottom: 0.5rem;
}
.feature-desc {
    font-size: 0.85rem;
    color: rgba(180,210,235,0.65);
    line-height: 1.55;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 2.5rem 0;
}
.stat-box {
    text-align: center;
    padding: 1.2rem 2rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(100,200,255,0.15);
    border-radius: 16px;
    min-width: 140px;
}
.stat-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #64c8ff;
}
.stat-label {
    font-size: 0.78rem;
    color: rgba(180,210,235,0.6);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}

/* ── Ethics banner ── */
.ethics-banner {
    background: linear-gradient(135deg, rgba(0,229,160,0.08), rgba(100,200,255,0.08));
    border: 1px solid rgba(0,229,160,0.25);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
}
.ethics-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #00e5a0;
    margin-bottom: 1rem;
}
.ethics-pill {
    display: inline-block;
    background: rgba(0,229,160,0.12);
    border: 1px solid rgba(0,229,160,0.3);
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    margin: 0.25rem;
    font-size: 0.82rem;
    color: #00e5a0;
}

/* ── API Key config box ── */
.api-config-box {
    background: linear-gradient(135deg, rgba(255,165,0,0.08), rgba(255,100,0,0.05));
    border: 1px solid rgba(255,165,0,0.3);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050d1a 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(100,200,255,0.1);
}
section[data-testid="stSidebar"] .stMarkdown {
    color: rgba(200,220,240,0.85);
}

/* Animated pulse dot */
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.85); }
}
.pulse-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #00e5a0;
    border-radius: 50%;
    animation: pulse 2s infinite;
    margin-right: 6px;
    vertical-align: middle;
}

/* Divider glow */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(100,200,255,0.4), transparent);
    border: none;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size: 3rem;'>🏥</div>
        <div style='font-family: Space Grotesk, sans-serif; font-size: 1.4rem; font-weight: 700;
                    background: linear-gradient(135deg, #64c8ff, #00e5a0);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            HealthAI
        </div>
        <div style='font-size: 0.75rem; color: rgba(180,210,235,0.5); letter-spacing: 1px; text-transform: uppercase;'>
            Powered by OpenAI
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    Use the **pages** in the sidebar to navigate:
    
    📋 **Report Summariser** — Upload PDF medical reports  
    💬 **Health Q&A** — Ask any health question  
    🔬 **Symptom Checker** — AI triage assessment  
    🖼️ **Image Analyser** — Analyse medical images  
    💊 **Medication Info** — Drug info & interactions  
    """)

    st.divider()

    # API Key configuration
    st.markdown("### 🔑 API Configuration")
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-…",
        help="Create an API key at: https://platform.openai.com/api-keys",
        value=os.getenv("OPENAI_API_KEY", ""),
    )
    if api_key_input and api_key_input != "your_openai_api_key_here":
        os.environ["OPENAI_API_KEY"] = api_key_input
        st.success("✅ API key set for this session")
    elif not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        st.warning("⚠️ Add your OpenAI API key to use AI features")

    st.divider()
    st.markdown("""
    <div style='font-size: 0.75rem; color: rgba(180,210,235,0.4); text-align: center; line-height: 1.6;'>
        <span class='pulse-dot'></span>OpenAI GPT-4o mini<br>
        Built with Streamlit & Python<br><br>
        ⚠️ For informational use only.<br>Not a substitute for medical advice.
    </div>
    """, unsafe_allow_html=True)

# ─── Hero Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-container'>
    <div class='hero-badge'>✦ Generative AI · Healthcare · OpenAI</div>
    <h1 class='hero-title'>AI-Powered Healthcare<br>Made Human-Centred</h1>
    <p class='hero-subtitle'>
        Transform complex medical information into clear, actionable insights.
        Understand your reports, check symptoms, analyse images, and get
        evidence-based health answers — all with ethical AI at the core.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Stats Row ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='stats-row'>
    <div class='stat-box'>
        <div class='stat-number'>5</div>
        <div class='stat-label'>AI Modules</div>
    </div>
    <div class='stat-box'>
        <div class='stat-number'>OpenAI</div>
        <div class='stat-label'>GPT-4o mini</div>
    </div>
    <div class='stat-box'>
        <div class='stat-number'>0</div>
        <div class='stat-label'>Data Stored</div>
    </div>
    <div class='stat-box'>
        <div class='stat-number'>100%</div>
        <div class='stat-label'>Privacy First</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)

# ─── Feature Cards ────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; margin-bottom: 1.5rem;'>
    <h2 style='font-family: Space Grotesk, sans-serif; color: #e8f4fd; font-size: 1.8rem; font-weight: 700;'>
        What HealthAI Can Do For You
    </h2>
    <p style='color: rgba(180,210,235,0.6); font-size: 0.95rem;'>Five powerful AI tools, one unified platform</p>
</div>

<div class='feature-grid'>
    <div class='feature-card'>
        <span class='feature-icon'>📋</span>
        <div class='feature-title'>Report Summariser</div>
        <div class='feature-desc'>Upload PDF lab reports, clinical notes, or discharge summaries and receive a plain-English summary with key findings highlighted.</div>
    </div>
    <div class='feature-card'>
        <span class='feature-icon'>💬</span>
        <div class='feature-title'>Health Q&A Chatbot</div>
        <div class='feature-desc'>Ask any health-related question and receive accurate, evidence-based answers with suggested reliable sources.</div>
    </div>
    <div class='feature-card'>
        <span class='feature-icon'>🔬</span>
        <div class='feature-title'>Symptom Checker</div>
        <div class='feature-desc'>Describe your symptoms for an AI-powered triage assessment — from mild monitoring to urgent emergency guidance.</div>
    </div>
    <div class='feature-card'>
        <span class='feature-icon'>🖼️</span>
        <div class='feature-title'>Image Analyser</div>
        <div class='feature-desc'>Upload X-rays, skin photos, MRI scans or other medical images for structured visual analysis using OpenAI's multimodal AI.</div>
    </div>
    <div class='feature-card'>
        <span class='feature-icon'>💊</span>
        <div class='feature-title'>Medication Info</div>
        <div class='feature-desc'>Look up any medication or check for drug interactions between multiple medicines — with clinical-grade detail.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)

# ─── Ethical AI Section ───────────────────────────────────────────────────────
st.markdown("""
<div class='ethics-banner'>
    <div class='ethics-title'>🛡️ Built on Ethical AI Principles</div>
    <p style='color: rgba(200,235,220,0.75); font-size: 0.9rem; margin-bottom: 1rem;'>
        HealthAI is designed with responsible AI at its foundation — not as an afterthought.
    </p>
    <span class='ethics-pill'>🔒 Zero data storage</span>
    <span class='ethics-pill'>🌐 Transparent sourcing</span>
    <span class='ethics-pill'>⚖️ Non-diagnostic framing</span>
    <span class='ethics-pill'>🔑 User-controlled API key</span>
    <span class='ethics-pill'>🩺 Always refer to professionals</span>
    <span class='ethics-pill'>🚨 Emergency escalation built-in</span>
    <span class='ethics-pill'>✅ Factual accuracy priority</span>
    <span class='ethics-pill'>🤝 Human-centred design</span>
</div>
""", unsafe_allow_html=True)

# ─── Quick-start CTA ─────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <div style='color: rgba(180,210,235,0.55); font-size: 0.9rem;'>
        👈 Use the sidebar to navigate to any feature and get started
    </div>
</div>
""", unsafe_allow_html=True)

# ─── API Key Check Banner ─────────────────────────────────────────────────────
api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key or api_key == "your_openai_api_key_here":
    st.markdown("""
    <div class='api-config-box'>
        <b>🔑 Getting Started — Set Your OpenAI API Key</b><br><br>
        To use any AI feature, enter your <b>OpenAI API key</b> in the sidebar.<br><br>
        <ol style='color: rgba(220,200,180,0.85); margin: 0; padding-left: 1.2rem;'>
            <li>Visit <a href='https://platform.openai.com/api-keys' target='_blank' style='color: #64c8ff;'>platform.openai.com/api-keys</a></li>
            <li>Sign in to your OpenAI account and create an API key</li>
            <li>Paste the key in the <b>API Configuration</b> section in the sidebar</li>
            <li>Navigate to any feature page and start exploring!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
