"""CLI вход для scraper. Запуск: uv run scraper crawl --urls-file urls.txt --out data/out.parquet"""
from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import typer

from .client import RateLimitedFetcher, make_client
from .config import settings
from .logging_setup import log, setup_logging
from .models import PageResult
from .parser import extract_title
from .storage import save_parquet

app = typer.Typer(add_completion=False)


async def _crawl_one(fetcher: RateLimitedFetcher, url: str) -> PageResult:
    try:
        r = await fetcher.get(url)
        return PageResult(
            url=url,
            title=extract_title(r.text),
            status_code=r.status_code,
            html_length=len(r.text),
        )
    except httpx.HTTPError as exc:
        log.warning("crawl.error", url=url, error=str(exc))
        return PageResult(
            url=url,
            title=None,
            status_code=0,
            html_length=0,
            error=str(exc),
        )


async def _crawl_all(urls: list[str]) -> list[PageResult]:
    sem = asyncio.Semaphore(settings.concurrency)
    async with make_client() as client:
        fetcher = RateLimitedFetcher(client)

        async def bounded(u: str) -> PageResult:
            async with sem:
                return await _crawl_one(fetcher, u)

        return await asyncio.gather(*[bounded(u) for u in urls])


@app.command()
def crawl(
    urls_file: Path = typer.Option(..., "--urls-file", exists=True, readable=True),
    out: Path = typer.Option(Path("data/result.parquet"), "--out"),
):
    setup_logging(settings.log_level, settings.log_json)
    urls = [line.strip() for line in urls_file.read_text().splitlines() if line.strip()]
    log.info("crawl.start", count=len(urls))
    results = asyncio.run(_crawl_all(urls))
    save_parquet(results, out)
    ok = sum(1 for r in results if r.error is None)
    log.info("crawl.done", total=len(results), ok=ok, failed=len(results) - ok)


if __name__ == "__main__":
    app()
