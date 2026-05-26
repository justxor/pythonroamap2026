# 🔄 Промпт 08 — Переписать sync в async

> Используй когда: код блокирующий (requests, time.sleep, sync-БД), а проект на FastAPI/asyncio.

---

```
[CONTEXT]
Python 3.13, проект полностью async (FastAPI + async SQLAlchemy + httpx).

[SYNC CODE]
[ВСТАВЬ ИСХОДНЫЙ SYNC-КОД]

[TASK]
Переведи в async, сохранив поведение.

[RULES]
- requests → httpx.AsyncClient.
- time.sleep → asyncio.sleep.
- threading → asyncio.TaskGroup / asyncio.gather.
- sync БД → SQLAlchemy 2.x async / asyncpg.
- CPU-bound участки (если есть): asyncio.to_thread() — НЕ блокировать event loop.
- Таймауты обязательно (httpx timeout, asyncio.wait_for).
- async with для всех ресурсов.
- Обработка CancelledError — пробрасывать наверх, не глотать.

[LENS]
1) **Список замен** — что → на что.
2) **Async-версия кода**.
3) **Подводные камни** — что может сломаться (порядок выполнения, ресурсы, ограничения).
4) **Тест** — pytest-asyncio пример.
```
