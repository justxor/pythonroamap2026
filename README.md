# 🐍 Python Roadmap 2026 (RU) — расширенная версия

> Полная и **актуальная** дорожная карта по изучению Python в 2026 году: от `Hello, World` до Senior / архитектора.
> С практикой, примерами кода и **только бесплатными** ресурсами.

> Python 3.13+ • free-threaded mode (PEP 703) • JIT (PEP 744) • uv/ruff • async-first • type-driven • AI-инфраструктура

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Status](https://img.shields.io/badge/status-actual%202026-brightgreen)
![Free](https://img.shields.io/badge/resources-free-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Как пользоваться роадмапом

1. **По этапам**, не перепрыгивая. Каждый раздел опирается на предыдущий.
2. На каждом этапе: **теория → код руками → мини-проект → разбор чужого кода**.
3. Минимум 70% времени — **код руками**, без копипасты.
4. Веди репозиторий-дневник: `learning-python/week-XX/` — туда коммить решения задач.
5. Раз в неделю — code review (свой старый код или открытый PR на GitHub).
6. Каждый этап заканчивается **чеклистом** — пока не отметишь всё, не идёшь дальше.

⏱ Ориентировочный темп: **6–9 месяцев** при 2–3 часах в день до уровня уверенного Junior+/Middle.

---

## 🗺️ Содержание

- [Этап 0. Окружение 2026](#этап-0-окружение-2026)
- [Этап 1. Основы языка](#этап-1-основы-языка)
- [Этап 2. Идиоматичный Python](#этап-2-идиоматичный-python)
- [Этап 3. ООП и проектирование](#этап-3-ооп-и-проектирование)
- [Этап 4. Типизация](#этап-4-типизация)
- [Этап 5. Стандартная библиотека](#этап-5-стандартная-библиотека)
- [Этап 6. Асинхронность и конкурентность](#этап-6-асинхронность-и-конкурентность)
- [Этап 7. Тестирование и качество кода](#этап-7-тестирование-и-качество-кода)
- [Этап 8. Внутренности CPython](#этап-8-внутренности-cpython)
- [Этап 9. Web-разработка](#этап-9-web-разработка)
- [Этап 10. Базы данных и ORM](#этап-10-базы-данных-и-orm)
- [Этап 11. Data / ML / AI](#этап-11-data--ml--ai)
- [Этап 12. DevOps и продакшн](#этап-12-devops-и-продакшн)
- [Этап 13. Архитектура и Senior](#этап-13-архитектура-и-senior)
- [📚 Бесплатные ресурсы (общая подборка)](#-бесплатные-ресурсы-общая-подборка)
- [🧠 Платформы для практики](#-платформы-для-практики)
- [✅ Финальный чеклист Middle+](#-финальный-чеклист-middle)

---

## Этап 0. Окружение 2026

> Настрой стек один раз — и забудь о боли с зависимостями.

### Стек

- **Python 3.13+** — основной интерпретатор. Доп. сборка `python3.13t` для free-threaded экспериментов.
- **uv** (от Astral) — заменяет pip, pipx, venv, poetry, pyenv. В 10–100× быстрее.
- **ruff** — линтер + форматтер (заменил black + isort + flake8 + pylint).
- **pyright** или **mypy --strict** — статическая типизация.
- **pytest** + **hypothesis** — тесты.
- **pre-commit** — хуки качества до коммита.
- **direnv** + `.envrc` — автоактивация окружения.
- IDE: **VS Code** + Pylance + Ruff, либо **PyCharm 2026**, либо **Zed** + Python LSP.

### Практика

```bash
# Установка uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Новый проект
uv init my-first-project && cd my-first-project
uv python install 3.13
uv add --dev ruff pyright pytest hypothesis pre-commit
uv run ruff check .
uv run pytest
```

`pyproject.toml` минимум на 2026:

```toml
[project]
name = "my-first-project"
version = "0.1.0"
requires-python = ">=3.13"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF", "ANN", "TID"]

[tool.pyright]
typeCheckingMode = "strict"
```

### Бесплатные ресурсы

- 📘 [uv docs](https://docs.astral.sh/uv/) — официальная документация.
- 📘 [ruff docs](https://docs.astral.sh/ruff/) — правила и конфиг.
- 🎥 [ArjanCodes — Modern Python tooling](https://www.youtube.com/@ArjanCodes) — серии про uv/ruff.
- 📝 [Hynek Schlawack — Production-ready Python](https://hynek.me/articles/) — блог о современной экосистеме.

✅ Чеклист этапа 0:
- [ ] uv, ruff, pyright, pytest установлены
- [ ] Создан проект и запущен `uv run pytest`
- [ ] pre-commit с ruff и pyright настроен
- [ ] Понимаю, чем `uv sync` отличается от `pip install`

---

## Этап 1. Основы языка

> Цель: научиться писать любой алгоритм на чистом Python без сторонних библиотек.

### Темы

- Синтаксис, отступы, PEP 8.
- Числа (`int`, `float`, `Decimal`, `Fraction`), строки, bytes, bytearray.
- f-strings: `f"{x=}"`, `f"{n:_>10.2f}"`.
- Коллекции: list, tuple, set, frozenset, dict (сохраняет порядок вставки с 3.7).
- `match/case` (structural pattern matching).
- Функции: `*args`, `**kwargs`, `/` (positional-only), `*` (keyword-only).
- LEGB scope, замыкания, `nonlocal`, `global`.
- Исключения: `try/except/else/finally`, `raise ... from`, иерархия.
- Контекстные менеджеры (`with`, `contextlib.contextmanager`).

### Пример: structural pattern matching

```python
def handle(event: dict) -> str:
    match event:
        case {"type": "click", "x": int(x), "y": int(y)}:
            return f"click at ({x},{y})"
        case {"type": "key", "key": str(k)} if k.isalpha():
            return f"letter {k.upper()}"
        case {"type": "key"}:
            return "non-letter key"
        case _:
            return "unknown"

print(handle({"type": "click", "x": 10, "y": 20}))  # click at (10,20)
```

### Пример: контекстный менеджер

```python
from contextlib import contextmanager
from time import perf_counter

@contextmanager
def timer(label: str):
    start = perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {perf_counter() - start:.3f}s")

with timer("sum"):
    total = sum(range(10_000_000))
```

### 🛠 Мини-проекты

1. **CLI-калькулятор** с поддержкой выражений и истории (`argparse` + `match`).
2. **CSV → JSON** парсер без сторонних либ (только stdlib).
3. **«Угадай число»** с сохранением истории попыток в файл.
4. **Анализатор текста**: топ-10 слов, частота букв, среднее число слов в предложении.

### Бесплатные ресурсы

- 📘 [Официальный туториал Python](https://docs.python.org/3/tutorial/) — лучший старт.
- 📘 [Python для начинающих — pythontutor.ru](https://pythontutor.ru/) — на русском, с задачами.
- 📘 [Real Python — Python Basics](https://realpython.com/tutorials/basics/) — бесплатные статьи.
- 🎮 [CheckiO](https://checkio.org/) — задачи в виде игры.
- 🎥 [Corey Schafer — Python Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) — лучший плейлист для новичков (англ).
- 🎥 [Sentdex Python 3 Basics](https://www.youtube.com/playlist?list=PLQVvvaa0QuDeAams7fkdcwOGBpGdHpXln) — короткие видео.
- 📝 [Automate the Boring Stuff (full book online, free)](https://automatetheboringstuff.com/) — практика для начинающих.

✅ Чеклист этапа 1:
- [ ] Решил 30+ задач на pythontutor.ru / CheckiO
- [ ] Реализовал 2+ мини-проекта
- [ ] Использую f-strings и `match/case`
- [ ] Различаю изменяемые и неизменяемые типы

---

## Этап 2. Идиоматичный Python

> Цель: писать «по-питоновски». Меньше кода, больше выразительности.

### Темы

- Итераторы и генераторы (`yield`, `yield from`).
- Comprehensions (list/dict/set/generator).
- `itertools`: `chain`, `groupby`, `islice`, `product`, `combinations`, `pairwise`, `batched` (3.12+).
- `functools`: `cache`, `lru_cache`, `partial`, `reduce`, `singledispatch`, `wraps`.
- Распаковка (`a, *rest, b = ...`), walrus `:=`, тернарники.
- EAFP vs LBYL.
- `dataclasses`, `attrs`, namedtuples — когда что.
- Декораторы (с аргументами и без).

### Пример: генератор vs список

```python
# ❌ загружает всё в память
def squares_bad(n):
    return [x*x for x in range(n)]

# ✅ ленивая обработка
def squares_good(n):
    yield from (x*x for x in range(n))

for sq in squares_good(10_000_000):
    if sq > 100: break
```

### Пример: декоратор с аргументами

```python
from functools import wraps
from time import sleep, perf_counter

def retry(times: int = 3, delay: float = 0.5):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise
                    print(f"retry {attempt}: {e}")
                    sleep(delay)
        return wrapper
    return decorator

@retry(times=5, delay=0.2)
def flaky():
    import random
    if random.random() < 0.7:
        raise RuntimeError("oops")
    return "done"
```

### Пример: `itertools.batched` (3.12+)

```python
from itertools import batched

for chunk in batched(range(10), 3):
    print(chunk)
# (0,1,2) (3,4,5) (6,7,8) (9,)
```

### 🛠 Практика

- Переписать «грязный» процедурный код в идиоматичный, замерить сложность через `ruff check --statistics`.
- Реализовать декораторы: `@timed`, `@memoize`, `@deprecated`.
- Заменить все циклы накопления на comprehensions / `sum` / `any` / `all` где это уместно.

### Бесплатные ресурсы

- 📘 [Python Cookbook (David Beazley) — главы доступны](https://github.com/dabeaz/python-cookbook) — рецепты идиоматичного Python.
- 📝 [Trey Hunner blog](https://treyhunner.com/blog/) — лучшие статьи об идиомах.
- 🎥 [mCoding YouTube](https://www.youtube.com/@mCoding) — короткие видео о тонкостях языка.
- 📘 [PEP 8](https://peps.python.org/pep-0008/) и [PEP 20 — Zen of Python](https://peps.python.org/pep-0020/).
- 📝 [Itertools recipes (official)](https://docs.python.org/3/library/itertools.html#itertools-recipes) — must-read.
- 🎮 [Exercism Python Track](https://exercism.org/tracks/python) — бесплатно, с менторами.

✅ Чеклист этапа 2:
- [ ] Написал минимум 3 рабочих декоратора
- [ ] Заменяю циклы на comprehensions/itertools там, где это читабельнее
- [ ] Понимаю разницу между `@cache` и `@lru_cache`
- [ ] Знаю, почему `mutable default argument` — антипаттерн

---

## Этап 3. ООП и проектирование

> Цель: уметь проектировать гибкие и тестируемые системы.

### Темы

- Классы, `__init__`, `__new__`, `__slots__`.
- Наследование, MRO (`Cls.__mro__`), `super()`, миксины.
- Dunder-методы: `__repr__`, `__eq__`, `__hash__`, `__iter__`, `__enter__`/`__exit__`.
- Дескрипторы, `property`, `classmethod`, `staticmethod`.
- Метаклассы — понимаем, но используем редко.
- Protocol-based ООП (duck typing + `typing.Protocol`).
- ABC (`abc.ABC`, `@abstractmethod`).
- Принципы **SOLID**, **DRY**, **KISS**, **YAGNI**.
- Паттерны на Python: Strategy, Factory, Observer, Adapter, Repository, Singleton (через модуль).

### Пример: Protocol вместо ABC

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsArea(Protocol):
    def area(self) -> float: ...

class Circle:
    def __init__(self, r: float): self.r = r
    def area(self) -> float: return 3.14159 * self.r ** 2

class Square:
    def __init__(self, a: float): self.a = a
    def area(self) -> float: return self.a ** 2

def total_area(shapes: list[SupportsArea]) -> float:
    return sum(s.area() for s in shapes)

print(total_area([Circle(2), Square(3)]))  # 21.566...
```

### Пример: Strategy pattern

```python
from typing import Protocol
from dataclasses import dataclass

class PricingStrategy(Protocol):
    def price(self, base: float) -> float: ...

class NoDiscount:
    def price(self, base): return base

class PercentOff:
    def __init__(self, pct: float): self.pct = pct
    def price(self, base): return base * (1 - self.pct / 100)

@dataclass
class Order:
    items_total: float
    strategy: PricingStrategy
    def total(self) -> float:
        return self.strategy.price(self.items_total)

print(Order(100, PercentOff(20)).total())  # 80.0
```

### 🛠 Проекты

1. **Геометрия**: фигуры через `Protocol` (без иерархии классов).
2. **In-memory ORM** на 200 строк: `Repository[T]` + dataclass + сериализация в JSON.
3. **Парсер выражений** в стиле visitor-паттерна.

### Бесплатные ресурсы

- 📘 [Refactoring.guru — паттерны на Python](https://refactoring.guru/design-patterns/python) — отличные иллюстрации.
- 🎥 [ArjanCodes — Design Patterns in Python](https://www.youtube.com/playlist?list=PLC0nd42SBTaNuP4iB4L6SJlMaHE71FG6N) — современный подход.
- 📘 [Python Patterns (faif/python-patterns on GitHub)](https://github.com/faif/python-patterns) — каталог реализаций.
- 📝 [Hillel Wayne — "What every CS student needs to know"](https://www.hillelwayne.com/post/) — про дизайн.
- 📘 [SOLID на русском (Habr)](https://habr.com/ru/articles/688530/) — пять статей цикла.

✅ Чеклист этапа 3:
- [ ] Объясняю разницу между `@classmethod` и `@staticmethod`
- [ ] Реализовал минимум 5 GoF-паттернов
- [ ] Использую `Protocol` вместо ABC там, где можно
- [ ] Понимаю MRO в diamond-наследовании

---

## Этап 4. Типизация

> В 2026 типизация — стандарт. Любая команда уровня выше Junior пишет код, проходящий `pyright --strict`.

### Темы

- Базовые типы: `list[int]`, `dict[str, T]`, `Callable[[int], str]`, `Iterable`.
- Generics PEP 695: `class Stack[T]: ...`, `def first[T](xs: list[T]) -> T`.
- `TypeVar`, `ParamSpec`, `Concatenate`.
- `Protocol`, structural subtyping.
- `Literal`, `Final`, `TypedDict`, `NotRequired`, `Required`.
- `Annotated[T, ...]` — метаданные для FastAPI/Pydantic.
- `Self`, `@override`, `assert_type`, `reveal_type`.
- `pyright --strict`, `# type: ignore[code]`.
- **Pydantic v2** — runtime-валидация.

### Пример: новые generics (PEP 695)

```python
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, x: T) -> None: self._items.append(x)
    def pop(self) -> T: return self._items.pop()

def first[T](xs: list[T]) -> T | None:
    return xs[0] if xs else None

s: Stack[int] = Stack()
s.push(1); s.push(2)
```

### Пример: Pydantic v2

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int
    email: EmailStr
    age: int = Field(ge=0, le=150)
    tags: list[str] = []

# Валидация в runtime
u = User.model_validate({"id": 1, "email": "a@b.c", "age": 30})
print(u.model_dump_json())
```

### Пример: TypedDict + NotRequired

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: int
    name: str
    email: NotRequired[str]   # поле опционально

def greet(u: UserDict) -> str:
    return f"Hello, {u['name']}!"
```

### 🛠 Практика

- Перевести проект из этапа 3 на `pyright --strict` без единого `Any`.
- Написать generic-репозиторий `Repository[T]` с CRUD.
- Описать API-схему через TypedDict + Pydantic.

### Бесплатные ресурсы

- 📘 [typing — official docs](https://docs.python.org/3/library/typing.html).
- 📘 [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) — лучший конспект.
- 📘 [pyright docs](https://microsoft.github.io/pyright/).
- 📘 [Pydantic v2 docs](https://docs.pydantic.dev/latest/) — must-read.
- 🎥 [mCoding — Python typing](https://www.youtube.com/watch?v=dgBCEB2jVU0).
- 📝 [Glyph: "Why Type Hints"](https://glyph.twistedmatrix.com/) — мотивация.
- 📘 [PEP 695 (новый синтаксис generics)](https://peps.python.org/pep-0695/).

✅ Чеклист этапа 4:
- [ ] Проект проходит `pyright --strict`
- [ ] Использую generics с PEP 695 синтаксисом
- [ ] Различаю `Protocol` и ABC по применению
- [ ] Умею писать кастомные валидаторы Pydantic

---

## Этап 5. Стандартная библиотека

> «Если функция есть в stdlib — не тащи зависимость».

### Темы (знать наизусть)

- `pathlib` (никаких `os.path` в новом коде).
- `collections`: `Counter`, `defaultdict`, `deque`, `ChainMap`, `OrderedDict`.
- `dataclasses`, `enum` (`StrEnum`, `IntEnum`, `Flag`).
- `datetime`, `zoneinfo` (с 3.9), `calendar`.
- `re` и `regex` (PyPI) для unicode-классов.
- `json`, `tomllib` (3.11+), `csv`.
- `subprocess`, `shutil`, `tempfile`.
- `logging` через `dictConfig`.
- CLI: `argparse`, `typer`, `click`.
- `concurrent.futures`, `threading`, `multiprocessing`.
- `sqlite3`, `pickle`, `shelve`.
- `secrets`, `hashlib`, `hmac`.
- `functools`, `itertools`, `operator`.

### Пример: pathlib

```python
from pathlib import Path

root = Path(__file__).resolve().parent
data_dir = root / "data"
data_dir.mkdir(exist_ok=True)

for py in root.rglob("*.py"):
    size = py.stat().st_size
    if size > 10_000:
        print(py.relative_to(root), size)
```

### Пример: logging dictConfig

```python
import logging
import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"format": '{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}'},
    },
    "handlers": {
        "stdout": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"level": "INFO", "handlers": ["stdout"]},
})

log = logging.getLogger("app")
log.info("hello world")
```

### Пример: Counter + collections

```python
from collections import Counter, defaultdict

words = "to be or not to be".split()
print(Counter(words).most_common(2))  # [('to', 2), ('be', 2)]

groups: dict[str, list[int]] = defaultdict(list)
for word, length in [("a", 1), ("ab", 2), ("a", 1)]:
    groups[word].append(length)
```

### 🛠 Проекты

1. **Backup-утилита**: pathlib + tarfile + logging + argparse.
2. **JSON-конфиг → TOML migrator** с валидацией.
3. **CLI-tracker привычек** с хранением в SQLite.

### Бесплатные ресурсы

- 📘 [Python Module of the Week (PyMOTW-3)](https://pymotw.com/3/) — главный справочник.
- 📘 [Официальная docs.python.org/3/library/](https://docs.python.org/3/library/).
- 📝 [Real Python — pathlib tutorial](https://realpython.com/python-pathlib/).
- 📝 [Loguru как альтернатива logging](https://github.com/Delgan/loguru) — но stdlib знать обязательно.
- 🎥 [Anthony Sottile YouTube](https://www.youtube.com/@anthonywritescode) — глубокие разборы stdlib.

✅ Чеклист этапа 5:
- [ ] Не пишу `os.path` в новом коде
- [ ] Настроил структурированное логирование
- [ ] Использую `Counter` и `defaultdict` к месту
- [ ] Прочитал PyMOTW по `itertools`, `functools`, `collections`

---

## Этап 6. Асинхронность и конкурентность

> Самая важная тема 2026 — после релиза free-threaded Python (PEP 703).

### Темы

- Модель **GIL** и **free-threaded** Python (PEP 703).
- **Потоки** — когда полезны (I/O, после 3.13t и CPU).
- **Процессы** — `multiprocessing`, `ProcessPoolExecutor`.
- **asyncio**: event loop, `await`, `asyncio.TaskGroup` (3.11+), `asyncio.timeout`.
- **Structured concurrency**: `anyio`, `trio`.
- Async-контекстные менеджеры, async-итераторы (`async for`, `async with`).
- HTTP-клиенты: `httpx`, `aiohttp`.
- БД: `asyncpg`, `aiosqlite`.
- Очереди задач: `arq`, `taskiq`, `dramatiq`, `faststream`, Celery 5.
- Backpressure, отмена задач, тайм-ауты, retry.

### Пример: TaskGroup (современный стиль)

```python
import asyncio
import httpx

async def fetch(client: httpx.AsyncClient, url: str) -> int:
    r = await client.get(url, timeout=5)
    return len(r.content)

async def main():
    urls = ["https://example.com"] * 10
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch(client, u)) for u in urls]
    sizes = [t.result() for t in tasks]
    print(sum(sizes))

asyncio.run(main())
```

### Пример: семафор как rate-limiter

```python
import asyncio

async def worker(sem: asyncio.Semaphore, i: int):
    async with sem:
        await asyncio.sleep(1)
        print(f"done {i}")

async def main():
    sem = asyncio.Semaphore(5)  # максимум 5 одновременно
    async with asyncio.TaskGroup() as tg:
        for i in range(20):
            tg.create_task(worker(sem, i))

asyncio.run(main())
```

### Пример: asyncio.timeout (3.11+)

```python
import asyncio

async def slow():
    await asyncio.sleep(10); return "ok"

async def main():
    try:
        async with asyncio.timeout(1):
            await slow()
    except TimeoutError:
        print("timed out")

asyncio.run(main())
```

### 🛠 Проекты

1. **Асинхронный краулер** на 1000 URL с лимитом, ретраями и метриками.
2. **Чат-сервер** на pure asyncio + WebSocket.
3. **Очередь задач** на Redis Streams через arq.

### Бесплатные ресурсы

- 📘 [Real Python — Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/).
- 📘 [Trio docs — structured concurrency](https://trio.readthedocs.io/) — лучшее введение в концепцию.
- 📝 [«Notes on structured concurrency» — Nathaniel J. Smith](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) — must-read.
- 🎥 [David Beazley — Python Concurrency](https://www.youtube.com/watch?v=MCs5OvhV9S4) — классика.
- 📘 [PEP 703 — Making GIL Optional](https://peps.python.org/pep-0703/).
- 📝 [aiohttp docs](https://docs.aiohttp.org/) и [httpx docs](https://www.python-httpx.org/).
- 🎥 [mCoding — async/await explained](https://www.youtube.com/watch?v=GpqAQxH1Afc).

✅ Чеклист этапа 6:
- [ ] Знаю разницу между concurrency и parallelism
- [ ] Пишу async-код через TaskGroup, а не `gather`
- [ ] Понимаю, когда нужен `asyncio`, а когда — `ProcessPoolExecutor`
- [ ] Реализовал retry с экспоненциальным бэкоффом

---

## Этап 7. Тестирование и качество кода

### Темы

- **pytest**: фикстуры, параметризация, маркеры, `conftest.py`, плагины.
- `pytest-asyncio`, `pytest-mock`, `pytest-cov`, `pytest-xdist`, `pytest-randomly`.
- **Hypothesis** — property-based testing.
- Моки/стабы/фейки. TestContainers для интеграционных тестов.
- Покрытие ≥ 80% — но без культа цифры (важнее edge-cases).
- Mutation testing: `mutmut`, `cosmic-ray`.
- Линтеры: ruff, pyright, bandit (security), vulture (dead code), pip-audit.
- pre-commit, GitHub Actions.

### Пример: параметризация pytest

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

### Пример: фикстура с teardown

```python
import pytest, sqlite3

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    yield conn
    conn.close()

def test_insert(db):
    db.execute("INSERT INTO users VALUES (1, 'Ann')")
    rows = db.execute("SELECT * FROM users").fetchall()
    assert rows == [(1, "Ann")]
```

### Пример: hypothesis (property-based)

```python
from hypothesis import given, strategies as st

def reverse(s: str) -> str:
    return s[::-1]

@given(st.text())
def test_reverse_twice_is_identity(s):
    assert reverse(reverse(s)) == s
```

### Пример: GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --all-extras
      - run: uv run ruff check .
      - run: uv run pyright
      - run: uv run pytest --cov
```

### 🛠 Практика

- Покрыть проект из этапа 5 тестами на 90%+.
- Добавить 5+ property-based тестов через hypothesis.
- Настроить mutation testing — снизить выживших мутантов до < 20%.

### Бесплатные ресурсы

- 📘 [pytest docs](https://docs.pytest.org/) — официальная.
- 📘 [Hypothesis docs](https://hypothesis.readthedocs.io/) — обязательно.
- 📝 [Brian Okken — Python Testing with pytest (free chapters)](https://pythontest.com/).
- 🎥 [Test & Code podcast](https://testandcode.com/) — короткие выпуски про практику.
- 📝 [«Effective pytest» (Anthony Sottile, YouTube)](https://www.youtube.com/@anthonywritescode/search?query=pytest).
- 📘 [Awesome pytest plugins](https://github.com/augustogoulart/awesome-pytest).

✅ Чеклист этапа 7:
- [ ] Покрытие тестами > 80%
- [ ] Использую hypothesis для невыделенных edge-cases
- [ ] Настроен CI с ruff + pyright + pytest
- [ ] Pre-commit-хуки запускаются автоматически

---

## Этап 8. Внутренности CPython

> Понимать «как оно устроено» — отличие Junior от Middle.

### Темы

- Объектная модель: всё — `PyObject*`.
- **Reference counting** + циклический GC.
- Байткод: `dis.dis(fn)`, peephole-оптимизации.
- **Specializing Adaptive Interpreter** (PEP 659) с 3.11.
- **JIT** (PEP 744) в 3.13+ — что ускоряется, что нет.
- **GIL** и free-threaded build (PEP 703).
- C-API на пальцах: CPython vs PyPy vs GraalPy.
- Профилирование: `cProfile`, `py-spy`, `scalene`, `memray`, `viztracer`.

### Пример: разбор байткода

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
# LOAD_FAST a
# LOAD_FAST b
# BINARY_OP +
# RETURN_VALUE
```

### Пример: измерение памяти

```python
import sys
print(sys.getsizeof([1, 2, 3]))     # 88
print(sys.getsizeof((1, 2, 3)))     # 64 — tuple компактнее
```

### Пример: py-spy (флеймграф продакшна)

```bash
pip install py-spy
py-spy record -o profile.svg -- python my_app.py
py-spy top --pid 12345   # live top по работающему процессу
```

### 🛠 Проект

- Взять «медленный» скрипт и **ускорить в 10×**. Зафиксировать до/после через `py-spy` + `memray`.
- Перевести цикл на NumPy/Polars, замерить разницу.

### Бесплатные ресурсы

- 📘 [Anthony Shaw — CPython Internals (некоторые главы бесплатно)](https://realpython.com/products/cpython-internals-book/) + статьи на Real Python.
- 📘 [«Inside The Python Virtual Machine» — Obi Ike-Nwosu (free book)](https://leanpub.com/insidethepythonvirtualmachine/read) — бесплатно для чтения онлайн.
- 📝 [Tenthousandmeters — "Python behind the scenes"](https://tenthousandmeters.com/) — лучшая серия о внутренностях.
- 🎥 [Łukasz Langa — keynote talks про релизы CPython](https://www.youtube.com/results?search_query=lukasz+langa+keynote).
- 📘 [PEP 659 — Adaptive Interpreter](https://peps.python.org/pep-0659/).
- 📘 [PEP 744 — JIT compilation](https://peps.python.org/pep-0744/).

✅ Чеклист этапа 8:
- [ ] Умею читать вывод `dis`
- [ ] Профилировал реальный код через `py-spy` и `memray`
- [ ] Объясняю, почему GIL — это не «питон медленный»
- [ ] Понимаю, что делает specializing interpreter

---

## Этап 9. Web-разработка

### Базис

- HTTP/1.1, HTTP/2, HTTP/3, WebSockets, Server-Sent Events.
- REST, gRPC, GraphQL (strawberry), JSON-RPC.
- OpenAPI, JSON Schema.

### Фреймворки 2026

- **FastAPI** — основной выбор (async, Pydantic, OpenAPI из коробки).
- **Litestar** — конкурент FastAPI с DI-контейнером.
- **Django 5.x** — для крупных монолитов, поддержка async views.
- **Starlette** — фундамент для своих ASGI-приложений.
- **Granian** / **uvicorn** / **hypercorn** — ASGI-сервера. Granian (Rust) — самый быстрый в 2026.

### Дополнительно

- Аутентификация: JWT, OAuth2, OIDC, PASETO.
- Кеширование: Redis, Dragonfly, Memcached, in-memory.
- Rate limiting, CORS, CSRF, CSP.
- HTMX как альтернатива SPA для маленьких UI.

### Пример: FastAPI hello

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Tasks API")

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

DB: dict[int, Task] = {}

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(DB.values())

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task) -> Task:
    DB[task.id] = task
    return task
```

Запуск: `uvicorn main:app --reload` → http://localhost:8000/docs

### Пример: dependency injection в FastAPI

```python
from fastapi import Depends, HTTPException, Header

def auth_user(authorization: str = Header()) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401)
    return authorization.removeprefix("Bearer ")

@app.get("/me")
def me(token: str = Depends(auth_user)) -> dict:
    return {"token": token}
```

### 🛠 Проект

- **SaaS Task Tracker API**: FastAPI + PostgreSQL + Redis + JWT + OpenAPI + Docker.

### Бесплатные ресурсы

- 📘 [FastAPI docs](https://fastapi.tiangolo.com/) — лучшая документация в Python-мире.
- 📘 [Litestar docs](https://docs.litestar.dev/).
- 📘 [Django docs](https://docs.djangoproject.com/) + [Django Girls Tutorial (RU)](https://tutorial.djangogirls.org/ru/) для новичков.
- 🎥 [ArjanCodes — FastAPI series](https://www.youtube.com/@ArjanCodes/search?query=fastapi).
- 📝 [TestDriven.io — бесплатные туториалы](https://testdriven.io/blog/) (часть статей открыта).
- 📘 [MDN HTTP docs](https://developer.mozilla.org/en-US/docs/Web/HTTP) — для базы.
- 📝 [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi).

✅ Чеклист этапа 9:
- [ ] Запустил FastAPI-приложение с авторизацией и БД
- [ ] Понимаю разницу WSGI vs ASGI
- [ ] Знаю, что делает CORS и зачем
- [ ] Реализовал rate-limiting на Redis

---

## Этап 10. Базы данных и ORM

### Темы

- **SQL**: JOIN'ы, индексы, EXPLAIN ANALYZE, оконные функции, CTE.
- **PostgreSQL 17+** как стандарт. SQLite — для встроенных задач.
- **SQLAlchemy 2.x** (Core + ORM, async).
- Альтернативы: **SQLModel**, **Tortoise ORM**, **Piccolo**.
- Миграции: **Alembic**.
- Connection pooling: PgBouncer, встроенный pool.
- NoSQL: Redis, MongoDB, ClickHouse (аналитика).
- Поиск: Meilisearch / Typesense / Elasticsearch.

### Пример: SQLAlchemy 2.x async ORM

```python
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)

engine = create_async_engine("postgresql+asyncpg://u:p@localhost/db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_user(email: str) -> User | None:
    async with SessionLocal() as s:
        result = await s.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

### Пример: миграция Alembic

```bash
uv run alembic init migrations
uv run alembic revision --autogenerate -m "users"
uv run alembic upgrade head
```

### 🛠 Проекты

1. **Аналитический дашборд** поверх ClickHouse + FastAPI + Plotly.
2. **Полнотекстовый поиск** на Meilisearch с индексацией из Postgres.
3. **CQRS-репозиторий**: read через async-view, write через aggregate.

### Бесплатные ресурсы

- 📘 [SQLAlchemy 2.x docs](https://docs.sqlalchemy.org/en/20/) — обязательно tutorial.
- 📘 [PostgreSQL Tutorial (postgresqltutorial.com)](https://www.postgresqltutorial.com/) — лучший бесплатный курс по PG.
- 📘 [«Use the Index, Luke!» (Markus Winand)](https://use-the-index-luke.com/) — бесплатная книга про индексы.
- 📘 [Mode SQL Tutorial](https://mode.com/sql-tutorial/) — интерактивно, бесплатно.
- 🎮 [SQLBolt](https://sqlbolt.com/) — короткие уроки + задачи.
- 📘 [Alembic docs](https://alembic.sqlalchemy.org/).
- 📝 [«Designing Data-Intensive Applications» — Martin Kleppmann (главы доступны на сайте автора)](https://dataintensive.net/).

✅ Чеклист этапа 10:
- [ ] Пишу JOIN-ы и оконные функции на SQL без подсказок
- [ ] Понимаю EXPLAIN ANALYZE и читаю план запроса
- [ ] Настроил Alembic-миграции в проекте
- [ ] Использую асинхронный SQLAlchemy 2.x

---

## Этап 11. Data / ML / AI

> Python — это де-факто язык AI-инфраструктуры в 2026.

### Темы

- **NumPy 2.x**, **pandas 2.x** (Arrow backend), **Polars** (must-have, в 10× быстрее pandas).
- **DuckDB** — embedded аналитика, читает CSV/Parquet/JSON.
- Визуализация: **plotly**, **altair**, **matplotlib**, **seaborn**.
- Notebooks: Jupyter, **marimo** (реактивные, без .ipynb).
- ML: scikit-learn, XGBoost, LightGBM, CatBoost.
- DL: **PyTorch 2.x**, JAX.
- LLM-стек: **LangChain / LlamaIndex / DSPy / Haystack**.
- Vector DB: **pgvector**, **Qdrant**, **Weaviate**, **Chroma**.
- MLOps: MLflow, Weights & Biases, Prefect, Dagster.

### Пример: Polars

```python
import polars as pl

df = pl.read_csv("sales.csv")
result = (
    df.filter(pl.col("amount") > 100)
      .group_by("region")
      .agg(pl.col("amount").sum().alias("total"))
      .sort("total", descending=True)
)
print(result)
```

### Пример: DuckDB (SQL по CSV)

```python
import duckdb

duckdb.sql("""
    SELECT region, SUM(amount) AS total
    FROM 'sales.csv'
    WHERE amount > 100
    GROUP BY region
    ORDER BY total DESC
""").show()
```

### Пример: scikit-learn baseline

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=42)
clf = RandomForestClassifier().fit(X_tr, y_tr)
print(clf.score(X_te, y_te))
```

### 🛠 Проекты

1. **RAG-бот по своей документации**: FastAPI + pgvector + любой open LLM API.
2. **Pipeline аналитики**: Polars + DuckDB + дашборд на marimo.
3. **Классификация табличных данных**: scikit-learn + XGBoost + MLflow для трекинга.

### Бесплатные ресурсы

- 📘 [«Python Data Science Handbook» — Jake VanderPlas (free online)](https://jakevdp.github.io/PythonDataScienceHandbook/).
- 📘 [«From Python to NumPy» — Nicolas Rougier (free book)](https://www.labri.fr/perso/nrougier/from-python-to-numpy/).
- 📘 [Polars user guide](https://docs.pola.rs/).
- 📘 [DuckDB docs](https://duckdb.org/docs/).
- 🎥 [3Blue1Brown — Neural Networks (must-watch)](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi).
- 📘 [«Dive into Deep Learning» — d2l.ai (free book)](https://d2l.ai/).
- 📘 [Hugging Face Course (free)](https://huggingface.co/learn).
- 📘 [Fast.ai — Practical Deep Learning (free)](https://course.fast.ai/).
- 📘 [Kaggle Learn (бесплатные мини-курсы)](https://www.kaggle.com/learn).
- 📝 [Sebastian Raschka — magazine.sebastianraschka.com](https://magazine.sebastianraschka.com/) — лучший блог про ML.

✅ Чеклист этапа 11:
- [ ] Освоил Polars, понимаю выгоду vs pandas
- [ ] Собрал RAG-бот на своей документации
- [ ] Понимаю векторные эмбеддинги
- [ ] Знаю, что такое cosine similarity и где она применяется

---

## Этап 12. DevOps и продакшн

### Темы

- **uv** + lock-файлы, reproducible builds, `uv.lock`.
- **Docker** multi-stage, distroless / chainguard-образы.
- Конфиги: `pydantic-settings`, переменные окружения, 12-factor app.
- Структурированные логи: **structlog**, JSON-формат.
- Observability: **OpenTelemetry**, Prometheus, Grafana, Sentry, Jaeger.
- CI/CD: **GitHub Actions**, GitLab CI.
- IaC: Terraform / Pulumi (Pulumi пишется на Python!).
- Kubernetes базово: Deployment, Service, HPA, ConfigMap, Secret.
- Безопасность: `bandit`, `pip-audit`, SBOM (cyclonedx-python).

### Пример: Dockerfile (multi-stage + uv)

```dockerfile
# syntax=docker/dockerfile:1.9
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src ./src
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "src.app"]
```

### Пример: structlog

```python
import structlog

log = structlog.get_logger()
log.info("user.signup", user_id=42, plan="pro")
# {"event":"user.signup","user_id":42,"plan":"pro","timestamp":"..."}
```

### Пример: pydantic-settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    redis_url: str = "redis://localhost"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

### 🛠 Практика

- Задеплоить проект из этапа 9 в Kubernetes с метриками и трейсами OpenTelemetry.
- Настроить CI на GitHub Actions: lint → typecheck → test → build → push image.
- Добавить SBOM-генерацию и pip-audit в pipeline.

### Бесплатные ресурсы

- 📘 [12-Factor App](https://12factor.net/) — must-read.
- 📘 [Docker docs — Get Started](https://docs.docker.com/get-started/).
- 📘 [Kubernetes basics (Katacoda-стиль)](https://kubernetes.io/docs/tutorials/kubernetes-basics/).
- 🎥 [TechWorld with Nana (Kubernetes/DevOps)](https://www.youtube.com/@TechWorldwithNana) — бесплатный курс.
- 📘 [structlog docs](https://www.structlog.org/).
- 📘 [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/).
- 📝 [Hynek Schlawack — production-ready Python](https://hynek.me/articles/) — серия статей.

✅ Чеклист этапа 12:
- [ ] Собрал multi-stage Docker-образ размером < 200 МБ
- [ ] Настроил CI с lint/typecheck/test/build
- [ ] Использую structlog с JSON-форматом
- [ ] Понимаю, что такое трейс, спан и контекст распространения

---

## Этап 13. Архитектура и Senior

### Темы

- **Clean Architecture / Hexagonal / Ports & Adapters** на Python.
- **DDD**: агрегаты, value objects, репозитории, application services, bounded contexts.
- **CQRS**, **Event Sourcing**.
- Сообщения: Kafka (`aiokafka`, `faststream`), NATS, RabbitMQ.
- Паттерны: **Saga**, **Outbox**, **Idempotency Key**.
- Эволюция: монолит → модульный монолит → микросервисы (без культа).
- Перформанс: профилирование, кеширование, batching, vectorization, Rust-вставки через **PyO3**.
- Code review, mentoring, **ADR** (Architecture Decision Records).

### Пример: гексагональная структура проекта

```
src/
  domain/        # чистая бизнес-логика, без зависимостей
    entities.py
    value_objects.py
    services.py
  application/   # use cases
    commands.py
    queries.py
  infrastructure/ # SQLAlchemy, Redis, Kafka — реализации портов
    repositories.py
    messaging.py
  interfaces/    # FastAPI, CLI, gRPC
    http/
    cli/
  config.py
```

### Пример: Outbox pattern (упрощённо)

```python
# в одной транзакции пишем и доменную сущность, и outbox-событие
async with session.begin():
    session.add(order)
    session.add(OutboxEvent(
        type="OrderCreated",
        payload=order.to_dict(),
    ))

# отдельный воркер забирает события и публикует в Kafka,
# гарантируя at-least-once delivery
```

### Пример: ADR

```markdown
# ADR-007: Используем Polars вместо pandas
Status: Accepted (2026-03-01)

## Context
pandas медленный на 10М+ строк, теряет память.

## Decision
Переходим на Polars 1.x для всех ETL-пайплайнов.

## Consequences
+ x10 быстрее, lazy execution
- Команда учит новый API
```

### 🛠 Финальный проект

**Модульный монолит «маркетплейс»** с DDD-структурой, событийной интеграцией, CQRS для read-моделей, OpenTelemetry, тестами на 90%, деплоем в k8s.

### Бесплатные ресурсы

- 📘 [«Cosmic Python» — Percival & Gregory (free online)](https://www.cosmicpython.com/) — лучшая книга по архитектуре Python-приложений.
- 📘 [Eric Evans — DDD Reference (free PDF)](https://www.domainlanguage.com/ddd/reference/).
- 📘 [Martin Fowler — статьи об архитектуре](https://martinfowler.com/architecture/).
- 📝 [microservices.io — Chris Richardson](https://microservices.io/) — паттерны с примерами.
- 🎥 [ArjanCodes — software design](https://www.youtube.com/@ArjanCodes/playlists).
- 📘 [ADR templates (joelparkerhenderson/architecture-decision-record)](https://github.com/joelparkerhenderson/architecture-decision-record).
- 📝 [«Designing Data-Intensive Applications» — главы на сайте](https://dataintensive.net/).

✅ Чеклист этапа 13:
- [ ] Реализовал модульный монолит с разделёнными слоями
- [ ] Написал минимум 3 ADR в проекте
- [ ] Понимаю trade-off микросервисов vs модульного монолита
- [ ] Знаю Saga и Outbox-паттерны на практике

---

## 📚 Бесплатные ресурсы (общая подборка)

### Бесплатные книги (полностью в открытом доступе)

- 📘 [«Automate the Boring Stuff with Python» — Al Sweigart](https://automatetheboringstuff.com/) — для старта.
- 📘 [«Think Python 2e» — Allen B. Downey](https://greenteapress.com/wp/think-python-2e/) — академический подход.
- 📘 [«A Byte of Python» — Swaroop C H (RU перевод есть)](https://python.swaroopch.com/) — компактный учебник.
- 📘 [«Composing Programs»](https://composingprograms.com/) — Berkeley CS61A на Python.
- 📘 [«Python Data Science Handbook» — Jake VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/).
- 📘 [«Cosmic Python» — архитектура Python-приложений](https://www.cosmicpython.com/).
- 📘 [«Dive Into Python 3» — Mark Pilgrim](https://diveintopython3.problemsolving.io/).
- 📘 [«Inside The Python Virtual Machine»](https://leanpub.com/insidethepythonvirtualmachine/read).

### Документация (закладывать в браузер)

- [docs.python.org/3](https://docs.python.org/3/)
- [peps.python.org](https://peps.python.org/) — все PEP'ы.
- [docs.astral.sh/uv](https://docs.astral.sh/uv/), [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)
- [docs.pydantic.dev](https://docs.pydantic.dev/)
- [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

### YouTube (англ)

- [mCoding](https://www.youtube.com/@mCoding) — тонкости языка.
- [ArjanCodes](https://www.youtube.com/@ArjanCodes) — дизайн и архитектура.
- [Anthony Sottile](https://www.youtube.com/@anthonywritescode) — глубокие разборы.
- [Sebastián Ramírez (tiangolo)](https://www.youtube.com/@tiangolo) — автор FastAPI.
- [Corey Schafer](https://www.youtube.com/@coreyms) — лучший для новичков.
- [Real Python YouTube](https://www.youtube.com/@realpython).
- [PyCon talks](https://www.youtube.com/@PyConUS) — записи всех конференций.

### YouTube / каналы на русском

- [selfedu (Балакирев)](https://www.youtube.com/@selfedu_rus) — большой курс Python.
- [PyLounge](https://www.youtube.com/@PyLounge) — практические разборы.
- [Диджитализируй!](https://www.youtube.com/@digitalize_me) — современный стек.

### Подкасты

- [Python Bytes](https://pythonbytes.fm/) — еженедельные новости.
- [Talk Python To Me](https://talkpython.fm/) — длинные интервью.
- [Real Python Podcast](https://realpython.com/podcasts/rpp/).
- [Test & Code](https://testandcode.com/) — про тестирование.

### Сообщества

- [Python Discord (discord.gg/python)](https://discord.gg/python).
- [r/Python](https://reddit.com/r/Python), [r/learnpython](https://reddit.com/r/learnpython).
- [Stack Overflow — python tag](https://stackoverflow.com/questions/tagged/python).
- Telegram: `@ru_python`, `@async_python`, `@pythontalk`.

### Рассылки (бесплатно)

- [PyCoder's Weekly](https://pycoders.com/) — каждую пятницу.
- [Python Weekly](https://www.pythonweekly.com/).
- [Awesome Python Newsletter](https://python.libhunt.com/newsletter).

---

## 🧠 Платформы для практики

- [Exercism Python Track](https://exercism.org/tracks/python) — бесплатно, с менторами.
- [LeetCode](https://leetcode.com/problemset/all/) — алгоритмы, фильтр по Python.
- [Codewars](https://www.codewars.com/) — задачи в виде ката.
- [HackerRank — Python](https://www.hackerrank.com/domains/python).
- [Edabit](https://edabit.com/challenges/python3) — маленькие задачи.
- [CheckiO](https://checkio.org/) — задачи как игра.
- [Project Euler](https://projecteuler.net/) — математические задачи.
- [Advent of Code](https://adventofcode.com/) — ежегодное событие, отличная практика.
- [Kaggle](https://www.kaggle.com/) — для ML/Data.
- [Codeforces](https://codeforces.com/) — соревнования.

---

## ✅ Финальный чеклист Middle+

### Язык
- [ ] Пишу идиоматичный Python без оглядки на документацию
- [ ] Прохожу `pyright --strict` без `Any` и подавлений
- [ ] Объясняю GIL, free-threaded mode, JIT
- [ ] Пишу async-код через TaskGroup, понимаю отмену задач

### Качество
- [ ] Покрытие тестами > 80%, есть property-based тесты
- [ ] Профилировал реальный код через py-spy / memray
- [ ] Настроен CI: ruff + pyright + pytest + security-сканеры

### Архитектура
- [ ] Знаю SOLID и применяю на практике
- [ ] Реализовал ≥ 5 паттернов GoF в реальных проектах
- [ ] Спроектировал и собрал модульный монолит
- [ ] Понимаю DDD: aggregate, value object, repository

### Базы данных
- [ ] Пишу JOIN-ы и оконные функции на SQL
- [ ] Читаю EXPLAIN ANALYZE
- [ ] Использую SQLAlchemy 2.x async + Alembic

### Web
- [ ] Запустил FastAPI-сервис с авторизацией, БД и тестами
- [ ] Разворачивал Python в Docker и k8s
- [ ] Настроил OpenTelemetry-трейсы

### Soft
- [ ] Прочитал минимум 3 книги из списка выше
- [ ] Сделал 5+ pet-проектов
- [ ] Регулярно делаю code review (свой/чужой)
- [ ] Веду личный блог / репозиторий-дневник

---

## 🤝 Контрибьют

Pull requests welcome:
- Исправления опечаток и неточностей
- Свежие ресурсы 2026 года (только бесплатные!)
- Переводы и адаптации
- Новые примеры кода

## 📜 Лицензия

MIT — используй свободно, упоминание автора приветствуется.

> ⭐ Если roadmap оказался полезным — поставь звезду репозиторию.
