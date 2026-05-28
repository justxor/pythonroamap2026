"""Shared httpx.AsyncClient — HTTP/2, connection pool, timeouts."""
from __future__ import annotations

import httpx

from async_starter.config import get_settings

_client: httpx.AsyncClient | None = None


async def init_http_client() -> None:
    global _client
    s = get_settings()
    limits = httpx.Limits(
        max_connections=s.http_max_connections,
        max_keepalive_connections=s.http_max_connections // 2,
    )
    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(s.http_timeout),
        http2=True,
        limits=limits,
    )


async def close_http_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_http_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("http client not initialized")
    return _client
