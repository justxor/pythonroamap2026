# Этап 4. Типизация

> 🎯 Пройти `pyright --strict` без `Any`. Норма 2026.
> ⏱ 2 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. Базовые аннотации](#урок-1-базовые-аннотации)
- [Урок 2. Generics PEP 695](#урок-2-generics-pep-695)
- [Урок 3. Protocol, TypedDict, Literal](#урок-3-protocol-typeddict-literal)
- [Урок 4. Pydantic v2](#урок-4-pydantic-v2)
- [Упражнения](#упражнения)

---

## Урок 1. Базовые аннотации

```python
name: str = "Anna"
age: int = 30
xs: list[int] = [1, 2, 3]
d: dict[str, int] = {"a": 1}

# Optional (3.10+)
def find(id: int) -> str | None: ...

# Callable
from collections.abc import Callable
def apply(fn: Callable[[int, int], int], a: int, b: int) -> int:
    return fn(a, b)

# Iterable — самое широкое
from collections.abc import Iterable
def total(xs: Iterable[float]) -> float:
    return sum(xs)
```

---

## Урок 2. Generics PEP 695

```python
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, x: T) -> None: self._items.append(x)
    def pop(self) -> T: return self._items.pop()

def first[T](xs: list[T]) -> T | None:
    return xs[0] if xs else None
```

### Несколько параметров

```python
class Pair[K, V]:
    def __init__(self, key: K, value: V) -> None:
        self.key, self.value = key, value
```

### Ограничения

```python
class Sized[T: (str, bytes, list)]:
    def __init__(self, value: T): self.value = value
    def length(self) -> int: return len(self.value)
```

---

## Урок 3. Protocol, TypedDict, Literal

### Protocol

```python
from typing import Protocol

class HasLen(Protocol):
    def __len__(self) -> int: ...

def total_len(items: list[HasLen]) -> int:
    return sum(len(x) for x in items)
```

### TypedDict

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: int
    name: str
    email: NotRequired[str]
```

### Literal

```python
from typing import Literal

Mode = Literal["read", "write", "append"]

def open_file(path: str, mode: Mode) -> None: ...
open_file("a.txt", "foo")    # pyright: error
```

### TypeIs (PEP 742)

```python
from typing import TypeIs

def is_str_list(xs: list[object]) -> TypeIs[list[str]]:
    return all(isinstance(x, str) for x in xs)

def process(xs: list[object]) -> None:
    if is_str_list(xs):
        # pyright знает: xs: list[str]
        print(",".join(xs))
```

### Self, Final, Override

```python
from typing import Self, Final, override

API_URL: Final = "https://api.example.com"

class Builder:
    def add(self, x: int) -> Self:
        self.items.append(x)
        return self

class Base:
    def hi(self) -> str: return "Base"

class Child(Base):
    @override
    def hi(self) -> str: return "Child"
```

---

## Урок 4. Pydantic v2

```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class User(BaseModel):
    id: int
    email: EmailStr
    age: int = Field(ge=0, le=150)
    tags: list[str] = []

    @field_validator("tags")
    @classmethod
    def lower(cls, v: list[str]) -> list[str]:
        return [t.lower() for t in v]

u = User.model_validate({"id": 1, "email": "a@b.c", "age": 30, "tags": ["A"]})
print(u.model_dump_json())
```

### TypeAdapter

```python
from pydantic import TypeAdapter

ta = TypeAdapter(list[int])
print(ta.validate_python(["1", 2, "3"]))   # [1, 2, 3]
```

---

## Упражнения

### Упражнение 1. Generic Stack PEP 695

В `stack.py` реализуй `Stack[T]` (push, pop, peek, __len__, __iter__, __contains__, is_empty). pyright strict, 10+ тестов.

#### Решение

```python
from collections.abc import Iterator

class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T:
        if not self._items: raise IndexError("pop from empty stack")
        return self._items.pop()
    def peek(self) -> T:
        if not self._items: raise IndexError("peek on empty stack")
        return self._items[-1]
    def __len__(self) -> int: return len(self._items)
    def __iter__(self) -> Iterator[T]: return reversed(self._items)
    def __contains__(self, item: object) -> bool: return item in self._items
    def is_empty(self) -> bool: return not self._items
```

### Упражнение 2. Pydantic-схема Task API

`TaskCreateRequest`: title (3..200), priority (Literal low/med/high), due (datetime, не в прошлом).
`TaskResponse`: id, title, priority, done, created_at, due.
`TaskUpdateRequest`: все опционально.
Валидатор: priority=high требует due.

#### Решение

```python
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, model_validator

Priority = Literal["low", "med", "high"]

class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    priority: Priority = "med"
    due: datetime | None = None

    @model_validator(mode="after")
    def validate(self) -> "TaskCreateRequest":
        if self.due and self.due < datetime.now(timezone.utc):
            raise ValueError("due cannot be in the past")
        if self.priority == "high" and self.due is None:
            raise ValueError("priority=high requires due")
        return self

class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    priority: Priority | None = None
    due: datetime | None = None
    done: bool | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: Priority
    done: bool
    created_at: datetime
    due: datetime | None = None
```

---

## Чеклист и ресурсы

- [ ] pyright --strict проходит
- [ ] Использую PEP 695 generics
- [ ] Различаю Protocol vs ABC
- [ ] Применяю TypeGuard/TypeIs
- [ ] Кастомные валидаторы Pydantic

Ресурсы:

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**
- 📘 [typing — docs](https://docs.python.org/3/library/typing.html)
- 📘 [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- 📘 [pyright docs](https://microsoft.github.io/pyright/)
- 📘 [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
- 📘 [PEP 695](https://peps.python.org/pep-0695/), [PEP 742](https://peps.python.org/pep-0742/)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 3](stage-03-oop.md) · [К оглавлению](README.md) · [Этап 5 →](stage-05-stdlib.md)
