"""Тесты для retry.async_retry."""
from __future__ import annotations

import asyncio

import pytest

from async_starter.retry import async_retry


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_retry_succeeds_after_failures() -> None:
    calls = 0

    @async_retry(tries=4, base_delay=0.001, backoff=1.5)
    async def flaky() -> int:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ValueError("nope")
        return 42

    assert await flaky() == 42
    assert calls == 3


@pytest.mark.anyio
async def test_retry_propagates_cancellation() -> None:
    @async_retry(tries=5, base_delay=10.0)
    async def will_cancel() -> None:
        raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError):
        await will_cancel()
