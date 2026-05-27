"""BentoML serving entry point."""
from typing import Any

import bentoml
from bentoml.io import JSON


runner = bentoml.mlflow.get("ml-starter:latest").to_runner()
svc = bentoml.Service("ml-starter", runners=[runner])


@svc.api(input=JSON(), output=JSON())  # type: ignore[misc]
async def predict(payload: dict[str, Any]) -> dict[str, float]:
    """Predict probability for a single sample."""
    features = payload["features"]
    proba = await runner.predict_proba.async_run([features])
    return {"score": float(proba[0][1])}
