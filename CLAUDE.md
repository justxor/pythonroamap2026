# CLAUDE.md — правила работы AI-агентов в этом репозитории

> Этот файл читают AI-агенты (Claude Code, Cursor с `.cursorrules`, Aider) при работе с репозиторием. Он зафиксирован для **примера в рамках курса**: смотри как должен выглядеть production-ready agent-config для Python-проекта 2026 года.

---

## 🎯 Что это за репозиторий

Учебный репозиторий — **Python Roadmap 2026 + практический курс**. Содержит:
- `README.md` — расширенный роадмап изучения Python в 2026.
- `course/` — практический курс из 15 этапов (stage-00 … stage-14) с уроками, упражнениями и решениями.
- `course/prompts/` — библиотека готовых промптов для AI-агентов по каждой теме.

Контент — на русском языке. Код в примерах — Python 3.13+.

---

## 🧰 Стек 2026 (для всех code-примеров в курсе)

- **Python 3.13+** (поддержка free-threaded `3.13t` и JIT).
- **Зависимости:** `uv` (заменяет pip + venv + poetry + pyenv).
- **Качество кода:** `ruff` (lint + format), `pyright --strict` (типы).
- **Тесты:** `pytest`, `pytest-asyncio`, `hypothesis`.
- **Web:** `FastAPI` + `Pydantic v2`.
- **Async HTTP:** `httpx`.
- **БД:** `SQLAlchemy 2.x async` + `asyncpg` + `Alembic`.
- **Data:** `Polars`, `DuckDB`, `NumPy`.
- **Логи:** `structlog` (JSON).
- **Наблюдаемость:** OpenTelemetry.
- **Контейнеры:** Docker multi-stage, не-root юзер, healthcheck.

---

## 📐 Архитектурные принципы (используются в примерах stage-13)

- `app/domain/` — pure Python, без фреймворков и ORM.
- `app/application/` — use-cases, зависимости через Protocol-порты.
- `app/infrastructure/` — адаптеры (БД, HTTP, очереди).
- `app/interfaces/api/` — тонкие FastAPI-роутеры.
- Зависимости направлены **внутрь**: домен ничего не импортирует из адаптеров.

---

## ✍️ Стиль кода в примерах курса

### Обязательно
- Type hints на всех публичных функциях и методах.
- Pydantic v2 `BaseModel` для всех публичных API-входов/выходов.
- `async def` для I/O. Sync — только чистые вычисления.
- f-strings вместо `%` или `.format()`.
- `pathlib.Path` вместо `os.path`.
- `structlog.get_logger()` вместо `print` или `logging.*`.
- Контекстные менеджеры (`with`/`async with`) для всех ресурсов.

### Запрещено
- `pip`, `poetry`, `requirements.txt` — только `uv` и `pyproject.toml` + `uv.lock`.
- `requests`, `urllib` — только `httpx`.
- `subprocess(shell=True, ...)` с пользовательским вводом.
- `eval()`, `exec()` — никогда.
- Mutable default arguments (`def f(x=[])`).
- `Any` и `cast()` без TODO-комментария с обоснованием.
- Хардкод секретов. Только `pydantic_settings.BaseSettings` + переменные окружения.
- `print()` в production-коде.

---

## ✅ Чеклист перед коммитом

Агент должен прогонять перед каждым commit:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run pyright
uv run pytest -x --ff
```

Если что-то красное — **не коммитим**, чиним. Никаких `# type: ignore` без объяснения.

---

## 📝 Стиль коммитов

Conventional Commits:

```
feat:     новая фича
fix:      исправление бага
refactor: рефакторинг без изменения поведения
test:     добавление/правка тестов
docs:     документация
chore:    инфраструктура (CI, deps, build)
perf:     ускорение
```

Заголовок ≤ 72 символа. Тело — при сложных изменениях.

---

## 🤖 Правила для агента

1. **Всегда сначала читай:** этот `CLAUDE.md`, `course/README.md` и затронутые файлы.
2. **Не выдумывай API.** Если не знаешь точно — спроси или проверь по существующему коду.
3. **Маленькие изменения.** Один логический шаг = один diff. Не смешивай рефакторинг и фичу.
4. **Тесты** — для каждой новой публичной функции/эндпоинта.
5. **Не правь несвязанные файлы** «заодно».
6. **Markdown-файлы курса:** соблюдай существующую структуру (🎯 цель, 📘 уроки, 🛠 упражнения, ✅ решения, 📚 ресурсы, ☑ чеклист, навигационные ссылки).
7. **Безопасность.** Не предлагай решений с `eval`, `shell=True`, хардкодом секретов даже если просят. Спрашивай уточнения.

---

## 📚 Где смотреть примеры

Если не уверен в стиле — посмотри как сделано в:
- `course/stage-07-testing.md` — pytest, fixtures, Hypothesis.
- `course/stage-09-web.md` — FastAPI, Pydantic, DI.
- `course/stage-13-architecture.md` — гексагональная архитектура, Outbox.
- `course/stage-14-vibecoding.md` — сам урок про работу с AI.

Готовые промпты — в `course/prompts/`.

---

*Этот файл — часть учебного курса. Он же служит примером `CLAUDE.md` для упражнения 14.2.*
