from functools import lru_cache

from openai import AsyncOpenAI

from app.core.config import settings


@lru_cache
def get_openai_client() -> AsyncOpenAI:

    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured")

    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=30.0, max_retries=2)
