# Этап 14. Вайбкодинг — AI-assisted разработка для Python в 2026

> ⏱ Время: 1–2 недели  
> 🎯 Цель: научиться писать код **в паре с LLM** так, чтобы получать в 5–10 раз больше результата без потери качества. Освоить Claude Code, Cursor, GitHub Copilot, локальные модели через ollama. Понять, где AI помогает, а где — мешает.

> 💡 **Вайбкодинг** (vibe coding) — стиль разработки, когда ты задаёшь *направление и контекст*, а LLM пишет код. Ты ревьюишь, правишь, ведёшь архитектуру. Это не «AI пишет за тебя», это **новая роль программиста** — оператор-архитектор.

---

## 📘 Урок 14.1 — Карта инструментов 2026

```
┌───────────────────────────────────────────────────────────────┐
│                    ВАЙБКОДИНГ-СТЕК 2026                       │
├───────────────────────────────────────────────────────────────┤
│  AGENT-РЕЖИМ (правит проект сам)                              │
│    ├─ Claude Code (CLI)          — терминал, файловые правки  │
│    ├─ Cursor / Windsurf          — IDE с агентом              │
│    └─ Aider                      — open-source CLI            │
│                                                               │
│  АВТОДОПОЛНЕНИЕ (по строке/блоку)                             │
│    ├─ GitHub Copilot             — VS Code/JetBrains          │
│    ├─ Codeium / Supermaven       — бесплатные альтернативы    │
│    └─ Continue.dev               — open-source, любая модель  │
│                                                               │
│  ЧАТ-АССИСТЕНТЫ                                               │
│    ├─ Claude.ai / ChatGPT        — браузер                    │
│    └─ Локально: ollama + open-webui                           │
│                                                               │
│  МОДЕЛИ КОДА (2026, open weights)                             │
│    ├─ Qwen3-Coder, DeepSeek-Coder-V3, Codestral               │
│    └─ Запуск: ollama / llama.cpp / vLLM                       │
└───────────────────────────────────────────────────────────────┘
```

**Что выбрать новичку:**
- Бесплатно и быстро: **GitHub Copilot** (бесплатен для студентов и OSS-разработчиков) + **Claude.ai** (бесплатный тариф) для архитектурных вопросов.
- Хочешь приватность и контроль: **ollama + Continue.dev** локально.
- Готов вкладываться в продуктивность: **Cursor** или **Claude Code** — agent-режим экономит часы.

---

## 📘 Урок 14.2 — Mental model: почему вайбкодинг работает

LLM — это **stateless turbo-junior с энциклопедической памятью**. Он:
- ✅ Знает синтаксис, библиотеки, паттерны лучше тебя.
- ✅ Печатает в 100 раз быстрее.
- ❌ Не помнит вчерашний разговор.
- ❌ Не видит твой проект целиком.
- ❌ Уверенно врёт, если не хватает контекста (галлюцинации).

**Главный принцип:** твоя работа — *компенсировать его слабости контекстом*, а не делать его работу руками.

```
       ТЫ                                LLM
   ┌────────────┐                   ┌────────────┐
   │ контекст   │ ────задача────►   │ генерация  │
   │ архитектура│                   │ кода       │
   │ ревью      │ ◄────патч─────    │            │
   │ тесты      │                   │            │
   └────────────┘                   └────────────┘
```

---

## 📘 Урок 14.3 — Анатомия хорошего промпта

Плохой промпт:
> «Напиши функцию для парсинга CSV»

Хороший промпт (структура **CTRL**: Context → Task → Rules → Lens):

```
[CONTEXT]
Python 3.13, проект на FastAPI + SQLAlchemy 2.x async.
Файл app/imports/csv_loader.py.
Загружаем CSV пользователей (id, email, created_at) до 100 МБ.

[TASK]
Реализуй async-функцию load_users(path: Path) -> AsyncIterator[User],
которая стримит строки без загрузки всего файла в память.

[RULES]
- type hints обязательно, проверяется pyright --strict
- никаких внешних либ кроме polars (уже в проекте)
- ошибки декодирования: пропустить строку, залогировать через structlog
- покрой pytest-тестом с использованием tmp_path

[LENS]
Напиши сначала скелет с docstring и сигнатурой,
потом реализацию, потом тест в tests/test_csv_loader.py.
```

Разница в результате — на порядок.

