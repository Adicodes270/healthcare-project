# HealthAI — Generative AI Healthcare Assistant

A comprehensive, ethical AI-powered healthcare application built with **Python**, **Streamlit**, and **OpenAI GPT-4o mini**.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📋 **Report Summariser** | Upload PDF medical reports → plain-English summary |
| 💬 **Health Q&A Chatbot** | Evidence-based health Q&A with chat history |
| 🔬 **Symptom Checker** | AI triage assessment with urgency classification |
| 🖼️ **Image Analyser** | OpenAI vision analysis of X-rays, skin images, MRIs |
| 💊 **Medication Info** | Drug lookup + drug interaction checker |

---

## 🛠️ Setup & Installation

### 1. Clone / open the project folder

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key
Edit the `.env` file:
```
OPENAI_API_KEY=your_actual_key_here
```
Or paste it directly in the **sidebar** when the app is running.

> **Create an API key:** https://platform.openai.com/api-keys. API usage may incur charges.

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📁 Project Structure

```
Healthcare AI project/
├── app.py                          # Main landing page
├── requirements.txt
├── .env                            # API key (not committed)
├── .streamlit/
│   └── config.toml                 # Streamlit theme
├── pages/
│   ├── 1_📋_Report_Summariser.py
│   ├── 2_💬_Health_QA_Chatbot.py
│   ├── 3_🔬_Symptom_Checker.py
│   ├── 4_🖼️_Image_Analyser.py
│   └── 5_💊_Medication_Info.py
└── utils/
    ├── openai_client.py             # OpenAI API configuration
    └── pdf_reader.py               # PDF text extraction
```

---

## 🛡️ Ethical AI Principles

- **Zero data storage** — All inputs processed in-memory, nothing persisted
- **Non-diagnostic framing** — AI provides information, never a diagnosis
- **Transparent sourcing** — Chatbot suggests evidence-based sources
- **Emergency escalation** — Urgent symptoms always flagged with emergency guidance
- **Medical disclaimer** — Every AI output includes a clear disclaimer
- **User-controlled API** — Users own their API key, no third-party data sharing

---

## ⚠️ Disclaimer

This application is for **informational purposes only**. It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions.
