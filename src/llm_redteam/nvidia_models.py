
import os

from dotenv import load_dotenv
from deepeval.metrics.utils import trimAndLoadJson
from deepeval.models import DeepEvalBaseLLM
from openai import AsyncOpenAI, OpenAI

load_dotenv()

_MAX_TOKENS = 8192


class NvidiaModel(DeepEvalBaseLLM):
    # Adapter that lets DeepEval/DeepTeam call an NVIDIA-hosted model
    # through the OpenAI-compatible API.

    def __init__(self, model: str | None = None):
        # An explicitly supplied model name takes priority over .env settings.
        self.model = model or os.getenv("NVIDIA_MODEL")

        # NVIDIA's endpoint exposes an OpenAI-compatible chat-completions API.
        self.client = OpenAI(
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url=os.getenv(
                "NVIDIA_BASE_URL",
                "https://integrate.api.nvidia.com/v1",
            ),
        )
        # DeepTeam can execute model calls asynchronously, so use a separate
        # async client instead of awaiting the synchronous OpenAI client.
        self.async_client = AsyncOpenAI(
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url=os.getenv(
                "NVIDIA_BASE_URL",
                "https://integrate.api.nvidia.com/v1",
            ),
        )

    def load_model(self):
        # DeepEval uses this hook to access the underlying client object.
        return self.client

    def _extract_content(self, response) -> str:
        content = response.choices[0].message.content
        if not content:
            raise ValueError("The NVIDIA model returned no final content")
        return content.strip()

    def _parse_with_schema(self, text: str, schema: type | None):
        # DeepTeam passes Pydantic schemas for structured attack generation.
        if schema is None:
            return text
        return schema(**trimAndLoadJson(text))

    def _request_options(self, schema: type | None) -> dict:
        # JSON mode alone only guarantees valid JSON; it does not guarantee
        # required fields such as SyntheticDataList.data or ReasonScore.score.
        if schema is not None:
            return {
                "reasoning_effort": "none",
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema.__name__,
                        "strict": True,
                        "schema": schema.model_json_schema(),
                    },
                },
            }
        return {}

    def generate(self, prompt: str, schema: type | None = None, **kwargs):
        # Synchronous generation for callers that do not use async workflows.
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            # Increase this if the model's reasoning consumes the full budget
            # before it writes its final answer.
            max_tokens=_MAX_TOKENS,
            **self._request_options(schema),
        )

        return self._parse_with_schema(self._extract_content(response), schema)

    async def a_generate(self, prompt: str, schema: type | None = None, **kwargs):
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=_MAX_TOKENS,
            **self._request_options(schema),
        )

        return self._parse_with_schema(self._extract_content(response), schema)

    def get_model_name(self) -> str:
        # DeepEval uses this name in logs and evaluation output.
        return self.model
