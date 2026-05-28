"""@async_retry декоратор с exponential backoff и jitter."""
from __future__ import annotations

import asyncio
import random
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import structlog

P = ParamSpec("P")
R = TypeVar("R")

log = structlog.get_logger()


def async_retry(
    *,
    tries: int = 3,
    backoff: float = 2.0,
    base_delay: float = 0.2,
    max_delay: float = 5.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Retry async-функции с exponential backoff + jitter.

    `CancelledError` НИКОГДА не ловится — отмена всегда пробрасывается.
    """

    def decorator(fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: BaseException | None = None
            for attempt in range(1, tries + 1):
                try:
                    return await fn(*args, **kwargs)
                except asyncio.CancelledError:
                    raise
                except exceptions as exc:
                    last_exc = exc
                    if attempt == tries:
                        break
                    delay = min(max_delay, base_delay * (backoff ** (attempt - 1)))
                    delay += random.uniform(0, delay * 0.25)
                    log.warning(
                        "async_retry",
                        fn=fn.__name__,
                        attempt=attempt,
                        delay=round(delay, 3),
                        error=repr(exc),
                    )
                    await asyncio.sleep(delay)
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator
