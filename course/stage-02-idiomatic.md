# Этап 2. Идиоматичный Python

> 🎯 Писать «по-питоновски». Меньше кода — больше выразительности.
> ⏱ 2–3 недели.

[← К оглавлению](README.md) · [← Этап 1](stage-01-basics.md)

## Содержание

- [Урок 1. Итераторы и генераторы](#урок-1-итераторы-и-генераторы)
- [Урок 2. Comprehensions](#урок-2-comprehensions)
- [Урок 3. itertools и functools](#урок-3-itertools-и-functools)
- [Урок 4. Декораторы](#урок-4-декораторы)
- [Урок 5. dataclass / namedtuple / TypedDict](#урок-5-dataclass--namedtuple--typeddict)
- [Урок 6. Антипаттерны → идиомы](#урок-6-антипаттерны--идиомы)
- [Упражнения](#упражнения)
- [Решения](#решения)
- [Чеклист и ресурсы](#чеклист-и-ресурсы)

---

## Урок 1. Итераторы и генераторы

Итератор реализует `__iter__` и `__next__`:

```python
xs = [1, 2, 3]
it = iter(xs)
print(next(it))   # 1
print(next(it))   # 2
```

Генератор — функция с `yield`:

```python
def count_up_to(n: int):
    i = 0
    while i < n:
        yield i
        i += 1

for x in count_up_to(5):
    print(x)
```

### Зачем — экономия памяти

```python
# ❌ грузит всё в память
nums = [x*x for x in range(10_000_000)]

# ✅ ленивая обработка
nums = (x*x for x in range(10_000_000))
for n in nums:
    if n > 100: break
```

### yield from

```python
def flatten(items):
    for x in items:
        if isinstance(x, list):
            yield from flatten(x)
        else:
            yield x

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

---

## Урок 2. Comprehensions

```python
# list
squares = [x*x for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]

# set
unique = {x % 5 for x in range(20)}

# dict
squares_dict = {x: x*x for x in range(10)}

# generator expression
total = sum(x*x for x in range(1000))
```

### Walrus := внутри comprehension

```python
import re

lines = ["a = 1", "noise", "b = 2"]
parsed = [
    {"key": m.group(1), "val": m.group(2)}
    for line in lines
    if (m := re.match(r"(w+)s*=s*(d+)", line))
]
```

**Правило:** если comprehension читается дольше 2 сек — переписать на обычный цикл.

---

## Урок 3. itertools и functools

### itertools

```python
from itertools import chain, islice, pairwise, batched, accumulate

list(chain([1, 2], [3, 4]))    # [1,2,3,4]
list(pairwise([1, 2, 3, 4]))    # [(1,2),(2,3),(3,4)]
list(batched(range(10), 3))     # [(0,1,2),(3,4,5),(6,7,8),(9,)]
list(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10]
```

### functools

```python
from functools import cache, lru_cache, partial, reduce, wraps, singledispatch

@cache                         # без лимита (3.9+)
def fib(n: int) -> int:
    return n if n < 2 else fib(n-1) + fib(n-2)

@lru_cache(maxsize=128)
def slow(x): ...

from operator import mul
double = partial(mul, 2)
print(double(7))   # 14

print(reduce(lambda a, b: a*b, [1,2,3,4]))   # 24
```

### singledispatch — overload по типу

```python
@singledispatch
def render(value) -> str:
    return f"<unknown {value!r}>"

@render.register
def _(value: int) -> str: return f"int={value}"

@render.register
def _(value: list) -> str: return f"list[{len(value)}]"
```

---

## Урок 4. Декораторы

### Базовый

```python
from functools import wraps

def log(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"call {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@log
def add(a, b): return a + b
```

### С аргументами

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
                    if attempt == times: raise
                    print(f"retry {attempt}: {e}")
                    sleep(delay)
        return wrapper
    return decorator

@retry(times=5, delay=0.2)
def flaky() -> str:
    import random
    if random.random() < 0.7: raise RuntimeError("oops")
    return "done"
```

### Стэк декораторов

```python
@timed
@retry(times=3)
def fn(): ...

# равно: timed(retry(times=3)(fn))
# внутренний применяется первым
```

---

## Урок 5. dataclass / namedtuple / TypedDict

### dataclass

```python
from dataclasses import dataclass, field

@dataclass(slots=True, frozen=True)
class Point:
    x: float
    y: float
    label: str = ""
    tags: list[str] = field(default_factory=list)
```

| Параметр | Что даёт |
|---|---|
| `frozen=True` | неизменяемый (hashable) |
| `slots=True` | без __dict__ — экономия памяти |
| `kw_only=True` | все поля только по имени |

### NamedTuple

```python
from typing import NamedTuple

class Vector(NamedTuple):
    x: float
    y: float

v = Vector(1.0, 2.0)
print(v.x, v[0])    # works as tuple
```

### TypedDict

```python
from typing import TypedDict, NotRequired

class User(TypedDict):
    id: int
    name: str
    email: NotRequired[str]
```

---

## Урок 6. Антипаттерны → идиомы

| ❌ Антипаттерн | ✅ Идиома |
|---|---|
| `for i in range(len(xs)): xs[i]` | `for x in xs` |
| `if x in d: v = d[x] else: v = default` | `v = d.get(x, default)` |
| `try/except KeyError` для дефолта | `defaultdict` |
| ручной цикл с append | comprehension |
| `def f(x=[])` | `def f(x=None): x = x or []` |
| `open(); ... close()` | `with open() as ...:` |
| `if x == None` | `if x is None` |
| `type(x) == int` | `isinstance(x, int)` |
| много `if/elif` | `match/case` или dict-lookup |

### Главный капкан: mutable default

```python
# ❌
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))   # ['a']
print(add_item("b"))   # ['a', 'b'] (!) общий список

# ✅
def add_item(item, items=None):
    items = items if items is not None else []
    items.append(item)
    return items
```

### EAFP vs LBYL

EAFP — Easier to Ask Forgiveness than Permission. **Идиоматично для Python.**

```python
# ✅ EAFP
try: value = d["key"]
except KeyError: value = default

# 👌
value = d.get("key", default)

# ❌ LBYL — менее питонично
if "key" in d: value = d["key"]
else: value = default
```

---

## Упражнения

### Упражнение 1. Свои декораторы

Реализуй `decorators.py` с тремя декораторами:

1. **@timed** — печатает время выполнения.
2. **@memoize(maxsize=None)** — свой `@lru_cache` с `.cache_clear()`, поддержка args+kwargs.
3. **@retry(times=3, delay=0.1, exceptions=(Exception,))** — экспоненциальный бэкофф.

Требования: `functools.wraps`, pyright strict, минимум 6 unit-тестов.

### Упражнение 2. Скользящее окно через генератор

```python
list(sliding_window([1, 2, 3, 4, 5], 3))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

Условия:
- Без `itertools.tee` (через `deque`).
- Работает с любым iterable.
- Если `n > len` — пустой генератор.
- Если `n <= 0` — ValueError.

---

## Решения

### Решение 1: Декораторы

```python
"""decorators.py"""
from __future__ import annotations
import time
from collections import OrderedDict
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P"); R = TypeVar("R")


def timed(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try: return fn(*args, **kwargs)
        finally: print(f"{fn.__name__}: {time.perf_counter()-start:.3f}s")
    return wrapper


def memoize(maxsize: int | None = None):
    def decorator(fn):
        cache: OrderedDict[tuple[Any, ...], Any] = OrderedDict()
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            result = fn(*args, **kwargs)
            cache[key] = result
            if maxsize is not None and len(cache) > maxsize:
                cache.popitem(last=False)
            return result
        wrapper.cache_clear = cache.clear  # type: ignore
        return wrapper
    return decorator


def retry(times=3, delay=0.1, exceptions=(Exception,)):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current = delay
            for attempt in range(1, times + 1):
                try: return fn(*args, **kwargs)
                except exceptions as e:
                    if attempt == times: raise
                    print(f"retry {attempt}/{times}: {e}")
                    time.sleep(current)
                    current *= 2
        return wrapper
    return decorator
```

### Решение 2: Sliding window

```python
from collections import deque
from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def sliding_window(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    if n <= 0:
        raise ValueError("n must be > 0")
    it = iter(iterable)
    window: deque[T] = deque(maxlen=n)
    for _ in range(n):
        try: window.append(next(it))
        except StopIteration: return
    yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)
```

---

## Чеклист и ресурсы

### Чеклист

- [ ] Написал минимум 4 декоратора
- [ ] Использую comprehensions/itertools уместно
- [ ] Понимаю @cache vs @lru_cache
- [ ] Не делаю mutable defaults
- [ ] Применяю walrus только где он упрощает код

### 📚 Бесплатные ресурсы

#### 🚀 Главные Telegram-источники

1. 🤖 **[t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — практика и примеры кода по Python, AI/ML, Big Data.
2. 🐍 **[t.me/pythonl](https://t.me/pythonl)** — Python-новости, рубрика «задача дня», вакансии.
3. 📚 **[Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка по Python / ML / DS / AI.

#### 📘 Документация и материалы

- [Python Cookbook (Beazley)](https://github.com/dabeaz/python-cookbook)
- [itertools recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes)
- [Trey Hunner blog](https://treyhunner.com/blog/) — про идиоматичный Python
- [mCoding (YouTube)](https://www.youtube.com/@mCoding) — короткие ролики про идиомы
- [PEP 8](https://peps.python.org/pep-0008/), [PEP 20](https://peps.python.org/pep-0020/)

---

[← Этап 1](stage-01-basics.md) · [К оглавлению](README.md) · [Этап 3 →](stage-03-oop.md)
