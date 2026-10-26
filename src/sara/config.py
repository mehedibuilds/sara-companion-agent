from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SARA_", extra="ignore")
    telegram_token: str = ""
    database_url: Path = Path("data/sara.sqlite3")
    groq_api_key: str = ""
    groq_transcription_model: str = "whisper-large-v3-turbo"
    edge_tts_voice: str = "en-US-JennyNeural"
    log_level: str = "INFO"