# 🌊 Курс по асинхронному Python 2026

> Глубокий курс по асинхронному программированию в Python 3.13+: `asyncio`, structured concurrency, `anyio`/`trio`, free-threaded Python (PEP 703), производительность и продакшен-паттерны.

---

## 📚 Бесплатные ресурсы

- 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — AI/ML и системный Python.
- 🐍 [t.me/pythonl](https://t.me/pythonl) — рубрики «задача дня», разборы async-паттернов.
- 📚 [Папка супер-полезных Python ресурсов](https://t.me/addlist/8vDUwYRGujRmZjFi) — целая подборка каналов.

---

## 🎯 Кому и зачем

Курс для тех, кто:
- путается между `asyncio.gather` / `TaskGroup` / `as_completed`;
- не понимает, почему `async` не ускоряет CPU-bound код;
- хочет писать **structured concurrency** без утечек задач;
- готовится к free-threaded Python (PEP 703) и нативной параллельности без GIL;
- строит высоконагруженные сервисы (FastAPI, websockets, очереди).

---

## 🗺️ Содержание

| #   | Урок                                                                 | Ключевые концепции                     |
| --- | -------------------------------------------------------------------- | -------------------------------------- |
| 01  | [Async-модель в 2026](#урок-01--async-модель-в-2026)                 | event loop, coroutine, awaitable       |
| 02  | [Корутины vs потоки vs процессы](#урок-02--корутины-vs-потоки-vs-процессы) | GIL, PEP 703, when to use what     |
| 03  | [Базовый asyncio](#урок-03--базовый-asyncio)                         | `run`, `sleep`, `gather`, `wait`     |
| 04  | [TaskGroup и structured concurrency](#урок-04--taskgroup-и-structured-concurrency) | PEP 654, cancel-scopes      |
| 05  | [Отмена и таймауты](#урок-05--отмена-и-таймауты)                     | `asyncio.timeout`, `CancelledError` |
| 06  | [Очереди и пайплайны](#урок-06--очереди-и-пайплайны)                 | `asyncio.Queue`, backpressure         |
| 07  | [anyio и trio](#урок-07--anyio-и-trio)                               | переносимый async, nursery             |
| 08  | [Async I/O в реальности](#урок-08--async-io-в-реальности)            | `httpx`, `aiofiles`, sockets         |
| 09  | [Async-БД](#урок-09--async-бд)                                       | `asyncpg`, `SQLAlchemy 2`, pools     |
| 10  | [Websockets и стримы](#урок-10--websockets-и-стримы)                 | `websockets`, SSE, `aiohttp`        |
| 11  | [Async + CPU: процессы и nogil](#урок-11--async--cpu-процессы-и-nogil) | `run_in_executor`, PEP 703         |
| 12  | [Производительность](#урок-12--производительность)                   | uvloop, профилирование, `asyncio.run` |
| 13  | [Тестирование async](#урок-13--тестирование-async)                   | `pytest-anyio`, fake clocks          |
| 14  | [Антипаттерны](#урок-14--антипаттерны)                               | blocking calls, fire-and-forget        |
| 15  | [Production-чеклист](#урок-15--production-чеклист)                   | observability, graceful shutdown       |

---

## Урок 01 — Async-модель в 2026

**Минимум для понимания:**

- `async def f(): ...` создаёт **корутину** — объект, который ничего не делает, пока его не `await`-нут или не запустят в loop.
- **Event loop** — однопоточный планировщик, который выполняет корутины кооперативно: задача добровольно отдаёт управление через `await`.
- **Awaitable** — всё, что можно `await`: корутины, `asyncio.Task`, `Future`, объекты с `__await__`.

```python
import asyncio

async def hello(name: str) -> str:
    await asyncio.sleep(0.1)
    return f"hi {name}"

async def main() -> None:
    print(await hello("world"))

asyncio.run(main())
```

> В 2026 `asyncio.run()` — единственный правильный entrypoint. Не создавайте loop вручную.

---

## Урок 02 — Корутины vs потоки vs процессы

| Тип          | GIL           | Когда использовать                              |
| ------------ | ------------- | ----------------------------------------------- |
| `asyncio`  | держит GIL    | I/O-bound: сеть, БД, диск, ожидание             |
| `threading`| держит GIL\* | блокирующие C-вызовы, легаси-API                |
| `multiprocessing` | свой GIL на процесс | CPU-bound: вычисления, ML, парсинг |
| **PEP 703 nogil** | GIL выключен | true parallel threads в Python 3.13t        |

\* На free-threaded билде (PEP 703, Python 3.13t) GIL можно выключить — потоки становятся настоящими параллельными.

**Правило:** если задача ждёт сеть/диск — `async`. Если считает — `ProcessPoolExecutor` или nogil-threads.

---

## Урок 03 — Базовый asyncio

```python
import asyncio

async def fetch(i: int) -> int:
    await asyncio.sleep(0.5)
    return i * 2

async def main() -> None:
    results = await asyncio.gather(*[fetch(i) for i in range(5)])
    print(results)  # [0, 2, 4, 6, 8] за ~0.5с, не 2.5с

asyncio.run(main())
```

**Шпаргалка:**
- `gather(*coros)` — параллельно, возвращает список результатов.
- `wait(tasks)` — низкоуровневый, возвращает `(done, pending)`.
- `as_completed(coros)` — итератор по мере завершения.
- `wait_for(coro, timeout)` — устарел в пользу `asyncio.timeout()`.

---

## Урок 04 — TaskGroup и structured concurrency

С Python 3.11+ — **только TaskGroup** для параллельных задач. `gather` оставлен для совместимости.

```python
import asyncio

async def worker(i: int) -> int:
    await asyncio.sleep(0.1)
    if i == 3:
        raise ValueError(f"boom {i}")
    return i

async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(worker(i)) for i in range(5)]
    print([t.result() for t in tasks])

asyncio.run(main())
```

**Почему это лучше `gather`:**
- Гарантированная отмена дочерних задач при ошибке.
- `ExceptionGroup` (PEP 654) с `except*` синтаксисом.
- Нет «осиротевших» задач — scope чётко определён `async with`.

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker(3))
        tg.create_task(worker(1))
except* ValueError as eg:
    for e in eg.exceptions:
        print("value error:", e)
```

---

## Урок 05 — Отмена и таймауты

```python
import asyncio

async def slow() -> str:
    await asyncio.sleep(10)
    return "done"

async def main() -> None:
    try:
        async with asyncio.timeout(1.0):
            await slow()
    except TimeoutError:
        print("timed out")

asyncio.run(main())
```

**Правила работы с `CancelledError`:**
1. Никогда не глотайте `CancelledError` молча — пробрасывайте дальше.
2. Cleanup в `finally`, а не в `except`.
3. `asyncio.shield(coro)` защищает критичный участок от отмены.

```python
async def critical():
    try:
        await asyncio.shield(write_to_db())
    except asyncio.CancelledError:
        raise
```

---

## Урок 06 — Очереди и пайплайны

```python
import asyncio

async def producer(q: asyncio.Queue[int]) -> None:
    for i in range(10):
        await q.put(i)
    await q.put(None)

async def consumer(q: asyncio.Queue[int]) -> None:
    while (item := await q.get()) is not None:
        print("got", item)
        q.task_done()

async def main() -> None:
    q: asyncio.Queue[int] = asyncio.Queue(maxsize=5)  # backpressure!
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(q))
        tg.create_task(consumer(q))

asyncio.run(main())
```

**`maxsize` — это backpressure.** Без него producer задавит потребителя и съест память.

---

## Урок 07 — anyio и trio

**`anyio`** — переносимый API поверх asyncio/trio. В 2026 — стандарт для библиотек (FastAPI, httpx, starlette).

```python
import anyio

async def worker(i: int) -> None:
    await anyio.sleep(0.1)
    print(i)

async def main() -> None:
    async with anyio.create_task_group() as tg:
        for i in range(5):
            tg.start_soon(worker, i)

anyio.run(main)
```

**Зачем:**
- Унифицированный API `create_task_group`.
- `CancelScope` — точечная отмена части задач.
- `anyio.from_thread` — безопасный мост sync → async.

---

## Урок 08 — Async I/O в реальности

**HTTP — `httpx`:**

```python
import httpx
import asyncio

async def fetch_all(urls: list[str]) -> list[str]:
    async with httpx.AsyncClient(timeout=10, http2=True) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(client.get(u)) for u in urls]
        return [t.result().text for t in tasks]
```

**Файлы — `aiofiles`:**

```python
import aiofiles

async def read_big(path: str) -> str:
    async with aiofiles.open(path) as f:
        return await f.read()
```

**Сокеты:** `asyncio.open_connection`, `start_server`. Для production — `aiohttp`/`fastapi` поверх `uvicorn`.

---

## Урок 09 — Async-БД

**PostgreSQL — `asyncpg` (самый быстрый драйвер):**

```python
import asyncpg

async def main() -> None:
    pool = await asyncpg.create_pool(dsn="postgresql://...", min_size=5, max_size=20)
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM users WHERE active = \$1", True)
    await pool.close()
```

**SQLAlchemy 2.x async:**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

engine = create_async_engine("postgresql+asyncpg://...", pool_size=20)

async def get_users():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.active.is_(True)))
        return result.scalars().all()
```

**Правила:**
- **Никогда** не используйте sync-драйвер из async-кода.
- Pool size = ожидаемая конкурентность, не больше `max_connections` в БД.
- Транзакции — через `async with session.begin()`.

---

## Урок 10 — Websockets и стримы

```python
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"echo: {message}")

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
```

**SSE (Server-Sent Events) в FastAPI:**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def event_stream():
    for i in range(10):
        yield f"data: {i}\n\n"
        await asyncio.sleep(1)

@app.get("/events")
async def events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

---

## Урок 11 — Async + CPU: процессы и nogil

**CPU-bound из async-кода:**

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def heavy(n: int) -> int:
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        results = await asyncio.gather(*[
            loop.run_in_executor(pool, heavy, 10_000_000)
            for _ in range(4)
        ])
    print(sum(results))

asyncio.run(main())
```

**PEP 703 — free-threaded Python:**
- Билд `python3.13t` (или новее) выключает GIL.
- Потоки становятся настоящими параллельными.
- Async + nogil-threads = новая мощная комбинация.

```bash
python3.13t -c "import sys; print(sys._is_gil_enabled())"
```

---

## Урок 12 — Производительность

**`uvloop` — drop-in замена loop (Linux/Mac), 2-4× быстрее:**

```python
import asyncio
import uvloop

uvloop.install()
asyncio.run(main())
```

**Профилирование:**
- `asyncio.run(main(), debug=True)` — варнинги о медленных корутинах.
- `py-spy record -o out.svg -- python app.py` — flamegraph без модификации кода.
- `PYTHONASYNCIODEBUG=1` — детектор blocking calls.

**Что обычно тормозит:**
1. Sync-вызов в async-коде (`requests`, `psycopg2`, `time.sleep`).
2. Слишком мелкие задачи (overhead больше работы).
3. `gather()` на 10k задач без `Semaphore`.

```python
sem = asyncio.Semaphore(50)

async def bounded(coro):
    async with sem:
        return await coro

await asyncio.gather(*[bounded(fetch(u)) for u in urls])
```

---

## Урок 13 — Тестирование async

**`pytest-anyio` (рекомендован в 2026):**

```python
import pytest
import anyio

@pytest.mark.anyio
async def test_fetch():
    result = await fetch_user(1)
    assert result.name == "Alice"

@pytest.fixture
def anyio_backend():
    return "asyncio"
```

**Fake time:**

```python
@pytest.mark.anyio
async def test_timeout():
    with pytest.raises(TimeoutError):
        async with anyio.fail_after(0.1):
            await anyio.sleep(10)
```

**Mock async:** `unittest.mock.AsyncMock` или `pytest-mock` с `AsyncMock`.

---

## Урок 14 — Антипаттерны

**❌ Sync-вызов внутри async:**
```python
async def bad():
    time.sleep(1)  # блокирует ВЕСЬ loop
    requests.get(...)  # то же самое
```
✅ `await asyncio.sleep(1)`, `httpx.AsyncClient`.

**❌ Fire-and-forget без хранения ссылки:**
```python
async def bad():
    asyncio.create_task(work())  # GC может убить
```
✅ Хранить task или использовать TaskGroup.

**❌ Глотание `CancelledError`** — нарушает контракт отмены.

**❌ Бесконечный `gather` без `Semaphore`** — съест файловые дескрипторы.

**❌ Создание loop вручную** — `asyncio.new_event_loop() + set_event_loop()` устарело. Используйте `asyncio.run()`.

---

## Урок 15 — Production-чеклист

- [ ] Все I/O-операции — async (нет `requests`, `psycopg2`, `time.sleep`).
- [ ] `asyncio.TaskGroup` (или `anyio.create_task_group`) вместо голого `gather`.
- [ ] Таймауты на все внешние вызовы (`asyncio.timeout`).
- [ ] `Semaphore` для bounded concurrency.
- [ ] `uvloop` в продакшене.
- [ ] Graceful shutdown: ловить `SIGTERM`, отменять TaskGroup, ждать дренажа.
- [ ] Connection pools закрыты в `finally`.
- [ ] Логирование без `print`: `structlog` + async handler.
- [ ] Метрики: `prometheus_client` с async exporter.
- [ ] Tracing: OpenTelemetry с asyncio instrumentation.
- [ ] Health-check эндпоинт, который реально проверяет БД/Redis.
- [ ] Тесты на отмену и таймауты (`pytest-anyio`).

---

## 🏋️ Упражнения

1. Напиши скачивалку 1000 URL с `TaskGroup` + `Semaphore(50)` + retry с exponential backoff.
2. Реализуй pub/sub поверх `asyncio.Queue` с N подписчиками.
3. Сделай rate limiter (token bucket) как async context manager.
4. Напиши websocket-чат на `websockets` с broadcast'ом.
5. Сравни бенчмарком `asyncio` vs `uvloop` vs free-threaded `python3.13t` на 10k параллельных HTTP-запросов.
6. Реализуй graceful shutdown FastAPI-сервиса: SIGTERM → стоп новых запросов → дренаж активных → закрытие пулов.
7. Напиши декоратор `@async_retry(tries=3, backoff=2.0)` со structured logging.
8. Сделай pipeline producer → transformer → consumer на трёх `Queue` с backpressure.

---

## 📚 Бесплатные ресурсы

**📌 Telegram (в порядке полезности для async):**
1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — продвинутый Python, системные темы.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — «задача дня», async-разборы.
3. 📚 [Папка Python-ресурсов](https://t.me/addlist/8vDUwYRGujRmZjFi) — целая подборка каналов.

**Документация:**
- [asyncio — Python docs](https://docs.python.org/3/library/asyncio.html)
- [PEP 654 — Exception Groups](https://peps.python.org/pep-0654/)
- [PEP 703 — Making the GIL Optional](https://peps.python.org/pep-0703/)
- [anyio docs](https://anyio.readthedocs.io/)
- [trio docs](https://trio.readthedocs.io/)

**Статьи и видео:**
- [Real Python — Async IO in Python](https://realpython.com/async-io-python/)
- [Łukasz Langa — AsyncIO + Music](https://www.youtube.com/watch?v=00Cqu_giOhU) — визуальный разбор loop
- [David Beazley — Build Your Own Async](https://www.youtube.com/watch?v=Y4Gt3Xjd7G8) — как устроен loop изнутри
- [Hynek Schlawack — Production-Ready Python AsyncIO](https://hynek.me/articles/python-async-typing/)

**Инструменты:**
- [uvloop](https://github.com/MagicStack/uvloop) — быстрый event loop.
- [aiomonitor](https://github.com/aio-libs/aiomonitor) — REPL для запущенного приложения.
- [py-spy](https://github.com/benfred/py-spy) — sampling-профайлер.

---

## ⏭️ Что дальше

- 🌐 [Stage 09 — Web (FastAPI, async-стек)](stage-09-web.md)
- 🗄️ [Stage 10 — Databases (asyncpg, SQLAlchemy 2)](stage-10-databases.md)
- 🕷️ [Stage 15 — Parsing (async-скрейпинг)](stage-15-parsing.md)
- 🤖 [Stage 17 — LLM Apps (async-стриминг)](stage-17-llm-apps.md)
- 🚀 [Template: async-starter](../templates/async-starter/)

[← К содержанию курса](README.md)
