from collections.abc import Awaitable, Callable
from sara.models import Intent

Specialist = Callable[[str, list[str]], Awaitable[str]]

class SpecialistRegistry:
    def __init__(self) -> None:
        self._handlers: dict[Intent, Specialist] = {}
    def register(self, intent: Intent, handler: Specialist) -> None:
        self._handlers[intent] = handler
    async def execute(self, intent: Intent, text: str, context: list[str]) -> str:
        handler = self._handlers.get(intent)
        return await handler(text, context) if handler else ""

async def default_companion(text: str, context: list[str]) -> str:
    prefix = f"I remember: {context[0]}\n\n" if context else ""
    return f"{prefix}{text}"