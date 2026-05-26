"""Pydantic-модели для строгой валидации спарсенных данных."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PageResult(BaseModel):
    """Одна спарсенная страница."""
    model_config = ConfigDict(str_strip_whitespace=True)

    url: HttpUrl
    title: str | None = Field(default=None, max_length=500)
    status_code: int = Field(ge=100, le=599)
    html_length: int = Field(ge=0)
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    error: str | None = None
