# app/llm/client.py
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("sk-LwmMKUKyn9YFbINr_z7qJQ"),
    base_url="http://3.110.18.218"
)

def llm_chat(messages, model="gemini-2.5-flash"):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    ).choices[0].message.content
