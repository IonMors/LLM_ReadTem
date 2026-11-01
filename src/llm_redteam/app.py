
from fastapi import FastAPI
from pydantic import BaseModel, Field

from llm_redteam.target import generate_response


app = FastAPI(
    title="LLM Red Team POC",
    description="Intentionally vulnerable chatbot for security testing",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = generate_response(request.message)

    return ChatResponse(response=response)
