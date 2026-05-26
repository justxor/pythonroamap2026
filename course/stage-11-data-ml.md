# Этап 11. Data & ML — NumPy, Polars, DuckDB, scikit-learn, RAG/LLM

> ⏱ Время: 4 недели  
> 🎯 Цель: уверенно работать с табличными данными, делать векторные вычисления, тренировать классические ML-модели и собрать минимальный RAG (Retrieval-Augmented Generation) на LLM.

---

## 📘 Урок 11.1 — Стек 2026

```
┌──────────────────────────────────────────────┐
│  Полёт мысли:                                │
│  CSV/Parquet/JSON ──► Polars / DuckDB        │
│            │                                 │
│            ▼                                 │
│       NumPy / scikit-learn / PyTorch         │
│            │                                 │
│            ▼                                 │
│       Plotly / Matplotlib / Streamlit        │
└──────────────────────────────────────────────┘
```

В 2026 **Polars** и **DuckDB** часто заменяют pandas: быстрее, lazy, меньше памяти. Pandas жив, но новые проекты лучше начинать с Polars.

```bash
uv add polars duckdb numpy scikit-learn matplotlib
```

---

## 📘 Урок 11.2 — NumPy: вектор вместо цикла

```python
import numpy as np

a = np.arange(1_000_000)
b = a * 2                        # ~100x быстрее, чем list comprehension
print(a.dtype, a.shape, a.nbytes)

# Broadcasting
m = np.arange(12).reshape(3, 4)
m + np.array([10, 20, 30, 40])   # прибавится к каждой строке

# Маски
m[m > 5]                          # все элементы > 5
```

**Главный приём:** избегай Python-циклов. Если пишешь `for` по массиву — почти всегда есть векторный аналог.

---

## 📘 Урок 11.3 — Polars: pandas-killer

```python
import polars as pl

df = pl.read_csv("sales.csv")

# Eager API (как pandas)
result = (
    df.filter(pl.col("amount") > 0)
      .group_by("country")
      .agg(pl.col("amount").sum().alias("total"))
      .sort("total", descending=True)
)

# Lazy API — план оптимизируется перед выполнением
plan = (
    pl.scan_csv("sales.csv")
      .filter(pl.col("amount") > 0)
      .group_by("country")
      .agg(pl.col("amount").sum())
)
result = plan.collect()
print(plan.explain())   # план запроса!
```

Polars использует все ядра CPU автоматически. Для файлов > RAM используй `scan_parquet` + `sink_parquet`.

---

## 📘 Урок 11.4 — DuckDB: SQL поверх Polars/CSV/Parquet

```python
import duckdb

# Без БД, просто SQL над файлами
con = duckdb.connect()
con.sql("""
    SELECT country, SUM(amount) AS total
    FROM read_parquet('sales/*.parquet')
    WHERE amount > 0
    GROUP BY country
    ORDER BY total DESC
""").pl()   # → Polars DataFrame
```

DuckDB — это SQLite для аналитики. Колоночный, векторизованный, поддерживает Parquet/CSV/JSON напрямую. **Идеален для ad-hoc анализа.**

---

## 📘 Урок 11.5 — scikit-learn: классический ML

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])
pipe.fit(Xtr, ytr)
print(classification_report(yte, pipe.predict(Xte)))
```

**Ключевые идеи:**
- Всегда отделяй train/test/val. Никаких "проверим на train".
- Используй `Pipeline` — иначе обязательно протечёт scaler из train в test.
- Метрики выбирай по задаче: `accuracy` ≠ `f1` ≠ `roc_auc`.
- Делай cross-validation (`cross_val_score`).

---

## 📘 Урок 11.6 — Воспроизводимость

```python
import numpy as np, random, os
SEED = 42
random.seed(SEED); np.random.seed(SEED); os.environ["PYTHONHASHSEED"] = str(SEED)
```

- Зафиксируй версии (`uv.lock`).
- Логи запусков (mlflow / wandb / простой JSON).
- Не коммить датасеты в git — `dvc`, S3, HuggingFace Datasets.

---

## 📘 Урок 11.7 — Введение в нейросети (на пальцах)

Нейросеть = композиция линейных слоёв + нелинейностей. Обучается градиентным спуском.

```python
# мини-пример с PyTorch (если ставил torch)
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(4, 16), nn.ReLU(),
    nn.Linear(16, 3),
)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()
# обучающий цикл: forward → loss → backward → step
```

Если не идёшь в DL — достаточно понимать на уровне идеи. Для большинства задач 2026 хватает gradient boosting (XGBoost/LightGBM/CatBoost).

---

## 📘 Урок 11.8 — Embeddings и векторный поиск

Embedding = вектор фиксированной длины, кодирующий смысл текста/картинки.

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("intfloat/multilingual-e5-small")
vec = model.encode(["Привет, мир"])
print(vec.shape)  # (1, 384)
```

