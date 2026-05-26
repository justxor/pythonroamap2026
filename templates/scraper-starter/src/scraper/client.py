"""HTTP-клиент с retry, rate-limit, прокси и HTTP/2."""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from aiolimiter import AsyncLimiter
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .config import settings
from .logging_setup import log


@asynccontextmanager
async def make_client() -> AsyncIterator[httpx.AsyncClient]:
    """Контекстный менеджер с готовым HTTP-клиентом."""
    headers = {"User-Agent": settings.user_agent}
    kwargs: dict[str, object] = {
        "http2": True,
        "timeout": settings.timeout,
        "follow_redirects": True,
        "headers": headers,
    }
    if settings.proxy:
        kwargs["proxy"] = settings.proxy

    async with httpx.AsyncClient(**kwargs) as client:  # type: ignore[arg-type]
        yield client


class RateLimitedFetcher:
    """Обёртка с rate-limit и retry вокруг httpx.AsyncClient."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self._limiter = AsyncLimiter(settings.rate_limit_per_sec, 1.0)

    async def get(self, url: str) -> httpx.Response:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(settings.max_retries),
            wait=wait_exponential(
                multiplier=1,
                min=settings.retry_min_wait,
                max=settings.retry_max_wait,
            ),
            retry=retry_if_exception_type(
                (httpx.TimeoutException, httpx.HTTPStatusError, httpx.TransportError),
            ),
            reraise=True,
        ):
            with attempt:
                async with self._limiter:
                    log.debug("http.fetch", url=url, attempt=attempt.retry_state.attempt_number)
                    response = await self._client.get(url)
                    response.raise_for_status()
                    return response
        msg = "unreachable"
        raise RuntimeError(msg)
