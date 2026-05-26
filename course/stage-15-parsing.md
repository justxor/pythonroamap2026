# Этап 15. Парсинг и веб-скрапинг (2026)

> 🎯 **Цель этапа:** научиться собирать данные с сайтов современным стеком — от простых HTML-страниц до SPA с JS-рендерингом и анти-бот защитой. С упором на этику, законность и устойчивость.

---

## 🧰 Стек 2026

| Задача | Инструмент | Почему |
|---|---|---|
| HTTP-клиент | `httpx` (sync/async + HTTP/2) | Замена `requests`, асинхронный |
| HTML-парсинг | `selectolax` (lexbor) | В 5–20× быстрее `BeautifulSoup` |
| CSS/XPath | `parsel` | Стандарт из Scrapy, удобный API |
| JS-рендер | `Playwright` | Современнее Selenium, async, авто-ожидания |
| Анти-детект | `playwright-stealth`, `camoufox` | Маскировка отпечатков |
| Краулер | `Scrapy 2.12+`, `crawlee-python` | Очереди, дедуп, ретраи |
| Очереди | `Redis` + `arq` / `taskiq` | Распределённый сбор |
| Хранение | `DuckDB`, `Polars`, `Parquet` | Аналитика на терабайтах |
| Прокси | `httpx-socks`, ротация | Обход rate-limit |
| LLM-парсинг | `firecrawl`, `crawl4ai`, `markitdown` | HTML → Markdown для RAG |

> 💡 В 2026 для AI-данных всё чаще используют **LLM-friendly** парсеры (`crawl4ai`, `firecrawl`), которые сразу выдают чистый Markdown.

---

## ⚖️ Этика и закон (читать до кода!)

1. **`robots.txt`** — уважай, парсь через `urllib.robotparser` или `reppy`.
2. **ToS сайта** — публичные данные ≠ разрешение на массовый сбор.
3. **Персональные данные** — GDPR/152-ФЗ. Не собирай ПД без основания.
4. **Rate-limit** — не больше 1 RPS на домен по умолчанию.
5. **User-Agent** — указывай реальный, с контактом: `MyBot/1.0 (+mailto:me@x.com)`.
6. **Кеширование** — не перезапрашивай одно и то же. `hishel` для HTTP-кеша.
7. **API > парсинг** — если есть официальное API, используй его.

---

## 📘 Уроки

### Урок 1. HTTP-основы: httpx вместо requests

```python
import httpx

# sync
with httpx.Client(http2=True, timeout=10.0, follow_redirects=True) as client:
    r = client.get("https://httpbin.org/get", headers={"User-Agent": "MyBot/1.0"})
    r.raise_for_status()
    print(r.json())

# async
import asyncio

async def fetch(url: str) -> str:
    async with httpx.AsyncClient(http2=True) as client:
        r = await client.get(url)
        return r.text

asyncio.run(fetch("https://example.com"))
```

**Запомни:**
- `http2=True` — многие сайты быстрее по HTTP/2
- `follow_redirects=True` — по умолчанию `False` в httpx
- `timeout` обязателен (иначе зависнет)

### Урок 2. Парсинг HTML: selectolax (быстро) и parsel (удобно)

```python
from selectolax.parser import HTMLParser

html = httpx.get("https://news.ycombinator.com").text
tree = HTMLParser(html)

for node in tree.css("span.titleline > a"):
    print(node.text(), node.attributes.get("href"))
```

Альтернатива с XPath:

```python
from parsel import Selector

sel = Selector(text=html)
titles = sel.xpath("//span[@class=\"titleline\"]/a/text()").getall()
```

**Бенчмарк:** `selectolax` парсит 1000 страниц за ~0.4с, `BeautifulSoup` — за ~8с.

### Урок 3. Асинхронный краулер на httpx + asyncio

```python
import asyncio, httpx
from selectolax.parser import HTMLParser

SEM = asyncio.Semaphore(10)  # макс 10 одновременных запросов

async def crawl(client: httpx.AsyncClient, url: str) -> dict:
    async with SEM:
        r = await client.get(url)
        tree = HTMLParser(r.text)
        title = tree.css_first("title")
        return {"url": url, "title": title.text() if title else None}

async def main(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient(http2=True, timeout=10) as client:
        return await asyncio.gather(*[crawl(client, u) for u in urls])

urls = [f"https://example.com/page/{i}" for i in range(100)]
results = asyncio.run(main(urls))
```

**Практика:** добавь `tenacity` для ретраев, `aiolimiter` для rate-limit 1 RPS.

