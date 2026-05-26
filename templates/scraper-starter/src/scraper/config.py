"""Настройки приложения. Читаются из .env / переменных окружения."""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SCRAPER_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    user_agent: str = Field(default="MyBot/1.0")
    timeout: float = Field(default=15.0, ge=1.0)
    concurrency: int = Field(default=10, ge=1, le=100)
    rate_limit_per_sec: float = Field(default=1.0, ge=0.1)

    max_retries: int = Field(default=5, ge=1, le=20)
    retry_min_wait: float = Field(default=2.0)
    retry_max_wait: float = Field(default=30.0)

    proxy: str | None = None

    out_dir: Path = Field(default=Path("data"))

    log_level: str = Field(default="INFO")
    log_json: bool = Field(default=True)

    respect_robots: bool = Field(default=True)


settings = Settings()
