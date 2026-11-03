from typing import Protocol

from app.services.llm.schemas import (
    LLMMessage,
    LLMResponse,
)


class LLMProvider(Protocol):
    async def generate(
        self,
        messages: list[LLMMessage],
        tools: list[dict] | None = None,
        response_schema: dict | None = None,
    ) -> LLMResponse: ...
