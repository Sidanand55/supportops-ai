from functools import lru_cache

from openai import AsyncOpenAI

from app.core.config import settings
from app.services.llm.schemas import LLMMessage, LLMResponse


@lru_cache
def get_openai_client() -> AsyncOpenAI:

    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured")

    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=30.0, max_retries=2)


class OpenAIProvider:
    provider_name = "openai"

    async def generate(
        self,
        messages: list[LLMMessage] | None = None,
        tools: list[dict] | None = None,
        response_schema: dict | None = None,
    ) -> LLMResponse:

        client = get_openai_client()

        instructions = "\n".join(
            message.content
            for message in messages
            if message.role in ("system", "developer")
        )

        input_messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
            if message.role not in ("system", "developer")
        ]

        request = {
            "model": settings.OPENAI_MODEL,
            "instructions": instructions,
            "input": input_messages,
        }

        if tools:
            request["tools"] = tools

        if response_schema:
            request["text"] = {"format": response_schema}

        response = await client.responses.create(**request)

        usage = response.usage

        return LLMResponse(
            text=response.output_text,
            provider=self.provider_name,
            model=settings.OPENAI_MODEL,
            input_tokens=(usage.input_tokens if usage else None),
            output_tokens=(usage.output_tokens if usage else None),
        )
