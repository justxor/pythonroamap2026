# Этап 1. Основы языка

> 🎯 Уверенно реализовать любой алгоритм на чистом Python.
> ⏱ 3–4 недели.

[← К оглавлению](README.md) · [← Этап 0](stage-00-environment.md)

## Содержание

- [Урок 1. Типы данных и операторы](#урок-1-типы-данных-и-операторы)
- [Урок 2. Строки и f-strings](#урок-2-строки-и-f-strings)
- [Урок 3. Коллекции](#урок-3-коллекции)
- [Урок 4. Управление потоком и match/case](#урок-4-управление-потоком-и-matchcase)
- [Урок 5. Функции](#урок-5-функции)
- [Урок 6. Исключения](#урок-6-исключения)
- [Урок 7. Контекстные менеджеры](#урок-7-контекстные-менеджеры)
- [Упражнения](#упражнения)
- [Решения](#решения)
- [Чеклист](#чеклист)
- [Ресурсы](#ресурсы)

---

## Урок 1. Типы данных и операторы

### Числовые типы

```python
i: int = 42
f: float = 3.14
c: complex = 1 + 2j

# Большие числа без переполнения
big = 10 ** 100
```

### Decimal — для денег

```python
from decimal import Decimal

# ❌ Опасно
print(0.1 + 0.2)               # 0.30000000000000004

# ✅ Точно
print(Decimal("0.1") + Decimal("0.2"))   # 0.3
```

### Операторы

```python
a, b = 7, 3
print(a + b, a - b, a * b)
print(a / b)     # 2.333... (float division)
print(a // b)    # 2 (integer division)
print(a % b)     # 1
print(a ** b)    # 343
```

### Цепочки сравнений

```python
age = 25
if 18 <= age < 65:
    print("работоспособный возраст")
```

---

## Урок 2. Строки и f-strings

### Базовое

```python
s = "Hello, World!"
print(len(s))         # 13
print(s.upper())
print(s.split(", "))  # ['Hello', 'World!']
print(s.replace("World", "Python"))
```

### f-strings

```python
name, age = "Anna", 30

print(f"{name} is {age} years old")
print(f"{name=}, {age=}")    # debug-форма
print(f"Сумма: {3 + 5}")
```

### Форматирование

```python
pi = 3.14159265

print(f"{pi:.2f}")         # 3.14
print(f"{pi:10.2f}")       # '      3.14'
print(f"{pi:_>10.2f}")     # '______3.14'
print(f"{1_000_000:_}")    # 1_000_000
print(f"{255:#x}")         # 0xff
print(f"{255:08b}")        # 11111111
```

### bytes

```python
b = "Привет".encode("utf-8")
print(b.decode("utf-8"))   # Привет
```

---

## Урок 3. Коллекции

### list

```python
xs: list[int] = [1, 2, 3]
xs.append(4)            # [1, 2, 3, 4]
xs.insert(0, 0)         # [0, 1, 2, 3, 4]
xs.pop()                # удаляет последний
xs.remove(2)            # удаляет первое вхождение значения
xs.sort()
xs.reverse()

# Срезы
print(xs[1:4])      # [1, 2, 3]
print(xs[::2])      # каждый второй
print(xs[::-1])     # реверс
```

### tuple

```python
point: tuple[int, int] = (3, 4)
x, y = point        # распаковка

# tuple единственного элемента — обязательная запятая
single = (42,)
```

### set / frozenset

```python
unique = {1, 2, 2, 3}     # {1, 2, 3}
unique.add(4)
unique.discard(99)        # не упадёт если нет

a, b = {1, 2, 3}, {2, 3, 4}
print(a & b)              # пересечение: {2, 3}
print(a | b)              # объединение
print(a - b)              # разность: {1}
```

### dict

```python
user: dict[str, int] = {"id": 1, "age": 25}
print(user["id"])
print(user.get("name", "default"))

for key, value in user.items():
    print(key, value)

# Объединение dict (3.9+)
merged = {"a": 1} | {"b": 2}
```

### Когда что использовать

| Нужно | Тип |
|---|---|
| упорядоченная последовательность с изменениями | `list` |
| фиксированная пара/тройка значений | `tuple` |
| коллекция уникальных значений | `set` |
| key → value | `dict` |
| ключ-композиция (frozen) | `frozenset` |

---

## Урок 4. Управление потоком и match/case

### Циклы

```python
for i in range(5):
    print(i)

# С индексом
for i, x in enumerate(["a", "b", "c"]):
    print(i, x)

# Параллельно
for name, age in zip(["A", "B"], [20, 30]):
    print(name, age)
```

### match/case (3.10+)

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
```

### Сопоставление с dataclass

```python
from dataclasses import dataclass

@dataclass
class Point: x: int; y: int

def quadrant(p: Point) -> str:
    match p:
        case Point(x=0, y=0): return "origin"
        case Point(x=0, y=_): return "y-axis"
        case Point(x=_, y=0): return "x-axis"
        case Point(x=x, y=y) if x > 0 and y > 0: return "Q1"
        case _: return "other"
```

---

## Урок 5. Функции

### Базовое

```python
def add(a: int, b: int) -> int:
    """Возвращает сумму двух чисел."""
    return a + b
```

### Аргументы

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

greet("Anna")                    # Hello, Anna!
greet("Anna", greeting="Hi")     # именованный
```

### *args, **kwargs

```python
def total(*nums: float, scale: float = 1.0, **labels: str) -> float:
    print(labels)
    return sum(nums) * scale

total(1, 2, 3, scale=2, source="api")
```

### Positional-only, keyword-only

```python
def f(pos1, pos2, /, normal, *, kw1, kw2) -> None:
    ...
# pos1, pos2 — только позиционно
# normal — как угодно
# kw1, kw2 — только по имени
```

### Замыкания и nonlocal

```python
def counter():
    n = 0
    def inc() -> int:
        nonlocal n
        n += 1
        return n
    return inc

c = counter()
print(c(), c(), c())    # 1 2 3
```

---

## Урок 6. Исключения

### try / except / else / finally

```python
def divide(a: float, b: float) -> float:
    try:
        result = a / b
    except ZeroDivisionError:
        return float("inf")
    except (TypeError, ValueError) as e:
        print(f"error: {e}")
        raise
    else:
        # выполнится, если не было исключения
        return result
    finally:
        # выполнится всегда
        print("cleanup")
```

### Свои классы

```python
class AppError(Exception): pass
class NotFoundError(AppError): pass

class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"{field}: {reason}")
        self.field = field
        self.reason = reason

try:
    raise ValidationError("user_id", "must be >= 0")
except AppError as e:
    print(type(e).__name__, e)
```

### raise ... from

```python
try:
    int("abc")
except ValueError as e:
    raise AppError("неверный формат") from e
```

### Что НЕ делать

- ❌ `except:` без класса (ловит `KeyboardInterrupt` тоже)
- ❌ `except Exception: pass` — глотает ошибки
- ❌ Использовать исключения для управления нормальным потоком

---

## Урок 7. Контекстные менеджеры

### with

```python
with open("data.txt") as f:
    content = f.read()
# файл закроется автоматически
```

### Свой класс

```python
class Database:
    def __enter__(self):
        print("connect")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("disconnect")
        return False   # вернуть True — подавить исключение

    def query(self, sql: str):
        print(f"SQL: {sql}")

with Database() as db:
    db.query("SELECT 1")
```

### @contextmanager

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

### suppress

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    open("not-exists.txt").read()
# код продолжится
```

---

## Упражнения

### Упражнение 1. CLI-калькулятор

Напиши `calc.py`:

1. Принимает выражение: `python calc.py "2 + 2 * 3"`.
2. Операции: `+ - * / // %`.
3. История в `history.json` (max 50 записей).
4. `--history` — последние 10.
5. `--clear` — очистка.
6. Использует `match/case`.
7. **БЕЗ** `eval()` и сторонних пакетов.

### Упражнение 2. CSV → JSON парсер

Напиши `csv2json.py`:

1. Парсит CSV (заголовки в первой строке).
2. Конвертирует в JSON-массив.
3. Флаги: `--pretty`, `--out FILE`.
4. Автоматически приводит числа и bool (`"42"` → `42`, `"true"` → `true`).
5. UTF-8 для кириллицы.

### Упражнение 3. Анализатор текста

Напиши `analyze.py`:

1. Всего слов, уникальных слов.
2. Средняя длина слова и предложения.
3. Топ-10 частых слов (без стоп-слов).
4. Топ-10 длинных уникальных слов.

---

## Решения

### Решение 1: CLI-калькулятор

```python
"""calc.py — CLI-калькулятор."""
from __future__ import annotations

import argparse
import json
import operator
import re
import sys
from pathlib import Path

HISTORY_FILE = Path("history.json")
MAX_HISTORY = 50

OPS = {
    "+": operator.add, "-": operator.sub, "*": operator.mul,
    "/": operator.truediv, "//": operator.floordiv, "%": operator.mod,
}

TOKEN = re.compile(r"\\s*(\\d+\\.?\\d*|//|[+\\-*/%])\\s*")


def tokenize(expr: str) -> list[str]:
    tokens, pos = [], 0
    while pos < len(expr):
        m = TOKEN.match(expr, pos)
        if not m:
            raise ValueError(f"unexpected at {pos}: {expr[pos:]!r}")
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


def evaluate(tokens: list[str]) -> float:
    if not tokens:
        raise ValueError("empty expression")
    result = float(tokens[0])
    i = 1
    while i < len(tokens):
        op, rhs = tokens[i], float(tokens[i + 1])
        if op not in OPS:
            raise ValueError(f"unknown op: {op}")
        try:
            result = OPS[op](result, rhs)
        except ZeroDivisionError as e:
            raise ValueError("division by zero") from e
        i += 2
    return result


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))


def save_history(h: list[dict]) -> None:
    HISTORY_FILE.write_text(
        json.dumps(h[-MAX_HISTORY:], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="CLI-калькулятор")
    p.add_argument("expression", nargs="?")
    p.add_argument("--history", action="store_true")
    p.add_argument("--clear", action="store_true")
    args = p.parse_args(argv)

    match (args.clear, args.history, args.expression):
        case (True, _, _):
            HISTORY_FILE.unlink(missing_ok=True)
            print("history cleared")
        case (_, True, _):
            for entry in load_history()[-10:]:
                print(f"{entry['expr']} = {entry['result']}")
        case (_, _, None):
            p.print_help(); return 1
        case (_, _, expr):
            try:
                result = evaluate(tokenize(expr))
            except ValueError as e:
                print(f"error: {e}", file=sys.stderr)
                return 2
            print(result)
            h = load_history()
            h.append({"expr": expr, "result": str(result)})
            save_history(h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Решение 2: CSV → JSON

```python
"""csv2json.py — CSV → JSON конвертер."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def coerce(value: str) -> Any:
    low = value.strip().lower()
    if low == "true": return True
    if low == "false": return False
    try: return int(value)
    except ValueError: pass
    try: return float(value)
    except ValueError: pass
    return value


def csv_to_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{k: coerce(v) for k, v in row.items()} for row in reader]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args(argv)

    records = csv_to_records(args.path)
    text = json.dumps(records, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.out: args.out.write_text(text, encoding="utf-8")
    else: sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Решение 3: Анализатор текста

```python
"""analyze.py — анализатор текста."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "to", "of", "in", "on",
    "и", "в", "не", "на", "с", "что", "как", "это", "по", "от", "за",
    "а", "но", "же", "так", "то", "у", "из", "о", "для", "к",
}

WORD_RE = re.compile(r"[\\w'-]+", re.UNICODE)
SENT_RE = re.compile(r"[.!?]+\\s*")


def analyze(text: str, stop: set[str]) -> dict:
    words = [w.lower() for w in WORD_RE.findall(text)]
    sentences = [s for s in SENT_RE.split(text) if s.strip()]
    counts = Counter(w for w in words if w not in stop)
    return {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "avg_word_len": round(sum(len(w) for w in words) / max(len(words), 1), 2),
        "avg_sentence_len": round(len(words) / max(len(sentences), 1), 2),
        "top_10_frequent": counts.most_common(10),
        "top_10_longest": sorted(set(words), key=len, reverse=True)[:10],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    args = p.parse_args()
    stats = analyze(args.path.read_text(encoding="utf-8"), STOP_WORDS)
    for k, v in stats.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

---

## Чеклист

- [ ] Решил 30+ задач на pythontutor.ru / CheckiO / Exercism
- [ ] Реализовал минимум 2 упражнения из этого этапа
- [ ] Уверенно использую f-strings и `match/case`
- [ ] Различаю изменяемые и неизменяемые типы
- [ ] Написал свою иерархию исключений
- [ ] Понимаю LEGB scope

---

## 📚 Бесплатные ресурсы

### 🚀 Главные Telegram-источники (подпишись первым делом)

1. 🤖 **[t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — практика и примеры кода по Python, AI/ML, Big Data. Свежие модели, ноутбуки, разборы статей. Полезен с самых первых шагов: видишь, *куда* приведёт язык.
2. 🐍 **[t.me/pythonl](https://t.me/pythonl)** — главный канал по Python: новости, библиотеки, разборы, рубрика «задача дня», вакансии. Идеально для ежедневной прокачки на этапе основ.
3. 📚 **[Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка лучших каналов по Python, ML, DS, AI и инфраструктуре. Один клик — и у тебя готовая лента качественных источников на весь курс.

### 📘 Учебники и туториалы

- [Официальный туториал Python (RU)](https://docs.python.org/3/tutorial/index.html) — первоисточник, читать обязательно
- [pythontutor.ru](https://pythontutor.ru/) — учебник + задачи с визуализацией выполнения
- [Real Python — Basics](https://realpython.com/tutorials/basics/) — короткие практические статьи
- [Automate the Boring Stuff (free)](https://automatetheboringstuff.com/) — классика для быстрого старта

### 🎮 Тренажёры и задачи

- [CheckiO](https://checkio.org/) — игровые задачи на Python
- [Exercism — Python track](https://exercism.org/tracks/python) — задачи с менторской обратной связью
- [edabit](https://edabit.com/challenges/python3) — короткие задачи на 5–15 минут

### 🎥 Видео-курсы

- [Corey Schafer — Python Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) (EN)
- [selfedu — Python 3 (RU)](https://www.youtube.com/@selfedu_rus) — системный курс на русском
- [mCoding](https://www.youtube.com/@mCoding) (EN) — короткие ролики про идиомы и подводные камни

### 📖 Шпаргалки

- [Python Cheatsheet (gto76)](https://github.com/gto76/python-cheatsheet) — самый полный one-page reference
- [PEP 8 (RU)](https://pep8.ru/doc/pep8/) — стиль кода

---

[← Этап 0](stage-00-environment.md) · [К оглавлению](README.md) · [Этап 2 →](stage-02-idiomatic.md)
