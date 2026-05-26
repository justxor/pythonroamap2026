# 🐍 Python Roadmap 2026 (RU) — расширенная версия

> Полный и **актуальный** маршрут изучения Python в 2026 году: от `Hello, World` до Senior / архитектора.
> С практикой, схемами, примерами кода и **только бесплатными** ресурсами.

> Python 3.13+ • free-threaded mode (PEP 703) • JIT (PEP 744) • uv/ruff • async-first • type-driven • AI-инфраструктура

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Status](https://img.shields.io/badge/status-actual%202026-brightgreen)
![Free](https://img.shields.io/badge/resources-free-orange)
![Telegram](https://img.shields.io/badge/Telegram-%40pythonl-26A5E4?logo=telegram)
![License](https://img.shields.io/badge/license-MIT-green)

🎓 **Практический курс по этому роадмапу:** [course/README.md](course/README.md) — уроки, примеры кода, упражнения и решения по каждому этапу. Отдельные этапы:
> - [🤖 Вайбкодинг (AI-assisted dev)](course/stage-14-vibecoding.md) — Claude Code, Cursor, Copilot, локальные модели.
> - [🕸 Парсинг и веб-скрапинг 2026](course/stage-15-parsing.md) — httpx, selectolax, Playwright, Scrapy, crawl4ai, антибот, этика.

📣 **Главные Telegram-источники этого роадмапа:**
> - 🐍 **[t.me/pythonl](https://t.me/pythonl)** — главный канал по Python: новости, библиотеки, разборы, вакансии.
> - 🤖 **[t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — практика и примеры кода по AI / ML / Big Data на Python: модели, ноутбуки, бенчмарки, статьи с разбором.
> - 📚 **[Отборная папка ресурсов 🎁](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка лучших Telegram-каналов по Python, ML, DS и инфраструктуре. Подписался один раз — закрыл вопрос «где брать актуальное».

---

## 🗺️ Общая карта пути

```
                  ┌──────────────────────────────────────────────┐
                  │              🐍 PYTHON ROADMAP 2026          │
                  └──────────────────────────────────────────────┘
                                       │
   ┌───────────────────────┬───────────┴───────────┬───────────────────────┐
   ▼                       ▼                       ▼                       ▼
┌──────────┐         ┌──────────┐            ┌──────────┐           ┌──────────┐
│ Месяц 1  │         │ Месяц 2-3│            │ Месяц 4-6│           │ Месяц 7-9│
│ Этапы 0-2│  ───▶   │ Этапы 3-5│   ───▶     │Этапы 6-9 │  ───▶     │Этапы10-13│
│ОСНОВЫ ЯЗ.│         │ STDLIB + │            │ ASYNC +  │           │ARCH + ML │
│          │         │ OOП + TYP│            │  WEB     │           │  + DEVOPS│
└──────────┘         └──────────┘            └──────────┘           └──────────┘
   Junior              Junior+                  Middle                 Middle+
                                                                       Senior
```

### Логика следования этапов

```
[0] Окружение ──▶ [1] Основы ──▶ [2] Идиомы ──▶ [3] ООП ──▶ [4] Типы ──▶ [5] Stdlib
                                                                            │
        ┌───────────────────────────────────────────────────────────────────┘
        ▼
[6] Async ──▶ [7] Тесты ──▶ [8] CPython внутри ──▶ [9] Web ──▶ [10] БД ──▶ [11] ML/AI
                                                                                  │
                              ┌───────────────────────────────────────────────────┘
                              ▼
                       [12] DevOps ──▶ [13] Архитектура / Senior
```

---

## 📌 Как пользоваться роадмапом

1. **По этапам**, не перепрыгивая. Каждый раздел опирается на предыдущий.
2. На каждом этапе: **теория → код руками → мини-проект → разбор чужого кода**.
3. Минимум **70% времени — код руками**, без копипасты.
4. Веди репозиторий-дневник `learning-python/week-XX/` — коммить туда решения задач.
5. Раз в неделю — code review (свой старый код или открытый PR на GitHub).
6. Каждый этап заканчивается **чеклистом** — пока не отметишь всё, не идёшь дальше.
7. Подпишись на [t.me/pythonl](https://t.me/pythonl) и читай раз в день — это держит «в курсе».

⏱ Ориентировочный темп: **6–9 месяцев** при 2–3 часах в день → уверенный Junior+/Middle.

---

## 🧭 Содержание

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
- [📚 Бесплатные ресурсы](#-бесплатные-ресурсы-общая-подборка)
- [🤖 Вайбкодинг (AI-assisted dev)](#-вайбкодинг--разработка-с-ai-в-2026)
- [💬 Telegram-каналы](#-telegram-каналы-2026)
- [🧠 Платформы для практики](#-платформы-для-практики)
- [✅ Финальный чеклист Middle+](#-финальный-чеклист-middle)

---

## Этап 0. Окружение 2026

> 🎯 **Цель:** настроить современный стек один раз — и забыть о боли с зависимостями навсегда.
> ⏱ **Время:** 1–2 вечера.

### Карта стека

```
┌──────────────────────────────────────────────────────────────┐
│                      ВЕРСИЯ PYTHON                           │
│   python 3.13+ (CPython)   ▒    python 3.13t (free-threaded) │
└──────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────┐
│                  ПАКЕТНЫЙ МЕНЕДЖЕР                           │
│        uv  ◀── заменяет pip + venv + poetry + pyenv          │
└──────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────┐
│       КАЧЕСТВО КОДА            │        ТЕСТЫ                │
│   ruff   (lint + format)       │   pytest                    │
│   pyright (типы)               │   hypothesis                │
│   pre-commit (хуки)            │   coverage                  │
└──────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────┐
│                       IDE                                    │
│  VS Code + Pylance + Ruff   │  PyCharm 2026   │  Zed + LSP   │
└──────────────────────────────────────────────────────────────┘
```

### Стек подробно

| Инструмент | Заменяет | Зачем |
|---|---|---|
| **Python 3.13+** | — | основной интерпретатор, JIT и nogil доступны |
| **uv** (Astral) | pip, pipx, venv, poetry, pyenv | в 10–100× быстрее, единый CLI |
| **ruff** | black, isort, flake8, pylint | один линтер + форматтер, на Rust |
| **pyright** или **mypy --strict** | — | статический контроль типов |
| **pytest** + **hypothesis** | unittest | де-факто стандарт |
| **pre-commit** | — | хуки качества до коммита |
| **direnv** + `.envrc` | venv activate | автоактивация окружения |
| **Docker / OrbStack** | — | контейнеры |

### Практика (выполнить целиком)

```bash
# 1. Установка uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Установка нужной версии Python
uv python install 3.13

# 3. Новый проект
uv init my-first-project && cd my-first-project

# 4. Зависимости разработки
uv add --dev ruff pyright pytest hypothesis pre-commit

# 5. Создаём базовый код и тест
mkdir src tests
echo 'def add(a: int, b: int) -> int: return a + b' > src/calc.py
echo 'from src.calc import add
def test_add(): assert add(2, 3) == 5' > tests/test_calc.py

# 6. Проверяем линтер, типы и тесты
uv run ruff check .
uv run pyright
uv run pytest -q

# 7. Подключаем pre-commit
echo '
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
      - id: ruff-format
' > .pre-commit-config.yaml
uv run pre-commit install
```

### Эталонный `pyproject.toml`

```toml
[project]
name = "my-first-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = ["ruff", "pyright", "pytest", "hypothesis", "pre-commit"]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF", "ANN", "TID", "C4", "PT"]
ignore = ["ANN101", "ANN102"]

[tool.ruff.format]
quote-style = "double"

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.13"

[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["tests"]
```

### 🛠 Мини-задачи

1. Поднять проект по шагам выше.
2. Сломать тест намеренно — посмотреть, как падает pre-commit.
3. Добавить хук pyright в pre-commit вручную.
4. Завести GitHub-репозиторий `learning-python` для всех будущих проектов.

### 📚 Бесплатные ресурсы этапа 0

- 📘 [uv docs](https://docs.astral.sh/uv/) — официальная документация.
- 📘 [ruff docs](https://docs.astral.sh/ruff/rules/) — все правила линтера.
- 📘 [pyright getting started](https://microsoft.github.io/pyright/#/getting-started).
- 🎥 [ArjanCodes — Modern Python tooling (uv/ruff)](https://www.youtube.com/@ArjanCodes).
- 📝 [Hynek Schlawack — Production-ready Python](https://hynek.me/articles/) — серия о современном стеке.
- 📘 [Awesome uv](https://github.com/tox-dev/awesome-uv).
- 💬 [t.me/pythonl](https://t.me/pythonl) — там часто разбирают новости uv/ruff.

### ✅ Чеклист этапа 0

- [ ] uv, ruff, pyright, pytest установлены и работают
- [ ] Создан репозиторий-дневник на GitHub
- [ ] pre-commit запускается при `git commit`
- [ ] Понимаю отличие `uv sync` от `pip install -r requirements.txt`
- [ ] Знаю, чем `uv lock` отличается от `pip freeze`

---

## Этап 1. Основы языка

> 🎯 **Цель:** уверенно реализовать любой алгоритм на чистом Python.
> ⏱ **Время:** 3–4 недели.

### Карта раздела

```
                    ┌─────────────── ОСНОВЫ ЯЗЫКА ──────────────┐
                    │                                           │
   ┌────────────┐ ┌─┴──────────┐ ┌──────────────┐ ┌─────────────┴──┐
   │ Синтаксис  │ │  Типы      │ │  Управление  │ │   Функции      │
   │ PEP 8      │ │  данных    │ │  потоком     │ │   замыкания    │
   └────────────┘ └────────────┘ └──────────────┘ └────────────────┘
                                                           │
                          ┌────────────────┬───────────────┘
                          ▼                ▼
                  ┌─────────────┐ ┌─────────────────┐
                  │ Исключения  │ │ Контекстные     │
                  │ try/except  │ │ менеджеры (with)│
                  └─────────────┘ └─────────────────┘
```

### Темы детально

| Подтема | Что освоить | Минимум практики |
|---|---|---|
| **Базовый синтаксис** | отступы, переменные, операторы | 5 простых скриптов |
| **Числа** | int, float, Decimal, Fraction, complex | калькулятор процентов и НДС |
| **Строки** | методы, f-strings (`f"{x=}"`, `f"{n:_>10.2f}"`), join, split | парсер логов |
| **bytes/bytearray** | encode/decode, hex, base64 | парсер бинарного формата |
| **Коллекции** | list, tuple, set, frozenset, dict | реализовать частотный словарь |
| **`match/case`** | structural pattern matching | парсер JSON-событий |
| **Функции** | `*args`, `**kwargs`, `/`, `*`, аннотации | 10 функций с разными сигнатурами |
| **LEGB scope** | глобальные/локальные/nonlocal | счётчик через замыкание |
| **Исключения** | try/except/else/finally, `raise ... from` | свой класс ошибок |
| **`with`** | контекстные менеджеры, contextlib | тайм-замер блока кода |

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
        case {"type": t, **rest}:
            return f"unknown type={t}, extra={rest}"
        case _:
            return "not an event"

print(handle({"type": "click", "x": 10, "y": 20}))   # click at (10,20)
print(handle({"type": "key", "key": "a"}))           # letter A
```

### Пример: контекстный менеджер таймера

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

### Пример: свой класс исключений

```python
class AppError(Exception): ...
class NotFoundError(AppError): ...
class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"{field}: {reason}")
        self.field, self.reason = field, reason

def find(user_id: int):
    if user_id < 0:
        raise ValidationError("user_id", "must be >= 0")
    raise NotFoundError(f"user {user_id} not found")

try:
    find(-1)
except AppError as e:
    print(type(e).__name__, e)
```

### 🛠 Мини-проекты этапа 1

1. **CLI-калькулятор** с поддержкой выражений и истории (`argparse` + `match`).
2. **CSV → JSON** парсер без сторонних библиотек (только stdlib).
3. **«Угадай число»** с сохранением статистики в файл.
4. **Анализатор текста**: топ-10 слов, частота букв, среднее число слов в предложении.
5. **Конвертер валют** на курсах из локального JSON.

### 📚 Бесплатные ресурсы этапа 1

- 📘 [Официальный туториал Python (RU)](https://docs.python.org/3/tutorial/index.html).
- 📘 [pythontutor.ru](https://pythontutor.ru/) — учебник + задачи на русском.
- 📘 [Real Python — Python Basics](https://realpython.com/tutorials/basics/).
- 📘 [Automate the Boring Stuff (free online)](https://automatetheboringstuff.com/).
- 🎮 [CheckiO](https://checkio.org/) — задачи в виде игры.
- 🎮 [Exercism Python Track](https://exercism.org/tracks/python) — бесплатно, с менторами.
- 🎥 [Corey Schafer — Python Tutorial (плейлист)](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU).
- 🎥 [selfedu — Python 3 (RU)](https://www.youtube.com/@selfedu_rus).
- 💬 [t.me/pythonl](https://t.me/pythonl) — рубрики «задача дня».

### ✅ Чеклист этапа 1

- [ ] Решил 30+ задач на pythontutor.ru / CheckiO / Exercism
- [ ] Реализовал минимум 2 мини-проекта из списка
- [ ] Уверенно использую f-strings и `match/case`
- [ ] Различаю изменяемые и неизменяемые типы (list vs tuple, dict vs frozenset)
- [ ] Написал свою иерархию исключений
- [ ] Понимаю LEGB и применяю `nonlocal`

---

## Этап 2. Идиоматичный Python

> 🎯 **Цель:** писать «по-питоновски». Меньше кода — больше выразительности.
> ⏱ **Время:** 2–3 недели.

### Карта раздела

```
   ┌──────────────────── ИДИОМАТИЧНЫЙ PYTHON ────────────────────┐
   │                                                             │
┌──┴───────────┐   ┌───────────────┐   ┌────────────────┐   ┌────┴────────┐
│ Итераторы /  │   │ Comprehensions│   │ itertools /    │   │ Декораторы  │
│ Генераторы   │   │ list/dict/gen │   │ functools      │   │ @wraps      │
└──────────────┘   └───────────────┘   └────────────────┘   └─────────────┘
        │                                       │
        ▼                                       ▼
   ┌────────────┐                       ┌────────────────┐
   │ EAFP / LBYL│                       │ dataclasses /  │
   │ walrus :=  │                       │ namedtuple     │
   └────────────┘                       └────────────────┘
```

### Что должен уметь идиоматичный питонист

| Антипаттерн ❌ | Идиома ✅ |
|---|---|
| `for i in range(len(xs)): xs[i]` | `for x in xs` / `enumerate` |
| `result = []; for x in xs: result.append(f(x))` | `[f(x) for x in xs]` |
| `if x in dct: v = dct[x] else: v = default` | `v = dct.get(x, default)` |
| `try: ... except KeyError: ...` для дефолта | `defaultdict` |
| `fn(x); fn(x); fn(x)` | `@cache` |
| мутабельный default `def f(x=[])` | `def f(x=None): x = x or []` |
| ручной `time.time()` вокруг кода | контекстный менеджер `@contextmanager` |
| `open(f); ... f.close()` | `with open(f) as ...` |

### Пример: генератор vs список (память)

```python
# ❌ грузит всё в память
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
from time import sleep

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

### Пример: `itertools.batched` (3.12+) и `pairwise`

```python
from itertools import batched, pairwise

for chunk in batched(range(10), 3):
    print(chunk)   # (0,1,2) (3,4,5) (6,7,8) (9,)

for a, b in pairwise([1, 3, 6, 10]):
    print(b - a)   # 2 3 4
```

### Пример: `functools.singledispatch`

```python
from functools import singledispatch

@singledispatch
def render(value) -> str:
    return f"<unknown {value!r}>"

@render.register
def _(value: int) -> str: return f"int={value}"

@render.register
def _(value: list) -> str: return f"list[{len(value)}]"

print(render(10))          # int=10
print(render([1, 2, 3]))   # list[3]
```

### Пример: walrus `:=` к месту

```python
import re

text = "hello world 42"
if (m := re.search(r"\d+", text)):
    print(f"число: {m.group()}")
```

### 🛠 Практика

- Реализовать декораторы: `@timed`, `@memoize`, `@deprecated`, `@retry`.
- Переписать процедурный код предыдущего этапа в идиомы; замерить разницу через `ruff check --statistics`.
- Заменить циклы накопления на comprehensions / `sum` / `any` / `all` где уместно.
- Написать генератор «скользящего окна» через itertools.

### 📚 Бесплатные ресурсы этапа 2

- 📘 [Python Cookbook (Beazley)](https://github.com/dabeaz/python-cookbook) — рецепты.
- 📘 [itertools recipes (official)](https://docs.python.org/3/library/itertools.html#itertools-recipes).
- 📝 [Trey Hunner blog](https://treyhunner.com/blog/) — лучшее об идиомах.
- 🎥 [mCoding YouTube](https://www.youtube.com/@mCoding).
- 📘 [PEP 8](https://peps.python.org/pep-0008/) и [PEP 20 — Zen of Python](https://peps.python.org/pep-0020/).
- 📝 [Real Python — Python Idioms](https://realpython.com/python-idioms/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — посты «как лучше написать».

### ✅ Чеклист этапа 2

- [ ] Написал минимум 4 рабочих декоратора
- [ ] Свободно использую comprehensions/itertools/functools
- [ ] Понимаю разницу `@cache` vs `@lru_cache(maxsize=N)`
- [ ] Знаю, почему mutable default — антипаттерн
- [ ] Применяю walrus только там, где он реально упрощает код
- [ ] Различаю dataclass / namedtuple / TypedDict по применению

---

## Этап 3. ООП и проектирование

> 🎯 **Цель:** проектировать гибкие, тестируемые системы. Думать «как поменять, не сломав».
> ⏱ **Время:** 3 недели.

### Карта раздела

```
                  ┌──────── ООП в Python ────────┐
                  │                              │
        ┌─────────┴────────┐         ┌───────────┴──────────┐
        │   Базовые блоки  │         │  Принципы и паттерны │
        │  class / __init__│         │  SOLID / DRY / KISS  │
        │  inheritance/MRO │         │  GoF: Strategy,      │
        │  dunder-методы   │         │  Factory, Adapter,   │
        │  property        │         │  Observer, Repo...   │
        └─────────┬────────┘         └───────────┬──────────┘
                  ▼                              ▼
        ┌───────────────────┐         ┌──────────────────────┐
        │ Дескрипторы       │         │ Protocol (duck typed)│
        │ Метаклассы (редко)│         │ vs ABC (формальный)  │
        └───────────────────┘         └──────────────────────┘
```

### SOLID — в одну строку каждый

- **S**ingle Responsibility — один класс = одна причина для изменения.
- **O**pen/Closed — открыт для расширения, закрыт для модификации.
- **L**iskov Substitution — подкласс должен заменять родителя без сюрпризов.
- **I**nterface Segregation — лучше много маленьких `Protocol`, чем один «толстый».
- **D**ependency Inversion — зависим от абстракций (`Protocol`), а не от конкретных классов.

### Топ магических методов (dunder)

| Метод | Что даёт |
|---|---|
| `__repr__` / `__str__` | вывод для отладки / для пользователя |
| `__eq__` + `__hash__` | сравнение и использование в set/dict |
| `__iter__` / `__next__` | объект-итератор |
| `__enter__` / `__exit__` | контекстный менеджер |
| `__call__` | объект как функция |
| `__len__`, `__getitem__` | поведение коллекции |
| `__slots__` | экономия памяти |

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

print(total_area([Circle(2), Square(3)]))   # 21.566...
```

### Пример: Strategy + dataclass

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

class BlackFriday:
    def price(self, base): return base * 0.5

@dataclass
class Order:
    items_total: float
    strategy: PricingStrategy
    def total(self) -> float:
        return self.strategy.price(self.items_total)

print(Order(100, PercentOff(20)).total())   # 80.0
print(Order(100, BlackFriday()).total())    # 50.0
```

### Пример: Repository pattern (in-memory)

```python
from typing import Protocol, TypeVar
from dataclasses import dataclass

T = TypeVar("T")

class Repository(Protocol[T]):
    def add(self, item: T) -> None: ...
    def get(self, id: int) -> T | None: ...
    def list(self) -> list[T]: ...

@dataclass
class User: id: int; name: str

class InMemoryUserRepo:
    def __init__(self): self._data: dict[int, User] = {}
    def add(self, u: User): self._data[u.id] = u
    def get(self, id: int) -> User | None: return self._data.get(id)
    def list(self) -> list[User]: return list(self._data.values())
```

### Пример: `@property` и валидация

```python
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius   # пройдёт через setter

    @property
    def celsius(self) -> float:
        return self._c

    @celsius.setter
    def celsius(self, v: float) -> None:
        if v < -273.15:
            raise ValueError("ниже абсолютного нуля")
        self._c = v

    @property
    def kelvin(self) -> float:
        return self._c + 273.15
```

### 🛠 Проекты этапа 3

1. **Геометрия**: набор фигур через `Protocol` (без жёсткой иерархии).
2. **In-memory ORM** (~200 строк): `Repository[T]` + dataclass + JSON-сериализация.
3. **Парсер выражений** в стиле Visitor.
4. **Игра «крестики-нолики»**: разделить домен, UI и контроллер.

### 📚 Бесплатные ресурсы этапа 3

- 📘 [Refactoring.guru — паттерны на Python](https://refactoring.guru/design-patterns/python).
- 📘 [faif/python-patterns (GitHub)](https://github.com/faif/python-patterns) — каталог.
- 🎥 [ArjanCodes — Design Patterns in Python](https://www.youtube.com/@ArjanCodes/playlists).
- 📝 [SOLID на русском (Habr, серия)](https://habr.com/ru/articles/688530/).
- 📘 [Real Python — OOP in Python 3](https://realpython.com/python3-object-oriented-programming/).
- 📘 [Python Type Hints — Protocol vs ABC](https://realpython.com/python-protocol/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — разборы реальных рефакторингов.

### ✅ Чеклист этапа 3

- [ ] Объясняю разницу `@classmethod` / `@staticmethod` / instance method
- [ ] Реализовал ≥ 5 GoF-паттернов на практике
- [ ] Использую `Protocol` вместо ABC, где это уместно
- [ ] Понимаю MRO в diamond-наследовании
- [ ] Знаю минимум 8 dunder-методов наизусть
- [ ] Применяю SOLID при разборе чужого кода

---

## Этап 4. Типизация

> 🎯 **Цель:** проходить `pyright --strict` без `Any`. Это норма 2026.
> ⏱ **Время:** 2 недели.

### Карта типов

```
            ┌─────── СТАТИЧЕСКАЯ ───────┐    ┌─── RUNTIME ───┐
            │ pyright / mypy            │    │ Pydantic v2   │
            │ (checker, не runtime!)    │    │ TypeAdapter   │
            └────────────┬──────────────┘    └───────┬───────┘
                         │                           │
       ┌─────────────────┴──────────────┐            │
       ▼                                ▼            ▼
┌────────────┐                   ┌────────────┐   ┌─────────────────┐
│ Generics   │                   │ Protocol   │   │ Валидация ввода │
│ PEP 695    │                   │ TypedDict  │   │ API, конфиги    │
│ TypeVar    │                   │ Literal    │   │ настройки       │
│ ParamSpec  │                   │ Final      │   └─────────────────┘
└────────────┘                   └────────────┘
```

### Темы

- Базовые типы: `list[int]`, `dict[str, T]`, `Callable[[int], str]`, `Iterable[T]`.
- **PEP 695 generics**: `class Stack[T]: ...`, `def first[T](xs: list[T]) -> T`.
- `TypeVar`, `ParamSpec`, `Concatenate` (для декораторов).
- `Protocol`, structural subtyping.
- `Literal`, `Final`, `TypedDict`, `NotRequired`, `Required`.
- `Annotated[T, ...]` — метаданные для FastAPI / Pydantic.
- `Self`, `@override` (PEP 698), `assert_type`, `reveal_type`.
- pyright strict mode, точечные `# type: ignore[error-code]`.
- **Pydantic v2** — runtime-валидация + сериализация.
- `TypeGuard` и `TypeIs` (PEP 742) для сужения типов.

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
from pydantic import BaseModel, EmailStr, Field, field_validator

class User(BaseModel):
    id: int
    email: EmailStr
    age: int = Field(ge=0, le=150)
    tags: list[str] = []

    @field_validator("tags")
    @classmethod
    def tags_lowercase(cls, v: list[str]) -> list[str]:
        return [t.lower() for t in v]

u = User.model_validate({"id": 1, "email": "a@b.c", "age": 30, "tags": ["A", "B"]})
print(u.model_dump_json())
```

### Пример: TypedDict + NotRequired

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: int
    name: str
    email: NotRequired[str]

def greet(u: UserDict) -> str:
    return f"Hello, {u['name']}!"
```

### Пример: TypeGuard

```python
from typing import TypeGuard

def is_str_list(xs: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in xs)

def process(xs: list[object]) -> None:
    if is_str_list(xs):
        # здесь pyright знает, что xs: list[str]
        print(",".join(xs))
```

### Пример: `ParamSpec` для декоратора

```python
from typing import ParamSpec, TypeVar, Callable
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def log_call(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper
```

### 🛠 Практика

- Перевести проект этапа 3 на `pyright --strict` без единого `Any` и подавлений.
- Написать generic-репозиторий `Repository[T]` с CRUD.
- Описать схему API через `TypedDict` + Pydantic.
- Реализовать декоратор `@log_call`, корректно типизированный через `ParamSpec`.

### 📚 Бесплатные ресурсы этапа 4

- 📘 [typing — official docs](https://docs.python.org/3/library/typing.html).
- 📘 [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
- 📘 [pyright docs](https://microsoft.github.io/pyright/).
- 📘 [Pydantic v2 docs](https://docs.pydantic.dev/latest/).
- 📘 [PEP 695 — type parameters syntax](https://peps.python.org/pep-0695/).
- 📘 [PEP 742 — TypeIs](https://peps.python.org/pep-0742/).
- 🎥 [mCoding — Python typing](https://www.youtube.com/watch?v=dgBCEB2jVU0).
- 📝 [Glyph: "Why Type Hints"](https://blog.glyph.im/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — посты-разборы новых PEP по типам.

### ✅ Чеклист этапа 4

- [ ] Проект проходит `pyright --strict`
- [ ] Использую generics в синтаксисе PEP 695
- [ ] Понимаю разницу `Protocol` vs ABC по применению
- [ ] Умею писать кастомные валидаторы Pydantic
- [ ] Знаю, когда нужен `TypedDict`, а когда `dataclass`
- [ ] Применяю `TypeGuard` / `TypeIs` для сужения типов

---

## Этап 5. Стандартная библиотека

> 🎯 **Цель:** «если функция есть в stdlib — не тащи зависимость».
> ⏱ **Время:** 3 недели.

### Карта stdlib (must-know)

```
                          ┌─── STDLIB ESSENTIALS ───┐
                          │                         │
        ┌─── Работа ──┐   │   ┌─── Данные ───┐      │  ┌─── I/O ────┐
        │ pathlib     │   │   │ collections  │      │  │ json/csv   │
        │ shutil      │   │   │ dataclasses  │      │  │ tomllib    │
        │ tempfile    │   │   │ enum         │      │  │ pickle     │
        │ subprocess  │   │   │ datetime     │      │  │ sqlite3    │
        └─────────────┘   │   │ zoneinfo     │      │  └────────────┘
                          │   │ Decimal      │
        ┌─── CLI ─────┐   │   └──────────────┘      │  ┌── Crypto ──┐
        │ argparse    │   │                         │  │ hashlib    │
        │ logging     │   │   ┌── Functional ──┐    │  │ hmac       │
        │ contextlib  │   │   │ itertools      │    │  │ secrets    │
        └─────────────┘   │   │ functools      │    │  └────────────┘
                          │   │ operator       │
                          │   └────────────────┘
                          │
                          │   ┌── Concurrent ──┐
                          │   │ threading      │
                          │   │ multiprocessing│
                          │   │ asyncio        │
                          │   │ concurrent.fut │
                          │   └────────────────┘
```

### Темы детально

| Модуль | Что освоить |
|---|---|
| `pathlib` | `Path`, `/`, `rglob`, `read_text`, `write_bytes` |
| `collections` | `Counter`, `defaultdict`, `deque`, `ChainMap` |
| `dataclasses` | `@dataclass`, `field`, `slots=True`, `frozen=True` |
| `enum` | `Enum`, `StrEnum`, `IntEnum`, `Flag` |
| `datetime` + `zoneinfo` | таймзоны, ISO 8601, арифметика дат |
| `re` | группы, `(?P<name>...)`, `re.compile` |
| `json` / `tomllib` / `csv` | сериализация, дефолтные decoder/encoder |
| `subprocess` | `run(check=True)`, `capture_output`, безопасно |
| `logging` | `dictConfig`, JSON-формат, уровни |
| `argparse` / `typer` / `click` | CLI |
| `concurrent.futures` | `ThreadPoolExecutor`, `ProcessPoolExecutor` |
| `sqlite3` | embedded SQL, context manager |
| `secrets` / `hashlib` / `hmac` | пароли, токены, подписи |

### Пример: pathlib

```python
from pathlib import Path

root = Path(__file__).resolve().parent
data_dir = root / "data"
data_dir.mkdir(exist_ok=True)

# Все .py больше 10 КБ
for py in root.rglob("*.py"):
    if py.stat().st_size > 10_000:
        print(py.relative_to(root))
```

### Пример: logging.dictConfig (JSON-логи)

```python
import logging
import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"format": '{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s","logger":"%(name)s"}'},
    },
    "handlers": {
        "stdout": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"level": "INFO", "handlers": ["stdout"]},
})

log = logging.getLogger("app")
log.info("hello world")
```

### Пример: `Counter` + `defaultdict`

```python
from collections import Counter, defaultdict

words = "to be or not to be".split()
print(Counter(words).most_common(2))   # [('to', 2), ('be', 2)]

groups: dict[str, list[int]] = defaultdict(list)
for word, length in [("a", 1), ("ab", 2), ("a", 1)]:
    groups[word].append(length)
```

### Пример: datetime + zoneinfo

```python
from datetime import datetime
from zoneinfo import ZoneInfo

msk = datetime.now(ZoneInfo("Europe/Moscow"))
ny  = msk.astimezone(ZoneInfo("America/New_York"))
print(msk.isoformat(), "->", ny.isoformat())
```

### Пример: безопасный subprocess

```python
import subprocess

result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True, text=True, check=True,
)
print(result.stdout)
```

### 🛠 Проекты этапа 5

1. **Backup-утилита** (pathlib + tarfile + logging + argparse).
2. **JSON-конфиг → TOML migrator** с валидацией.
3. **CLI-tracker привычек** на SQLite.
4. **Парсер логов nginx** в структурированный JSON.
5. **Утилита очистки папки** (старше N дней) с dry-run.

### 📚 Бесплатные ресурсы этапа 5

- 📘 [PyMOTW-3 (Python Module of the Week)](https://pymotw.com/3/) — главный справочник.
- 📘 [docs.python.org/3/library](https://docs.python.org/3/library/).
- 📝 [Real Python — pathlib tutorial](https://realpython.com/python-pathlib/).
- 📝 [Real Python — Working with JSON](https://realpython.com/python-json/).
- 🎥 [Anthony Sottile — глубокие разборы stdlib](https://www.youtube.com/@anthonywritescode).
- 📝 [Loguru](https://github.com/Delgan/loguru) — альтернатива logging (но stdlib знать обязательно).
- 💬 [t.me/pythonl](https://t.me/pythonl) — заметки «фичи stdlib, о которых забыли».

### ✅ Чеклист этапа 5

- [ ] В новом коде не использую `os.path`
- [ ] Настроил структурированное логирование
- [ ] Применяю `Counter`/`defaultdict`/`deque` по месту
- [ ] Прочитал PyMOTW по `itertools`, `functools`, `collections`
- [ ] Работаю с таймзонами через `zoneinfo`, без `pytz`
- [ ] Знаю, чем `json.loads` отличается от `json.load`

---

## Этап 6. Асинхронность и конкурентность

> 🎯 **Цель:** не путать concurrency и parallelism. Уверенно писать async-код без race-conditions.
> ⏱ **Время:** 4 недели.

### Модель конкурентности в Python 2026

```
                 ┌───── Что у нас в Python ─────┐
                 │                              │
   I/O-bound  ───┼──▶ asyncio (1 поток, event loop)
                 │                              │
   CPU-bound  ───┼──▶ multiprocessing (N процессов, обходим GIL)
                 │                              │
   Mixed/легко  ─┼──▶ threading (с GIL — для I/O)
                 │                              │
   Без GIL (PEP 703) ─▶ python3.13t threads на CPU — экспериментально
                 │                              │
   Structured  ──┼──▶ anyio / trio + TaskGroup
                 └──────────────────────────────┘
```

### Когда что выбирать

| Задача | Инструмент |
|---|---|
| 1000 HTTP-запросов | `asyncio` + `httpx` |
| Обработка изображений (CPU) | `ProcessPoolExecutor` |
| Чтение/запись файлов с лимитом | `asyncio.Semaphore` |
| Парсинг N CSV параллельно | `ProcessPoolExecutor` |
| Realtime-сервер | `asyncio` + WebSocket |
| Очередь задач | `arq` / `taskiq` / `dramatiq` / Celery |

### Темы

- Модель **GIL** и **free-threaded** Python (PEP 703).
- Потоки (`threading`) — когда полезны (I/O, а после 3.13t — и CPU).
- Процессы (`multiprocessing`, `ProcessPoolExecutor`).
- **asyncio**: event loop, `await`, `asyncio.TaskGroup` (3.11+), `asyncio.timeout`.
- **Structured concurrency**: `anyio`, `trio`.
- Async-контекстные менеджеры, async-итераторы (`async for`, `async with`).
- HTTP-клиенты: `httpx`, `aiohttp`.
- БД: `asyncpg`, `aiosqlite`, async SQLAlchemy 2.x.
- Очереди задач: `arq`, `taskiq`, `dramatiq`, `faststream`, Celery 5.
- Backpressure, отмена задач, тайм-ауты, retry с экспоненциальным бэкоффом.

### Пример: TaskGroup (3.11+ стиль)

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

### Пример: Семафор как rate-limiter

```python
import asyncio

async def worker(sem: asyncio.Semaphore, i: int):
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

### Пример: `asyncio.timeout` (3.11+)

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

### Пример: retry с экспоненциальным бэкоффом

```python
import asyncio
import random

async def with_retry(fn, *, attempts=5, base=0.2):
    for i in range(1, attempts + 1):
        try:
            return await fn()
        except Exception as e:
            if i == attempts:
                raise
            delay = base * (2 ** (i - 1)) * (1 + random.random())
            await asyncio.sleep(delay)
```

### Пример: CPU-задача через процессы

```python
from concurrent.futures import ProcessPoolExecutor

def heavy(n: int) -> int:
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(heavy, [10_000_000] * 8))
    print(sum(results))
```

### 🛠 Проекты этапа 6

1. **Async-краулер** 1000 URL с лимитом, ретраями, метриками.
2. **WebSocket-чат** на pure asyncio (без фреймворков).
3. **Очередь задач** на Redis Streams через arq.
4. **Скан портов** на asyncio + Semaphore.
5. **Сравнение sync vs async vs процессы** на одной и той же задаче.

### 📚 Бесплатные ресурсы этапа 6

- 📘 [Real Python — Async IO: Complete Walkthrough](https://realpython.com/async-io-python/).
- 📘 [Trio docs — structured concurrency](https://trio.readthedocs.io/).
- 📝 [Nathaniel J. Smith — «Notes on structured concurrency»](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/).
- 🎥 [David Beazley — Python Concurrency from the Ground Up](https://www.youtube.com/watch?v=MCs5OvhV9S4).
- 📘 [PEP 703 — Making GIL Optional](https://peps.python.org/pep-0703/).
- 📘 [httpx docs](https://www.python-httpx.org/) / [aiohttp docs](https://docs.aiohttp.org/).
- 🎥 [mCoding — async/await explained](https://www.youtube.com/watch?v=GpqAQxH1Afc).
- 💬 [t.me/pythonl](https://t.me/pythonl) — посты про asyncio, GIL, JIT.

### ✅ Чеклист этапа 6

- [ ] Объясняю concurrency vs parallelism
- [ ] Пишу async-код через TaskGroup, а не `gather`
- [ ] Применяю `asyncio.timeout` и Semaphore по месту
- [ ] Реализовал retry с экспоненциальным бэкоффом
- [ ] Понимаю, когда нужен `asyncio`, а когда `ProcessPoolExecutor`
- [ ] Знаю, как корректно отменить задачу и обработать `CancelledError`

---

## Этап 7. Тестирование и качество кода

> 🎯 **Цель:** ваш код проходит CI без вашего участия. Покрытие — не цель, а побочный эффект.
> ⏱ **Время:** 2 недели.

### Пирамида тестов

```
                     ┌──────────────┐
                     │  E2E (мало)  │
                     ├──────────────┤
                     │ Integration  │
                     │ (среднее)    │
                     ├──────────────┤
                     │ Unit (много) │
                     └──────────────┘
   Скорость:        ↑ медленно       ↓ быстро
   Стоимость:       ↑ дорого         ↓ дёшево
   Стабильность:    ↓ флакает        ↑ стабильно
```

### Темы

- **pytest**: фикстуры, параметризация, маркеры, `conftest.py`, плагины.
- Плагины: `pytest-asyncio`, `pytest-mock`, `pytest-cov`, `pytest-xdist`, `pytest-randomly`.
- **Hypothesis** — property-based testing.
- Моки/стабы/фейки. **TestContainers** для интеграционных тестов.
- Покрытие ≥ 80%, но edge-cases важнее цифры.
- Mutation testing: `mutmut`, `cosmic-ray`.
- Линтеры: ruff, pyright, bandit (security), vulture (dead code), pip-audit.
- pre-commit + GitHub Actions.

### Пример: параметризация

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

### Пример: hypothesis

```python
from hypothesis import given, strategies as st

def reverse(s: str) -> str:
    return s[::-1]

@given(st.text())
def test_reverse_twice_is_identity(s):
    assert reverse(reverse(s)) == s
```

### Пример: async-тест

```python
import pytest, asyncio

@pytest.mark.asyncio
async def test_sleep():
    start = asyncio.get_event_loop().time()
    await asyncio.sleep(0.1)
    assert asyncio.get_event_loop().time() - start >= 0.1
```

### Пример: GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          python-version: ${{ matrix.python }}
      - run: uv sync --all-extras
      - run: uv run ruff check .
      - run: uv run pyright
      - run: uv run pytest --cov --cov-report=xml
```

### 🛠 Практика этапа 7

- Покрыть тестами проект этапа 5 на 90%+.
- Добавить ≥ 5 property-based тестов через hypothesis.
- Настроить mutation testing — снизить выживших мутантов до < 20%.
- Запустить TestContainers с Postgres и проверить интеграцию.

### 📚 Бесплатные ресурсы этапа 7

- 📘 [pytest docs](https://docs.pytest.org/).
- 📘 [Hypothesis docs](https://hypothesis.readthedocs.io/).
- 📝 [Brian Okken — Python Testing with pytest (free chapters)](https://pythontest.com/).
- 🎥 [Test & Code podcast](https://testandcode.com/).
- 🎥 [Anthony Sottile — pytest deep-dives](https://www.youtube.com/@anthonywritescode).
- 📘 [Awesome pytest plugins](https://github.com/augustogoulart/awesome-pytest).
- 💬 [t.me/pythonl](https://t.me/pythonl) — обзоры подходов к тестированию.

### ✅ Чеклист этапа 7

- [ ] Покрытие тестами > 80%
- [ ] Есть минимум 3 property-based теста
- [ ] CI собирает: lint + typecheck + tests + coverage
- [ ] Pre-commit запускается при каждом коммите
- [ ] Использую `pytest-xdist` для параллельного запуска
- [ ] Понимаю разницу mock / stub / fake / spy

---

## Этап 8. Внутренности CPython

> 🎯 **Цель:** понимать, **как Python работает изнутри**. Это отличает Middle от Senior.
> ⏱ **Время:** 2–3 недели.

### Архитектура CPython (упрощённо)

```
   .py файл
      │  (compile)
      ▼
   .pyc байткод  ──▶  ┌──────────────────────┐
                      │ Specializing Adaptive│
                      │ Interpreter (PEP 659)│
                      └──────────┬───────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │ JIT (PEP 744, 3.13+) │
                      └──────────┬───────────┘
                                 │
                                 ▼
                       Объектная модель:
                       PyObject* + refcount
                                 │
                                 ▼
                       GC (циклический)
                                 │
                       ┌─────────┴─────────┐
                       │      GIL          │
                       │  free-threaded?   │
                       │   (PEP 703)       │
                       └───────────────────┘
```

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
print(sys.getsizeof("abc"))         # 52
```

### Пример: `__slots__` экономит память

```python
class A:
    def __init__(self): self.x = 1; self.y = 2

class B:
    __slots__ = ("x", "y")
    def __init__(self): self.x = 1; self.y = 2

import sys
print(sys.getsizeof(A().__dict__))   # ~104
# у B нет __dict__, экономия ~40-50% на больших коллекциях объектов
```

### Пример: профилирование py-spy

```bash
pip install py-spy   # или uv add --dev py-spy

# Флеймграф продакшна
py-spy record -o profile.svg -- python my_app.py

# Live top по работающему процессу
py-spy top --pid 12345
```

### Пример: memray для памяти

```bash
pip install memray
python -m memray run my_app.py
python -m memray flamegraph memray-my_app.bin
```

### 🛠 Проекты этапа 8

- Взять «медленный» скрипт и **ускорить в 10×**. Зафиксировать до/после через `py-spy` + `memray`.
- Перевести узкий цикл на NumPy/Polars, замерить разницу.
- Сравнить производительность CPython 3.13 vs PyPy на одной задаче.

### 📚 Бесплатные ресурсы этапа 8

- 📘 [«Inside The Python Virtual Machine» (free online)](https://leanpub.com/insidethepythonvirtualmachine/read).
- 📝 [tenthousandmeters.com — "Python behind the scenes" (серия)](https://tenthousandmeters.com/).
- 📘 [PEP 659 — Specializing Adaptive Interpreter](https://peps.python.org/pep-0659/).
- 📘 [PEP 744 — JIT compilation](https://peps.python.org/pep-0744/).
- 📘 [PEP 703 — Making GIL Optional](https://peps.python.org/pep-0703/).
- 🎥 [Łukasz Langa — keynote talks про CPython](https://www.youtube.com/results?search_query=lukasz+langa+keynote).
- 📝 [Real Python — Memory Management in Python](https://realpython.com/python-memory-management/).
- 📘 [py-spy на GitHub](https://github.com/benfred/py-spy) / [memray](https://github.com/bloomberg/memray).
- 💬 [t.me/pythonl](https://t.me/pythonl) — разборы релизов CPython.

### ✅ Чеклист этапа 8

- [ ] Читаю и понимаю вывод `dis`
- [ ] Профилировал реальный код через py-spy и memray
- [ ] Объясняю, почему GIL — это не «питон медленный»
- [ ] Понимаю работу specializing interpreter
- [ ] Знаю, когда применить `__slots__`
- [ ] Сравнил CPython vs PyPy на собственной задаче

---

## Этап 9. Web-разработка

> 🎯 **Цель:** собрать production-ready API с авторизацией, БД, тестами и документацией.
> ⏱ **Время:** 4–5 недель.

### Стек 2026 (схема)

```
   Клиент (Browser / Mobile / SPA / HTMX)
       │
       ▼  HTTPS
   ┌────────────────────────────────────────┐
   │  Reverse Proxy / Load Balancer         │
   │  (nginx / Caddy / Traefik)             │
   └────────────────────────────────────────┘
       │
       ▼  ASGI
   ┌────────────────────────────────────────┐
   │  ASGI server                           │
   │  granian (Rust) / uvicorn / hypercorn  │
   └────────────────────────────────────────┘
       │
       ▼
   ┌────────────────────────────────────────┐
   │  Framework: FastAPI / Litestar /Django │
   │  Pydantic v2  •  OpenAPI  •  DI        │
   └────────────────────────────────────────┘
       │
       ▼
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │ PostgreSQL  │  │   Redis     │  │  S3 / MinIO │
   └─────────────┘  └─────────────┘  └─────────────┘
```

### Базис

- HTTP/1.1, HTTP/2, HTTP/3, WebSockets, Server-Sent Events.
- REST, gRPC, GraphQL (strawberry), JSON-RPC.
- OpenAPI 3.1, JSON Schema.
- Cookies, sessions, JWT, OAuth2, OIDC, PASETO.

### Фреймворки 2026

| Фреймворк | Когда выбирать |
|---|---|
| **FastAPI** | API, микросервисы, async — топ-выбор |
| **Litestar** | FastAPI-альтернатива с DI и плагинами |
| **Django 5.x** | большой монолит, админка, ORM «из коробки» |
| **Starlette** | свой ASGI-фундамент, минимализм |
| **Granian** | самый быстрый ASGI-сервер (Rust) |

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

### Пример: DI и авторизация

```python
from fastapi import Depends, HTTPException, Header

def auth_user(authorization: str = Header()) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Unauthorized")
    return authorization.removeprefix("Bearer ")

@app.get("/me")
def me(token: str = Depends(auth_user)) -> dict:
    return {"token": token}
```

### Пример: WebSocket-эхо

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def ws_echo(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text(f"echo: {msg}")
    except Exception:
        await ws.close()
```

### Пример: rate-limiter на Redis (псевдо-код)

```python
async def rate_limited(redis, user_id: str, limit: int = 100) -> bool:
    key = f"rl:{user_id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 60)
    return count <= limit
```

### 🛠 Проекты этапа 9

1. **Task Tracker API**: FastAPI + Postgres + Redis + JWT + OpenAPI + Docker.
2. **URL-shortener**: FastAPI + Redis + статистика кликов.
3. **Реалтайм чат**: FastAPI WebSocket + Redis Pub/Sub.
4. **OAuth2 интеграция** с GitHub login.

### 📚 Бесплатные ресурсы этапа 9

- 📘 [FastAPI docs](https://fastapi.tiangolo.com/) — образцовая документация.
- 📘 [Litestar docs](https://docs.litestar.dev/).
- 📘 [Django docs](https://docs.djangoproject.com/).
- 📘 [Django Girls Tutorial (RU)](https://tutorial.djangogirls.org/ru/) — для новичков в Django.
- 🎥 [ArjanCodes — FastAPI series](https://www.youtube.com/@ArjanCodes/search?query=fastapi).
- 📝 [TestDriven.io blog](https://testdriven.io/blog/) — много бесплатных туториалов.
- 📘 [MDN HTTP docs](https://developer.mozilla.org/en-US/docs/Web/HTTP).
- 📘 [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi).
- 💬 [t.me/pythonl](https://t.me/pythonl) — разборы новых web-фич.

### ✅ Чеклист этапа 9

- [ ] Запустил FastAPI с авторизацией, БД и Swagger
- [ ] Понимаю WSGI vs ASGI
- [ ] Знаю, что делает CORS и зачем
- [ ] Реализовал rate-limiting
- [ ] Написал WebSocket-эндпоинт
- [ ] Завернул API в Docker

---

## Этап 10. Базы данных и ORM

> 🎯 **Цель:** уверенно писать SQL, читать `EXPLAIN ANALYZE`, использовать ORM как инструмент, а не магию.
> ⏱ **Время:** 3 недели.

### Карта

```
              ┌─────── ХРАНЕНИЕ ДАННЫХ ───────┐
              │                               │
   ┌──────────┴────────┐         ┌────────────┴────────┐
   │ Реляционные SQL   │         │      NoSQL          │
   ├───────────────────┤         ├─────────────────────┤
   │ PostgreSQL 17+    │         │ Redis (kv, queues)  │
   │ SQLite (embedded) │         │ MongoDB (docs)      │
   │ MySQL / MariaDB   │         │ ClickHouse (OLAP)   │
   └───────┬───────────┘         │ Qdrant (vectors)    │
           │                     └─────────────────────┘
           ▼
   ┌────────────────────┐         ┌─────────────────────┐
   │  ORM / Toolkit     │         │     Поиск           │
   │  SQLAlchemy 2.x    │         │ Meilisearch         │
   │  SQLModel          │         │ Typesense           │
   │  Piccolo / Tortoise│         │ Elasticsearch       │
   └─────────┬──────────┘         └─────────────────────┘
             │
             ▼
   ┌────────────────────┐
   │ Миграции: Alembic  │
   └────────────────────┘
```

### Темы

- **SQL**: SELECT/JOIN/GROUP BY/HAVING, индексы, CTE, оконные функции.
- **PostgreSQL 17+** — основной выбор. SQLite — для embedded.
- **SQLAlchemy 2.x** (Core + ORM, async).
- Альтернативы: SQLModel, Tortoise, Piccolo.
- Миграции: **Alembic**.
- Pooling: PgBouncer, встроенный pool.
- NoSQL: Redis, MongoDB, ClickHouse.
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

### Пример: оконная функция в SQL

```sql
SELECT
    user_id,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total
FROM payments;
```

### Пример: миграция Alembic

```bash
uv run alembic init migrations
# редактируем env.py, добавляем target_metadata = Base.metadata
uv run alembic revision --autogenerate -m "users"
uv run alembic upgrade head
```

### Пример: индексы и EXPLAIN

```sql
-- ❌ медленно
SELECT * FROM users WHERE LOWER(email) = 'a@b.c';

-- ✅ создаём функциональный индекс
CREATE INDEX users_email_lower ON users (LOWER(email));

EXPLAIN ANALYZE SELECT * FROM users WHERE LOWER(email) = 'a@b.c';
```

### 🛠 Проекты этапа 10

1. **Аналитический дашборд** поверх ClickHouse + FastAPI + Plotly.
2. **Полнотекстовый поиск** на Meilisearch с индексацией из Postgres.
3. **CQRS-репозиторий**: read через async-view, write через aggregate.
4. **Аудит-лог** через триггеры и outbox-таблицу.

### 📚 Бесплатные ресурсы этапа 10

- 📘 [SQLAlchemy 2.x docs](https://docs.sqlalchemy.org/en/20/) — пройти tutorial обязательно.
- 📘 [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — лучший бесплатный курс по PG.
- 📘 [«Use the Index, Luke!»](https://use-the-index-luke.com/) — бесплатная книга про индексы.
- 📘 [Mode SQL Tutorial](https://mode.com/sql-tutorial/) — интерактивно.
- 🎮 [SQLBolt](https://sqlbolt.com/) — короткие уроки + задачи.
- 📘 [Alembic docs](https://alembic.sqlalchemy.org/).
- 📘 [Designing Data-Intensive Applications — главы автора](https://dataintensive.net/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — посты про SQLAlchemy и Postgres.

### ✅ Чеклист этапа 10

- [ ] Пишу JOIN-ы и оконные функции на SQL без подсказок
- [ ] Читаю `EXPLAIN ANALYZE` и понимаю seq scan vs index scan
- [ ] Настроил Alembic-миграции в проекте
- [ ] Использую асинхронный SQLAlchemy 2.x
- [ ] Знаю, когда нужен индекс, а когда он вредит
- [ ] Понимаю уровни изоляции транзакций

---

## Этап 11. Data / ML / AI

> 🎯 **Цель:** уверенно работать с табличными данными и собрать практический RAG/ML-проект.
> ⏱ **Время:** 4–6 недель.

### Карта данных и ML

```
   ┌──────── ВВОД ────────┐         ┌──────── ОБРАБОТКА ────────┐
   │ CSV / Parquet / JSON │  ───▶   │ NumPy 2.x                 │
   │ Postgres / ClickHouse│         │ pandas 2.x (Arrow)        │
   │ S3 / MinIO           │         │ Polars (lazy, ★★★)        │
   │ API                  │         │ DuckDB (SQL embedded)     │
   └──────────────────────┘         └────────────┬──────────────┘
                                                 │
                                                 ▼
                ┌────────────── МОДЕЛИРОВАНИЕ ─────────────┐
                │  scikit-learn (классика)                 │
                │  XGBoost / LightGBM / CatBoost (boosting)│
                │  PyTorch 2.x (DL)                        │
                │  JAX (исследования)                      │
                └─────────────────────┬────────────────────┘
                                      ▼
                ┌────────────── LLM-стек ──────────────────┐
                │  LangChain / LlamaIndex / DSPy / Haystack│
                │  Vector DB: pgvector / Qdrant / Weaviate │
                │  Embeddings + RAG-пайплайны              │
                └──────────────────────────────────────────┘
```

### Темы

- **NumPy 2.x** — основа. Векторизация вместо циклов.
- **pandas 2.x** (Arrow backend) и **Polars** (must-have, в 5–10× быстрее).
- **DuckDB** — embedded аналитика, читает CSV/Parquet/JSON напрямую.
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

### Пример: RAG (упрощённо)

```python
# 1. Создаём эмбеддинги документов
# 2. Кладём в vector DB (например, pgvector)
# 3. На запрос ищем top-K похожих
# 4. Подставляем контекст в промпт LLM

# Псевдо-код:
docs = load_docs("./knowledge/")
embeddings = embed_model.encode(docs)
vector_db.upsert(docs, embeddings)

def answer(query: str) -> str:
    q_emb = embed_model.encode([query])
    context = vector_db.search(q_emb, k=5)
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    return llm.generate(prompt)
```

### 🛠 Проекты этапа 11

1. **RAG-бот по своей документации**: FastAPI + pgvector + open LLM API.
2. **Pipeline аналитики**: Polars + DuckDB + дашборд на marimo.
3. **Классификация табличных данных** (Kaggle): sklearn + XGBoost + MLflow.
4. **Парсер + NER** с использованием spaCy.
5. **Бенчмарк pandas vs Polars** на ваших данных.

### 📚 Бесплатные ресурсы этапа 11

- 📘 [«Python Data Science Handbook» — VanderPlas (free)](https://jakevdp.github.io/PythonDataScienceHandbook/).
- 📘 [«From Python to NumPy» — Nicolas Rougier (free book)](https://www.labri.fr/perso/nrougier/from-python-to-numpy/).
- 📘 [Polars user guide](https://docs.pola.rs/).
- 📘 [DuckDB docs](https://duckdb.org/docs/).
- 🎥 [3Blue1Brown — Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) (must-watch).
- 📘 [«Dive into Deep Learning» — d2l.ai (free book)](https://d2l.ai/).
- 📘 [Hugging Face Course (free)](https://huggingface.co/learn).
- 📘 [Fast.ai — Practical Deep Learning (free)](https://course.fast.ai/).
- 📘 [Kaggle Learn (бесплатные мини-курсы)](https://www.kaggle.com/learn).
- 📝 [Sebastian Raschka magazine](https://magazine.sebastianraschka.com/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — обзоры новых ML/AI инструментов.

### ✅ Чеклист этапа 11

- [ ] Освоил Polars, понимаю выгоду vs pandas
- [ ] Собрал работающий RAG-бот по своей документации
- [ ] Понимаю векторные эмбеддинги
- [ ] Знаю, что такое cosine similarity и где она применяется
- [ ] Прошёл хотя бы 1 курс на Kaggle Learn
- [ ] Запушил Kaggle-решение и попал в leaderboard

---

## Этап 12. DevOps и продакшн

> 🎯 **Цель:** довести Python-сервис до прод-готовности: контейнер, конфиги, логи, метрики, CI/CD.
> ⏱ **Время:** 3 недели.

### Карта продакшн-стека

```
   Код  ──▶  uv lock  ──▶  Docker (multi-stage)  ──▶  Registry
                                                          │
                                                          ▼
                                              ┌────────────────────┐
                                              │  CI: GitHub Actions│
                                              │  lint/typecheck/   │
                                              │  test/build/push   │
                                              └─────────┬──────────┘
                                                        ▼
                                              ┌────────────────────┐
                                              │  K8s (Helm/Kustom) │
                                              │  Deploy + HPA      │
                                              └─────────┬──────────┘
                                                        ▼
                ┌───────────────────────────────────────┴────────────────────┐
                │            OBSERVABILITY                                   │
                │  structlog (JSON logs) → Loki                              │
                │  OpenTelemetry traces  → Tempo / Jaeger                    │
                │  Prometheus metrics    → Grafana                           │
                │  Sentry (errors)                                           │
                └────────────────────────────────────────────────────────────┘
```

### Темы

- **uv** + lock-файлы, reproducible builds.
- **Docker** multi-stage, distroless / chainguard.
- Конфиги: `pydantic-settings`, ENV, 12-factor.
- Логи: **structlog**, JSON-формат.
- Observability: **OpenTelemetry**, Prometheus, Grafana, Sentry, Jaeger.
- CI/CD: **GitHub Actions**, GitLab CI.
- IaC: Terraform / **Pulumi** (на Python!).
- Kubernetes: Deployment, Service, HPA, ConfigMap, Secret.
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
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    db_url: str
    redis_url: str = "redis://localhost"
    debug: bool = False

settings = Settings()
```

### Пример: OpenTelemetry (минимум)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-service")
with tracer.start_as_current_span("work"):
    ...   # бизнес-логика
```

### Пример: K8s манифест (упрощённо)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-api
spec:
  replicas: 3
  selector: { matchLabels: { app: my-api } }
  template:
    metadata: { labels: { app: my-api } }
    spec:
      containers:
        - name: app
          image: registry/my-api:1.0.0
          ports: [{ containerPort: 8000 }]
          env:
            - name: DB_URL
              valueFrom:
                secretKeyRef: { name: my-api, key: db_url }
```

### 🛠 Практика этапа 12

- Задеплоить проект этапа 9 в Kubernetes с метриками и трейсами OpenTelemetry.
- Настроить CI на GitHub Actions: lint → typecheck → test → build → push image.
- Добавить SBOM-генерацию и pip-audit в pipeline.
- Поднять Grafana + Prometheus + Loki локально через docker-compose.

### 📚 Бесплатные ресурсы этапа 12

- 📘 [12-Factor App](https://12factor.net/) — must-read.
- 📘 [Docker docs — Get Started](https://docs.docker.com/get-started/).
- 📘 [Kubernetes basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/).
- 🎥 [TechWorld with Nana — Kubernetes/DevOps Bootcamp](https://www.youtube.com/@TechWorldwithNana).
- 📘 [structlog docs](https://www.structlog.org/).
- 📘 [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/).
- 📝 [Hynek Schlawack — production-ready Python](https://hynek.me/articles/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — DevOps-новости из мира Python.

### ✅ Чеклист этапа 12

- [ ] Собрал multi-stage Docker-образ < 200 МБ
- [ ] Настроил CI: lint + typecheck + test + build
- [ ] Использую structlog с JSON-форматом
- [ ] Понимаю, что такое span, trace и контекст распространения
- [ ] Развёрнут OpenTelemetry → Jaeger
- [ ] Знаю, что такое HPA в Kubernetes

---

## Этап 13. Архитектура и Senior

> 🎯 **Цель:** проектировать системы, которые переживут пять команд и три рефакторинга.
> ⏱ **Время:** на всю жизнь.

### Слои гексагональной архитектуры

```
   ┌────────────────────────────────────────────────────────┐
   │                    INTERFACES                          │
   │   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────────┐        │
   │   │ HTTP │   │ CLI  │   │ gRPC │   │ Kafka    │        │
   │   └───┬──┘   └──┬───┘   └──┬───┘   └────┬─────┘        │
   └───────┼─────────┼──────────┼────────────┼──────────────┘
           ▼         ▼          ▼            ▼
   ┌────────────────────────────────────────────────────────┐
   │                   APPLICATION                          │
   │       Use cases (commands / queries / handlers)        │
   └─────────────────────┬──────────────────────────────────┘
                         ▼
   ┌────────────────────────────────────────────────────────┐
   │                     DOMAIN                             │
   │   Entities • Value Objects • Aggregates • Services     │
   │            (никаких зависимостей наружу)               │
   └─────────────────────┬──────────────────────────────────┘
                         ▼
   ┌────────────────────────────────────────────────────────┐
   │                INFRASTRUCTURE                          │
   │   SQLAlchemy • Redis • Kafka • S3 — реализуют порты    │
   └────────────────────────────────────────────────────────┘
```

### Темы

- **Clean Architecture / Hexagonal / Ports & Adapters** на Python.
- **DDD**: агрегаты, value objects, репозитории, application services, bounded contexts.
- **CQRS** и **Event Sourcing**.
- Сообщения: Kafka (`aiokafka`, `faststream`), NATS, RabbitMQ.
- Паттерны: **Saga**, **Outbox**, **Idempotency Key**, **Circuit Breaker**.
- Эволюция: монолит → модульный монолит → микросервисы (без культа).
- Перформанс: профилирование, кеширование, batching, vectorization, Rust-вставки через **PyO3**.
- Code review, mentoring, **ADR** (Architecture Decision Records).

### Пример: структура проекта (гексагональная)

```
src/
  domain/              # чистая бизнес-логика, без зависимостей наружу
    entities.py
    value_objects.py
    services.py
    events.py
  application/         # use cases
    commands.py
    queries.py
    handlers.py
  infrastructure/      # реализации портов: SQLAlchemy, Redis, Kafka
    repositories.py
    messaging.py
    cache.py
  interfaces/          # FastAPI / CLI / gRPC
    http/
    cli/
  config.py
  main.py
```

### Пример: Outbox-паттерн (упрощённо)

```python
# В ОДНОЙ транзакции пишем и доменную сущность, и outbox-событие
async with session.begin():
    session.add(order)
    session.add(OutboxEvent(
        type="OrderCreated",
        payload=order.to_dict(),
    ))

# Отдельный воркер забирает события и публикует в Kafka,
# гарантируя at-least-once delivery без потери при падении.
```

### Пример: Idempotency Key

```python
async def create_payment(idempotency_key: str, amount: int):
    cached = await cache.get(f"idem:{idempotency_key}")
    if cached:
        return cached   # уже создано раньше
    payment = await db.create_payment(amount=amount)
    await cache.set(f"idem:{idempotency_key}", payment, ttl=86400)
    return payment
```

### Пример: ADR (Architecture Decision Record)

```markdown
# ADR-007: Переход с pandas на Polars
Status: Accepted (2026-03-01)

## Context
pandas медленный на 10M+ строк, теряет память в ETL.

## Decision
Переходим на Polars 1.x для всех ETL-пайплайнов.

## Consequences
+ x10 быстрее, lazy execution
+ Arrow-совместимость с DuckDB
- Команда учит новый API
- Часть legacy-кода придётся переписать
```

### 🛠 Финальный проект

**Модульный монолит «маркетплейс»** с DDD-структурой, событийной интеграцией, CQRS для read-моделей, OpenTelemetry, тестами на 90%, деплоем в k8s, документацией и ADR.

### 📚 Бесплатные ресурсы этапа 13

- 📘 [«Cosmic Python» — Percival & Gregory (free online)](https://www.cosmicpython.com/) — лучшая книга по архитектуре Python-приложений.
- 📘 [Eric Evans — DDD Reference (free PDF)](https://www.domainlanguage.com/ddd/reference/).
- 📘 [Martin Fowler — статьи об архитектуре](https://martinfowler.com/architecture/).
- 📝 [microservices.io — Chris Richardson](https://microservices.io/) — паттерны с примерами.
- 🎥 [ArjanCodes — Software Design playlists](https://www.youtube.com/@ArjanCodes/playlists).
- 📘 [ADR templates](https://github.com/joelparkerhenderson/architecture-decision-record).
- 📘 [Designing Data-Intensive Applications — главы автора](https://dataintensive.net/).
- 📘 [The Twelve-Factor App](https://12factor.net/).
- 💬 [t.me/pythonl](https://t.me/pythonl) — разборы архитектурных решений.

### ✅ Чеклист этапа 13

- [ ] Реализовал модульный монолит с разделёнными слоями
- [ ] Написал ≥ 3 ADR в проекте
- [ ] Понимаю trade-off микросервисов vs модульного монолита
- [ ] Использовал Saga / Outbox / Idempotency Key на практике
- [ ] Провёл хотя бы 5 чужих code review с полезным фидбеком
- [ ] Могу объяснить архитектуру проекта новичку за 10 минут

---

## 📚 Бесплатные ресурсы (общая подборка)

### Бесплатные книги (полностью в открытом доступе)

- 📘 [«Automate the Boring Stuff with Python» — Al Sweigart](https://automatetheboringstuff.com/) — для старта.
- 📘 [«Think Python 2e» — Allen B. Downey](https://greenteapress.com/wp/think-python-2e/) — академический подход.
- 📘 [«A Byte of Python» — Swaroop C H (есть RU перевод)](https://python.swaroopch.com/).
- 📘 [«Composing Programs» — Berkeley CS61A on Python](https://composingprograms.com/).
- 📘 [«Python Data Science Handbook» — VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/).
- 📘 [«Cosmic Python» — архитектура](https://www.cosmicpython.com/).
- 📘 [«Dive Into Python 3» — Mark Pilgrim](https://diveintopython3.problemsolving.io/).
- 📘 [«Inside The Python Virtual Machine»](https://leanpub.com/insidethepythonvirtualmachine/read).
- 📘 [«From Python to NumPy» — Rougier](https://www.labri.fr/perso/nrougier/from-python-to-numpy/).
- 📘 [«Dive into Deep Learning» — d2l.ai](https://d2l.ai/).

### Документация (закладывать в браузер)

- [docs.python.org/3](https://docs.python.org/3/)
- [peps.python.org](https://peps.python.org/) — все PEP'ы.
- [docs.astral.sh/uv](https://docs.astral.sh/uv/) / [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)
- [docs.pydantic.dev](https://docs.pydantic.dev/)
- [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- [docs.sqlalchemy.org/en/20](https://docs.sqlalchemy.org/en/20/)

### YouTube (англ)

- [mCoding](https://www.youtube.com/@mCoding) — тонкости языка.
- [ArjanCodes](https://www.youtube.com/@ArjanCodes) — дизайн и архитектура.
- [Anthony Sottile](https://www.youtube.com/@anthonywritescode) — глубокие разборы.
- [Sebastián Ramírez (tiangolo)](https://www.youtube.com/@tiangolo) — автор FastAPI.
- [Corey Schafer](https://www.youtube.com/@coreyms) — лучший для новичков.
- [Real Python](https://www.youtube.com/@realpython).
- [PyCon talks](https://www.youtube.com/@PyConUS).
- [Michael Kennedy (Talk Python)](https://www.youtube.com/@talkpython).

### YouTube / каналы на русском

- [selfedu (Балакирев)](https://www.youtube.com/@selfedu_rus) — большой курс Python.
- [PyLounge](https://www.youtube.com/@PyLounge) — практические разборы.
- [Диджитализируй!](https://www.youtube.com/@digitalize_me) — современный стек.

### Подкасты

- [Python Bytes](https://pythonbytes.fm/) — еженедельные новости.
- [Talk Python To Me](https://talkpython.fm/) — длинные интервью.
- [Real Python Podcast](https://realpython.com/podcasts/rpp/).
- [Test & Code](https://testandcode.com/) — про тестирование.

### Рассылки (бесплатно)

- [PyCoder's Weekly](https://pycoders.com/).
- [Python Weekly](https://www.pythonweekly.com/).
- [Awesome Python Newsletter](https://python.libhunt.com/newsletter).

---

## 🤖 Вайбкодинг — разработка с AI в 2026

> Вайбкодинг (vibe coding) — стиль работы, когда ты задаёшь *направление и контекст*, а LLM пишет код. Ты ревьюишь, ведёшь архитектуру, отвечаешь за качество. Это **базовый навык Python-разработчика 2026 года**.

```
   ТЫ                                LLM
┌────────────┐                   ┌────────────┐
│ контекст   │ ────задача────►   │ генерация  │
│ архитектура│                   │ кода       │
│ ревью      │ ◄────патч─────    │            │
│ тесты      │                   │            │
└────────────┘                   └────────────┘
```

### Стек вайбкодинга 2026

| Категория | Инструменты | Когда использовать |
|---|---|---|
| **Агент в IDE** | Cursor, Windsurf | многошаговая правка нескольких файлов |
| **Агент в CLI** | Claude Code, Aider | рефакторинг, агент видит весь проект |
| **Автодополнение** | GitHub Copilot, Codeium, Supermaven | повседневный typing-by-typing |
| **Open-source / локально** | Continue.dev + ollama (qwen2.5-coder, deepseek-coder, codestral) | приватность, нет интернета |
| **Чат-ассистент** | Claude.ai, ChatGPT, локальный open-webui | архитектура, ревью, объяснения |

### Главные правила

- 🧠 **LLM = турбо-джун с энциклопедией.** Знает синтаксис лучше тебя, но не помнит вчерашний разговор и врёт уверенно. Контекст — твоя ответственность.
- 📝 **Промпт по структуре CTRL:** Context → Task → Rules → Lens. Дай стек, задачу, ограничения и формат ответа.
- 📁 **`.cursorrules` / `CLAUDE.md`** — зафиксируй стек, запреты, стиль один раз. Агент будет читать каждую сессию.
- 🧪 **TDD-вайбкодинг:** сначала docstring → проси тесты → ревьюй спеку → проси реализацию → запускай pytest.
- 🚨 **Красные флаги в коде от LLM:** `# TODO` без реализации, `eval()` без причины, импорт несуществующего модуля, «магическое» решение сложной задачи в 3 строки.
- 🔒 **Безопасность:** никогда не давай LLM `.env` и секреты; security-критичный код (auth, payments, crypto) — тройное ревью; `gitleaks` в pre-commit.

### Воркфлоу одного дня

```
Утро    → Claude.ai: «декомпозируй фичу X на задачи, укажи риски»
День    → Cursor agent: реализация фичи по @file-mention
Сложное → Claude Code в CLI: «найди все места где...»
Тесты   → «параметризованный pytest для всех edge cases + hypothesis»
PR      → «сформируй PR description, проверь нет ли лишнего»
Review  → «объясни этот патч построчно, найди баги»
```

### Бесплатные ресурсы

- 📕 [Claude Code docs](https://docs.anthropic.com/claude-code), [Cursor docs](https://docs.cursor.com/), [Aider](https://aider.chat/), [Continue.dev](https://docs.continue.dev/).
- 📕 [Ollama library](https://ollama.com/library) — каталог локальных моделей кода.
- 📺 [Andrej Karpathy — Software 1.0/2.0/3.0](https://www.youtube.com/@AndrejKarpathy) — концепция от автора термина.
- 📺 [Anthropic — Claude Code tutorials](https://www.youtube.com/@AnthropicAI).
- 🎓 **Полный урок в курсе:** [course/stage-14-vibecoding.md](course/stage-14-vibecoding.md) — 11 уроков, 5 упражнений, пример `CLAUDE.md`, локальный стек, чеклист.
- 💬 **Telegram:** [@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — свежие модели кода, бенчмарки, инструменты.

---

## 🕸 Парсинг и веб-скрапинг 2026

> Сбор данных с веба — отдельная инженерная дисциплина. Включена в курс как этап 15, потому что почти любой AI/ML/аналитический проект начинается с данных, а API «закрытое» или «дорогое».

### 🧰 Стек 2026

| Слой | Инструмент | Заметка |
|---|---|---|
| HTTP | `httpx` (sync/async, HTTP/2) | Современная замена `requests` |
| HTML | `selectolax` (lexbor) | В 5–20× быстрее BeautifulSoup |
| CSS/XPath | `parsel` | Удобный селекторный API из Scrapy |
| JS-рендер | `Playwright` | Async, авто-ожидания, headless |
| Антидетект | `curl_cffi`, `camoufox`, `playwright-stealth` | TLS-fingerprint, stealth |
| Краулер | `Scrapy 2.12+`, `crawlee-python` | Очереди, дедуп, ретраи |
| LLM-парсинг | `crawl4ai`, `firecrawl`, `markitdown` | HTML → Markdown для RAG |
| Хранение | `Polars` + `Parquet` + `DuckDB` | Аналитика на терабайтах |

### 🧭 Принципы

1. **API > парсинг.** Сначала проверь, есть ли официальное API или скрытый JSON-endpoint в DevTools → Network.
2. **Async > sync.** Один процесс с `asyncio + httpx` тянет 1000+ RPS, не теряя памяти.
3. **Этика и закон.** Уважай `robots.txt`, ToS, GDPR/152-ФЗ. Не собирай персональные данные без основания.
4. **Устойчивость.** `tenacity` для ретраев, `aiolimiter` для rate-limit, кеш через `hishel`.
5. **LLM-friendly формат.** Для RAG/датасетов парси сразу в Markdown через `crawl4ai`.

### 📚 Ресурсы

- 🎓 **Полный урок в курсе:** [course/stage-15-parsing.md](course/stage-15-parsing.md) — 15 уроков, 7 упражнений, антибот, прокси, Scrapy + Crawlee, LLM-парсинг.
- 🛡 **Глубоко про антибот:** [course/stage-15-antibot.md](course/stage-15-antibot.md) — 7 уровней детекта, TLS/JA3, stealth, behavioral.
- 📦 **Готовый стартер:** [templates/scraper-starter](templates/scraper-starter/) — production-ready асинхронный скрапер с Docker и CI.
- 📕 [httpx docs](https://www.python-httpx.org), [Playwright Python](https://playwright.dev/python/), [Scrapy docs](https://docs.scrapy.org).
- 📕 [Apify Academy](https://docs.apify.com/academy) — бесплатные курсы по скрапингу.
- 📕 [crawl4ai](https://github.com/unclecode/crawl4ai), [firecrawl](https://github.com/mendableai/firecrawl) — LLM-friendly парсеры.
- 💬 **Telegram:** [@pythonl](https://t.me/pythonl) — Python-практика, [@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — датасеты под ML.

---

## 💬 Telegram-каналы 2026

> Главное место для оперативных новостей, разборов и обсуждения. Подпишись на 3–4 основных.

### 🎁 Отборная папка ресурсов (one-click setup)

> 📚 **[Открыть папку →](https://t.me/addlist/8vDUwYRGujRmZjFi)** — одним нажатием добавь себе кураторскую подборку лучших каналов по Python, ML, DS, AI и инфраструктуре. Это короткий путь к качественной ленте: меньше шума — больше пользы. Идеально для тех, кто только начинает и не хочет тратить недели на поиск «правильных» каналов.

### 🐍 Python — must-read

- 📣 **[t.me/pythonl](https://t.me/pythonl)** — главный русскоязычный канал: новости, библиотеки, разборы, вакансии. **Подписаться в первую очередь.**
- 💬 [@ru_python](https://t.me/ru_python) — чат и канал русскоязычного сообщества.
- 💬 [@async_python](https://t.me/async_python) — про asyncio, конкурентность, performance.
- 💬 [@pythontalk](https://t.me/pythontalk) — обсуждения, флуд, q&a.
- 💬 [@python_easy_en](https://t.me/python_easy_en) — короткие подсказки на каждый день.
- 💬 [@PythonHub](https://t.me/PythonHub) — англоязычный агрегатор статей.

### 🤖 AI / ML / Data Science — практика и код

- 🔥 **[t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — практика и примеры кода по AI / ML / Big Data на Python: разборы моделей, ноутбуки, бенчмарки, свежие статьи и репозитории. **Лучший источник, если идёшь в ML/DS.**
- 📊 [@data_analysis_ml](https://t.me/data_analysis_ml) — анализ данных и Machine Learning на практике.
- 🧠 [@machinelearning_interview](https://t.me/machinelearning_interview) — подготовка к собеседованиям по ML.
- 🤖 [@ds_interview_lib](https://t.me/ds_interview_lib) — задачи и тесты по Data Science.

### 🛠 Бэкенд / DevOps / Архитектура

- 🌐 [@django_prog](https://t.me/django_prog) — Django, FastAPI, веб-разработка.
- 🐳 [@DevOPSitsec](https://t.me/DevOPSitsec) — Docker, Kubernetes, CI/CD.
- 🏗 [@SystemDesign](https://t.me/SystemDesign) — system design, архитектура распределённых систем.

---

## 🧠 Платформы для практики

```
   ┌─────── НАЧИНАЮЩИМ ───────┐  ┌─── СРЕДНИЙ УРОВЕНЬ ───┐  ┌── ПРОДВИНУТЫЕ ──┐
   │ Exercism                 │  │ LeetCode               │  │ Advent of Code  │
   │ CheckiO                  │  │ Codewars               │  │ Project Euler   │
   │ Edabit                   │  │ HackerRank             │  │ Codeforces      │
   │ pythontutor.ru           │  │ Kaggle Learn           │  │ Open-source PR  │
   └──────────────────────────┘  └────────────────────────┘  └─────────────────┘
```

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
- [ ] Регулярно делаю code review
- [ ] Веду личный блог / репозиторий-дневник
- [ ] Подписан на [t.me/pythonl](https://t.me/pythonl) и читаю регулярно

---

## 🤝 Контрибьют

Pull requests welcome:
- Исправления опечаток и неточностей
- Свежие ресурсы 2026 года (**только бесплатные!**)
- Переводы и адаптации
- Новые примеры кода

## 📜 Лицензия

MIT — используй свободно, упоминание автора приветствуется.

> ⭐ Если roadmap оказался полезным — поставь звезду репозиторию и подпишись на [t.me/pythonl](https://t.me/pythonl).
