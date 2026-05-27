# Этап 8. CPython внутри — байткод, GIL, no-GIL, JIT, профилирование

> ⏱ Время: 2 недели  
> 🎯 Цель: понять, как Python исполняет твой код. Уметь читать байткод, профилировать, оптимизировать, объяснить GIL, free-threaded mode (PEP 703) и JIT (PEP 744).

---

## 📘 Урок 8.1 — Модель исполнения

```
src.py ──[lexer]──> tokens ──[parser]──> AST ──[compile]──> bytecode (.pyc)
                                                                │
                                                                ▼
                                                    ┌──────────────────┐
                                                    │  CPython VM      │
                                                    │  стек-машина     │
                                                    │  (eval loop)     │
                                                    └─────────┬────────┘
                                                              ▼
                                                    нативные вызовы C
```

Каждый `.py` компилируется в **байткод** (`__pycache__/*.pyc`), который исполняется виртуальной машиной CPython — это **стековая машина**.

### Что почитать прямо в Python
```python
import dis, ast
dis.dis(lambda x: x + 1)        # байткод
print(ast.dump(ast.parse("x+1"), indent=2))  # AST
```

---

## 📘 Урок 8.2 — Читаем байткод

```python
def f(xs: list[int]) -> int:
    total = 0
    for x in xs:
        total += x
    return total

import dis; dis.dis(f)
```

Ключевые опкоды Python 3.13:
| Опкод | Что делает |
|---|---|
| `LOAD_FAST` | положить локальную переменную на стек |
| `STORE_FAST` | снять со стека → локальная переменная |
| `BINARY_OP` | бинарная операция (+,-,*,…) |
| `CALL` | вызов функции |
| `RETURN_VALUE` | вернуть со стека |
| `FOR_ITER` | шаг итератора |

⚙️ В 3.13 включён **adaptive interpreter** (PEP 659): горячие опкоды специализируются (`BINARY_OP` → `BINARY_OP_ADD_INT`).

---

## 📘 Урок 8.3 — Объектная модель и refcount

```python
import sys
a = []
print(sys.getrefcount(a))  # 2 (a + аргумент)
b = a
print(sys.getrefcount(a))  # 3
```

- Все объекты в Python — `PyObject` с refcount + типом.
- Освобождение: **счётчик ссылок → 0** + сборщик циклов (gc).
- `__slots__` экономит память: вместо `__dict__` — массив.

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y
# vs обычный класс — экономия ~50% памяти на миллионах объектов
```

---

## 📘 Урок 8.4 — GIL: что это и почему он есть

**GIL (Global Interpreter Lock)** — мьютекс, который защищает internal state CPython. В любой момент **только один поток** исполняет байткод.

```
Поток 1 ──[удерживает GIL 5мс]──┐
                                 ├── переключение
Поток 2 ─────────────────────────┘
```

Из-за GIL **CPU-bound** многопоточность в Python не ускоряет. Что делать:
- **I/O-bound** → потоки/asyncio (GIL отпускается на I/O).
- **CPU-bound** → `multiprocessing`, `concurrent.futures.ProcessPoolExecutor`, нативные расширения (NumPy, Polars) которые отпускают GIL.
- **2026** → free-threaded build (PEP 703).

---

## 📘 Урок 8.5 — Free-threaded Python (PEP 703)

С 3.13 доступна сборка `python3.13t` **без GIL** (экспериментально). С 3.14 — стабильнее.

```bash
uv python install 3.13t
uv run --python 3.13t python -c "import sys; print(sys._is_gil_enabled())"
```

```python
# CPU-bound параллельно (раньше так было нельзя!)
from concurrent.futures import ThreadPoolExecutor

