from enum import StrEnum
from typing import TypedDict

class Intent(StrEnum):
    CHAT = "chat"
    CODE = "code"
    RESEARCH = "research"
    SEO = "seo"
    REASONING = "reasoning"
    VIDEO = "video"
    IMAGE = "image"

class Turn(TypedDict, total=False):
    chat_id: int
    user_id: int
    text: str
    wants_voice: bool
    intent: str
    memories: list[str]
    response: str
    specialist_result: str