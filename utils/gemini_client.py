"""
utils/gemini_client.py
Centralised Gemini API client with safety settings and error handling.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_client():
    """Initialise and return a configured Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("❌ GEMINI_API_KEY is not set. Please add it to your .env file.")
    genai.configure(api_key=api_key)
    return genai


def get_text_model():
    """Return Gemini 3.8 Flash model for text generation."""
    get_client()
    return genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            top_p=0.9,
            max_output_tokens=4096,
        ),
    )


def get_vision_model():
    """Return Gemini 3.8 Flash model for multimodal (vision) tasks."""
    get_client()
    return genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            top_p=0.9,
            max_output_tokens=4096,
        ),
    )


MEDICAL_SAFETY_DISCLAIMER = """
---
> ⚠️ **Medical Disclaimer:** This AI-generated content is for **informational purposes only** and does **not** constitute professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions. In case of emergency, call your local emergency services immediately.
"""
