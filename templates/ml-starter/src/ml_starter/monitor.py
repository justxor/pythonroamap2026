"""Data drift monitoring via Evidently."""
from pathlib import Path

import polars as pl
import typer

import evidently
from packaging.version import Version

if Version(evidently.__version__) >= Version("0.7.0"):
    from evidently.legacy.metric_preset import DataDriftPreset
    from evidently.legacy.report import Report
else:
    from evidently.metric_preset import DataDriftPreset
    from evidently.report import Report

from ml_starter.config import settings

app = typer.Typer(no_args_is_help=True)


@app.command()
def drift(reference_path: Path, current_path: Path) -> None:
    """Generate drift HTML report."""
    ref = pl.read_parquet(reference_path).to_pandas()
    cur = pl.read_parquet(current_path).to_pandas()

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref, current_data=cur)

    out = settings.artifacts_dir / "drift_report.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    report.save_html(str(out))
    typer.echo(f"saved {out}")


if __name__ == "__main__":
    app()