### Урок 4. Ретраи и устойчивость с tenacity

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
)
async def fetch_safe(client, url):
    r = await client.get(url)
    r.raise_for_status()
    return r
```

### Урок 5. Rate-limit: aiolimiter

```python
from aiolimiter import AsyncLimiter

limiter = AsyncLimiter(1, 1)  # 1 запрос в секунду

async def polite_get(client, url):
    async with limiter:
        return await client.get(url)
```

### Урок 6. JS-рендеринг: Playwright

```python
from playwright.async_api import async_playwright

async def scrape_spa(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 ...",
            viewport={"width": 1280, "height": 800},
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_selector(".product-card")
        html = await page.content()
        await browser.close()
        return html
```

**Когда нужен Playwright:**
- Контент рендерится через JS (React/Vue/Svelte SPA)
- Нужна авторизация через UI
- Сайт ставит куки через JS

**Когда НЕ нужен:**
- HTML отдаётся сервером (SSR) → `httpx` достаточно
- Есть скрытый JSON API → парси его напрямую (DevTools → Network)

### Урок 7. Поиск скрытых API (главный лайфхак)

1. Открой DevTools → вкладка **Network** → фильтр **Fetch/XHR**.
2. Прокликай нужный функционал на сайте.
3. Найди запрос, который возвращает JSON с данными.
4. Скопируй как `cURL` → конвертни в `httpx` через [curlconverter.com](https://curlconverter.com).

Это в 100× быстрее, чем парсить HTML, и стабильнее.

### Урок 8. Анти-бот защита: что бывает и как обходить

| Защита | Признак | Решение |
|---|---|---|
| Rate-limit по IP | 429 после N запросов | Прокси + задержки |
| User-Agent / Headers | 403 без браузерных заголовков | Реальные заголовки браузера |
| JS-челлендж | Пустая страница без JS | Playwright |
| Cloudflare/DataDome | Капча, JS-челлендж | `camoufox`, `playwright-stealth`, иногда платные решатели |
| Fingerprinting | TLS/HTTP2-отпечаток | `curl_cffi` (имитирует TLS Chrome) |
| Behavioral | Подозрительные клики/скролл | Имитация поведения, паузы |

> ⚠️ Обход защит может нарушать ToS и закон. Только для своих проектов и legal-grey зон, понимая риски.

### Урок 9. curl_cffi — обход TLS-фингерпринта

```python
from curl_cffi import requests

r = requests.get("https://protected-site.com", impersonate="chrome120")
print(r.text)
```

Многие защиты ловят `httpx` именно по TLS-отпечатку. `curl_cffi` притворяется реальным Chrome.

### Урок 10. Прокси и их ротация

```python
import random, httpx

PROXIES = [
    "http://user:pass@proxy1:8080",
    "socks5://user:pass@proxy2:1080",
]

async def fetch_via_proxy(url: str):
    proxy = random.choice(PROXIES)
    async with httpx.AsyncClient(proxy=proxy, timeout=15) as c:
        return await c.get(url)
```

**Типы прокси (от дешёвых к дорогим):**
- Datacenter (быстрые, легко детектятся)
- Residential (домашние IP, дороже, незаметнее)
- Mobile (4G/5G, самые незаметные, самые дорогие)

### Урок 11. Scrapy для больших проектов

```python
# spider.py
import scrapy

class HNSpider(scrapy.Spider):
    name = "hn"
    start_urls = ["https://news.ycombinator.com"]
    custom_settings = {
        "CONCURRENT_REQUESTS": 16,
        "DOWNLOAD_DELAY": 0.5,
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "MyBot/1.0 (+mailto:me@x.com)",
    }

    def parse(self, response):
        for item in response.css("tr.athing"):
            yield {
                "title": item.css("span.titleline > a::text").get(),
                "url": item.css("span.titleline > a::attr(href)").get(),
            }
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

**Когда выбрать Scrapy:**
- > 100k страниц
- Нужны pipelines (валидация, дедуп, хранение)
- Распределённый сбор (`scrapy-redis`)

### Урок 12. crawlee-python — современная альтернатива

```python
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler

async def main():
    crawler = BeautifulSoupCrawler(max_requests_per_crawl=50)

    @crawler.router.default_handler
    async def handler(ctx):
        await ctx.enqueue_links()
        await ctx.push_data({"url": ctx.request.url, "title": ctx.soup.title.string})

    await crawler.run(["https://crawlee.dev"])
```

Из коробки: дедуп, ретраи, persist-очередь, прокси-ротация.

### Урок 13. Хранение: Parquet + DuckDB

```python
import polars as pl

# Сохраняем результаты
df = pl.DataFrame(results)
df.write_parquet("data/scraped.parquet", compression="zstd")

# Аналитика через DuckDB прямо по файлам
import duckdb
duckdb.sql("SELECT domain, COUNT(*) FROM 'data/*.parquet' GROUP BY domain").show()
```

### Урок 14. LLM-парсинг: crawl4ai и firecrawl

Для подготовки данных под RAG/обучение моделей удобно сразу получать **Markdown**:

```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com/article")
    print(result.markdown)  # чистый Markdown без шума
```

Или через `firecrawl` (есть бесплатный self-hosted):

```bash
curl -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"url":"https://example.com","formats":["markdown"]}'
```

### Урок 15. Мониторинг и наблюдаемость

- **Логи:** `structlog` с JSON-выводом
- **Метрики:** Prometheus — `requests_total`, `errors_total`, `latency`
- **Tracing:** OpenTelemetry → Jaeger
- **Алерты:** падение success-rate ниже 95% → Telegram-бот

---

## 🛠 Практические упражнения

1. **Hacker News scraper.** Собери топ-30 постов с заголовком, ссылкой, числом голосов. Сохрани в Parquet. Async, 1 RPS, ретраи.
2. **Скрытый API.** Открой DevTools на любимом маркетплейсе, найди JSON-эндпоинт каталога. Спарси 1000 товаров без Playwright.
3. **SPA-сайт.** Через Playwright собери цены с любого SPA-сайта. Дождись `networkidle`.
4. **Pipeline.** Scrapy-проект с pipeline: валидация (`pydantic`), дедуп (по hash URL), сохранение в Postgres.
5. **Защита от обнаружения.** Сделай скрапер с `curl_cffi` impersonate chrome120 + ротацией residential-прокси.
6. **LLM-датасет.** С `crawl4ai` собери 100 статей в Markdown, сложи в DuckDB. Затем построй простой RAG поверх.
7. **Мониторинг.** Подключи `structlog` + Prometheus exporter. Нарисуй дашборд в Grafana.

---

## ✅ Решения / примеры репозиториев

- [scrapinghub/scrapy](https://github.com/scrapy/scrapy) — эталонный код
- [apify/crawlee-python](https://github.com/apify/crawlee-python) — современные паттерны
- [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) — LLM-friendly
- [mendableai/firecrawl](https://github.com/mendableai/firecrawl) — self-hosted

---

## 📚 Ресурсы

**Документация:**
- [httpx docs](https://www.python-httpx.org)
- [Playwright Python](https://playwright.dev/python/)
- [Scrapy docs](https://docs.scrapy.org)
- [selectolax](https://github.com/rushter/selectolax)
- [parsel](https://parsel.readthedocs.io)

**Telegram:**
- [@pythonl](https://t.me/pythonl) — Python новости и практика
- [@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — для LLM-парсинга и подготовки датасетов
- [Отборная папка ресурсов](https://t.me/addlist/8vDUwYRGujRmZjFi)

**Книги и курсы (бесплатно):**
- [ScrapingHub Learn](https://www.zyte.com/learn/) — статьи от создателей Scrapy
- [Web Scraping with Python (Ryan Mitchell)](https://github.com/REMitchell/python-scraping) — код примеров на GitHub
- [Apify Academy](https://docs.apify.com/academy) — бесплатные курсы

**Юридическое:**
- [GDPR.eu](https://gdpr.eu) — что нельзя собирать в ЕС
- [robots.txt spec (RFC 9309)](https://www.rfc-editor.org/rfc/rfc9309)

---

## ☑ Чеклист этапа

- [ ] Понимаю разницу sync vs async HTTP
- [ ] Умею парсить HTML через `selectolax` и `parsel`
- [ ] Знаю, когда нужен Playwright, а когда — нет
- [ ] Умею искать скрытые JSON API через DevTools
- [ ] Применяю `tenacity` для ретраев и `aiolimiter` для rate-limit
- [ ] Понимаю типы анти-бот защит и базовые методы обхода
- [ ] Уважаю `robots.txt`, ToS, GDPR/152-ФЗ
- [ ] Сделал хотя бы 3 упражнения из списка
- [ ] Сохраняю данные в Parquet, анализирую через DuckDB
- [ ] Знаю про LLM-friendly парсеры (`crawl4ai`, `firecrawl`)

---

## 🔗 Навигация

⬅️ [Этап 14. Vibe coding](./stage-14-vibecoding.md) · 🏠 [К оглавлению курса](./README.md) · ➡️ Этап 16 (скоро)
