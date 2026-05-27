"""SHAP-based model interpretation."""
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import shap
import typer

from ml_starter.config import settings
from ml_starter.data import load, split

app = typer.Typer(no_args_is_help=True)


@app.command()
def explain(data_path: Path, model_uri: str = "models:/ml-starter/latest") -> None:
    """Generate SHAP summary plot for the latest model."""
    mlflow.set_tracking_uri(settings.mlflow_uri)
    model = mlflow.lightgbm.load_model(model_uri)

    X, y = load(data_path)
    s = split(X, y)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(s.X_test.to_pandas())

    out = settings.artifacts_dir / "shap_summary.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    shap.summary_plot(shap_values, s.X_test.to_pandas(), show=False)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    typer.echo(f"saved {out}")


if __name__ == "__main__":
    app()
