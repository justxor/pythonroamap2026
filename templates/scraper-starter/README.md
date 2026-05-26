# 🕸 scraper-starter — production-ready Python scraper (2026)

> Минимальный, но реальный шаблон асинхронного веб-скрапера 2026 года. Получаешь всё из коробки: HTTP-клиент, парсер, ретраи, rate-limit, прокси, хранение в Parquet, логи, Docker, CI.

---

## 🧰 Стек

| Слой | Инструмент |
|---|---|
| Runtime | Python 3.13 |
| Package manager | `uv` |
| HTTP | `httpx` (async, HTTP/2) |
| HTML | `selectolax` |
| Retry | `tenacity` |
| Rate-limit | `aiolimiter` |
| Logs | `structlog` |
| Config | `pydantic-settings` |
| Storage | `polars` + Parquet |
| CLI | `typer` |
| Tests | `pytest` + `pytest-asyncio` + `respx` |
| Lint/Format | `ruff` |
| Types | `pyright --strict` |
| Container | Docker (multi-stage, distroless) |
| CI | GitHub Actions |

---

## 📁 Структура

```
scraper-starter/
├─ pyproject.toml             — зависимости, ruff, pyright
├─ .env.example               — пример конфига
├─ Dockerfile                 — multi-stage сборка
├─ docker-compose.yml         — приложение + Redis (для очереди)
├─ src/scraper/
│  ├─ __init__.py
│  ├─ main.py                 — CLI вход
│  ├─ config.py               — настройки (pydantic-settings)
│  ├─ client.py               — httpx клиент + retry + rate-limit
│  ├─ parser.py               — selectolax парсинг
│  ├─ storage.py              — сохранение в Parquet
│  ├─ models.py               — pydantic схемы
│  └─ logging_setup.py        — structlog JSON
├─ tests/
│  ├─ test_client.py
│  └─ test_parser.py
└─ .github/workflows/ci.yml
```

---

## 🚀 Quick start

```bash
# 1. Установи uv (один раз)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Синхронизируй зависимости
uv sync

# 3. Настрой конфиг
cp .env.example .env

# 4. Запусти скрапер
uv run scraper crawl --urls-file urls.txt --out data/result.parquet

# 5. Проверь результат
uv run python -c "import polars as pl; print(pl.read_parquet('data/result.parquet').head())"
```

---

## 🐳 Docker

```bash
docker build -t scraper-starter .
docker run --rm -v $(pwd)/data:/app/data scraper-starter crawl --urls-file urls.txt
```

Или через compose:

```bash
docker compose up --build
```

---

## ✅ Что внутри

- ✅ Async-клиент с HTTP/2, ретраями (`tenacity`), rate-limit (`aiolimiter`)
- ✅ Парсинг через `selectolax` (lexbor, в 5–20× быстрее BS4)
- ✅ Структурированные JSON-логи (`structlog`)
- ✅ Pydantic v2 валидация данных
- ✅ Сохранение в Parquet + zstd compression
- ✅ Прокси из .env (опционально)
- ✅ Реальный User-Agent с контактом
- ✅ Поддержка `robots.txt`
- ✅ 100% type hints, `pyright --strict`
- ✅ Тесты с моком HTTP (`respx`)
- ✅ Multi-stage Docker (финальный образ ~80 MB)
- ✅ GitHub Actions CI (lint + types + tests)

---

## 📚 Контекст

Этот шаблон — референсная реализация к [Этапу 15. Парсинг и веб-скрапинг](../../course/stage-15-parsing.md). Начни с него любой реальный проект — и экономь часы на бойлерплейте.