def heavy(n: int) -> int:
    s = 0
    for i in range(n):
        s += i * i
    return s

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(heavy, [10_000_000] * 8))
```

На free-threaded build получишь почти линейный speed-up.

---

## 📘 Урок 8.6 — JIT (PEP 744)

С 3.13 экспериментальный **copy-and-patch JIT**. Включается флагом сборки. С 3.14/3.15 — будет в релизных билдах.

```bash
PYTHON_JIT=1 python myscript.py   # если собран с --enable-experimental-jit
```

Эффект: 5–30% на типичном коде, до 2x на численных циклах.

---

## 📘 Урок 8.7 — Профилирование: cProfile, py-spy, line_profiler

### cProfile (встроен)
```bash
python -m cProfile -o out.prof myscript.py
python -m pstats out.prof
# в pstats: sort cumulative; stats 20
```

### py-spy (sampling profiler, без модификации кода)
```bash
uv tool install py-spy
py-spy record -o flame.svg --pid 12345
py-spy top --pid 12345
```

### line_profiler (по строкам)
```python
@profile  # ставится через kernprof
def hot_function() -> None: ...
```

```bash
uv add --dev line_profiler
kernprof -l -v myscript.py
```

### memray (память)
```bash
uv add --dev memray
python -m memray run myscript.py
python -m memray flamegraph memray-*.bin
```

---

## 📘 Урок 8.8 — Простые оптимизации, которые дают 10x

1. **Локальные переменные быстрее глобальных** — кешируй методы:  
   `append = lst.append` в горячем цикле.
2. **`set` вместо `list` для проверки членства**: `x in s` это O(1) vs O(n).
3. **Comprehensions** быстрее ручных циклов с `.append()`.
4. **f-string** быстрее `%` и `.format()`.
5. **NumPy/Polars** вместо ручных циклов по большим массивам — отдают GIL и работают на C.
6. **functools.lru_cache** на чистых функциях.
7. Профилируй **до** оптимизаций. "Premature optimization is the root of all evil." (Knuth)

---

## 🛠 Упражнения

### Упражнение 8.1 — Дизасм
Возьми функцию `fib(n)` (рекурсивную и итеративную). Сравни их байткод через `dis.dis`. Какая короче?

### Упражнение 8.2 — Память slots
Создай `class Point` обычный и со `__slots__`. Создай по 1 млн объектов. Сравни память (`tracemalloc`).

### Упражнение 8.3 — GIL vs процессы
Напиши CPU-bound функцию `pi_montecarlo(samples)`. Запусти на:
- 1 потоке;
- 4 потоках через ThreadPoolExecutor;
- 4 процессах через ProcessPoolExecutor.
Измерь время. Объясни результат.

### Упражнение 8.4 — Профиль
Возьми любой свой скрипт > 1с. Запусти `py-spy record`, открой flamegraph, найди топ-3 узких места.

---

## ✅ Решение 8.2

```python
import tracemalloc

class A:
    def __init__(self, x: int, y: int) -> None: self.x, self.y = x, y

class B:
    __slots__ = ("x", "y")
    def __init__(self, x: int, y: int) -> None: self.x, self.y = x, y

def measure(cls: type) -> int:
    tracemalloc.start()
    items = [cls(i, i) for i in range(1_000_000)]
    cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak

print("dict:",  measure(A))   # ~ 180 MB
print("slots:", measure(B))   # ~ 80  MB
```

## ✅ Решение 8.3

```python
import time, random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def pi(n: int) -> float:
    inside = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x*x + y*y < 1: inside += 1
    return 4 * inside / n

N = 5_000_000

def bench(label: str, fn) -> None:
    t = time.perf_counter()
    fn()
    print(f"{label}: {time.perf_counter()-t:.2f}s")

bench("1 поток",  lambda: pi(N))
bench("4 потока", lambda: list(ThreadPoolExecutor(4).map(pi, [N//4]*4)))
bench("4 проц.",  lambda: list(ProcessPoolExecutor(4).map(pi, [N//4]*4)))
# На обычном CPython: процессы ~3.5x, потоки ~1x (GIL)
# На free-threaded: потоки тоже ~3.5x
```

---

## 📚 Бесплатные ресурсы

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**

- 📕 [CPython Internals — Anthony Shaw (free read on archive)](https://realpython.com/cpython-source-code-guide/).
- 📕 [PEP 659 — Adaptive Interpreter](https://peps.python.org/pep-0659/).
- 📕 [PEP 703 — Free-threaded CPython](https://peps.python.org/pep-0703/).
- 📕 [PEP 744 — JIT](https://peps.python.org/pep-0744/).
- 📺 [mCoding — How Python Works](https://www.youtube.com/@mCoding).
- 📺 [PyCon talks — Brandt Bucher (JIT), Sam Gross (no-GIL)](https://www.youtube.com/@PyConUS).
- 🛠 [py-spy](https://github.com/benfred/py-spy), [memray](https://github.com/bloomberg/memray).
- 💬 **Telegram: [@pythonl](https://t.me/pythonl)**.

---

## ☑ Чеклист этапа

- [ ] Читаю `dis.dis` и понимаю основные опкоды.
- [ ] Знаю, что GIL отпускается на I/O и в нативных расширениях.
- [ ] Запускал код на 3.13t (free-threaded).
- [ ] Профилировал через cProfile или py-spy, делал flamegraph.
- [ ] Использую `__slots__` где это уместно.

---

[⬅ Этап 7](stage-07-testing.md) | [📚 Оглавление](README.md) | [Этап 9 ➡](stage-09-web.md)
