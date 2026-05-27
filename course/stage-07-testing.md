# Этап 7. Тестирование — pytest, hypothesis, mutation, CI

> ⏱ Время: 2 недели  
> 🎯 Цель: писать тесты, которые **реально ловят баги**, а не просто покрывают строки. Освоить pytest, fixtures, параметризацию, моки, property-based тестирование, мутационное тестирование и интеграцию в CI.

---

## 📘 Урок 7.1 — Зачем тестировать и какие бывают тесты

**Пирамида тестов (2026 редакция):**

```
       ▲   E2E (мало, медленно, дорого)
      ╱ ╲
     ╱   ╲ Integration (БД, HTTP, очереди)
    ╱─────╲
   ╱       ╲ Unit (много, быстро, изолировано)
  ╱─────────╲
 ╱  Static   ╲  ← typing, ruff, pyright (бесплатные тесты!)
╱─────────────╲
```

**Правила:**
- 70% юнит, 20% интеграционных, 10% e2e.
- Тест должен падать **по одной причине**.
- Имя теста = спецификация: `test_<что>_<когда>_<ожидаем>`.
- Один `assert` — одна мысль. Множественные `assert` допустимы только в проверке одного объекта.

---

## 📘 Урок 7.2 — pytest за 15 минут

```bash
uv add --dev pytest pytest-cov pytest-asyncio pytest-xdist hypothesis
```

```python
# tests/test_calc.py
import pytest
from app.calc import divide

def test_divide_returns_quotient() -> None:
    assert divide(10, 2) == 5

def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(1, 0)
```

Запуск:
```bash
uv run pytest -q                # тихо
uv run pytest -x --ff           # стоп на первой ошибке, провалившиеся сначала
uv run pytest -k "divide and not zero"
uv run pytest --cov=app --cov-report=term-missing
uv run pytest -n auto           # параллельно (pytest-xdist)
```

**pyproject.toml:**
```toml
[tool.pytest.ini_options]
addopts = "-ra --strict-markers --strict-config"
testpaths = ["tests"]
asyncio_mode = "auto"
filterwarnings = ["error"]      # любое предупреждение = ошибка
```

---

## 📘 Урок 7.3 — Fixtures: подготовка и очистка

Фикстура = функция, которая готовит данные/ресурсы. Pytest подставляет её по имени параметра.

```python
# tests/conftest.py
import pytest
from collections.abc import Iterator
from app.db import Database

@pytest.fixture
def db() -> Iterator[Database]:
    d = Database(":memory:")
    d.migrate()
    yield d               # ← всё до yield = setup, после = teardown
    d.close()

@pytest.fixture(scope="session")
def api_client() -> Iterator["TestClient"]:
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as c:
        yield c
```

**Scopes:** `function` (по умолчанию) → `class` → `module` → `package` → `session`.

**Композиция фикстур:**
```python
@pytest.fixture
def user(db: Database) -> User:
    return db.create_user(email="a@b.c")
```

---

## 📘 Урок 7.4 — Параметризация

```python
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, 2),
        (0, 0, 0),
        (-1, 1, 0),
        pytest.param(10**18, 1, 10**18 + 1, id="huge"),
    ],
)
def test_add(a: int, b: int, expected: int) -> None:
    assert a + b == expected
```

Каскад параметризаций даёт декартово произведение (осторожно — растёт быстро).

---

## 📘 Урок 7.5 — Моки и фейки

**Правило:** не мокай то, чем не владеешь. Оборачивай чужой API своим адаптером и мокай **адаптер**.

```python
from unittest.mock import Mock, AsyncMock, patch

def test_sends_email(monkeypatch: pytest.MonkeyPatch) -> None:
    sent: list[str] = []
    monkeypatch.setattr("app.mailer.smtp_send", lambda to, body: sent.append(to))
    notify("a@b.c", "hi")
    assert sent == ["a@b.c"]

async def test_http_client() -> None:
    client = AsyncMock()
    client.get.return_value.json.return_value = {"ok": True}
    assert await fetch_status(client) is True
```

**Fake вместо Mock** — реализация интерфейса в памяти, ведёт себя как настоящая.

```python
class FakeRepo:
    def __init__(self) -> None:
        self._data: dict[int, User] = {}
    def save(self, u: User) -> None: self._data[u.id] = u
    def get(self, id_: int) -> User | None: return self._data.get(id_)
```

---

## 📘 Урок 7.6 — Property-based тесты (Hypothesis)

Вместо примеров — **свойства**, которые должны выполняться для любых входов.

```python
from hypothesis import given, strategies as st, settings

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs: list[int]) -> None:
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.text(), st.text())
def test_concat_length(a: str, b: str) -> None:
    assert len(a + b) == len(a) + len(b)

@given(st.integers(min_value=1, max_value=10**6))
@settings(max_examples=500)
def test_factorial_positive(n: int) -> None:
    assert factorial(n) > 0
```

Hypothesis сам найдёт минимальный контрпример (shrinking) — это супер-сила.

---

## 📘 Урок 7.7 — Тестирование async-кода

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_fetch() -> None:
    result = await fetch("https://httpbin.org/get")
    assert result.status == 200

# Таймаут
@pytest.mark.asyncio
@pytest.mark.timeout(2)
async def test_slow() -> None:
    await asyncio.sleep(1)