---

## 📘 Урок 14.4 — Контекст: главный ресурс

LLM «видит» только то, что ты ему дал. Способы расширить контекст:

| Уровень | Инструмент | Когда |
|---|---|---|
| 1 строка | Copilot autocomplete | typing-by-typing |
| 1 файл | Чат с вставленным файлом | мелкие правки |
| Несколько файлов | Cursor @-mentions, Aider /add | фича в модуле |
| Весь проект | Claude Code, Cursor agent, Aider repo-map | рефакторинг |
| Внешние доки | MCP-серверы, RAG | работа с чужим API |

**Правило:** дай минимум, нужный для задачи. Слишком много контекста = модель путается и галлюцинирует.

---

## 📘 Урок 14.5 — Claude Code в терминале

```bash
npm install -g @anthropic-ai/claude-code
cd my-python-project
claude   # запускает агент в текущей папке
```

В сессии ты говоришь нормальным языком, Claude **сам читает файлы, правит, запускает тесты**:

```
> Добавь rate-limiting на POST /tasks: 10 запросов в минуту на IP.
> Используй slowapi. Покрой тестом.

[Claude reads app/main.py, pyproject.toml]
[Claude edits app/main.py — добавляет limiter]
[Claude edits pyproject.toml — добавляет slowapi]
[Claude creates tests/test_ratelimit.py]
[Claude runs: uv run pytest tests/test_ratelimit.py]
✓ 2 passed in 0.45s
```

Твоя работа — **читать diff и принимать/отклонять**. Не «всё подряд yes», а реально ревью.

---

## 📘 Урок 14.6 — Cursor: IDE-вайбкодинг

Cursor — это форк VS Code с встроенным агентом. Ключевые фичи:

- **Cmd+K** — переписать выделенное по описанию.
- **Cmd+L** — чат с проектом, можно `@-mention` файлы, папки, доки.
- **Composer / Agent** — многошаговая правка нескольких файлов.
- **.cursorrules** — файл с правилами проекта, который агент читает каждый раз.

Пример `.cursorrules` для Python-проекта:

```
# Project: Tasks API

## Stack
- Python 3.13, FastAPI, SQLAlchemy 2.x async, Pydantic v2
- uv для зависимостей, ruff + pyright для качества

## Rules
- Используй type hints везде, pyright --strict должен проходить
- Никаких Any и cast — если не получается типизировать, спроси меня
- Pydantic-модели для всех публичных API
- Тесты обязательны для каждого нового публичного метода
- Архитектура: domain/application/infrastructure/interfaces

## Forbidden
- print() — используй structlog
- requests/urllib — только httpx
- pip/poetry — только uv
```

---

## 📘 Урок 14.7 — Локально через ollama + Continue.dev

Когда нужно: чувствительные данные, нет интернета, политика компании.

```bash
# Установка
brew install ollama   # или curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5-coder:7b   # или deepseek-coder-v3, или codestral

# Запуск
ollama serve   # API на localhost:11434
```

В VS Code ставишь расширение **Continue**, в `~/.continue/config.json`:

```json
{
  "models": [{
    "title": "Qwen Coder local",
    "provider": "ollama",
    "model": "qwen2.5-coder:7b"
  }],
  "tabAutocompleteModel": {
    "title": "Qwen autocomplete",
    "provider": "ollama",
    "model": "qwen2.5-coder:1.5b"
  }
}
```

Получаешь приватный Copilot + чат. На M1/M2 Mac или GPU 12+ ГБ работает плавно.

---

## 📘 Урок 14.8 — Тест-первый вайбкодинг (TDD + LLM)

Самый мощный паттерн 2026:

1. Ты пишешь **сигнатуру и docstring** функции.
2. Просишь LLM **сначала написать тесты** по docstring.
3. Ревьюешь тесты — это и есть спека.
4. Просишь реализацию, которая проходит тесты.
5. Запускаешь pytest. Если красное — LLM правит, ты ревьюешь diff.

```python
# 1. Я пишу:
def normalize_phone(raw: str, default_country: str = "RU") -> str:
    """Привести телефон к E.164 (+71234567890).

    >>> normalize_phone("8 (905) 123-45-67")
    '+79051234567'
    >>> normalize_phone("+1 415 555 0100")
    '+14155550100'
    >>> normalize_phone("bad input")
    Traceback (most recent call last):
        ...
    ValueError: not a phone number
    """
    raise NotImplementedError
```

