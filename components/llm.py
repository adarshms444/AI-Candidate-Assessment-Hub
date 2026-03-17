import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    if not os.getenv("NVIDIA_API_KEY"):
        raise ValueError("Missing NVIDIA_API_KEY")
    return ChatNVIDIA(
        model="qwen/qwen2.5-coder-32b-instruct",
        temperature=0,
        max_tokens=4096
    )