# ☕ async-starter

Шаблон для асинхронного Python-сервиса 2026 года: FastAPI + asyncpg + httpx + uvloop + structured concurrency.

## Ключевые решения

| Область    | Инструмент                              |
| ---------- | ---------------------------------------- |
| Python     | 3.13+ (включая free-threaded 3.13t)     |
| Loop       | `uvloop` (Linux/Mac)                    |
| Web        | `fastapi` + `uvicorn`                   |
| HTTP-client| `httpx` (HTTP/2, async)                  |
| БД         | `asyncpg` или `sqlalchemy[asyncio]`     |
| Concurrency| `anyio` + `asyncio.TaskGroup`           |
| Logging    | `structlog` (async-safe)                 |
| Тесты      | `pytest-anyio`                           |
| Lint/Type  | `ruff` + `pyright --strict`             |
| Deploy     | Docker (slim, non-root)                  |

## Структура

```
async-starter/
├── pyproject.toml
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── src/async_starter/
│   ├── __init__.py
│   ├── main.py            # FastAPI app + lifespan
│   ├── config.py          # pydantic-settings
│   ├── db.py              # asyncpg pool
│   ├── http_client.py     # общий httpx клиент
│   ├── tasks.py           # TaskGroup + Semaphore-паттерны
│   ├── retry.py           # @async_retry декоратор
│   └── logging_setup.py   # structlog
└── tests/
    ├── test_tasks.py
    └── test_retry.py
```

## Quickstart

```bash
uv sync
uv run uvicorn async_starter.main:app --reload
```

## Чеклист production-ready

- [ ] `uvloop.install()` в main перед `asyncio.run`.
- [ ] FastAPI lifespan создаёт и закрывает пулы.
- [ ] Все внешние вызовы с `asyncio.timeout()`.
- [ ] `Semaphore` ограничивает параллелизм.
- [ ] Graceful shutdown по SIGTERM.
- [ ] Structlog в async-mode.
- [ ] OpenTelemetry instrumentation подключён.

## Куда дальше

- 🌊 [Курс по асинхронности](../../course/async-course.md)
- 🌐 [Stage 09 — Web](../../course/stage-09-web.md)
