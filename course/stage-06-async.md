# Этап 6. Асинхронность и конкурентность

> 🎯 Не путать concurrency и parallelism. Уверенно писать async-код без race-conditions.
> ⏱ 4 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. GIL, потоки, процессы](#урок-1-gil-потоки-процессы)
- [Урок 2. asyncio с нуля](#урок-2-asyncio-с-нуля)
- [Урок 3. TaskGroup и structured concurrency](#урок-3-taskgroup-и-structured-concurrency)
- [Урок 4. httpx — async HTTP](#урок-4-httpx--async-http)
- [Урок 5. Semaphore, timeout, retry](#урок-5-semaphore-timeout-retry)
- [Упражнения](#упражнения)

---

## Урок 1. GIL, потоки, процессы

- **GIL** — в каждый момент один поток исполняет Python-байткод.
- На CPython 3.13 GIL пока есть. PEP 703 даёт `python3.13t` без GIL.

### Когда что

| Задача | Решение |
|---|---|
| 1000 HTTP-запросов | `asyncio` |
| Сжатие 1000 картинок | `ProcessPoolExecutor` |
| Парсинг 100 CSV | `ProcessPoolExecutor` |
| Чтение/запись файлов | `asyncio` или `threading` |
| Realtime-сервер | `asyncio` |

### ProcessPoolExecutor (CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor

def heavy(n: int) -> int:
    return sum(i*i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(heavy, [10_000_000] * 8))
    print(sum(results))
```

---

## Урок 2. asyncio с нуля

```python
import asyncio

async def say_hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")

asyncio.run(say_hello())
```

### Параллельно через gather

```python
async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    results = await asyncio.gather(
        fetch("A", 1), fetch("B", 2), fetch("C", 1),
    )
    print(results)
```

### Создание задачи

```python
async def main():
    task = asyncio.create_task(fetch("A", 2))
    print("работа параллельно...")
    await asyncio.sleep(1)
    result = await task
```

---

## Урок 3. TaskGroup и structured concurrency

### Что не так с gather

```python
# Если одна задача упала — остальные продолжают.
# Ресурсы текут, ошибки прячутся.
results = await asyncio.gather(t1, t2, t3, return_exceptions=True)
```

### TaskGroup (3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch("A", 1))
        t2 = tg.create_task(fetch("B", 2))
        t3 = tg.create_task(fetch("C", 1))
    # все гарантированно завершены
    # если одна упала — остальные отменены, ошибки в ExceptionGroup
    print(t1.result(), t2.result(), t3.result())
```

### ExceptionGroup и except*

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(bad1())
        tg.create_task(bad2())
except* ValueError as eg:
    print("ValueErrors:", eg.exceptions)
except* TimeoutError as eg:
    print("Timeouts:", eg.exceptions)
```

### Async-итераторы

```python
class Counter:
    def __init__(self, n: int):
        self.n = n; self.i = 0
    def __aiter__(self): return self
    async def __anext__(self) -> int:
        if self.i >= self.n: raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.i += 1
        return self.i

async def main():
    async for x in Counter(5):
        print(x)
```

---

## Урок 4. httpx — async HTTP

```bash
uv add httpx
```

### Sync и async

```python
import httpx

# sync
r = httpx.get("https://example.com", timeout=5)
print(r.status_code, len(r.content))

# async
import asyncio
async def main():
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get("https://example.com")
        print(r.status_code)
asyncio.run(main())
```

### Параллельные запросы

```python
async def fetch(client, url):
    r = await client.get(url)
    return len(r.content)

async def main():
    urls = ["https://example.com"] * 20
    async with httpx.AsyncClient(timeout=10) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch(client, u)) for u in urls]
    print("total:", sum(t.result() for t in tasks))
```

### Headers, query, JSON

```python
r = await client.get(
    "https://api.example.com/users",
    headers={"Authorization": "Bearer ..."},
    params={"limit": 10},
)
data = r.json()

r = await client.post("/users", json={"name": "Anna"})
```

---

## Урок 5. Semaphore, timeout, retry

### Semaphore — ограничение параллелизма

```python
import asyncio

async def worker(sem, i):
    async with sem:
        await asyncio.sleep(1)
        print(f"done {i}")

async def main():
    sem = asyncio.Semaphore(5)   # максимум 5 одновременно
    async with asyncio.TaskGroup() as tg:
        for i in range(20):
            tg.create_task(worker(sem, i))

asyncio.run(main())
```

### Timeout (3.11+)

```python
async def main():
    try:
        async with asyncio.timeout(1):
            await long_call()
    except TimeoutError:
        print("too slow")
```

### Retry с экспоненциальным бэкоффом

```python
import asyncio, random
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")

async def with_retry(
    fn: Callable[[], Awaitable[T]], *,
    attempts: int = 5, base: float = 0.2, max_delay: float = 5.0,
) -> T:
    for i in range(1, attempts + 1):
        try:
            return await fn()
        except Exception as e:
            if i == attempts: raise
            delay = min(base * (2 ** (i-1)) * (1 + random.random()), max_delay)
            print(f"retry {i}: {e}, sleep {delay:.2f}")
            await asyncio.sleep(delay)
    raise RuntimeError("unreachable")
```

### Отмена задачи

```python
async def main():
    task = asyncio.create_task(long_call())
    await asyncio.sleep(1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled cleanly")
```

Внутри async функции обязательно ловите CancelledError если нужен cleanup.

---

## Упражнения

### Упражнение 1. Async-краулер

`crawler.py`:
1. Принимает файл со списком URL.
2. Лимит 20 одновременно.
3. JSON-отчёт `[{"url":"...","status":200,"size":123,"ms":45}, ...]`.
4. TaskGroup + Semaphore + asyncio.timeout(10).
5. Retry 3 раза при сетевых ошибках.

#### Решение

```python
"""crawler.py"""
import argparse, asyncio, json, logging
from pathlib import Path
from time import perf_counter
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("crawler")


async def fetch_one(client, sem, url):
    async with sem:
        start = perf_counter()
        for attempt in range(3):
            try:
                async with asyncio.timeout(10):
                    r = await client.get(url, follow_redirects=True)
                ms = int((perf_counter() - start) * 1000)
                log.info("%s %d %d %dms", url, r.status_code, len(r.content), ms)
                return {"url": url, "status": r.status_code, "size": len(r.content), "ms": ms}
            except (httpx.HTTPError, TimeoutError) as e:
                log.warning("attempt %d %s: %s", attempt + 1, url, e)
                await asyncio.sleep(2 ** attempt)
        return {"url": url, "status": None, "size": 0, "ms": 0, "error": "max retries"}


async def crawl(urls, concurrency=20):
    sem = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(client, sem, u)) for u in urls]
    return [t.result() for t in tasks]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("urls", type=Path)
    p.add_argument("--out", type=Path, default=Path("crawl-report.json"))
    p.add_argument("--concurrency", type=int, default=20)
    args = p.parse_args()
    urls = [l.strip() for l in args.urls.read_text().splitlines() if l.strip()]
    results = asyncio.run(crawl(urls, args.concurrency))
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

### Упражнение 2. Bulk HTTP с лимитом

Функция `bulk_get(urls, *, concurrency, timeout)`:
- Возвращает ответы **в том же порядке**.
- При ошибке — None.

#### Решение

```python
import asyncio
import httpx

async def _one(client, sem, url, timeout):
    async with sem:
        try:
            async with asyncio.timeout(timeout):
                return await client.get(url, follow_redirects=True)
        except (httpx.HTTPError, TimeoutError):
            return None

async def bulk_get(urls, *, concurrency=10, timeout=10.0):
    sem = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*(_one(client, sem, u, timeout) for u in urls))
```

---

## Чеклист и ресурсы

- [ ] Объясняю concurrency vs parallelism
- [ ] Пишу async через TaskGroup, не gather
- [ ] Применяю asyncio.timeout и Semaphore
- [ ] Реализовал retry с экспоненциальным бэкоффом
- [ ] Понимаю, когда asyncio, а когда ProcessPool
- [ ] Корректно обрабатываю CancelledError

Ресурсы:

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**
- 📘 [Real Python — Async IO Walkthrough](https://realpython.com/async-io-python/)
- 📘 [Trio docs](https://trio.readthedocs.io/) — structured concurrency
- 📝 [Nathaniel Smith — structured concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)
- 🎥 [David Beazley — Python Concurrency](https://www.youtube.com/watch?v=MCs5OvhV9S4)
- 📘 [PEP 703](https://peps.python.org/pep-0703/)
- 📘 [httpx docs](https://www.python-httpx.org/)
- 🎥 [mCoding — async/await](https://www.youtube.com/watch?v=GpqAQxH1Afc)
- 💬 [t.me/pythonl](https://t.me/pythonl) и [t.me/async_python](https://t.me/async_python)

---

[← Этап 5](stage-05-stdlib.md) · [К оглавлению](README.md) · [Этап 7 →](stage-07-testing.md)
