# 14. Найти скрытое API и превратить cURL в httpx

> Промпт для быстрого реверса JSON-API сайта без парсинга HTML. Самый быстрый и стабильный способ собрать данные.

---

## 🧭 Алгоритм (делаешь руками)

1. Открой сайт в Chrome/Firefox → DevTools (F12) → вкладка **Network**.
2. Фильтр **Fetch/XHR**.
3. Прокликай нужный функционал (поиск, пагинация, фильтры).
4. Найди запрос с JSON-ответом, в котором есть нужные данные.
5. Правый клик → Copy → **Copy as cURL (bash)**.
6. Вставь в промпт ниже.

---

## 📦 Промпт

```
# Контекст
Я нашёл скрытый JSON-API в DevTools. Вот cURL-запрос:

<ВСТАВЬ cURL СЮДА>

# Задача
1. Преврати cURL в асинхронный httpx-код на Python 3.13.
2. Разбери параметры: какие влияют на пагинацию, фильтры, сортировку.
3. Покажи pydantic v2-схему ответа (создай по примеру JSON).
4. Напиши функцию fetch_page(client, page: int, **filters) -> ResponseModel.
5. Покажи как пройти все страницы (async generator).

# Правила
- httpx.AsyncClient с http2=True, timeout=15, follow_redirects=True.
- Сохрани только необходимые заголовки. Убери лишние (Cookie — только если API их требует).
- type hints, pyright --strict.
- Retry: tenacity 5 попыток, exponential backoff.
- Rate-limit через aiolimiter (1 RPS по умолчанию).
- Логи через structlog.

# Ограничения
- Не обходи captcha/Cloudflare. Если эндпоинт возвращает 401/403 без валидных кук/CSRF — скажи явно, не пытайся подделывать.
- Не вставляй мои cookie в код по умолчанию — вынеси в .env.

# На выходе
- 1 файл кода (api_client.py).
- Объяснение каждого параметра одной строкой.
- Пример вызова с первыми 3 страницами.
```

---

## 💡 Лайфхаки

- **[curlconverter.com](https://curlconverter.com)** — онлайн-конвертер cURL → Python (но LLM разбирается лучше и даёт сразу асинхронный вариант).
- **HAR-экспорт:** DevTools → Network → Export HAR. Можно скормить LLM весь HAR-файл, он сам найдёт нужные вызовы.
- **GraphQL:** проверь, нет ли `__schema { types { name } }` — иногда introspection открыт.
- **gRPC-Web:** если Content-Type `application/grpc-web` — нужны protobuf-схемы, обычный httpx не подойдёт.

---

## 🔗 Связанное

- [Этап 15. Парсинг — урок 7](../stage-15-parsing.md)
- [13-write-scraper.md](./13-write-scraper.md)
