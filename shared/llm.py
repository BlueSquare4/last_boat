import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Spike AI LiteLLM Proxy Configuration
LITELLM_BASE_URL = "http://3.110.18.218"
# The key should be in .env or passed via environment variable
API_KEY = os.getenv("LITELLM_API_KEY", "sk-fake-key-for-now") 

def get_openai_client():
    """Returns a configured OpenAI client for the LiteLLM proxy."""
    return OpenAI(
        api_key=API_KEY,
        base_url=LITELLM_BASE_URL
    )

def get_model_name():
    """Returns the default model to use."""
    return "gemini-1.5-pro"
