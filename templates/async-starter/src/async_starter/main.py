"""FastAPI entrypoint with lifespan, structured concurrency и graceful shutdown."""
from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator

import structlog
from fastapi import FastAPI

from async_starter.config import get_settings
from async_starter.db import close_pool, init_pool
from async_starter.http_client import close_http_client, init_http_client
from async_starter.logging_setup import configure_logging

log = structlog.get_logger()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    log.info("startup", env=settings.app_env)

    try:
        with contextlib.suppress(ImportError):
            import uvloop  # type: ignore[import-untyped]

            uvloop.install()
    except Exception as exc:  # pragma: no cover
        log.warning("uvloop_unavailable", error=str(exc))

    await init_pool()
    await init_http_client()

    try:
        yield
    finally:
        log.info("shutdown")
        with contextlib.suppress(Exception):
            await close_http_client()
        with contextlib.suppress(Exception):
            await close_pool()


app = FastAPI(lifespan=lifespan, default_response_class=None)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/fanout")
async def fanout(n: int = 10) -> dict[str, int]:
    """Пример structured concurrency в эндпоинте."""
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(asyncio.sleep(0.01, result=i)) for i in range(n)]
    return {"sum": sum(t.result() for t in tasks)}
