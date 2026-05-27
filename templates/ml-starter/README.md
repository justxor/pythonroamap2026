# ⚡ ml-starter — стартер ML-проекта (2026)

> Продакшен-готовый шаблон для табличных ML-задач с полным пайплайном: данные → обучение → tracking → деплой.

## 🧱 Стек

| Слой | Инструмент |
|---|---|
| Python | 3.13+ |
| package manager | uv |
| linter/format | ruff |
| types | pyright (strict) |
| data | polars, duckdb, pyarrow |
| ML | scikit-learn, lightgbm, catboost |
| tuning | optuna |
| explain | shap |
| tracking | mlflow |
| data versioning | dvc |
| serving | bentoml, onnxruntime |
| monitoring | evidently |
| config | hydra-core, pydantic-settings |
| logging | structlog |
| tests | pytest, pytest-cov |
| CI | GitHub Actions |

## 📁 Структура

```text
ml-starter/
├── pyproject.toml
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── dvc.yaml                  # DVC-пайплайн
├── conf/
│   └── config.yaml           # Hydra-конфиг
├── src/ml_starter/
│   ├── __init__.py
│   ├── config.py             # pydantic-settings
│   ├── data.py               # загрузка и split
│   ├── features.py           # feature engineering
│   ├── model.py              # CatBoost + sklearn Pipeline
│   ├── tune.py               # Optuna
│   ├── train.py              # train + MLflow
│   ├── explain.py            # SHAP
│   ├── serve.py              # BentoML
│   ├── monitor.py            # Evidently drift
│   └── logging_setup.py
├── tests/
│   ├── test_features.py
│   └── test_model.py
└── .github/workflows/ci.yml
```

## 🚀 Quick start

```bash
# 1. Установка зависимостей
uv sync

# 2. Обучение модели
uv run python -m ml_starter.train

# 3. Подбор гиперпараметров
uv run python -m ml_starter.tune --n-trials 100

# 4. Интерпретация
uv run python -m ml_starter.explain

# 5. MLflow UI
uv run mlflow ui --port 5000

# 6. Сервинг через BentoML
uv run bentoml serve src.ml_starter.serve:svc --reload

# 7. Drift-отчёт
uv run python -m ml_starter.monitor
```

## ✅ Чеклист выпуска

- [ ] Метрика выбрана под бизнес-задачу
- [ ] CV-split без утечек (timestamp/group)
- [ ] Препроцессинг внутри sklearn Pipeline
- [ ] Early stopping в бустингах
- [ ] Optuna с pruner
- [ ] SHAP-разбор топ-10 фичей
- [ ] MLflow logging метрик/артефактов
- [ ] DVC версионирует данные
- [ ] ONNX-экспорт + inference-бенчмарк
- [ ] BentoML сервис в Docker
- [ ] Evidently отчёт в CI/cron
- [ ] Нагрузочный тест (locust/k6)

## 📚 Ресурсы

- [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)
- [t.me/pythonl](https://t.me/pythonl)
- [Папка каналов](https://t.me/addlist/8vDUwYRGujRmZjFi)
- [Этап 16: Machine Learning](../../course/stage-16-ml.md)
