from __future__ import annotations

import os

from autogen_core.models import ChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def build_chat_client() -> ChatCompletionClient:
    """Ollama by default; LiteLLM via OpenAI-compatible proxy when LITELLM_BASE_URL is set."""
    base = os.environ.get("LITELLM_BASE_URL", "").strip()
    if base:
        from autogen_ext.models.openai import OpenAIChatCompletionClient

        model = os.environ.get("LITELLM_MODEL", "ollama/llama3.2")
        api_key = os.environ.get("LITELLM_API_KEY", "litellm")
        return OpenAIChatCompletionClient(model=model, base_url=base, api_key=api_key)
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    # Lower default generation length for faster local inference while preserving output quality.
    options = {
        "num_predict": _int_env("OLLAMA_NUM_PREDICT", 220),
        "temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0.2")),
        "num_ctx": _int_env("OLLAMA_NUM_CTX", 4096),
    }
    return OllamaChatCompletionClient(model=model, host=host, options=options)
