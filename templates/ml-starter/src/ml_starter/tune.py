"""Optuna-based hyperparameter tuning."""
from pathlib import Path

import optuna
import polars as pl
import typer
from sklearn.model_selection import cross_val_score

from ml_starter.config import settings
from ml_starter.data import load
from ml_starter.model import make_model

app = typer.Typer(no_args_is_help=True)


def objective(trial: optuna.Trial, X: pl.DataFrame, y: pl.Series) -> float:
    params = {
        "learning_rate": trial.suggest_float("lr", 1e-3, 0.1, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 16, 256),
        "feature_fraction": trial.suggest_float("ff", 0.5, 1.0),
        "bagging_fraction": trial.suggest_float("bf", 0.5, 1.0),
        "min_data_in_leaf": trial.suggest_int("min_leaf", 10, 200),
        "lambda_l2": trial.suggest_float("l2", 1e-8, 10, log=True),
    }
    model = make_model(**params)
    scores = cross_val_score(model, X.to_pandas(), y.to_pandas(), cv=settings.n_folds, scoring="roc_auc", n_jobs=-1)
    return float(scores.mean())


@app.command()
def tune(data_path: Path, n_trials: int = 100) -> None:
    """Run Optuna study."""
    X, y = load(data_path)
    study = optuna.create_study(
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=settings.random_seed),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=10),
    )
    study.optimize(lambda t: objective(t, X, y), n_trials=n_trials, show_progress_bar=True)
    typer.echo(f"Best AUC: {study.best_value:.4f}")
    typer.echo(f"Best params: {study.best_params}")


if __name__ == "__main__":
    app()
