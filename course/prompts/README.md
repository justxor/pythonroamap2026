# 📝 Библиотека промптов — готовые шаблоны для AI-агентов

> Коллекция отлаженных промптов под Python-задачи 2026. Скопировал → подставил свой контекст → получил результат на порядок лучше, чем «напиши функцию для X».

Все промпты построены по структуре **CTRL** (см. [stage-14-vibecoding.md](../stage-14-vibecoding.md)):

```
[CONTEXT]  стек, проект, файл
[TASK]     что нужно сделать
[RULES]    ограничения, запреты, стиль
[LENS]     формат ответа, последовательность
```

---

## 🗂️ Каталог

| Файл | Когда использовать |
|---|---|
| [01-generate-tests.md](01-generate-tests.md) | Сгенерировать pytest-тесты по сигнатуре/docstring |
| [02-code-review.md](02-code-review.md) | Ревью своего кода или чужого PR |
| [03-refactor.md](03-refactor.md) | Рефакторинг без изменения поведения |
| [04-explain-code.md](04-explain-code.md) | Разобрать незнакомый код построчно |
| [05-fix-bug.md](05-fix-bug.md) | Починить баг по traceback / описанию |
| [06-design-api.md](06-design-api.md) | Спроектировать REST/FastAPI-эндпоинт |
| [07-sql-query.md](07-sql-query.md) | Написать SQL / SQLAlchemy 2.x запрос |
| [08-async-rewrite.md](08-async-rewrite.md) | Переписать sync-код в async |
| [09-type-annotate.md](09-type-annotate.md) | Добавить типы в нетипизированный код |
| [10-docker-ci.md](10-docker-ci.md) | Написать Dockerfile / GitHub Actions workflow |
| [11-arch-review.md](11-arch-review.md) | Архитектурное ревью / границы модулей |
| [12-commit-pr.md](12-commit-pr.md) | Описать commit / PR / changelog |
| [13-write-scraper.md](13-write-scraper.md) | Написать веб-скрапер под конкретный сайт |
| [14-find-hidden-api.md](14-find-hidden-api.md) | Найти скрытое JSON API, cURL → httpx |
| [15-ml-baseline.md](15-ml-baseline.md) | ML-baseline за 5 минут (polars + LightGBM + MLflow) |
| [16-feature-ideas.md](16-feature-ideas.md) | Брейншторм 20 идей фичей с риском утечки |
| [17-explain-shap.md](17-explain-shap.md) | Интерпретация SHAP-результатов для бизнеса |
| [18-async-refactor.md](18-async-refactor.md) | Перевод sync-кода в async: blocking calls → TaskGroup + timeout |
| [19-async-review.md](19-async-review.md) | Async code review по чеклисту из 12 пунктов |
| [20-async-bench.md](20-async-bench.md) | Бенчмарк asyncio vs uvloop vs nogil-threads vs processes |
| [21-dockerfile-review.md](21-dockerfile-review.md) | Ревью Dockerfile по 14 пунктам (multi-stage, security, layers) |
| [22-compose-to-k8s.md](22-compose-to-k8s.md) | Конвертация docker-compose в production k8s/Helm |
| [23-image-slim.md](23-image-slim.md) | Радикальное сокращение Docker-образа (1+ГБ → ~120МБ) |

---

## 🎓 Как пользоваться

1. **Открой нужный промпт**, скопируй текст.
2. **Подставь свой контекст** в плейсхолдеры `<...>`.
3. **Вставь файлы / сниппеты** туда, где написано `[ВСТАВЬ КОД]`.
4. Отправь в Claude / ChatGPT / Cursor chat / Claude Code.
5. **Ревьюй ответ построчно** перед применением.

---

## 💡 Универсальные правила

- Длинный контекст ≠ хороший результат. Дай **минимум, нужный для задачи**.
- Очисти секреты: `.env`, ключи, токены, PII — никогда в промпте.
- Если результат не тот — не «переделай», а **уточни ограничение или контекст**.
- Сохраняй удачные промпты — со временем у тебя соберётся свой набор.

---

## 📚 Источники

- 🎓 Полный урок: [course/stage-14-vibecoding.md](../stage-14-vibecoding.md).
- 📕 [Anthropic — Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering).
- 📕 [OpenAI Cookbook](https://cookbook.openai.com/).
- 💬 Telegram: [@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — свежие примеры промптов и моделей.

---

[⬅ Назад к курсу](../README.md)
