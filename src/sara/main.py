import asyncio
import logging
import structlog
from sara.agents.registry import SpecialistRegistry, default_companion
from sara.config import Settings
from sara.graph import build_graph
from sara.memory import MemoryStore
from sara.models import Intent
from sara.transport.telegram import build_telegram_app

async def create_app():
    settings = Settings()
    if not settings.telegram_token:
        raise RuntimeError("SARA_TELEGRAM_TOKEN is required. Copy .env.example to .env and configure it.")
    settings.database_url.parent.mkdir(parents=True, exist_ok=True)
    memory = MemoryStore(str(settings.database_url))
    await memory.initialize()
    specialists = SpecialistRegistry()
    specialists.register(Intent.CHAT, default_companion)
    return build_telegram_app(settings.telegram_token, build_graph(memory, specialists))

def run() -> None:
    logging.basicConfig(level=Settings().log_level)
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))
    asyncio.run(create_app()).run_polling(allowed_updates=["message"])