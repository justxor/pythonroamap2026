# Этап 3. ООП и проектирование

> 🎯 Уметь проектировать гибкие, тестируемые системы.
> ⏱ 3 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. Классы и dunder-методы](#урок-1-классы-и-dunder-методы)
- [Урок 2. Наследование, MRO, super](#урок-2-наследование-mro-super)
- [Урок 3. Protocol vs ABC](#урок-3-protocol-vs-abc)
- [Урок 4. SOLID на примерах](#урок-4-solid-на-примерах)
- [Урок 5. Паттерны GoF](#урок-5-паттерны-gof)
- [Упражнения и решения](#упражнения-и-решения)

---

## Урок 1. Классы и dunder-методы

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point): return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
```

### Топ dunder-методов

| Метод | Зачем |
|---|---|
| `__repr__` / `__str__` | вывод для debug / для user |
| `__eq__` + `__hash__` | использование в set/dict |
| `__lt__`, `__gt__` | сортировка |
| `__len__` | `len(obj)` |
| `__iter__` | работа в for |
| `__getitem__` | `obj[i]` |
| `__call__` | `obj()` |
| `__enter__/__exit__` | `with obj:` |

### @property

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

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

### @classmethod, @staticmethod

```python
class User:
    def __init__(self, name: str): self.name = name

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        return cls(d["name"])

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return name.isalpha() and len(name) >= 2
```

---

## Урок 2. Наследование, MRO, super

```python
class Animal:
    def __init__(self, name: str): self.name = name
    def speak(self) -> str: return "..."

class Dog(Animal):
    def speak(self) -> str: return "Woof!"

class Puppy(Dog):
    def speak(self) -> str: return super().speak() + " (cute)"
```

### MRO

```python
class A:
    def hi(self): return "A"
class B(A):
    def hi(self): return "B"
class C(A):
    def hi(self): return "C"
class D(B, C): pass

print(D.__mro__)    # (D, B, C, A, object)
print(D().hi())     # B
```

### Миксины

```python
class SerializableMixin:
    def to_dict(self) -> dict:
        return self.__dict__.copy()

class User(SerializableMixin):
    def __init__(self, name: str): self.name = name

User("Anna").to_dict()   # {'name': 'Anna'}
```

---

## Урок 3. Protocol vs ABC

### ABC — формальное наследование

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
```

Требует **явного** наследования.

### Protocol — структурная типизация (duck typing)

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsArea(Protocol):
    def area(self) -> float: ...

class Circle:                          # без наследования!
    def __init__(self, r): self.r = r
    def area(self) -> float: return 3.14 * self.r ** 2

def total(shapes: list[SupportsArea]) -> float:
    return sum(s.area() for s in shapes)
```

### Когда что

| Нужно | Использовать |
|---|---|
| Формальный «контракт» внутри пакета | ABC |
| «Всё, у чего есть метод X» | Protocol |
| Template method | ABC |
| DI и подмена | Protocol |

**В 2026 — в 90% случаев Protocol.**

---

## Урок 4. SOLID на примерах

### S — Single Responsibility

❌ Класс делает всё:

```python
class Order:
    def calculate_total(self): ...
    def save_to_db(self): ...
    def send_email(self): ...
    def render_html(self): ...
```

✅ Разделение:

```python
class Order: ...
class OrderRepository: ...
class EmailNotifier: ...
class OrderRenderer: ...
```

### O — Open/Closed

Открыт для расширения, закрыт для модификации.

```python
class PricingStrategy(Protocol):
    def price(self, base: float) -> float: ...

class NoDiscount:
    def price(self, base): return base

class PercentOff:
    def __init__(self, pct: float): self.pct = pct
    def price(self, base): return base * (1 - self.pct / 100)
```

Чтобы добавить новый алгоритм — пишем новый класс, старые не трогаем.

### L — Liskov Substitution

Подкласс полноценно заменяет родителя. Прямоугольник vs квадрат — классический контр-пример.

### I — Interface Segregation

Много маленьких Protocol лучше одного «толстого»:

```python
class Readable(Protocol):
    def read(self) -> bytes: ...

class Writable(Protocol):
    def write(self, data: bytes) -> None: ...
```

### D — Dependency Inversion

```python
class Repo(Protocol):
    def find(self, id: int) -> User | None: ...

class Service:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo   # зависим от абстракции
```

---

## Урок 5. Паттерны GoF

### Strategy

```python
@dataclass
class Order:
    total: float
    strategy: PricingStrategy
    def final(self) -> float:
        return self.strategy.price(self.total)
```

### Factory

```python
def make_strategy(kind: str) -> PricingStrategy:
    match kind:
        case "none": return NoDiscount()
        case "10":   return PercentOff(10)
        case _:      raise ValueError(f"unknown: {kind}")
```

### Observer

```python
class Observer(Protocol):
    def __call__(self, event: str) -> None: ...

class Subject:
    def __init__(self): self._observers: list[Observer] = []
    def subscribe(self, ob: Observer): self._observers.append(ob)
    def notify(self, event: str):
        for ob in self._observers: ob(event)
```

### Adapter

```python
class ThirdPartyHTTP:
    def fetch(self, url: str) -> bytes: ...

class HttpClient(Protocol):
    def get(self, url: str) -> str: ...

class Adapter:
    def __init__(self, raw: ThirdPartyHTTP): self.raw = raw
    def get(self, url: str) -> str:
        return self.raw.fetch(url).decode("utf-8")
```

### Repository

```python
class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get(self, id: int) -> User | None: ...

class InMemoryUserRepo:
    def __init__(self): self._data: dict[int, User] = {}
    def add(self, u): self._data[u.id] = u
    def get(self, id): return self._data.get(id)
```

---

## Упражнения и решения

### Упражнение 1. Геометрия через Protocol

Модуль `geometry.py`:
1. `Protocol Shape` с `area()` и `perimeter()`.
2. `Circle, Rectangle, Triangle` (без наследования от Shape).
3. `total_area`, `largest`, `sorted_by_area`.
4. 8+ тестов.

#### Решение

```python
import math
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

@runtime_checkable
class Shape(Protocol):
    def area(self) -> float: ...
    def perimeter(self) -> float: ...

@dataclass
class Circle:
    radius: float
    def area(self): return math.pi * self.radius ** 2
    def perimeter(self): return 2 * math.pi * self.radius

@dataclass
class Rectangle:
    width: float; height: float
    def area(self): return self.width * self.height
    def perimeter(self): return 2 * (self.width + self.height)

@dataclass
class Triangle:
    a: float; b: float; c: float
    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))
    def perimeter(self): return self.a + self.b + self.c

def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)

def largest(shapes: list[Shape]) -> Shape:
    return max(shapes, key=lambda s: s.area())

def sorted_by_area(shapes: list[Shape]) -> list[Shape]:
    return sorted(shapes, key=lambda s: s.area())
```

### Упражнение 2. Generic Repository

`Repository[T]` с методами `add/get/list/delete/update`, JSON-сериализация, 10+ тестов.

---

## Чеклист и ресурсы

- [ ] Объясняю @classmethod / @staticmethod / instance
- [ ] Реализовал 5+ GoF-паттернов
- [ ] Использую Protocol вместо ABC где уместно
- [ ] Понимаю MRO в diamond-наследовании
- [ ] Применяю SOLID при ревью

### 📚 Бесплатные ресурсы

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Документация и материалы:**

- [Refactoring.guru — паттерны Python](https://refactoring.guru/design-patterns/python)
- [faif/python-patterns](https://github.com/faif/python-patterns)
- [ArjanCodes — Design Patterns (YouTube)](https://www.youtube.com/@ArjanCodes/playlists)

---

[← Этап 2](stage-02-idiomatic.md) · [К оглавлению](README.md) · [Этап 4 →](stage-04-typing.md)
