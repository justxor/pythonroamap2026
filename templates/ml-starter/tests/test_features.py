"""Tests for features module."""
from datetime import datetime

import polars as pl

from ml_starter.features import add_rolling, add_time_features


def test_add_time_features_adds_cyclic_columns() -> None:
    df = pl.DataFrame({"timestamp": [datetime(2026, 1, 1, 12, 0)]})
    out = add_time_features(df)
    assert "hour_sin" in out.columns
    assert "hour_cos" in out.columns
    assert "is_weekend" in out.columns


def test_add_rolling_creates_window_columns() -> None:
    df = pl.DataFrame({
        "user": ["a", "a", "a", "b"],
        "amount": [1.0, 2.0, 3.0, 10.0],
    })
    out = add_rolling(df, key="user", col="amount", windows=(2,))
    assert "amount_ma2" in out.columns
