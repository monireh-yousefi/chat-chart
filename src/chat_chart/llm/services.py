from abc import ABC, abstractmethod

from openai import AsyncClient

from chat_chart.llm.entities import LLMMessage


class LLMService(ABC):
    @abstractmethod
    async def query(self, messages: list[LLMMessage]) -> str:
        pass


class OpenAILLMService(LLMService):
    def __init__(
            self,
            api_key: str,
            model_name: str,
    ):
        self._model_name = model_name

        self._client = AsyncClient(
            api_key=api_key,
        )

    async def query(self, messages: list[LLMMessage]) -> str:
        response = await self._client.chat.completions.create(
            model=self._model_name,
            messages=[message.model_dump() for message in messages],
        )
        return response.choices[0].message.content
