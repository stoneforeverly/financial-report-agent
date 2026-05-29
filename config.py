import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")


def get_llm():
    if LLM_PROVIDER == "claude":
        print(f"[llm] provider=claude, model={CLAUDE_MODEL}")
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=CLAUDE_MODEL, api_key=ANTHROPIC_API_KEY)
    print(f"[llm] provider=ollama, model={OLLAMA_MODEL}")
    from langchain_ollama import ChatOllama
    return ChatOllama(model=OLLAMA_MODEL)