→ LLM: «вот pytest-параметризованные тесты по docstring + реализация через regex».  
Ты: «ок, но не используй regex, есть же `phonenumbers` — он в проекте».  
→ LLM пишет через `phonenumbers`, тесты зелёные.

---

## 📘 Урок 14.9 — Когда LLM мешает

LLM **плох** в:
- **Архитектурных решениях** — он реализует, что попросил, не вопрошая «а нужно ли это вообще». Думай сам.
- **Свежих API** (моложе training cutoff). Дай ему доку в контексте.
- **Длинных рефакторингах** — теряет контекст, ломает несвязанные места. Дроби на шаги.
- **Безопасности** — выдаёт типичные паттерны, не зная твоей модели угроз. Ревьюй security вручную.
- **Производительности** — пишет «работает» вместо «работает быстро». Профилируй сам.

🚨 **Красные флаги в коде от LLM:**
- `# TODO: handle errors` — он забил.
- `eval()`, `exec()` без причины — он галлюцинирует.
- Импорт несуществующего модуля — проверь.
- «Магическое» решение в 3 строки сложной задачи — почти всегда баг.

---

## 📘 Урок 14.10 — Безопасность и гигиена

- **Никогда** не давай LLM `.env`, секреты, ключи. Очисти контекст.
- **Code review LLM-кода = твоя ответственность.** PR подписываешь ты.
- **Pre-commit hooks** обязательны: ruff, pyright, secret-scan (`gitleaks`).
- **CI** должен ловить всё, что LLM может незаметно сломать: типы, тесты, lint.
- Для **production-критичного кода** (auth, payments, crypto) — пиши руками или утраивай ревью.
- В команде договоритесь о правилах: помечаются ли LLM-коммиты, кто ревьюит, что запрещено.

---

## 📘 Урок 14.11 — Воркфлоу одного дня

```
09:00  Утренний план в Claude.ai:
       «Сегодня делаю фичу X. Декомпозируй на задачи,
        предложи риски, что забыл учесть.»

10:00  Реализация в Cursor:
       - открываю модуль, Cmd+L «по @file дополни обработку ошибок»
       - агент пишет, я ревьюю diff построчно

12:00  Сложное место — Claude Code в терминале:
       «Найди все места где мы шлём email и убедись, что
        используется единая шаблонизация.»

14:00  Тесты:
       «Напиши параметризованный pytest для всех edge cases
        в normalize_phone(). Используй hypothesis.»

16:00  PR:
       «Сформируй PR description: что/зачем/как протестировано.
        Проверь, что нет лишних изменений.»

18:00  Review чужого PR:
       Claude.ai: «Объясни этот патч построчно,
        укажи возможные баги и нарушения соглашений проекта.»
```

---

## 🛠 Упражнения

### Упражнение 14.1 — Сравни инструменты
Реализуй одну и ту же задачу (CRUD для заметок на FastAPI) тремя способами:
1. Без AI, руками.
2. С Copilot (только автодополнение).
3. С Claude Code или Cursor Agent (агент пишет сам).
Замерь время. Что заметил по качеству?

### Упражнение 14.2 — .cursorrules / CLAUDE.md
Напиши для своего pet-проекта файл правил (`.cursorrules` для Cursor или `CLAUDE.md` для Claude Code). Зафиксируй: стек, запреты, стиль, обязательные шаги (тесты, lint). Прогони агента на типичной задаче — заметь, как поведение изменилось.

### Упражнение 14.3 — TDD-вайбкодинг
Возьми задачу из этапа 1 («калькулятор римских чисел») или придумай свою. Сначала напиши docstring с примерами, попроси LLM сгенерировать тесты, отревьюй их, потом проси реализацию. Сколько итераций до зелёного pytest?

### Упражнение 14.4 — Локальный стек
Подними `ollama + qwen2.5-coder` локально. Подключи Continue.dev. Сравни качество автодополнения с Copilot на 10 типичных задачах из твоего кода.

### Упражнение 14.5 — Анти-вайбкодинг
Найди в open-source PR с явными признаками LLM-кода без ревью (TODO без реализации, неиспользуемые импорты, неверные API). Опиши, как именно ревьюер должен был это поймать.

---

