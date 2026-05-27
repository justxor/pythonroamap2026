# Этап 0. Окружение 2026

> 🎯 Настроить современный стек: Python 3.13, uv, ruff, pyright, pytest, pre-commit.
> ⏱ 1–2 вечера.

[← К оглавлению курса](README.md)

## Содержание

- [Урок 1. Установка Python 3.13 и uv](#урок-1-установка-python-313-и-uv)
- [Урок 2. Первый проект и зависимости](#урок-2-первый-проект-и-зависимости)
- [Урок 3. ruff, pyright, pytest](#урок-3-ruff-pyright-pytest)
- [Урок 4. pre-commit и базовый CI](#урок-4-pre-commit-и-базовый-ci)
- [Упражнения](#упражнения)
- [Решения](#решения)
- [Чеклист](#чеклист)
- [Бесплатные ресурсы](#бесплатные-ресурсы)

---

## Урок 1. Установка Python 3.13 и uv

### Зачем uv

В 2026 году **uv** — стандарт. Один инструмент заменяет: pip, pipx, venv, poetry, pyenv, pip-tools. Скорость — в 10–100 раз выше pip. Написан на Rust компанией Astral (авторы ruff).

### Установка

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Проверка:

```bash
uv --version
```

### Установка Python 3.13

```bash
uv python install 3.13
uv python list
```

uv сам скачает и распакует нужную версию. Системный Python не трогается.

### Free-threaded билд (для экспериментов)

```bash
uv python install 3.13t   # без GIL, PEP 703
```

---

## Урок 2. Первый проект и зависимости

### Создание проекта

```bash
uv init my-first-project
cd my-first-project
```

uv создаст:

```
my-first-project/
├── .python-version
├── README.md
├── hello.py
└── pyproject.toml
```

### Зависимости

```bash
uv add httpx                              # рантайм
uv add --dev ruff pyright pytest hypothesis pre-commit   # dev
```

После этого появятся:

- `.venv/` — изолированное окружение (в .gitignore).
- `uv.lock` — точные версии (коммитим!).

### Запуск кода

```bash
uv run python hello.py
uv run pytest
```

`uv run` сам активирует venv.

### Структура для серьёзного проекта

```
my-first-project/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── my_pkg/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

### Эталонный pyproject.toml

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

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.13"

[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["tests"]
pythonpath = ["src"]
```

---

## Урок 3. ruff, pyright, pytest

### ruff — линтер и форматтер

```bash
uv run ruff check .              # проверка
uv run ruff check --fix .        # авто-фикс
uv run ruff format .             # форматирование
```

Заменяет: black + isort + flake8 + pylint.

Что выбирать в `select`:

| Код | Что |
|---|---|
| `E`, `F` | базовые pycodestyle/pyflakes |
| `I` | сортировка импортов |
| `B` | bugbear |
| `UP` | модернизация синтаксиса |
| `SIM` | упрощения |
| `RUF` | специфичное для ruff |
| `ANN` | требование аннотаций |
| `C4` | comprehensions |
| `PT` | pytest best practices |

### pyright — статические типы

```bash
uv run pyright
```

В `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "strict"
```

Цель — пройти strict без `Any` и подавлений.

### pytest — тесты

`tests/test_basic.py`:

```python
def add(a: int, b: int) -> int:
    return a + b

def test_add() -> None:
    assert add(2, 3) == 5

def test_add_negative() -> None:
    assert add(-1, 1) == 0
```

```bash
uv run pytest -v
```

---

## Урок 4. pre-commit и базовый CI

### Зачем pre-commit

Хуки запускаются при `git commit`. Если код плохой — коммит не пройдёт.

### Конфиг `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

Активация:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

### Базовый CI на GitHub Actions

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
      - run: uv run pytest -v
```

---

## Упражнения

### Упражнение 1. Создай проект с нуля

С нуля собрать проект `hello-py`:

1. Использует uv и Python 3.13.
2. Модуль `src/hello/main.py` с функцией `greet(name: str) -> str`.
3. Тест `tests/test_main.py` минимум с 2 случаями.
4. ruff (strict select) и pyright (strict) настроены.
5. Все 3 команды зелёные:
   ```bash
   uv run ruff check .
   uv run pyright
   uv run pytest -v
   ```

### Упражнение 2. Сломай и почини pre-commit

1. В проекте из ex-1 подключи pre-commit.
2. Сделай коммит со сломанным кодом — pre-commit должен заблокировать.
3. Исправь и закоммить заново.

---

## Решения

### Решение упражнения 1

**Структура:**

```
hello-py/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── hello/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

**src/hello/main.py:**

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

**tests/test_main.py:**

```python
from hello.main import greet


def test_greet_basic() -> None:
    assert greet("World") == "Hello, World!"


def test_greet_empty() -> None:
    assert greet("") == "Hello, !"
```

**pyproject.toml** (ключевое):

```toml
[project]
name = "hello-py"
version = "0.1.0"
requires-python = ">=3.13"

[dependency-groups]
dev = ["ruff", "pyright", "pytest"]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF", "ANN"]

[tool.pyright]
typeCheckingMode = "strict"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

**.gitignore:**

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
```

### Решение упражнения 2

**.pre-commit-config.yaml:**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: uv run pyright
        language: system
        types: [python]
        pass_filenames: false
```

**Эксперимент:**

1. Добавь `import json` (не используем) в `main.py`.
2. `git add . && git commit -m "test"` → ruff падает на `F401` (unused import).
3. `ruff --fix` автоматически уберёт импорт. Снова коммит — проходит.

---

## Чеклист

- [ ] uv, ruff, pyright, pytest установлены и работают
- [ ] Создан репозиторий-дневник на GitHub
- [ ] pre-commit запускается при `git commit`
- [ ] Понимаю отличие `uv sync` от `pip install -r requirements.txt`
- [ ] Знаю, чем `uv lock` отличается от `pip freeze`

---

## 📚 Бесплатные ресурсы

### 🚀 Главные Telegram-источники

1. 🤖 **[t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — практика и примеры кода по Python, AI/ML, Big Data.
2. 🐍 **[t.me/pythonl](https://t.me/pythonl)** — Python-новости, библиотеки, рубрика «задача дня», вакансии.
3. 📚 **[Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка по Python / ML / DS / AI.

### 📘 Документация и материалы


- 📘 [docs.astral.sh/uv](https://docs.astral.sh/uv/)
- 📘 [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)
- 📘 [pyright getting started](https://microsoft.github.io/pyright/#/getting-started)
- 🎥 [ArjanCodes — Modern Python tooling](https://www.youtube.com/@ArjanCodes)
- 📝 [Hynek Schlawack — Production-ready Python](https://hynek.me/articles/)
- 📘 [Awesome uv](https://github.com/tox-dev/awesome-uv)
- 💬 [t.me/pythonl](https://t.me/pythonl) — новости uv/ruff

---

[← К оглавлению](README.md) · [Дальше: Этап 1. Основы языка →](stage-01-basics.md)
