"""Feature engineering on polars."""
import math

import polars as pl


def add_time_features(df: pl.DataFrame, ts_col: str = "timestamp") -> pl.DataFrame:
    """Add cyclic time encodings."""
    return df.with_columns([
        (2 * math.pi * pl.col(ts_col).dt.hour() / 24).sin().alias("hour_sin"),
        (2 * math.pi * pl.col(ts_col).dt.hour() / 24).cos().alias("hour_cos"),
        (pl.col(ts_col).dt.weekday() >= 5).alias("is_weekend"),
    ])


def add_rolling(df: pl.DataFrame, key: str, col: str, windows: tuple[int, ...] = (3, 7, 30)) -> pl.DataFrame:
    """Add rolling-mean features per group."""
    exprs = [
        pl.col(col).rolling_mean(window_size=w).over(key).alias(f"{col}_ma{w}")
        for w in windows
    ]
    return df.with_columns(exprs)
