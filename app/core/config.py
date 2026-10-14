
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

  model_config = SettingsConfigDict(
    env_file=PROJECT_ROOT / ".env",
    env_file_encoding = "utf-8",
    extra = "ignore",
  )


settings = Settings()
