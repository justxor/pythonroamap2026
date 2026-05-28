"""Тесты для tasks.gather_bounded."""
from __future__ import annotations

import asyncio

import pytest

from async_starter.tasks import gather_bounded, map_bounded


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_gather_bounded_returns_in_order() -> None:
    async def work(i: int) -> int:
        await asyncio.sleep(0.01)
        return i * 2

    res = await gather_bounded((work(i) for i in range(5)), max_concurrency=3)
    assert res == [0, 2, 4, 6, 8]


@pytest.mark.anyio
async def test_map_bounded_timeout() -> None:
    async def slow(_: int) -> int:
        await asyncio.sleep(10)
        return 1

    with pytest.raises(BaseExceptionGroup) as eg:
        await map_bounded(slow, [1, 2, 3], max_concurrency=2, per_task_timeout=0.05)
    assert any(isinstance(e, TimeoutError) for e in eg.value.exceptions)
