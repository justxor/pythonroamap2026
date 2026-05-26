# 📝 Промпт 12 — Commit / PR / Changelog

> Используй когда: написал кучу кода, надо красиво оформить.

---

```
[CONTEXT]
Команда использует Conventional Commits (feat, fix, refactor, test, docs, chore, perf).
PR пойдёт на ревью к старшим разработчикам.

[DIFF]
[ВСТАВЬ DIFF / СПИСОК ИЗМЕНЁННЫХ ФАЙЛОВ С ОПИСАНИЕМ]

[TASK]
Сгенерируй:
1) Commit-сообщение (или несколько, если стоит разбить).
2) PR description.
3) Запись в CHANGELOG.md (если public-facing изменение).

[RULES]
- Заголовок коммита ≤ 72 символа.
- Глаголы в повелительном наклонении («add», «fix», не «added»).
- Тело коммита — что и **почему**, не как (как — это diff).
- PR description: проблема → решение → как протестировано → скриншоты/логи (если нужны) → breaking changes.
- CHANGELOG: формат Keep a Changelog (Added/Changed/Fixed/Removed).
- Не упоминать имена коллег без необходимости. Никаких внутренних ссылок.

[LENS]
1) **Commit-сообщение(я)** — в блоке кода, готовое для \`git commit -m\`.
2) **PR description** — markdown.
3) **CHANGELOG entry** — если нужно.
4) **Совет** — стоит ли разбить на несколько коммитов и почему.
```
