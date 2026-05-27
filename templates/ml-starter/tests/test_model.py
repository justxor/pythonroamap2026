"""Tests for model factory and end-to-end fit."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

from ml_starter.model import make_model


def test_make_model_returns_lgbm_classifier() -> None:
    model = make_model()
    assert hasattr(model, "fit")
    assert hasattr(model, "predict_proba")


def test_model_trains_and_predicts() -> None:
    rng = np.random.default_rng(42)
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    model = make_model(n_estimators=50)
    model.fit(X, y)
    proba = model.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, proba)
    assert auc > 0.8
