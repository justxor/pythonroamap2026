# Этап 7. Тестирование и качество кода

> 🎯 Покрытие — не цель, а побочный эффект. Цель — уверенность.
> ⏱ 2 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. pytest основы](#урок-1-pytest-основы)
- [Урок 2. Фикстуры и параметризация](#урок-2-фикстуры-и-параметризация)
- [Урок 3. Hypothesis (property-based)](#урок-3-hypothesis-property-based)
- [Урок 4. CI на GitHub Actions](#урок-4-ci-на-github-actions)
- [Упражнения](#упражнения)

---

## Урок 1. pytest основы

```python
def add(a: int, b: int) -> int: return a + b

def test_add() -> None:
    assert add(2, 3) == 5
```

```bash
uv run pytest -v
```

### Параметризация

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3), (-1, 1, 0), (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Проверка исключений

```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_with_message():
    with pytest.raises(ValueError, match="must be positive"):
        validate(-1)
```

### Маркеры

```python
@pytest.mark.slow
def test_heavy(): ...
# pytest -m "not slow"
```

---

## Урок 2. Фикстуры и параметризация

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

### Scope

```python
@pytest.fixture(scope="session")
def heavy(): ...    # один на всю сессию

@pytest.fixture(scope="module")
def per_module(): ...

@pytest.fixture
def per_test(): ...   # default
```

### conftest.py

Фикстуры из conftest.py автоматически доступны во всех тестах ниже.

### Моки

```python
from unittest.mock import MagicMock

def test_email_sent():
    smtp = MagicMock()
    notifier = EmailNotifier(smtp)
    notifier.send("hi")
    smtp.sendmail.assert_called_once()
```

---

## Урок 3. Hypothesis (property-based)

```python
from hypothesis import given, strategies as st

def reverse(s: str) -> str: return s[::-1]

@given(st.text())
def test_reverse_twice(s):
    assert reverse(reverse(s)) == s
```

Hypothesis сгенерирует ~100 строк (включая edge: пустую, эмодзи, NULL) и попытается сломать инвариант.

### Стратегии

```python
st.integers()
st.integers(min_value=0, max_value=100)
st.floats(allow_nan=False)
st.text(max_size=20)
st.lists(st.integers(), min_size=1, max_size=10)
st.dictionaries(st.text(), st.integers())
```

### Инварианты

```python
@given(st.lists(st.integers()))
def test_sort_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.lists(st.integers()))
def test_sort_same_length(xs):
    assert len(sorted(xs)) == len(xs)
```

---

## Урок 4. CI на GitHub Actions

`.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          python-version: "3.13"
      - run: uv sync --all-extras
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pyright
      - run: uv run pytest --cov --cov-report=xml -v
```

---

## Упражнения

### Упражнение. Покрыть Stack тестами на 100%

Возьми `Stack[T]` из этапа 4. Покрой:
1. Все методы на 100% (`pytest --cov`).
2. Property-based через hypothesis:
   - push + pop возвращает исходный элемент
   - push N раз + `__len__` = N
   - после pop всех — пустой
3. Mutation testing (mutmut), цель < 20% выживших.

```bash
uv add --dev pytest pytest-cov hypothesis mutmut
uv run pytest --cov=stack --cov-report=term-missing
uv run mutmut run --paths-to-mutate=stack.py
```

---

## Чеклист и ресурсы

- [ ] Покрытие > 80%
- [ ] Есть property-based тесты
- [ ] CI собирает: lint + typecheck + test
- [ ] pre-commit
- [ ] pytest-xdist для параллельного запуска
- [ ] Различаю mock / stub / fake

Ресурсы:
- 📘 [pytest docs](https://docs.pytest.org/)
- 📘 [Hypothesis docs](https://hypothesis.readthedocs.io/)
- 🎥 [Test & Code podcast](https://testandcode.com/)
- 🎥 [Anthony Sottile — pytest](https://www.youtube.com/@anthonywritescode)
- 📘 [Awesome pytest plugins](https://github.com/augustogoulart/awesome-pytest)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 6](stage-06-async.md) · [К оглавлению](README.md) · [Этап 8 →](stage-08-cpython.md)
