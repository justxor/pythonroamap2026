"""Application configuration via pydantic-settings."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = "local"
    log_level: str = "INFO"

    database_url: str = Field(default="postgresql://user:pass@localhost:5432/app")
    db_pool_min: int = 5
    db_pool_max: int = 20

    http_timeout: float = 10.0
    http_max_connections: int = 100

    max_concurrent_requests: int = 50

    otel_service_name: str = "async-starter"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
