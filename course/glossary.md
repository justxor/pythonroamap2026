# 📖 Глоссарий Python 2026

> Единый словарь терминов, используемых в курсе. Все термины снабжены ссылками на этапы, где они раскрываются подробно.

## A

### async / await
Ключевые слова для написания асинхронного кода в Python. Корутины (`async def`) приостанавливаются на `await`, отдавая управление event loop'у. См. [stage-06-async](./stage-06-async.md).

### asyncio
Стандартная библиотека event loop'а. В 2026 уступает место `anyio` для библиотек, но остаётся базой. См. [stage-06-async](./stage-06-async.md).

### anyio
Структурированная конкурентность поверх asyncio/trio. Task groups, cancel scopes, корректное завершение задач. См. [stage-06-async](./stage-06-async.md).

## C

### CRDT
Conflict-free replicated data types. Используются для offline-first и реалтайм-коллаборации (Yjs/Automerge). См. [stage-13-architecture](./stage-13-architecture.md).

### curl_cffi
HTTP-клиент с TLS-fingerprint impersonation (Chrome/Safari/Edge). Обходит JA3/JA4-детект. См. [stage-15-antibot](./stage-15-antibot.md).

### crawlee-python
Высокоуровневый фреймворк скрапинга от Apify: queue, dedup, session pool, proxy rotation. См. [stage-15-parsing](./stage-15-parsing.md).

## D

### DDD / Domain-Driven Design
Подход к моделированию сложной бизнес-логики: aggregates, entities, value objects, bounded contexts. См. [stage-13-architecture](./stage-13-architecture.md).

### DuckDB
In-process OLAP-СУБД, читает Parquet/CSV напрямую. Замена pandas для аналитики. См. [stage-11-data-ml](./stage-11-data-ml.md).

## F

### FastAPI
Async web-фреймворк на Starlette + Pydantic. Стандарт REST API в 2026. См. [stage-09-web](./stage-09-web.md).

### free-threaded Python / PEP 703
Сборка Python без GIL. С 3.13 — экспериментально, с 3.14 — стабильно. См. [stage-08-cpython](./stage-08-cpython.md).

## G

### GIL
Global Interpreter Lock. Ограничивает выполнение Python-байткода одним потоком. Снимается через PEP 703. См. [stage-08-cpython](./stage-08-cpython.md).

## H

### httpx
Async HTTP-клиент. Полноценная замена requests + поддержка HTTP/2. См. [stage-15-parsing](./stage-15-parsing.md).

### hexagonal / ports & adapters
Архитектура с изоляцией домена от инфраструктуры через интерфейсы (ports). См. [stage-13-architecture](./stage-13-architecture.md).

## J

### JA3 / JA4
TLS-fingerprint клиента (cipher suites, extensions). Используется антибот-системами. См. [stage-15-antibot](./stage-15-antibot.md).

### JIT / PEP 744
Just-in-time компилятор в CPython 3.13+. Ускорение горячих циклов без изменений в коде. См. [stage-08-cpython](./stage-08-cpython.md).

## L

### LangGraph / LangChain
Фреймворки для построения LLM-агентов и RAG-пайплайнов. См. [stage-14-vibecoding](./stage-14-vibecoding.md).

## M

### mypyc / Cython / Rust extensions
Способы ускорения горячего Python-кода компиляцией. См. [stage-08-cpython](./stage-08-cpython.md).

## P

### Parquet
Колоночный формат хранения данных. Сжатие zstd, predicate pushdown. См. [stage-11-data-ml](./stage-11-data-ml.md).

### Playwright
Браузерная автоматизация (Chromium/Firefox/WebKit). Замена Selenium. См. [stage-15-parsing](./stage-15-parsing.md).

### Polars
Колоночный DataFrame на Rust. Замена pandas. Lazy API, query optimizer. См. [stage-11-data-ml](./stage-11-data-ml.md).

### Pydantic v2
Валидация и сериализация на Rust-ядре (pydantic-core). См. [stage-04-typing](./stage-04-typing.md).

### pyright
Type checker от Microsoft. Строже mypy, быстрее. Стандарт строгой типизации. См. [stage-04-typing](./stage-04-typing.md).

## R

### RAG
Retrieval-Augmented Generation. Поиск релевантных чанков + LLM-генерация. См. [stage-14-vibecoding](./stage-14-vibecoding.md).

### ruff
Линтер + форматтер на Rust. Заменяет black/isort/flake8/pyupgrade. См. [stage-00-environment](./stage-00-environment.md).

## S

### SQLAlchemy 2.x async
ORM с typed-API и async-движком. См. [stage-10-databases](./stage-10-databases.md).

### selectolax
HTML-парсер на C (Modest/lexbor). В 10–20× быстрее BeautifulSoup. См. [stage-15-parsing](./stage-15-parsing.md).

### structlog
Структурное логирование (JSON-output, context binding). См. [stage-12-devops](./stage-12-devops.md).

## T

### tenacity
Библиотека ретраев (exponential backoff + jitter). См. [stage-15-parsing](./stage-15-parsing.md).

### typer
CLI-фреймворк поверх Click с типизацией. См. [stage-05-stdlib](./stage-05-stdlib.md).

## U

### uv
Менеджер пакетов и виртуальных окружений на Rust от Astral. Замена pip/poetry/pyenv. См. [stage-00-environment](./stage-00-environment.md).

## V

### vibecoding
Метод разработки в паре с LLM: формулировка намерения → итеративная генерация → ревью. См. [stage-14-vibecoding](./stage-14-vibecoding.md) и [stage-14-models-benchmark](./stage-14-models-benchmark.md).

---

## Сокращения

| Сокращение | Расшифровка |
|---|---|
| ADR | Architecture Decision Record |
| ASGI | Asynchronous Server Gateway Interface |
| CTR | Click-Through Rate (в промптах) |
| DI | Dependency Injection |
| DTO | Data Transfer Object |
| ORM | Object-Relational Mapping |
| PEP | Python Enhancement Proposal |
| SLA | Service Level Agreement |
| SLO | Service Level Objective |
| SRP | Single Responsibility Principle |

---

[← Главная курса](./README.md) · [← Корень репо](../README.md)
