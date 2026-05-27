"""Data loading and splitting via polars."""
from pathlib import Path
from typing import NamedTuple

import polars as pl
from sklearn.model_selection import train_test_split

from ml_starter.config import settings


class Split(NamedTuple):
    X_train: pl.DataFrame
    X_test: pl.DataFrame
    y_train: pl.Series
    y_test: pl.Series


def load(path: Path, target: str = "target") -> tuple[pl.DataFrame, pl.Series]:
    """Load Parquet/CSV file and split into X, y."""
    if path.suffix == ".parquet":
        df = pl.read_parquet(path)
    else:
        df = pl.read_csv(path)
    y = df[target]
    X = df.drop(target)
    return X, y


def split(X: pl.DataFrame, y: pl.Series) -> Split:
    """Stratified train/test split."""
    X_train, X_test, y_train, y_test = train_test_split(
        X.to_pandas(),
        y.to_pandas(),
        test_size=settings.test_size,
        stratify=y.to_pandas(),
        random_state=settings.random_seed,
    )
    return Split(
        X_train=pl.from_pandas(X_train),
        X_test=pl.from_pandas(X_test),
        y_train=pl.from_pandas(y_train),
        y_test=pl.from_pandas(y_test),
    )
