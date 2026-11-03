import logging

from fastapi import FastAPI, HTTPException
from openai import OpenAIError

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm.schemas import LLMResponse
from app.services.llm.service import generate_response

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="SupportOps AI",
    description="Multi-agent AI Customer Support Platform",
)


@app.get("/")
async def root():
    return {"message": "Welcome to SupportOps AI", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        llm_response: LLMResponse = await generate_response(request.message)

        return ChatResponse(
            reply=llm_response.text,
            model=llm_response.model,
            provider=llm_response.provider,
        )

    except ValueError as exc:
        logger.error(
            "LLM configuration error: %s",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="LLM provider is not configured",
        ) from exc

    except OpenAIError:
        logger.exception("OpenAI API request failed")

        raise HTTPException(
            status_code=502,
            detail="LLM provider request failed",
        )
