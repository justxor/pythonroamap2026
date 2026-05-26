# Этап 11. Data / ML / AI

> 🎯 Уверенно работать с табличными данными, собрать RAG-проект.
> ⏱ 4–6 недель.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. NumPy, pandas, Polars](#урок-1-numpy-pandas-polars)
- [Урок 2. DuckDB](#урок-2-duckdb)
- [Урок 3. RAG-пайплайн](#урок-3-rag-пайплайн)
- [Упражнение](#упражнение)

---

## Урок 1. NumPy, pandas, Polars

### NumPy

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(a * 2)        # [2 4 6 8 10]
print(a.mean())     # 3.0
print(a[a > 2])     # [3 4 5]
```

### pandas

```python
import pandas as pd

df = pd.read_csv("sales.csv")
result = df[df["amount"] > 100].groupby("region")["amount"].sum().sort_values(ascending=False)
```

### Polars (в 5-10× быстрее pandas)

```python
import polars as pl

df = pl.read_csv("sales.csv")
result = (
    df.filter(pl.col("amount") > 100)
      .group_by("region")
      .agg(pl.col("amount").sum().alias("total"))
      .sort("total", descending=True)
)
```

### Когда что

| Размер | Тул |
|---|---|
| < 100K строк | pandas |
| 100K – 100M | **Polars** или DuckDB |
| > 100M | Spark / DuckDB |

В новых проектах 2026 — **сразу Polars**.

---

## Урок 2. DuckDB

Embedded аналитическая БД, читает CSV/Parquet/JSON без импорта.

```bash
uv add duckdb
```

```python
import duckdb

# SQL по CSV
duckdb.sql("""
    SELECT region, SUM(amount) AS total
    FROM 'sales.csv'
    WHERE amount > 100
    GROUP BY region
    ORDER BY total DESC
""").show()

# JOIN двух CSV
duckdb.sql("""
    SELECT u.name, SUM(o.amount) AS revenue
    FROM 'users.csv' u
    JOIN 'orders.csv' o ON o.user_id = u.id
    GROUP BY u.name
""").show()

# С Polars (через Arrow, без копирования)
import polars as pl
df = pl.read_csv("sales.csv")
result = duckdb.sql("SELECT region, SUM(amount) FROM df GROUP BY region").pl()
```

---

## Урок 3. RAG-пайплайн

**Retrieval-Augmented Generation**: LLM получает ответ из внешней базы знаний.

```python
import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 1. Индексация
docs = ["Python — язык программирования.", "FastAPI — фреймворк."]
doc_vecs = embedder.encode(docs)

# 2. Поиск через косинусное сходство
def search(query: str, k: int = 2) -> list[str]:
    qv = embedder.encode([query])
    sims = doc_vecs @ qv[0] / (np.linalg.norm(doc_vecs, axis=1) * np.linalg.norm(qv[0]))
    top = np.argsort(-sims)[:k]
    return [docs[i] for i in top]

# 3. Генерация
def answer(query: str) -> str:
    ctx = "\n".join(search(query))
    prompt = f"Контекст:\n{ctx}\n\nВопрос: {query}"
    return llm_call(prompt)
```

### Для продакшна

- Vector DB: `pgvector`, Qdrant, Weaviate.
- Chunking документов ~500 токенов с overlap.
- Rerank через cross-encoder.
- Libraries: **LlamaIndex** или **LangChain** или **DSPy**.

---

## Упражнение. RAG-бот по своей документации

1. Возьми папку с `.md` файлами (например, этот roadmap).
2. Разбей на чанки ~500 символов.
3. Эмбеддинги через `sentence-transformers`.
4. Сохрани в Qdrant или pgvector.
5. CLI: `python ask.py "Что такое TaskGroup?"` → ответ с цитатой.
6. Бонус: обернуть в FastAPI.

Стек:

```
sentence-transformers
qdrant-client  # или pgvector
fastapi
```

---

## Чеклист и ресурсы

- [ ] Освоил Polars (понимаю выгоду vs pandas)
- [ ] Собрал работающий RAG-бот
- [ ] Понимаю векторные эмбеддинги
- [ ] Знаю cosine similarity
- [ ] Прошёл 1 курс на Kaggle Learn
- [ ] Запушил Kaggle-решение

Ресурсы:
- 📘 [«Python Data Science Handbook» — VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/) — free
- 📘 [«From Python to NumPy»](https://www.labri.fr/perso/nrougier/from-python-to-numpy/) — free
- 📘 [Polars user guide](https://docs.pola.rs/)
- 📘 [DuckDB docs](https://duckdb.org/docs/)
- 🎥 [3Blue1Brown — Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- 📘 [«Dive into Deep Learning»](https://d2l.ai/) — free book
- 📘 [Hugging Face Course](https://huggingface.co/learn) — free
- 📘 [Fast.ai](https://course.fast.ai/) — free
- 📘 [Kaggle Learn](https://www.kaggle.com/learn)
- 📝 [Sebastian Raschka magazine](https://magazine.sebastianraschka.com/)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 10](stage-10-databases.md) · [К оглавлению](README.md) · [Этап 12 →](stage-12-devops.md)
