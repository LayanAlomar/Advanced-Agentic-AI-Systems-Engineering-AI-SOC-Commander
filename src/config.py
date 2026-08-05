from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    log_path: str = os.getenv("LOG_PATH", "soc_events.jsonl")
    checkpoint_db: str = os.getenv("CHECKPOINT_DB", "soc_checkpoints.sqlite")

settings = Settings()
