"""Structured concurrency patterns: TaskGroup + Semaphore + timeout."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def gather_bounded(
    coros: Iterable[Awaitable[R]],
    *,
    max_concurrency: int,
    per_task_timeout: float | None = None,
) -> list[R]:
    """Параллельный gather с ограничением и таймаутом на задачу.

    Падение любой задачи отменяет все остальные через TaskGroup.
    """
    sem = asyncio.Semaphore(max_concurrency)

    async def runner(coro: Awaitable[R]) -> R:
        async with sem:
            if per_task_timeout is None:
                return await coro
            async with asyncio.timeout(per_task_timeout):
                return await coro

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(runner(c)) for c in coros]
    return [t.result() for t in tasks]


async def map_bounded(
    fn: Callable[[T], Awaitable[R]],
    items: Iterable[T],
    *,
    max_concurrency: int,
    per_task_timeout: float | None = None,
) -> list[R]:
    return await gather_bounded(
        (fn(x) for x in items),
        max_concurrency=max_concurrency,
        per_task_timeout=per_task_timeout,
    )
