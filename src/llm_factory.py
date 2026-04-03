from __future__ import annotations

import os

from autogen_core.models import ChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient

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
    return OllamaChatCompletionClient(model=model, host=host)
