import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration (supports OpenAI API-compatible endpoints)
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-default-key")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

def get_openai_client():
    """Returns a configured OpenAI client."""
    return OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL
    )

def get_model_name():
    """Returns the model name to use."""
    return LLM_MODEL
