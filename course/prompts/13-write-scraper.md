# 13. Написать скрапер

> Промпт для быстрого создания production-ready веб-скрапера под конкретный сайт. Структура CTRL: Context → Task → Rules → Limits.

---

## 📦 Промпт

```
# Контекст
Я пишу Python 3.13+ скрапер. Стек 2026: httpx (async, HTTP/2), selectolax, tenacity, aiolimiter, structlog, polars, pydantic v2, typer.
Цель — собрать данные с <САЙТ>:
- URL-паттерн листинга: <https://...>
- URL-паттерн детальной страницы: <https://...>
- Поля для извлечения: title, price, sku, image_url, in_stock
- Объём: ~5000 страниц
- HTML отдаётся сервером (SSR) / нужен Playwright — укажи

# Задача
Сделай асинхронный скрапер, который:
1. Читает список URL из файла.
2. Последовательно обходит листинги, собирает ссылки на детальные страницы.
3. Парсит поля в pydantic-модель Product.
4. Сохраняет в Parquet с zstd-сжатием.
5. Логи в JSON-формате через structlog.

# Правила
- httpx.AsyncClient с http2=True, follow_redirects=True, timeout=15.
- tenacity: stop_after_attempt(5), wait_exponential(min=2, max=30).
- aiolimiter: 1 запрос в секунду на домен.
- asyncio.Semaphore(10) для конкуррентности.
- User-Agent с реальным email-контактом.
- robots.txt — проверяем через urllib.robotparser до сбора.
- Все функции с type hints, pyright --strict.
- Без except Exception: — лови только httpx-исключения.
- ConventionalCommits, один коммит на фичу.

# Ограничения
- Не используй requests, BeautifulSoup, urllib3.
- Не обходи анти-бот защиты. Если 403/captcha — логируй и остановись.
- Не храни ПД пользователей.
- < 200 строк на всё решение без тестов.

# На выходе
- Структура файлов (список).
- Код каждого файла.
- Команда запуска.
- Как проверить результат (чтение Parquet в polars).
```

---

## 💭 Как использовать

1. Замени `<САЙТ>` и URL-паттерны на свои.
2. Добавь поля, если выходят за рамки базовых (напр. `currency`, `seller_rating`).
3. Отправь Claude / Cursor / Copilot.
4. Полученный код сравни с [templates/scraper-starter](../../templates/scraper-starter/) — скорее всего скелет будет похож.

---

## 🔗 Связанное

- [Этап 15. Парсинг](../stage-15-parsing.md)
- [templates/scraper-starter](../../templates/scraper-starter/)
- [@pythonl](https://t.me/pythonl), [@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data)
