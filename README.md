# 🐍 Python Roadmap 2026 (RU)

> Полная и актуальная дорожная карта по изучению Python с нуля до уровня Senior / архитектора.
> Ориентирована на 2026 год: Python 3.13+, free-threaded mode (PEP 703), JIT (PEP 744),
> uv/ruff экосистема, async-first подход, type-driven development и AI-инфраструктура.

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Status](https://img.shields.io/badge/status-actual%202026-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Как пользоваться роадмапом

1. Идём строго **по этапам** — не перепрыгиваем. Каждый раздел опирается на предыдущий.
2. На каждом этапе: **теория → 2–3 мини-проекта → разбор кода более опытного автора**.
3. Минимум 70% времени — **код руками**, без копипасты.
4. Ведём личный репозиторий-дневник: `learning-python/week-XX/...`
5. Каждую неделю — code review (свой старый код или чужой PR на GitHub).

---

## 🗺️ Структура

- [Этап 0. Подготовка окружения (2026 stack)](#этап-0-подготовка-окружения)
- [Этап 1. Основы языка](#этап-1-основы-языка)
- [Этап 2. Идиоматичный Python](#этап-2-идиоматичный-python)
- [Этап 3. ООП и проектирование](#этап-3-ооп-и-проектирование)
- [Этап 4. Типизация и mypy/pyright](#этап-4-типизация)
- [Этап 5. Стандартная библиотека вглубь](#этап-5-стандартная-библиотека)
- [Этап 6. Асинхронность и конкурентность](#этап-6-асинхронность-и-конкурентность)
- [Этап 7. Тестирование и качество кода](#этап-7-тестирование-и-качество-кода)
- [Этап 8. Внутренности CPython](#этап-8-внутренности-cpython)
- [Этап 9. Web-разработка](#этап-9-web-разработка)
- [Этап 10. Базы данных и ORM](#этап-10-базы-данных-и-orm)
- [Этап 11. Data / ML / AI инфраструктура](#этап-11-data--ml--ai)
- [Этап 12. DevOps и продакшн](#этап-12-devops-и-продакшн)
- [Этап 13. Архитектура и Senior-уровень](#этап-13-архитектура-и-senior)
- [📚 Книги, каналы, сообщества](#-ресурсы)

---

## Этап 0. Подготовка окружения

> Цель: настроить современный 2026-stack за один вечер.

- **Python 3.13+** (с поддержкой free-threaded build — `python3.13t`)
- **uv** — единый менеджер пакетов и venv (заменил pip/poetry/pyenv/pip-tools)
- **ruff** — линтер + форматтер (заменил black, isort, flake8, pylint)
- **pyright** или **mypy --strict** — статическая типизация
- **pytest** + **hypothesis** — тесты
- **VS Code** / **PyCharm 2026** / **Zed** + Pylance / Ruff LSP
- **Docker Desktop / OrbStack** — контейнеры
- **direnv** + `.envrc` — автоактивация окружений

📦 Практика:
- Создать `uv init`, добавить `ruff`, `pyright`, `pytest`
- Настроить `pre-commit` с ruff/pyright
- Поднять devcontainer

---

## Этап 1. Основы языка

- Синтаксис, отступы, PEP 8 (минимально, остальное доделает ruff)
- Числа, строки (включая f-strings с `=`, `:#x`), bytes, bytearray
- Коллекции: list, tuple, set, frozenset, dict (вставка/упорядоченность)
- Управляющие конструкции, `match/case` (structural pattern matching)
- Функции: позиционные/именованные, `*args`, `**kwargs`, `/`, `*`
- Области видимости (LEGB), замыкания
- Исключения, `try/except/else/finally`, `raise ... from`
- Контекстные менеджеры (`with`, `contextlib`)

🛠 Мини-проекты:
1. CLI-калькулятор с поддержкой выражений (`argparse` + `match`)
2. Парсер CSV → JSON без сторонних библиотек
3. Игра «Угадай число» с историей попыток в файле

---

## Этап 2. Идиоматичный Python

- Итераторы, генераторы, `yield from`
- Comprehensions (list/dict/set/gen)
- `itertools`, `functools` (`cache`, `partial`, `reduce`, `singledispatch`)
- Распаковка, walrus `:=`, тернарники
- EAFP vs LBYL
- `dataclasses`, `attrs`, namedtuples — когда что
- Чистый функциональный стиль: иммутабельность, `functools.reduce`

🛠 Практика: переписать «грязный» процедурный код в идиоматичный, замерить ruff-сложность.

---

## Этап 3. ООП и проектирование

- Классы, `__init__`, `__new__`, `__slots__`
- Наследование, MRO, `super()`, миксины
- Магические методы (dunder): `__repr__`, `__eq__`, `__hash__`, `__iter__`, `__enter__`
- Дескрипторы и `property`
- Метаклассы (понимать, но почти не использовать)
- Protocol-based ООП (duck typing + `typing.Protocol`)
- ABC (`abc.ABC`, `abstractmethod`)
- Принципы **SOLID**, **GRASP**
- Паттерны GoF на Python (Strategy, Factory, Observer, Adapter, Repository)

🛠 Проект: библиотека для работы с геометрией — фигуры через `Protocol`, без жёсткой иерархии.

---

## Этап 4. Типизация

> В 2026 типизация — это не опция, это стандарт.

- `typing` модуль: `list[int]`, `dict[str, T]`, `Callable`, `Iterable`
- Generics (PEP 695: `class Stack[T]: ...`)
- `TypeVar`, `ParamSpec`, `Concatenate`
- `Protocol`, structural subtyping
- `Literal`, `Final`, `TypedDict`, `NotRequired`
- `Annotated`, метаданные для FastAPI/Pydantic
- `typing.Self`, `override`, `assert_type`, `reveal_type`
- pyright strict mode, `# type: ignore[code]`
- Pydantic v2 как runtime-валидация

🛠 Практика: перевести проект из этапа 3 на `pyright --strict` без `Any`.

---

## Этап 5. Стандартная библиотека

Темы, которые нужно знать наизусть:

- `pathlib` (никаких `os.path`)
- `collections` (`Counter`, `defaultdict`, `deque`, `ChainMap`)
- `dataclasses`, `enum` (включая `StrEnum`)
- `datetime`, `zoneinfo`, `calendar`
- `re` (и базово `regex` для unicode)
- `json`, `tomllib` (стандарт с 3.11), `csv`
- `subprocess`, `shutil`, `tempfile`
- `logging` (конфиг через dictConfig)
- `argparse` / `typer` / `click`
- `concurrent.futures`
- `sqlite3`, `pickle`, `shelve`
- `secrets`, `hashlib`, `hmac`

🛠 Проект: backup-утилита (pathlib + tarfile + logging + argparse).

---

## Этап 6. Асинхронность и конкурентность

> Самая важная тема 2026 — после free-threaded mode.

- Модель GIL и free-threaded Python (PEP 703)
- Потоки (`threading`) и когда они реально полезны после 3.13t
- Процессы (`multiprocessing`, `concurrent.futures.ProcessPoolExecutor`)
- **asyncio**: event loop, `await`, `asyncio.TaskGroup`, `asyncio.timeout`
- Structured concurrency, `anyio`, `trio`
- async-контекстные менеджеры, async-итераторы
- `aiohttp`, `httpx`, `aiofiles`, `asyncpg`
- Очереди задач: `arq`, `dramatiq`, `taskiq`, Celery 5
- Backpressure, отмена задач, тайм-ауты

🛠 Проект: асинхронный краулер на 1000 URL с лимитом, ретраями и метриками.

---

## Этап 7. Тестирование и качество кода

- pytest: фикстуры, параметризация, маркеры, `conftest.py`
- `pytest-asyncio`, `pytest-mock`, `pytest-cov`, `pytest-xdist`
- **Hypothesis** — property-based testing
- Моки, стабы, фейки, TestContainers
- Покрытие 80%+ без культа цифры
- Mutation testing (`mutmut`)
- Линтеры: ruff, pyright, bandit (security), vulture (dead code)
- pre-commit + CI (GitHub Actions)

🛠 Практика: добавить hypothesis-тесты к проекту из этапа 5.

---

## Этап 8. Внутренности CPython

- Объектная модель: всё — объект, `PyObject`
- Reference counting + GC (циклический сборщик)
- Байткод, `dis`, peephole-оптимизации
- Specializing Adaptive Interpreter (PEP 659)
- JIT в 3.13+ (PEP 744) — что ускоряется, а что нет
- GIL: что это, как работает, как убрали (PEP 703)
- C-API на пальцах, чем отличаются CPython / PyPy / GraalPy
- Профилирование: `cProfile`, `py-spy`, `scalene`, `memray`

🛠 Проект: оптимизировать «медленный» скрипт в 10×, замерить `py-spy`.

---

## Этап 9. Web-разработка

Базис:
- HTTP/1.1, HTTP/2, HTTP/3, WebSockets, SSE
- REST, gRPC, GraphQL (strawberry), tRPC-аналоги

Фреймворки 2026:
- **FastAPI** — основной выбор (async, Pydantic, OpenAPI)
- **Litestar** — конкурент FastAPI с DI
- **Django 5.x** — для крупных монолитов, async views
- **Starlette** — фундамент
- **Granian** / **uvicorn** / **hypercorn** — ASGI-сервера

Дополнительно:
- Аутентификация: JWT, OAuth2, OIDC, PASETO
- Кеширование: Redis, dragonfly, in-memory
- Rate limiting, CORS, CSRF

🛠 Проект: SaaS-API «task tracker» на FastAPI + Postgres + Redis + JWT.

---

## Этап 10. Базы данных и ORM

- SQL: JOIN'ы, индексы, EXPLAIN ANALYZE, оконные функции
- PostgreSQL 17+ как стандарт
- **SQLAlchemy 2.x** (Core + ORM, async)
- **SQLModel**, **Tortoise**, **Piccolo**
- Миграции: Alembic
- Connection pooling, PgBouncer
- NoSQL: Redis, MongoDB, ClickHouse (для аналитики)
- Поиск: Meilisearch / Typesense / Elasticsearch

🛠 Проект: дашборд аналитики поверх ClickHouse + FastAPI.

---

## Этап 11. Data / ML / AI

> Python в 2026 — это де-факто язык AI-инфраструктуры.

- **NumPy 2.x**, **pandas 2.x** (Arrow backend), **Polars** (must-have)
- **DuckDB** — embedded аналитика
- Визуализация: **plotly**, **altair**, **matplotlib** (для отчётов)
- Jupyter, marimo (реактивные ноутбуки)
- ML: scikit-learn, XGBoost, LightGBM
- DL: PyTorch 2.x, JAX
- LLM-стек: **LangChain / LlamaIndex / Haystack / DSPy**
- Vector DB: pgvector, Qdrant, Weaviate
- MLOps: MLflow, Weights & Biases, Prefect, Dagster

🛠 Проект: RAG-бот по своей документации (FastAPI + pgvector + LLM API).

---

## Этап 12. DevOps и продакшн

- **uv** + lock-файлы, reproducible builds
- Multi-stage Docker (distroless / chainguard)
- Конфиги: pydantic-settings, dynaconf, переменные окружения, 12-factor
- Логи структурированные: **structlog**, JSON-логи
- Observability: **OpenTelemetry**, Prometheus, Grafana, Sentry
- CI/CD: GitHub Actions, GitLab CI
- IaC: Terraform / Pulumi (на Python)
- Kubernetes базово: Deployment, Service, HPA
- Безопасность: bandit, pip-audit, SBOM (cyclonedx)

🛠 Практика: задеплоить проект из этапа 9 в k8s с метриками и трейсами.

---

## Этап 13. Архитектура и Senior

- Clean Architecture / Hexagonal / Ports & Adapters на Python
- DDD: агрегаты, value objects, репозитории, application services
- CQRS, Event Sourcing
- Сообщения: Kafka (aiokafka, faststream), NATS, RabbitMQ
- Saga, Outbox pattern
- Монолит → модульный монолит → микросервисы (без культа)
- Перформанс: профилирование, кеширование, batching, vectorization
- Когда **не** Python: Rust/Go-вставки через PyO3, ctypes, cffi
- Code review, mentoring, ADR (Architecture Decision Records)

🛠 Финал: спроектировать и реализовать модульный монолит «маркетплейс» с DDD-структурой.

---

## 📚 Ресурсы

### Книги (2024–2026)
- *Fluent Python, 2nd ed.* — Luciano Ramalho
- *Python Concurrency with asyncio* — Matthew Fowler
- *Architecture Patterns with Python* — Percival & Gregory
- *Robust Python* — Patrick Viafore
- *High Performance Python, 3rd ed.* — Gorelick & Ozsvald
- *CPython Internals* — Anthony Shaw

### Документация
- https://docs.python.org/3/
- https://peps.python.org/
- https://docs.astral.sh/ruff/ , https://docs.astral.sh/uv/

### YouTube / блоги
- mCoding, ArjanCodes, Anthony Sottile, Sebastián Ramírez (tiangolo), Trey Hunner
- Real Python, PyCoder's Weekly, Python Bytes

### Сообщества
- r/Python, r/learnpython
- Python Discord (discord.gg/python)

---

## ✅ Чеклист готовности к Middle

- [ ] Знаю отличие `__new__` от `__init__`
- [ ] Объясню GIL и free-threaded mode
- [ ] Пишу `async`-код без race-conditions
- [ ] Прохожу `pyright --strict` без `Any`
- [ ] Покрываю код тестами + hypothesis
- [ ] Понимаю SQL `EXPLAIN`
- [ ] Деплоил Python в Docker/k8s
- [ ] Читал минимум 3 книги из списка
- [ ] Сделал 5+ pet-проектов из roadmap

---

## 🤝 Контрибьют

PR'ы приветствуются: исправления, новые ресурсы 2026, переводы.

## 📜 Лицензия

MIT
