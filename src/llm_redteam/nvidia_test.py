
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("NVIDIA_BASE_URL")
model = os.getenv("NVIDIA_MODEL")

if not api_key:
    raise RuntimeError("NVIDIA_API_KEY is missing in .env")

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: NVIDIA CONNECTION SUCCESS",
        }
    ],
    temperature=0,
    # Nemotron-3.5-Super is a reasoning model — it consumes tokens for internal
    # chain-of-thought (reasoning_content) before writing the final answer.
    # 50 tokens was exhausted entirely by reasoning, leaving content=None.
    # Use at least 512 to give the model room to reason AND respond.
    max_tokens=512,
)

msg = response.choices[0].message
print("Model   :", model)
print("Thinking:", getattr(msg, "reasoning_content", None))
print("Response:", msg.content)
