"""
pages/2_💬_Health_QA_Chatbot.py
Evidence-based health question-answering chatbot with chat history.
"""
import streamlit as st
from utils.gemini_client import get_text_model, MEDICAL_SAFETY_DISCLAIMER

st.set_page_config(page_title="Health Q&A Chatbot | HealthAI", page_icon="💬", layout="wide")

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.chat-bubble-user {
    background: linear-gradient(135deg, #1a3a5c, #2d6a9f);
    border-radius: 18px 18px 4px 18px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
    border: 1px solid rgba(100,180,255,0.3);
    color: #e8f4fd;
}
.chat-bubble-ai {
    background: linear-gradient(135deg, #0d2137, #1a3a5c);
    border-radius: 18px 18px 18px 4px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0;
    max-width: 85%;
    border: 1px solid rgba(100,255,180,0.2);
    color: #e8f4fd;
}
.quick-chip {
    display: inline-block;
    background: rgba(100,200,255,0.1);
    border: 1px solid rgba(100,200,255,0.4);
    border-radius: 20px;
    padding: 0.3rem 0.85rem;
    margin: 0.2rem;
    cursor: pointer;
    font-size: 0.82rem;
    color: #64c8ff;
    transition: all 0.2s;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 💬 Health Q&A Chatbot")
st.markdown("Ask any **health-related question** and get clear, evidence-based answers powered by Gemini AI.")

# ─── Sidebar Config ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    response_style = st.selectbox(
        "Response style",
        ["Comprehensive (detailed)", "Concise (brief bullets)", "Empathetic & supportive"],
        index=0,
    )
    include_sources = st.toggle("Suggest reliable sources", value=True)
    st.divider()
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are HealthAI, an empathetic, knowledgeable, and ethical medical AI assistant.

Your role:
- Answer health and medical questions clearly, accurately, and compassionately
- Translate complex medical concepts into plain, understandable language
- Always encourage users to consult healthcare professionals for personal medical decisions
- Never diagnose conditions definitively — provide information and guidance only
- Flag urgent/emergency situations clearly and direct users to seek immediate care
- Cite evidence-based sources when relevant (WHO, NHS, Mayo Clinic, CDC, PubMed)
- Be warm, non-judgmental, and supportive

You must NEVER:
- Prescribe medications or dosages for individual cases
- Replace professional medical consultation
- Provide information that could be harmful if misapplied
"""

# ─── Chat History ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None

# Quick-start questions
if not st.session_state.chat_history:
    st.markdown("#### 💡 Quick questions to get started:")
    quick_questions = [
        "What does a high HbA1c level mean?",
        "How can I lower my blood pressure naturally?",
        "What are early signs of vitamin D deficiency?",
        "Is it normal to feel anxious before surgery?",
        "What does a cholesterol panel test measure?",
        "How does diabetes affect the kidneys?",
    ]
    cols = st.columns(3)
    for i, q in enumerate(quick_questions):
        if cols[i % 3].button(q, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

# ─── Handle Input ─────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask your health question…")

# Handle quick-start buttons
if "pending_question" in st.session_state:
    user_input = st.session_state.pop("pending_question")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    style_instruction = {
        "Comprehensive (detailed)": "Provide a thorough, well-structured response with sections and detail.",
        "Concise (brief bullets)": "Keep your response concise. Use bullet points. Maximum 5–6 lines.",
        "Empathetic & supportive": "Respond with warmth and emotional support alongside medical information.",
    }[response_style]

    sources_instruction = "At the end, suggest 2–3 reliable sources (WHO, NHS, Mayo Clinic, CDC, PubMed links)." if include_sources else ""

    full_prompt = f"""{SYSTEM_PROMPT}

Style instruction: {style_instruction}
{sources_instruction}

User question: {user_input}
"""

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking…"):
            try:
                model = get_text_model()
                response = model.generate_content(full_prompt)
                answer = response.text
                st.markdown(answer)
                st.caption("⚠️ For informational purposes only — always consult a qualified healthcare provider.")
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                err_msg = f"❌ Error: {e}"
                st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
