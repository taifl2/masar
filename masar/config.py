import os
from langchain_openai import ChatOpenAI

MODEL_NAME = "openai/gpt-oss-120b"
BASE_URL = "https://api.groq.com/openai/v1"


def get_llm(temperature: float = 0) -> ChatOpenAI:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")
    return ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=api_key,
        temperature=temperature,
    )
