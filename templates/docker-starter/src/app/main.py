"""FastAPI demo сервис с healthcheck и graceful shutdown."""
from __future__ import annotations

import contextlib
import os
from collections.abc import AsyncIterator

import structlog
from fastapi import FastAPI

log = structlog.get_logger()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    log.info("startup", env=os.getenv("APP_ENV", "local"))
    yield
    log.info("shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/")
async def index() -> dict[str, str]:
    return {"app": "docker-starter", "version": "0.1.0"}
