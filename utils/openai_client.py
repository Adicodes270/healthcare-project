"""Centralized OpenAI API client for text and image analysis."""
import base64
from io import BytesIO
import os
from types import SimpleNamespace

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIModel:
    """Small adapter exposing a common text result for text and vision calls."""

    def __init__(self, client: OpenAI, model_name: str):
        self.client = client
        self.model_name = model_name

    def generate_content(self, content):
        if isinstance(content, str):
            prompt = content
            message_content = prompt
        else:
            prompt = next((part for part in content if isinstance(part, str)), "")
            message_content = [{"type": "text", "text": prompt}]
            for image in content:
                if isinstance(image, str):
                    continue
                image_buffer = BytesIO()
                image.save(image_buffer, format="PNG")
                encoded_image = base64.b64encode(image_buffer.getvalue()).decode("ascii")
                message_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"},
                    }
                )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": message_content}],
            temperature=0.3,
            max_tokens=4096,
        )
        return SimpleNamespace(text=response.choices[0].message.content or "")


def get_client() -> OpenAI:
    """Initialize and return a configured OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file or the app sidebar.")
    return OpenAI(api_key=api_key)


def get_text_model() -> OpenAIModel:
    """Return the configured OpenAI model for text generation."""
    return OpenAIModel(get_client(), "gpt-4o-mini")


def get_vision_model() -> OpenAIModel:
    """Return the configured OpenAI model for text and image analysis."""
    return OpenAIModel(get_client(), "gpt-4o-mini")


MEDICAL_SAFETY_DISCLAIMER = """
---
> ⚠️ **Medical Disclaimer:** This AI-generated content is for **informational purposes only** and does **not** constitute professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions. In case of emergency, call your local emergency services immediately.
"""