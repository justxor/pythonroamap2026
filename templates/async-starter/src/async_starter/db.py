"""Asyncpg connection pool management."""
from __future__ import annotations

from typing import TYPE_CHECKING

import asyncpg

from async_starter.config import get_settings

if TYPE_CHECKING:
    from asyncpg.pool import Pool

_pool: "Pool | None" = None


async def init_pool() -> None:
    global _pool
    s = get_settings()
    _pool = await asyncpg.create_pool(
        dsn=s.database_url,
        min_size=s.db_pool_min,
        max_size=s.db_pool_max,
        command_timeout=s.http_timeout,
    )


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> "Pool":
    if _pool is None:
        raise RuntimeError("db pool not initialized")
    return _pool
