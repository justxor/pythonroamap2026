"""Typed config via pydantic-settings."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ML_", extra="ignore")

    # paths
    data_dir: Path = Path("data")
    artifacts_dir: Path = Path("artifacts")

    # training
    random_seed: int = 42
    test_size: float = 0.2
    n_folds: int = 5

    # model
    n_estimators: int = 2000
    learning_rate: float = 0.03
    early_stopping_rounds: int = 100

    # tracking
    mlflow_uri: str = "http://localhost:5000"
    experiment_name: str = "ml-starter"


settings = Settings()
