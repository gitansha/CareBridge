import logging
from openai import OpenAI

from config.settings import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class LLMClient:
    """OpenAI client with function calling support."""

    def __init__(self, api_key=None):
        self._client = OpenAI(api_key=api_key or OPENAI_API_KEY)

    def chat(self, messages, model=None, tools=None, temperature=0.1, max_tokens=4096):
        """Send a chat completion request. Returns the raw API response dict."""
        kwargs = {
            "model": model or OPENAI_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self._client.chat.completions.create(**kwargs)
        return response.model_dump()

    def get_response_content(self, api_response):
        """Extract the assistant message content from an API response."""
        return api_response["choices"][0]["message"].get("content", "")

    def get_tool_calls(self, api_response):
        """Extract tool_calls from an API response, or empty list."""
        return api_response["choices"][0]["message"].get("tool_calls", []) or []

    def has_tool_calls(self, api_response):
        return bool(self.get_tool_calls(api_response))


llm_client = LLMClient()
