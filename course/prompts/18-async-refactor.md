# 18 — Async-рефакторинг

> Промпт для перевода sync-кода на async с выявлением blocking calls.

---

## Промпт

```
Ты — Python-эксперт по асинхронному коду в 2026 году.
Проанализируй sync-файл ниже и переведи его на async по следующим правилам:

1. Используй `asyncio.TaskGroup` (Python 3.11+) вместо `asyncio.gather`.
2. Замени `requests` на `httpx.AsyncClient` (с http2=True).
3. Замени `time.sleep` на `asyncio.sleep`.
4. Для всех внешних вызовов добавь `asyncio.timeout()`.
5. Для ограничения параллелизма добавь `asyncio.Semaphore(N)` (N подбери логически).
6. CPU-bound участки вынеси в `loop.run_in_executor(ProcessPoolExecutor(), ...)`.
7. Добавь type hints (PEP 695 или `Generic`).
8. Не лови `CancelledError` — пробрасывай дальше.

Формат ответа:
- Список выявленных blocking calls (файл:строка).
- Полный async-вариант файла.
- Короткое объяснение каждого существенного изменения.
- Список рисков (race conditions, изменения порядка).

--- FILE START ---
{paste your sync code here}
--- FILE END ---
```

## Когда использовать

- Старый sync-сервис нужно перевести на FastAPI.
- Скрапер на `requests` тормозит на больших объёмах.
- Скрипт с `ThreadPoolExecutor`, который на 90% ждёт сеть.

## Связанные материалы

- [Курс по асинхронности](../async-course.md)
- [Stage 06 — Async](../stage-06-async.md)
