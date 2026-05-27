"""Training entry point with MLflow tracking."""
from pathlib import Path

import lightgbm as lgb
import mlflow
import typer
from sklearn.metrics import roc_auc_score

from ml_starter.config import settings
from ml_starter.data import load, split
from ml_starter.logging_setup import get_logger
from ml_starter.model import make_model

log = get_logger(__name__)
app = typer.Typer(no_args_is_help=True)


@app.command()
def train(data_path: Path) -> None:
    """Train model and log to MLflow."""
    mlflow.set_tracking_uri(settings.mlflow_uri)
    mlflow.set_experiment(settings.experiment_name)

    X, y = load(data_path)
    s = split(X, y)

    with mlflow.start_run():
        mlflow.log_params({
            "n_estimators": settings.n_estimators,
            "learning_rate": settings.learning_rate,
            "random_seed": settings.random_seed,
        })

        model = make_model()
        model.fit(
            s.X_train.to_pandas(), s.y_train.to_pandas(),
            eval_set=[(s.X_test.to_pandas(), s.y_test.to_pandas())],
            callbacks=[lgb.early_stopping(settings.early_stopping_rounds), lgb.log_evaluation(0)],
        )

        proba = model.predict_proba(s.X_test.to_pandas())[:, 1]
        auc = float(roc_auc_score(s.y_test.to_pandas(), proba))
        mlflow.log_metric("val_auc", auc)
        mlflow.lightgbm.log_model(model, "model", registered_model_name=settings.experiment_name)

        log.info("training_complete", val_auc=auc)
        typer.echo(f"val AUC: {auc:.4f}")


if __name__ == "__main__":
    app()
