# Этап 16. Machine Learning на Python (2026)

> 🎯 Освоить современный ML-стек: от классики (sklearn) до бустингов, нейросетей и LLM-инфраструктуры.
> ⏱ 6–10 недель (после этапов 0–11).

[← К оглавлению](README.md) · [← Этап 15: парсинг](stage-15-parsing.md)

> 🤖 **Главные Telegram-источники этого этапа:**
> 1. [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — практика, модели, ноутбуки, бенчмарки.
> 2. [t.me/pythonl](https://t.me/pythonl) — Python-новости и ML-разборы.
> 3. [Папка лучших каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi)

---

## Содержание

- [Урок 1. ML-стек 2026 — что выбрать](#урок-1-ml-стек-2026)
- [Урок 2. Данные: Polars, DuckDB, Parquet](#урок-2-данные)
- [Урок 3. EDA и подготовка фичей](#урок-3-eda-и-feature-engineering)
- [Урок 4. Классика: scikit-learn + Pipeline](#урок-4-scikit-learn)
- [Урок 5. Бустинги: XGBoost / LightGBM / CatBoost](#урок-5-бустинги)
- [Урок 6. Валидация и метрики](#урок-6-валидация-и-метрики)
- [Урок 7. Hyperparameter tuning: Optuna](#урок-7-optuna)
- [Урок 8. Интерпретация: SHAP](#урок-8-shap)
- [Урок 9. Нейросети: PyTorch 2.x](#урок-9-pytorch)
- [Урок 10. Lightning + Hydra](#урок-10-lightning--hydra)
- [Урок 11. HuggingFace: transformers, datasets](#урок-11-huggingface)
- [Урок 12. Embeddings и векторный поиск](#урок-12-embeddings)
- [Урок 13. MLOps: MLflow, DVC, W&B](#урок-13-mlops)
- [Урок 14. Деплой моделей: BentoML, Triton, ONNX](#урок-14-деплой)
- [Урок 15. Мониторинг: drift, evidently](#урок-15-мониторинг)
- [Упражнения](#упражнения)
- [Решения](#решения)
- [Чеклист](#чеклист)
- [📚 Бесплатные ресурсы](#-бесплатные-ресурсы)

---
## Урок 1. ML-стек 2026

| Слой | Стандарт 2026 | Зачем |
|---|---|---|
| Данные | **Polars**, **DuckDB**, Parquet+zstd | в 10–100× быстрее pandas; lazy API; OLAP-запросы прямо к файлам |
| Классика | **scikit-learn 1.5+** | базовые модели, pipelines, GridSearch |
| Бустинги | **LightGBM**, **CatBoost**, **XGBoost 2.x** | табличные задачи, баланс speed/quality |
| Тюнинг | **Optuna 4.x** | TPE, pruning, multi-objective, distributed |
| Интерпретация | **SHAP**, **InterpretML**, **PDPbox** | объяснимость прогнозов |
| Нейросети | **PyTorch 2.5+** (torch.compile) | де-факто стандарт; JAX — для исследований |
| Тренировка | **Lightning 2.x**, **Hydra**, **Accelerate** | убираем boilerplate, мульти-GPU |
| NLP/CV/Audio | **HuggingFace transformers 4.x**, **datasets**, **diffusers** | готовые модели и пайплайны |
| Vector DB | **Qdrant**, **LanceDB**, **pgvector** | embeddings, поиск, RAG |
| Experiments | **MLflow 2.x**, **Weights & Biases** (free tier), **DVC** | tracking, регистр моделей |
| Сервинг | **BentoML**, **Triton**, **vLLM** (LLM), **ONNX Runtime** | прод-инференс |
| Мониторинг | **Evidently AI**, **NannyML** | data/concept drift |

### Чего избегать в 2026

- ❌ **pandas** для больших данных → polars / duckdb
- ❌ **TensorFlow 1.x / Keras без TF** → PyTorch + Lightning
- ❌ **plain numpy** для табличек → polars
- ❌ **pickle** для моделей в проде → ONNX / safetensors
- ❌ **Jupyter без version control** → nbstripout + DVC + papermill

---

## Урок 2. Данные

### Polars вместо pandas

```python
import polars as pl

# lazy-режим: запрос оптимизируется до выполнения
df = (
    pl.scan_parquet("data/train.parquet")
    .filter(pl.col("amount") > 0)
    .with_columns(
        log_amount=pl.col("amount").log(),
        is_weekend=pl.col("date").dt.weekday() >= 5,
    )
    .group_by("user_id")
    .agg([
        pl.col("amount").sum().alias("total"),
        pl.col("amount").mean().alias("avg"),
        pl.len().alias("n_tx"),
    ])
    .collect()  # запуск
)
```

### DuckDB для аналитических запросов

```python
import duckdb

# SQL прямо по Parquet — без загрузки в память
result = duckdb.sql("""
    SELECT category, AVG(price) AS avg_price, COUNT(*) AS n
    FROM 'data/sales/*.parquet'
    WHERE date >= '2025-01-01'
    GROUP BY category
    ORDER BY avg_price DESC
""").pl()  # сразу в polars
```

### Parquet + zstd

```python
df.write_parquet("out.parquet", compression="zstd", compression_level=9)
```

---

## Урок 3. EDA и feature engineering

### Профилирование

```python
# Быстрый отчёт по датасету
from ydata_profiling import ProfileReport
report = ProfileReport(df.to_pandas(), title="EDA")
report.to_file("eda.html")
```

### Feature engineering на polars

```python
df = df.with_columns([
    # цикличность времени
    (2 * pl.col("hour") * 3.14159 / 24).sin().alias("hour_sin"),
    (2 * pl.col("hour") * 3.14159 / 24).cos().alias("hour_cos"),
    # target encoding (через group_by + join)
    # rolling-фичи
    pl.col("amount").rolling_mean(window_size=7).over("user_id").alias("amt_ma7"),
])
```

### Категориальные с CatBoost-кодированием

```python
from category_encoders import TargetEncoder, CatBoostEncoder

enc = CatBoostEncoder(cols=["city", "device"])
X_train_enc = enc.fit_transform(X_train, y_train)
X_test_enc = enc.transform(X_test)
```

---
## Урок 4. scikit-learn

### Pipeline — единственно правильный путь

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

numeric = ["age", "amount", "tenure"]
categorical = ["city", "device"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical),
])

pipe = Pipeline([
    ("prep", preprocess),
    ("clf", RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42)),
])
pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)
```

**Почему Pipeline:** нет data leakage, легко сериализуется, работает с GridSearchCV.

---

## Урок 5. Бустинги

### LightGBM (быстрый старт)

```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=2000,
    learning_rate=0.03,
    num_leaves=63,
    feature_fraction=0.8,
    bagging_fraction=0.8,
    bagging_freq=5,
    objective="binary",
    metric="auc",
    n_jobs=-1,
    random_state=42,
)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    callbacks=[lgb.early_stopping(100), lgb.log_evaluation(0)],
)
```

### CatBoost — лучший на категориальных

```python
from catboost import CatBoostClassifier, Pool

cat_features = ["city", "device", "browser"]
train_pool = Pool(X_train, y_train, cat_features=cat_features)
val_pool = Pool(X_val, y_val, cat_features=cat_features)

model = CatBoostClassifier(
    iterations=3000, learning_rate=0.03, depth=6,
    eval_metric="AUC", early_stopping_rounds=200,
    task_type="GPU",  # если есть
    verbose=200,
)
model.fit(train_pool, eval_set=val_pool)
```

### Когда какой

| Случай | Выбор |
|---|---|
| Много категориальных | CatBoost |
| Большой датасет (10M+) | LightGBM |
| Нужно sklearn-совместимое API | XGBoost |
| Маленький датасет (<10k) | RandomForest или CatBoost |

---

## Урок 6. Валидация и метрики

### Cross-validation

```python
from sklearn.model_selection import StratifiedKFold, TimeSeriesSplit, cross_val_score

# Классификация — стратифицированный
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Временные ряды — БЕЗ перемешивания
cv = TimeSeriesSplit(n_splits=5, gap=7)  # gap — анти-утечка

scores = cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
print(f"AUC: {scores.mean():.4f} ± {scores.std():.4f}")
```

### Какую метрику выбрать

| Задача | Метрика |
|---|---|
| Бинарная классификация (сбаланс.) | accuracy, F1 |
| Бинарная (дисбаланс) | **ROC-AUC**, PR-AUC, F1 |
| Мультикласс | macro-F1, weighted-F1 |
| Регрессия | RMSE, MAE, **MAPE** для бизнеса |
| Ранжирование | NDCG, MAP |
| Аномалии | Precision@K |

⚠️ **Утечки данных** — главный враг ML. Чеклист:
- target encoding ТОЛЬКО внутри fold
- scaler.fit ТОЛЬКО на train
- timestamp в test строго больше train

---
## Урок 7. Optuna

```python
import optuna
from sklearn.model_selection import cross_val_score
import lightgbm as lgb

def objective(trial: optuna.Trial) -> float:
    params = {
        "n_estimators": 2000,
        "learning_rate": trial.suggest_float("lr", 1e-3, 0.1, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 16, 256),
        "feature_fraction": trial.suggest_float("ff", 0.5, 1.0),
        "bagging_fraction": trial.suggest_float("bf", 0.5, 1.0),
        "min_data_in_leaf": trial.suggest_int("min_leaf", 10, 200),
        "lambda_l2": trial.suggest_float("l2", 1e-8, 10, log=True),
        "verbosity": -1,
    }
    model = lgb.LGBMClassifier(**params, n_jobs=-1, random_state=42)
    scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc", n_jobs=-1)
    return scores.mean()

study = optuna.create_study(
    direction="maximize",
    sampler=optuna.samplers.TPESampler(seed=42),
    pruner=optuna.pruners.MedianPruner(n_startup_trials=10),
)
study.optimize(objective, n_trials=100, n_jobs=4, show_progress_bar=True)
print(study.best_value, study.best_params)
```

**Фишки Optuna:**
- `pruner` — обрывает плохие trial'ы → ×3 быстрее
- `study.trials_dataframe()` — анализ в polars
- `optuna-dashboard` — web-UI
- `RDBStorage` — параллельная оптимизация на нескольких машинах

---

## Урок 8. SHAP

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Глобальная важность
shap.summary_plot(shap_values, X_test)

# Объяснение одного предсказания
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])

# Зависимость от признака
shap.dependence_plot("age", shap_values, X_test)
```

**Что даёт:** не просто «важность фичи», а **направление влияния** на конкретный прогноз. Обязателен для прод-моделей в финтехе/медицине.

---

## Урок 9. PyTorch

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

class TabularNet(nn.Module):
    def __init__(self, n_features: int, hidden: int = 256) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_features, hidden),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(hidden, hidden),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(hidden, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = TabularNet(n_features=X.shape[1]).to(device)

# 2026: torch.compile ускоряет в 1.3–2×
model = torch.compile(model)

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
loss_fn = nn.BCEWithLogitsLoss()
```

### Mixed precision (FP16/BF16)

```python
scaler = torch.amp.GradScaler("cuda")

for x, y in loader:
    x, y = x.to(device), y.to(device)
    optimizer.zero_grad()
    with torch.amp.autocast("cuda", dtype=torch.bfloat16):
        logits = model(x)
        loss = loss_fn(logits, y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

---
## Урок 10. Lightning + Hydra

### Lightning убирает boilerplate

```python
import lightning as L
import torchmetrics

class LitTabular(L.LightningModule):
    def __init__(self, n_features: int, lr: float = 1e-3) -> None:
        super().__init__()
        self.save_hyperparameters()
        self.model = TabularNet(n_features)
        self.loss = nn.BCEWithLogitsLoss()
        self.auc = torchmetrics.AUROC(task="binary")

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = self.loss(logits, y)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        self.auc.update(torch.sigmoid(logits), y.int())
        self.log("val_auc", self.auc, on_epoch=True, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.hparams.lr)

trainer = L.Trainer(
    max_epochs=50,
    accelerator="auto",
    precision="bf16-mixed",
    callbacks=[L.pytorch.callbacks.EarlyStopping("val_auc", mode="max", patience=5)],
    logger=L.pytorch.loggers.MLFlowLogger("my_exp"),
)
trainer.fit(LitTabular(n_features=128), train_loader, val_loader)
```

### Hydra для конфигов

```yaml
# conf/config.yaml
defaults:
  - model: tabular
  - dataset: prod
  - optimizer: adamw

training:
  epochs: 50
  batch_size: 1024
  precision: bf16-mixed
```

```python
import hydra
from omegaconf import DictConfig

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    model = hydra.utils.instantiate(cfg.model)
    trainer = L.Trainer(**cfg.training)
    trainer.fit(model, ...)
```

---

## Урок 11. HuggingFace

### transformers — за 10 строк

```python
from transformers import pipeline

# zero-shot классификация
clf = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
result = clf(
    "Доставка опоздала на 2 дня, упаковка повреждена",
    candidate_labels=["логистика", "оплата", "качество товара"],
)
```

### Fine-tuning через Trainer

```python
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments,
)
from datasets import load_dataset

ds = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, max_length=256)

ds = ds.map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2,
)

args = TrainingArguments(
    output_dir="out",
    num_train_epochs=3,
    per_device_train_batch_size=32,
    learning_rate=2e-5,
    bf16=True,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    report_to="mlflow",
)
trainer = Trainer(model=model, args=args, train_dataset=ds["train"], eval_dataset=ds["test"])
trainer.train()
```

### LoRA / QLoRA для больших моделей

```python
# peft — для эффективного fine-tuning LLM
from peft import LoraConfig, get_peft_model

lora = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"], lora_dropout=0.05)
model = get_peft_model(model, lora)
model.print_trainable_parameters()  # обычно <1% весов
```

---
## Урок 12. Embeddings

```python
from sentence_transformers import SentenceTransformer

# sota 2026: BGE-M3, e5-mistral, jina-v3
enc = SentenceTransformer("BAAI/bge-m3")
vectors = enc.encode(
    ["Python — отличный язык", "JavaScript для фронта"],
    normalize_embeddings=True,
    convert_to_numpy=True,
)
```

### Qdrant — vector DB

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

qd = QdrantClient(url="http://localhost:6333")
qd.create_collection(
    "docs",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)
qd.upsert("docs", points=[
    PointStruct(id=i, vector=v.tolist(), payload={"text": t})
    for i, (v, t) in enumerate(zip(vectors, texts))
])

# поиск
results = qd.search("docs", query_vector=enc.encode("Python").tolist(), limit=5)
```

**Альтернативы:** LanceDB (file-based, без сервера), pgvector (если уже есть Postgres).

---

## Урок 13. MLOps

### MLflow — tracking

```python
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("churn")

with mlflow.start_run():
    mlflow.log_params({"lr": 0.03, "n_est": 2000})
    model.fit(X_train, y_train)
    auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
    mlflow.log_metric("val_auc", auc)
    mlflow.sklearn.log_model(model, "model", registered_model_name="churn-prod")
```

### DVC — версионирование данных

```bash
dvc init
dvc remote add -d s3 s3://my-bucket/dvc
dvc add data/train.parquet
git add data/train.parquet.dvc .gitignore
git commit -m "data: add v1 of train"
dvc push
```

### W&B (free tier)

```python
import wandb

wandb.init(project="churn", config={"lr": 0.03})
wandb.log({"train_loss": 0.42, "val_auc": 0.87})
wandb.log({"shap_summary": wandb.Image("shap.png")})
```

---

## Урок 14. Деплой

### Конвертация в ONNX

```python
import onnxmltools
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

initial_type = [("input", FloatTensorType([None, X_train.shape[1]]))]
onnx_model = convert_sklearn(pipe, initial_types=initial_type)
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

### Инференс через ONNX Runtime (CPU, ×5–10 быстрее sklearn)

```python
import onnxruntime as ort

sess = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
preds = sess.run(None, {"input": X_test.astype("float32")})[0]
```

### BentoML — сервинг с REST/gRPC

```python
# service.py
import bentoml
from bentoml.io import JSON

runner = bentoml.sklearn.get("churn:latest").to_runner()
svc = bentoml.Service("churn", runners=[runner])

@svc.api(input=JSON(), output=JSON())
async def predict(payload: dict) -> dict:
    proba = await runner.predict_proba.async_run([payload["features"]])
    return {"score": float(proba[0][1])}
```

```bash
bentoml serve service.py:svc --reload
bentoml containerize churn:latest
```

**Для LLM:** vLLM (PagedAttention, ×24 throughput vs HF), TGI, llama.cpp.

---

## Урок 15. Мониторинг

### Drift detection через Evidently

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=ref_df, current_data=prod_df)
report.save_html("drift.html")
```

**Что мониторить в проде:**
1. **Data drift** — распределение фичей
2. **Concept drift** — связь X→y меняется
3. **Prediction drift** — сдвиг распределения скоров
4. **Performance** — если есть ground truth с задержкой
5. **Infrastructure** — latency p95/p99, RPS, ошибки

Связка для прода: **Evidently → Prometheus → Grafana → Alertmanager**.

---
## Упражнения

1. **Табличка → бустинг.** Возьми датасет [Telco Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). Построй pipeline: polars EDA → CatBoost → Optuna 50 trials → SHAP. Цель: ROC-AUC ≥ 0.84 на тесте.

2. **Утечка данных.** Намеренно сделай target leakage (например, target encoding до split). Сравни CV vs holdout. Опиши, как leakage искажает метрику.

3. **Временные ряды.** Прогноз продаж по магазину (любой публичный датасет). TimeSeriesSplit с gap=7. Сравни LightGBM с lag-фичами против naive (вчера = сегодня).

4. **NLP fine-tune.** Дообучи `distilbert-base-multilingual` на отзывах с Маркета/Озона (любой открытый датасет тональности). Сравни с zero-shot DeBERTa.

5. **PyTorch + Lightning.** Перепиши пример из урока 9 на Lightning, добавь MLflow-логгер, EarlyStopping и `bf16-mixed`. Сравни время эпохи с/без `torch.compile`.

6. **RAG-индекс.** Скачай 1000 статей (Хабр / arXiv abstracts). Построй индекс на Qdrant с BGE-M3. Сделай поиск top-5 по запросу. Оцени Recall@5 на 20 ручных запросах.

7. **Деплой.** Заверни модель из задания 1 в BentoML, собери Docker, прогони нагрузочный тест через [locust](https://locust.io/). Зафиксируй p50/p95/p99 latency.

8. **Мониторинг.** Сгенерируй искусственный data drift (сдвиг распределения 1 фичи). Поставь Evidently, проверь, что drift обнаружен.

---

## Решения

Эталонные решения и тетради — в репозитории курса в папке `solutions/stage-16/` (по мере наполнения).

Подсказка к задаче 1:

```python
# Старт-скелет
import polars as pl
from catboost import CatBoostClassifier
from sklearn.model_selection import StratifiedKFold
import optuna

df = pl.read_csv("telco.csv")
# 1. EDA, чистка
# 2. cat_features = [...]
# 3. objective(trial): catboost + 5-fold CV → mean AUC
# 4. study.optimize(objective, n_trials=50)
# 5. финальный refit + SHAP
```

---

## Чеклист

- [ ] Делаю EDA через polars/duckdb, не pandas
- [ ] Все препроцессинги — в sklearn `Pipeline`
- [ ] Кросс-валидация выбрана под задачу (Stratified / TimeSeries)
- [ ] Использую `early_stopping` в бустингах
- [ ] Гиперпараметры подбирал Optuna с pruner
- [ ] Интерпретирую модель через SHAP
- [ ] PyTorch обучение: `torch.compile` + `bf16-mixed`
- [ ] Эксперименты пишутся в MLflow или W&B
- [ ] Данные версионируются DVC
- [ ] Модель в проде — ONNX или BentoML
- [ ] Настроен мониторинг drift через Evidently
- [ ] Прогнал нагрузочный тест на инференс

---

## 📚 Бесплатные ресурсы

### 🚀 Главные Telegram-источники

1. 🤖 **[t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — главный канал этапа: модели, ноутбуки, разборы статей, бенчмарки. Свежий ML-стек именно отсюда.
2. 🐍 **[t.me/pythonl](https://t.me/pythonl)** — Python-новости, ML-разборы, рубрика «задача дня», вакансии.
3. 📚 **[Папка лучших каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка по Python / ML / DS / AI.

### 📘 Курсы и книги

- 🆓 [ODS — открытый курс ML (RU)](https://mlcourse.ai/) — классика на русском, всё ещё актуально
- 🆓 [Stanford CS229 — Machine Learning (Andrew Ng)](https://cs229.stanford.edu/) — фундамент
- 🆓 [Stanford CS231n — CNN](http://cs231n.stanford.edu/) — компьютерное зрение
- 🆓 [Stanford CS224n — NLP](https://web.stanford.edu/class/cs224n/) — NLP
- 🆓 [Fast.ai — Practical Deep Learning](https://course.fast.ai/) — практический deep learning
- 🆓 [HuggingFace NLP course](https://huggingface.co/learn/nlp-course) — transformers с нуля
- 🆓 [HuggingFace Deep RL course](https://huggingface.co/learn/deep-rl-course) — обучение с подкреплением
- 🆓 [d2l.ai — Dive into Deep Learning](https://d2l.ai/) — открытая книга с примерами на PyTorch
- 🆓 [Andrej Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — YouTube + GitHub
- 🆓 [ШАД — лекции](https://academy.yandex.ru/handbook/ml) — учебник ML от ШАД (RU)

### 📖 Документация и cheatsheets

- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)
- [PyTorch tutorials](https://pytorch.org/tutorials/)
- [Lightning docs](https://lightning.ai/docs/pytorch/stable/)
- [Polars user guide](https://docs.pola.rs/user-guide/)
- [HuggingFace Transformers docs](https://huggingface.co/docs/transformers)
- [Optuna tutorial](https://optuna.readthedocs.io/en/stable/tutorial/index.html)
- [SHAP docs](https://shap.readthedocs.io/)

### 🎮 Соревнования и датасеты

- 🏆 [Kaggle](https://www.kaggle.com/) — соревнования + бесплатные GPU/TPU notebooks
- 🏆 [DrivenData](https://www.drivendata.org/) — social-good ML-соревнования
- 🏆 [Codabench](https://www.codabench.org/) — open-source платформа
- 📦 [HuggingFace Datasets](https://huggingface.co/datasets) — 200k+ датасетов
- 📦 [Papers with Code](https://paperswithcode.com/datasets) — датасеты под задачи
- 📦 [UCI ML Repo](https://archive.ics.uci.edu/) — классические таблички

### 🎥 YouTube

- [3Blue1Brown — Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) — интуиция за нейросетями
- [StatQuest with Josh Starmer](https://www.youtube.com/@statquest) — статистика и ML понятным языком
- [Yannic Kilcher](https://www.youtube.com/@YannicKilcher) — разборы свежих ML-статей
- [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers) — короткие обзоры исследований

### 🔧 Инструменты

- [Google Colab](https://colab.research.google.com/) — бесплатный GPU/TPU
- [Kaggle Notebooks](https://www.kaggle.com/code) — бесплатные GPU 30 ч/нед
- [Lightning Studios](https://lightning.ai/) — free tier GPU
- [Hugging Face Spaces](https://huggingface.co/spaces) — бесплатный хостинг демо

---

[← Этап 15: парсинг](stage-15-parsing.md) · [К оглавлению](README.md)
