import httpx
import pytest
import respx

from scraper.client import RateLimitedFetcher


@pytest.mark.asyncio
@respx.mock
async def test_get_ok() -> None:
    respx.get("https://example.com/ok").mock(
        return_value=httpx.Response(200, text="<html></html>")
    )
    async with httpx.AsyncClient() as client:
        fetcher = RateLimitedFetcher(client)
        r = await fetcher.get("https://example.com/ok")
        assert r.status_code == 200


@pytest.mark.asyncio
@respx.mock
async def test_get_retries_on_5xx() -> None:
    route = respx.get("https://example.com/flaky").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(503),
            httpx.Response(200, text="ok"),
        ]
    )
    async with httpx.AsyncClient() as client:
        fetcher = RateLimitedFetcher(client)
        r = await fetcher.get("https://example.com/flaky")
        assert r.status_code == 200
        assert route.call_count == 3
