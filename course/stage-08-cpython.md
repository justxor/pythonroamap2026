# Этап 8. Внутренности CPython

> 🎯 Понимать, как Python работает внутри. Отличает Middle от Senior.
> ⏱ 2–3 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. Байткод и dis](#урок-1-байткод-и-dis)
- [Урок 2. GIL и память](#урок-2-gil-и-память)
- [Урок 3. Профилирование](#урок-3-профилирование)
- [Упражнение](#упражнение)

---

## Урок 1. Байткод и dis

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
# RESUME 0
# LOAD_FAST a
# LOAD_FAST b
# BINARY_OP +
# RETURN_VALUE
```

### Specializing Adaptive Interpreter (PEP 659)

С 3.11 байткод **специализируется** для типов в runtime. `BINARY_OP` заменяется на `BINARY_OP_ADD_INT` — в 1.5-2× быстрее.

### Тонкости

```python
# ❌ вызов append в цикле
for _ in range(1_000_000):
    result.append(x)

# ✅ закешировать атрибут
ap = result.append
for _ in range(1_000_000):
    ap(x)
```

---

## Урок 2. GIL и память

### Reference counting + GC

Python считает ссылки. Когда ссылок 0 — объект удаляется. Циклический GC ловит `a -> b -> a`.

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))   # 2 (x и аргумент)
```

### __slots__ экономит память

```python
class A:
    def __init__(self): self.x = 1; self.y = 2

class B:
    __slots__ = ("x", "y")
    def __init__(self): self.x = 1; self.y = 2

# B без __dict__, экономия 40-50% на больших коллекциях
```

### Free-threaded Python (PEP 703)

В 3.13+ — отдельный билд `python3.13t` без GIL. К 2026 стабилизирован.

---

## Урок 3. Профилирование

### cProfile

```bash
python -m cProfile -o profile.stats my_script.py
python -m pstats profile.stats
```

### py-spy — для продакшна (без перезапуска!)

```bash
uv add --dev py-spy

py-spy record -o profile.svg -- python my_app.py
py-spy top --pid 12345
```

### memray — для памяти

```bash
uv add --dev memray
python -m memray run my_app.py
python -m memray flamegraph memray-my_app.bin
```

### Что искать

1. Hot spots (>50% времени).
2. Аллокации в цикле — наружу.
3. N+1 запросы к БД.
4. Лишние конверсии list ↔ tuple ↔ set.

---

## Упражнение

Ускорить медленный скрипт в 10×:

```python
def slow():
    result = []
    for i in range(1_000_000):
        if i % 2 == 0:
            result.append(str(i) + " is even")
    return "\n".join(result)
```

1. Замерь через `py-spy`.
2. Оптимизируй (генератор, f-string, кеш атрибута, `range(0, N, 2)`).
3. Отчёт: было/стало/почему.

---

## Чеклист и ресурсы

- [ ] Читаю вывод dis
- [ ] Профилировал через py-spy и memray
- [ ] Объясняю, почему GIL — не «питон медленный»
- [ ] Применяю `__slots__` к месту
- [ ] Сравнил CPython vs PyPy

Ресурсы:
- 📘 [«Inside The Python Virtual Machine»](https://leanpub.com/insidethepythonvirtualmachine/read) — free
- 📝 [tenthousandmeters — "Python behind the scenes"](https://tenthousandmeters.com/)
- 📘 [PEP 659](https://peps.python.org/pep-0659/) / [PEP 744](https://peps.python.org/pep-0744/) / [PEP 703](https://peps.python.org/pep-0703/)
- 📘 [py-spy](https://github.com/benfred/py-spy), [memray](https://github.com/bloomberg/memray)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 7](stage-07-testing.md) · [К оглавлению](README.md) · [Этап 9 →](stage-09-web.md)
