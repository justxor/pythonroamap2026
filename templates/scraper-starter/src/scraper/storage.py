"""Сохранение результатов в Parquet через polars."""
from __future__ import annotations

from pathlib import Path

import polars as pl

from .logging_setup import log
from .models import PageResult


def save_parquet(results: list[PageResult], out: Path) -> None:
    """Сохраняет результаты в Parquet с zstd сжатием."""
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = [r.model_dump(mode="json") for r in results]
    df = pl.DataFrame(rows)
    df.write_parquet(out, compression="zstd")
    log.info("storage.saved", path=str(out), rows=len(rows))

