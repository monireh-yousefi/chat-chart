from enum import StrEnum, auto

from pydantic import BaseModel


class LLMMessageRole(StrEnum):
    SYSTEM = auto()
    USER = auto()
    ASSISTANT = auto()


class LLMMessage(BaseModel):
    role: LLMMessageRole
    content: str