## ✅ Решение 14.2 (пример CLAUDE.md)

```markdown
# CLAUDE.md — правила работы агента в этом репозитории

## Стек
- Python 3.13 (cpython), uv для зависимостей.
- FastAPI 0.115+, SQLAlchemy 2.x async + asyncpg.
- pyright --strict, ruff (E, F, I, B, UP, SIM, PTH).
- pytest + pytest-asyncio + hypothesis.

## Архитектура
- `app/domain/` — pure Python, не импортирует фреймворк/ORM.
- `app/application/` — use-cases, зависят от portов из `ports.py`.
- `app/infrastructure/` — адаптеры (SQLAlchemy, httpx, redis).
- `app/interfaces/api/` — FastAPI-роутеры, тонкие.

## Стиль
- Type hints везде. Никаких Any/cast без TODO с обоснованием.
- async для I/O. Sync — только pure-computation.
- Логирование: structlog, JSON. print/logging.* запрещены.
- Pydantic v2 модели для всех публичных входов/выходов API.

## Запрещено
- pip, poetry, requirements.txt — только uv.
- requests, urllib — только httpx.
- subprocess(shell=True) с пользовательским вводом.
- Хардкод секретов. Только `Settings(BaseSettings)`.

## Перед коммитом
- `uv run ruff check . --fix && uv run ruff format .`
- `uv run pyright`
- `uv run pytest -x`
- Если что-то красное — НЕ коммить, чини.

## Стиль коммитов
- Conventional Commits: feat:, fix:, refactor:, test:, docs:.
- Краткое описание (< 72 символа) + тело при сложных изменениях.
```

---

## 📚 Бесплатные ресурсы

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — AI-инструменты и модели, разборы, новые стартовые модели для vibe coding.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — Python-новости, AI-тулы, вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**

### 📕 Документация инструментов
- [Claude Code docs](https://docs.anthropic.com/claude-code).
- [Cursor docs](https://docs.cursor.com/).
- [Aider docs](https://aider.chat/) — open-source агент в CLI.
- [Continue.dev](https://docs.continue.dev/) — open-source расширение для VS Code/JetBrains.
- [GitHub Copilot docs](https://docs.github.com/en/copilot).
- [Ollama](https://ollama.com/library) — каталог локальных моделей.

### 📺 Видео
- [Andrej Karpathy — Software 1.0/2.0/3.0](https://www.youtube.com/@AndrejKarpathy) — концепция вайбкодинга от автора термина «software 2.0».
- [Anthropic — Claude Code tutorials](https://www.youtube.com/@AnthropicAI).
- [AI Jason / Fireship / Theo](https://www.youtube.com/@t3dotgg) — практика AI-разработки.

### 💬 Telegram (must-read для этого этапа)
- 🔥 **[@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)** — свежие модели кода, бенчмарки, инструменты вайбкодинга, разборы.
- 🐍 **[@pythonl](https://t.me/pythonl)** — Python-новости, включая AI-инструменты.
- 📚 **[Папка лучших ресурсов 🎁](https://t.me/addlist/8vDUwYRGujRmZjFi)** — кураторская подборка каналов по Python, ML и AI-разработке.

---

## ☑ Чеклист этапа

- [ ] Понимаю, что LLM — это турбо-джун, а не «AI пишет за меня».
- [ ] Умею писать промпт по структуре Context → Task → Rules → Lens.
- [ ] Настроил `.cursorrules` или `CLAUDE.md` под свой проект.
- [ ] Использую TDD-вайбкодинг: тесты до реализации.
- [ ] Знаю, где LLM мешает: архитектура, безопасность, перф.
- [ ] Запустил локальную модель (ollama + qwen-coder) и сравнил с облачной.
- [ ] Не коммичу LLM-код без ревью построчно.
- [ ] Pre-commit, ruff, pyright, pytest, gitleaks — всё в CI.

---

# 🎯 Финал курса

Этот этап завершает курс. У тебя есть всё:
- **Этапы 0–13** — фундамент классического Python-разработчика.
- **Этап 14** — современный навык работы в паре с AI.

Это и есть Python-разработчик 2026 года: глубоко понимает язык, использует AI как мультипликатор, отвечает за качество.

---

[⬅ Этап 13](stage-13-architecture.md) | [📚 Оглавление](README.md) | [🏠 Главная README](../README.md)
