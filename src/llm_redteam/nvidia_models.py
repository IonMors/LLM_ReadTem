
import os
import json

from dotenv import load_dotenv
from deepeval.models import DeepEvalBaseLLM
from deepeval.metrics.utils import trimAndLoadJson
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel


load_dotenv()

# Nemotron-3.5-Super is a reasoning model: it spends tokens on internal
# chain-of-thought (reasoning_content) BEFORE writing content.
# DeepTeam sends long structured prompts, so we need a large token budget.
_MAX_TOKENS = 8192


class NvidiaModel(DeepEvalBaseLLM):
    """
    NVIDIA-hosted model adapter for DeepTeam.
    Implements the DeepEvalBaseLLM interface.
    """

    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("NVIDIA_MODEL")

        nvidia_config = dict(
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url=os.getenv(
                "NVIDIA_BASE_URL",
                "https://integrate.api.nvidia.com/v1",
            ),
        )

        # Synchronous client for generate()
        self.client = OpenAI(**nvidia_config)

        # Async client for a_generate() — OpenAI client is NOT awaitable
        self.async_client = AsyncOpenAI(**nvidia_config)

    def load_model(self):
        return self.client

    def _extract_content(self, response) -> str:
        """
        Extract text from the API response.

        Nemotron-3.5-Super is a reasoning model — its final answer lives in
        `content`, while internal thinking lives in `reasoning_content`.
        If `content` is None the model ran out of tokens before writing its
        answer; raise so callers can handle / retry.
        """
        msg = response.choices[0].message
        content = msg.content

        if not content:
            thinking = getattr(msg, "reasoning_content", None) or ""
            raise ValueError(
                f"Model returned empty content (finish_reason="
                f"{response.choices[0].finish_reason!r}). "
                f"The reasoning trace consumed all tokens. "
                f"Increase max_tokens. Thinking preview: {thinking[:200]!r}"
            )

        return content.strip()

    def _parse_with_schema(self, text: str, schema: type | None):
        """
        If a Pydantic schema is provided, parse the JSON text and return a
        schema instance. DeepTeam checks isinstance(res, schema) to decide
        whether to use the object directly or call trimAndLoadJson on it.
        Returning the right type avoids the 'str has no attribute .data' error.
        """
        if schema is None:
            return text

        data = trimAndLoadJson(text)
        return schema(**data)

    def generate(self, prompt: str, schema: type | None = None, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=_MAX_TOKENS,
        )
        text = self._extract_content(response)
        return self._parse_with_schema(text, schema)

    async def a_generate(self, prompt: str, schema: type | None = None, **kwargs) -> str:
        # Use AsyncOpenAI so .create() returns a coroutine that can be awaited
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=_MAX_TOKENS,
        )
        text = self._extract_content(response)
        return self._parse_with_schema(text, schema)

    def get_model_name(self) -> str:
        return self.model