```

---

## 📘 Урок 7.8 — Coverage и качество, а не количество

```bash
uv run pytest --cov=app --cov-fail-under=85 --cov-report=html
```

⚠️ **Coverage ≠ качество**. 100% покрытие легко достичь, не проверяя ничего полезного. Проверяй:
- Граничные значения (0, -1, пустота, переполнение).
- Ошибочные пути (исключения, таймауты, отказы сети).
- Инварианты (через Hypothesis).

---

## 📘 Урок 7.9 — Мутационное тестирование

`mutmut` или `cosmic-ray` ломают твой код (мутируют операторы, константы) и запускают тесты. Если тесты прошли — твои тесты слабые.

```bash
uv add --dev mutmut
uv run mutmut run --paths-to-mutate=app/
uv run mutmut results
```

---

## 📘 Урок 7.10 — CI на GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { python-version: ["3.13", "3.14"] }
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --all-extras --dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pyright
      - run: uv run pytest --cov=app --cov-fail-under=85 -n auto
```

---

## 🛠 Упражнения

### Упражнение 7.1 — Тесты для калькулятора
Дан модуль `calc.py` с функциями `add, sub, mul, div`. Напиши:
1. По 2 теста на каждую функцию (норма + ошибка).
2. Параметризованный тест `test_div_by_zero_raises` для разных типов чисел.
3. Hypothesis-тест: `add(a, b) == add(b, a)` (коммутативность).

### Упражнение 7.2 — Тесты с моками
Функция `notify(user_id)` достаёт юзера из БД и шлёт email. Напиши тест, не используя реальную БД и SMTP. Подсказка: `monkeypatch` + `Fake`.

### Упражнение 7.3 — Async и таймаут
Напиши `async def fetch_with_retry(url, attempts=3)`. Покрой тестами: успех с первой попытки, успех с третьей, исчерпание попыток. Замокай `httpx.AsyncClient`.

### Упражнение 7.4 — Property-based
Реализуй функцию `roundtrip_json(obj) -> obj` (encode → decode). Напиши Hypothesis-тест: для любого `dict[str, int|str|bool|None]` результат равен оригиналу.

---

## ✅ Решение 7.1

```python
# tests/test_calc.py
import pytest
from hypothesis import given, strategies as st
from app.calc import add, sub, mul, div

class TestAdd:
    def test_positive(self) -> None:
        assert add(2, 3) == 5
    def test_negative(self) -> None:
        assert add(-1, -1) == -2

class TestDiv:
    def test_basic(self) -> None:
        assert div(10, 2) == 5
    @pytest.mark.parametrize("a", [1, 1.0, -7, 10**18])
    def test_div_by_zero_raises(self, a: int | float) -> None:
        with pytest.raises(ZeroDivisionError):
            div(a, 0)

@given(st.integers(), st.integers())
def test_add_commutative(a: int, b: int) -> None:
    assert add(a, b) == add(b, a)
```

## ✅ Решение 7.3 (async retry)

```python
# app/fetcher.py
import httpx
from typing import Final

class FetchError(Exception): ...

async def fetch_with_retry(client: httpx.AsyncClient, url: str, attempts: int = 3) -> str:
    last: Exception | None = None
    for _ in range(attempts):
        try:
            r = await client.get(url, timeout=5.0)
            r.raise_for_status()
            return r.text
        except httpx.HTTPError as e:
            last = e
    raise FetchError(f"failed after {attempts} attempts") from last

# tests/test_fetcher.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.fetcher import fetch_with_retry, FetchError

@pytest.mark.asyncio
async def test_success_first_try() -> None:
    client = AsyncMock()
    response = MagicMock(text="ok"); response.raise_for_status = MagicMock()
    client.get.return_value = response
    assert await fetch_with_retry(client, "http://x") == "ok"
    assert client.get.call_count == 1

@pytest.mark.asyncio
async def test_exhausts_attempts() -> None:
    import httpx
    client = AsyncMock()
    client.get.side_effect = httpx.ConnectError("boom")
    with pytest.raises(FetchError):
        await fetch_with_retry(client, "http://x", attempts=3)
    assert client.get.call_count == 3
```

---

## 📚 Бесплатные ресурсы

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**

- 📕 [pytest docs](https://docs.pytest.org/) — официальная документация.
- 📕 [Hypothesis docs](https://hypothesis.readthedocs.io/).
- 📺 [Anthony Sottile — pytest](https://www.youtube.com/@anthonywritescode) — короткие видео по pytest.
- 📕 [Brian Okken — Python Testing](https://pythontest.com/) — блог и подкаст Test & Code.
- 📺 [mCoding — Hypothesis](https://www.youtube.com/@mCoding).
- 💬 **Telegram: [@pythonl](https://t.me/pythonl)** — Python | Машинное обучение | Анализ данных.

---

## ☑ Чеклист этапа

- [ ] Запускаю pytest с `-x --ff -n auto`.
- [ ] Использую fixtures и параметризацию вместо копипасты.
- [ ] Не мокаю чужие библиотеки напрямую — оборачиваю адаптерами.
- [ ] Покрытие ≥ 85%, проверяю граничные случаи.
- [ ] Минимум 1 Hypothesis-тест на критическую функцию.
- [ ] CI прогоняет ruff + pyright + pytest на каждом PR.

---

[⬅ Этап 6](stage-06-async.md) | [📚 Оглавление](README.md) | [Этап 8 ➡](stage-08-cpython.md)