Косинусное сходство:
```python
import numpy as np
def cos(a, b): return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

Векторные БД (бесплатные): **Qdrant**, **Chroma**, **Weaviate**, **pgvector** (расширение Postgres).

---

## 📘 Урок 11.9 — Мини-RAG за 50 строк

```python
from sentence_transformers import SentenceTransformer
import numpy as np

docs = ["Python — язык программирования",
        "FastAPI — фреймворк для API на Python",
        "Polars — быстрая альтернатива pandas"]

model = SentenceTransformer("intfloat/multilingual-e5-small")
emb = model.encode(["passage: " + d for d in docs])

def retrieve(query: str, k: int = 2) -> list[str]:
    q = model.encode(["query: " + query])[0]
    scores = emb @ q / (np.linalg.norm(emb, axis=1) * np.linalg.norm(q))
    top = np.argsort(-scores)[:k]
    return [docs[i] for i in top]

print(retrieve("чем заменить pandas"))
# → ["Polars — быстрая альтернатива pandas", ...]
```

Дальше: подставляешь найденные фрагменты в промпт LLM (`openai`/`anthropic`/локальная через `ollama`) → ответ с цитатами.

---

## 🛠 Упражнения

### Упражнение 11.1 — EDA
Скачай датасет [Titanic с Kaggle](https://www.kaggle.com/c/titanic). Через Polars:
1. Доля выживших по полу/классу.
2. Средний возраст по классу.
3. Корреляция `Age` ↔ `Fare`.

### Упражнение 11.2 — DuckDB SQL
К тому же датасету: ответь на 3 вопроса из 11.1, но через DuckDB SQL.

### Упражнение 11.3 — Классификатор
Натренируй `LogisticRegression` и `RandomForestClassifier` на Titanic. Сравни `accuracy`, `f1`. Используй `Pipeline`. Не забудь cross-validation.

### Упражнение 11.4 — RAG
Возьми 20 статей из Wikipedia (любая тема). Сделай embeddings, реализуй поиск top-3. Бонус: подключи LLM (ollama llama3 локально) и пусть отвечает по найденному контексту.

---

## ✅ Решение 11.1 (фрагмент)

```python
import polars as pl
df = pl.read_csv("train.csv")

# Выживаемость по полу
print(df.group_by("Sex").agg(pl.col("Survived").mean().alias("rate")))

# Средний возраст по классу
print(df.group_by("Pclass").agg(pl.col("Age").mean().alias("avg_age")).sort("Pclass"))

# Корреляция
print(df.select(pl.corr("Age", "Fare")))
```

---

## 📚 Бесплатные ресурсы

### 📺 Видео и книги
- 📕 [NumPy User Guide](https://numpy.org/doc/stable/user/).
- 📕 [Polars Book](https://docs.pola.rs/) — отличная документация.
- 📕 [DuckDB docs](https://duckdb.org/docs/).
- 📕 [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html).
- 📺 [StatQuest](https://www.youtube.com/@statquest) — ML на пальцах.
- 📺 [3Blue1Brown — Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi).
- 📕 [HuggingFace Course](https://huggingface.co/learn) — бесплатно про трансформеры и RAG.

### 💬 Telegram-каналы (особенно важно на этом этапе)
- 🔥 **[@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — must-read для этого этапа: ежедневный поток практических примеров кода по AI/ML/Big Data, разборы моделей, ноутбуки, бенчмарки, свежие репозитории и статьи.
- 🐍 **[@pythonl](https://t.me/pythonl)** — общий канал по Python.
- 📚 **[Папка лучших ресурсов 🎁](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка каналов по Python, ML, DS и инфраструктуре. Один клик — готовая лента.

---

## ☑ Чеклист этапа

- [ ] Векторизую через NumPy/Polars вместо ручных циклов.
- [ ] Использую lazy API Polars для больших файлов.
- [ ] Считаю SQL прямо над Parquet через DuckDB.
- [ ] Не путаю train/test, использую `Pipeline` и cross-validation.
- [ ] Понимаю, что такое embedding и косинусное сходство.
- [ ] Собрал минимальный RAG со своими документами.

---

[⬅ Этап 10](stage-10-databases.md) | [📚 Оглавление](README.md) | [Этап 12 ➡](stage-12-devops.md)
