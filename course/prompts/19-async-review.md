# 19 — Async code review

> Промпт для проверки асинхронного кода на типовые баги и антипаттерны.

---

## Промпт

```
Ты — senior Python-ревьюер с фокусом на asyncio.
Проведи ревью файла ниже по чеклисту:

Проверь каждый пункт и отметь находки:

1. **Blocking calls в async-коротинах**: `time.sleep`, `requests`, `psycopg2`, синхронный file I/O.
2. **Глотание `CancelledError`**: `except Exception` вокруг await.
3. **Fire-and-forget без ссылки на task**: `asyncio.create_task(...)` без сохранения.
4. **Отсутствие таймаутов**: внешние вызовы без `asyncio.timeout()`.
5. **Неограниченный gather**: `gather(*coros)` при большом N без `Semaphore`.
6. **Пулы без lifespan**: открываются, но не закрываются.
7. **`asyncio.run` вложенный**: вызовы внутри async-функции.
8. **Мутабельный shared state без `asyncio.Lock`**.
9. **Старые API**: `asyncio.wait_for` (вместо `asyncio.timeout`), `get_event_loop` (вместо `get_running_loop`), свой loop.
10. **Отсутствие graceful shutdown**: нет обработки SIGTERM.
11. **Нет backpressure**: `asyncio.Queue` без `maxsize`.
12. **TaskGroup vs gather**: есть ли смысл перевести на `TaskGroup` для лучшей отмены.

Формат ответа:
- Находки по пунктам с номерами строк.
- Severity (BLOCKER / HIGH / MEDIUM / LOW).
- Конкретный фикс для каждой находки.
- Итоговая оценка production-readiness (0–10).

--- FILE START ---
{paste your async code here}
--- FILE END ---
```

## Связанные материалы

- [Курс по асинхронности — Антипаттерны](../async-course.md#урок-14--антипаттерны)
- [Production-чеклист](../async-course.md#урок-15--production-чеклист)
