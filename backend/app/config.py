from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_ROOT / "data"
DEFAULT_DB_PATH = DATA_DIR / "devguard.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DEVGUARD_", env_file=".env", extra="ignore")

    app_name: str = "DevGuard AI"
    app_version: str = "0.1.0"
    database_url: str = f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]


settings = Settings()
