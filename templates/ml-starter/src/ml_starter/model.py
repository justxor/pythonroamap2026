"""LightGBM model factory."""
from typing import Any

import lightgbm as lgb

from ml_starter.config import settings


def make_model(**override: Any) -> lgb.LGBMClassifier:
    """Create LightGBM classifier with sensible defaults."""
    params: dict[str, Any] = {
        "n_estimators": settings.n_estimators,
        "learning_rate": settings.learning_rate,
        "num_leaves": 63,
        "feature_fraction": 0.8,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "objective": "binary",
        "metric": "auc",
        "n_jobs": -1,
        "random_state": settings.random_seed,
        "verbosity": -1,
    }
    params.update(override)
    return lgb.LGBMClassifier(**params)
