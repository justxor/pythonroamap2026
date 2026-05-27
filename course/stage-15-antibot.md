# Этап 15+. Антибот: глубокий разбор (2026)

> 🎯 **Цель:** разобраться, как современные сайты детектят ботов и какие техники существуют для обхода. С упором на этику, легальность и устойчивость.

> ⚠️ **Дисклеймер:** обход защит может нарушать ToS и законы. Материал — для исследовательских целей, тестирования собственных систем, и работы с legal-grey зонами при понимании рисков. Не используй против сайтов, которые явно запрещают парсинг в robots.txt и ToS.

---

## 🧠 Как сайты детектят ботов: 7 уровней

| Уровень | Что детектят | Сложность обхода |
|---|---|---|
| 1. IP | Rate, datacenter ASN, blacklists | ⭐ Низкая (прокси) |
| 2. HTTP-заголовки | Отсутствие/неправильный порядок | ⭐ Низкая (User-Agent, Accept) |
| 3. TLS | JA3/JA4 fingerprint | ⭐⭐⭐ Средняя (curl_cffi) |
| 4. HTTP/2 | Settings frame, pseudo-headers order | ⭐⭐⭐ Средняя |
| 5. JS-runtime | navigator.webdriver, plugins, canvas | ⭐⭐⭐⭐ Высокая (stealth) |
| 6. Behavioral | Mouse, scroll, тайминги | ⭐⭐⭐⭐⭐ Очень высокая |
| 7. ML/Reputation | История поведения IP/cookie | ⭐⭐⭐⭐⭐ Почти невозможно |

---

## 1. IP-уровень

### Сигналы для детекта
- Datacenter ASN (AWS, GCP, OVH, Hetzner — мгновенный red flag).
- Чёрные списки (Spamhaus, Project Honey Pot).
- Слишком высокий RPS с одного IP.
- Подозрительная гео-смена.

### Решения
- **Residential proxies** — IP домашних провайдеров. Дороже, но незаметнее.
- **Mobile proxies (4G/5G)** — лучшие. Один IP делят сотни абонентов, заблокировать целый CGNAT-пул сайт не может.
- **Ротация:** меняй IP на каждый запрос или каждые N минут.

```python
import random
import httpx

PROXY_POOL = [
    "http://user:pass@residential1:8080",
    "http://user:pass@residential2:8080",
]

async def fetch_with_rotation(url: str) -> httpx.Response:
    proxy = random.choice(PROXY_POOL)
    async with httpx.AsyncClient(proxy=proxy, timeout=15) as c:
        return await c.get(url)
```

---

## 2. HTTP-заголовки

### Сигналы
- Нет `User-Agent` или питоновский (`python-requests/2.31`).
- Нет `Accept`, `Accept-Language`, `Accept-Encoding`.
- Неправильный порядок заголовков (httpx vs Chrome отличаются).
- Нет `Sec-Fetch-*` заголовков (Chrome всегда шлёт).

### Решение

```python
CHROME_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}
```

> 💡 Скопируй заголовки реального Chrome из DevTools → Network → клик по запросу → Request Headers.

---

## 3. TLS fingerprint (JA3/JA4)

TLS handshake уникален для каждого клиента. Python `ssl` / `httpx` выдают характерный JA3, не похожий ни на один браузер. Это самый коварный детект — заголовки могут быть идеальные, но сайт сравнит TLS и отдаст 403.

### Решение: `curl_cffi`

`curl_cffi` использует libcurl с patches, имитирующими TLS-стек Chrome/Firefox/Safari.

```python
from curl_cffi import requests

r = requests.get(
    "https://tls.peet.ws/api/all",  # проверка JA3
    impersonate="chrome131",
)
print(r.json()["tls"]["ja3_hash"])
```

Список impersonate: `chrome99-131`, `firefox133`, `safari17_0`, `edge99`.

### Async-версия

```python
from curl_cffi.requests import AsyncSession

async with AsyncSession(impersonate="chrome131") as s:
    r = await s.get("https://protected.com")
```

### Проверка
- [tls.peet.ws/api/all](https://tls.peet.ws/api/all) — твой JA3/JA4.
- [browserleaks.com/ssl](https://browserleaks.com/ssl) — full TLS-отчёт.

---

## 4. HTTP/2 fingerprint

HTTP/2 имеет AKAMAI-fingerprint: порядок SETTINGS, pseudo-headers, WINDOW_UPDATE. Каждый браузер свой.

`curl_cffi` с `impersonate` решает и эту проблему.

Проверка: [tls.peet.ws/api/all](https://tls.peet.ws/api/all) → поле `http2`.

---

## 5. JS-runtime детект

Когда сайт открывается в headless-браузере, скрипты на странице проверяют десятки сигналов:

- `navigator.webdriver === true` → бот.
- `navigator.plugins.length === 0` → подозрительно.
- `navigator.languages === []` → бот.
- `window.chrome` отсутствует → не Chrome.
- `WebGL.vendor === "Brian Paul"` → headless Chrome.
- Canvas fingerprint совпадает с известным headless.
- Permissions API отдаёт неправильный статус.

### Решения

**1. playwright-stealth** — патчит navigator.* перед загрузкой страницы.

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    ctx = await browser.new_context()
    page = await ctx.new_page()
    await stealth_async(page)
    await page.goto("https://bot.sannysoft.com")
```

**2. camoufox** — форк Firefox с встроенным антидетектом, активно поддерживается в 2025-2026.

```python
from camoufox.async_api import AsyncCamoufox

async with AsyncCamoufox(humanize=True) as browser:
    page = await browser.new_page()
    await page.goto("https://bot.sannysoft.com")
```

**3. patchright** — патченный Playwright с фиксами для CDP-детектов.

### Тесты
- [bot.sannysoft.com](https://bot.sannysoft.com) — мгновенный отчёт.
- [arh.antoinevastel.com/bots/areyouheadless](https://arh.antoinevastel.com/bots/areyouheadless).
- [pixelscan.net](https://pixelscan.net) — комплексная проверка.

---

## 6. Behavioral детект

Современные защиты (DataDome, Cloudflare Turnstile, Akamai Bot Manager) собирают тайминги, движения мыши, скролл, время на странице.

### Имитация

```python
import random
import asyncio

async def human_like_actions(page):
    # Случайные паузы
    await asyncio.sleep(random.uniform(1.0, 3.0))
    # Скролл с паузами
    for _ in range(random.randint(3, 7)):
        await page.mouse.wheel(0, random.randint(200, 500))
        await asyncio.sleep(random.uniform(0.3, 1.2))
    # Случайное движение мыши
    for _ in range(5):
        x = random.randint(100, 1000)
        y = random.randint(100, 700)
        await page.mouse.move(x, y, steps=random.randint(10, 30))
        await asyncio.sleep(random.uniform(0.1, 0.4))
```

> 💡 Лучше всего: запиши реальную сессию в DevTools recorder, экспортируй в Playwright, добавь рандом.

---

## 7. Reputation и ML

Cloudflare/DataDome/PerimeterX строят профиль на основе сотен сигналов и истории IP+cookie. Свежий residential IP с правильным TLS и stealth-браузером может пройти, но через 100 запросов на чувствительные эндпоинты — забанят.

### Стратегии
- **Не превышай нормальный пользовательский паттерн** (не 1000 RPS на чекаут).
- **Грей сессии** — одна cookie живёт час-два, потом новая.
- **Дели нагрузку** между десятками IP+cookie+браузер-профилей.
- **Реалистичный referrer-цепочки** (Google → листинг → деталь, а не сразу деталь).

---

## 🧰 Готовые сервисы (когда лень делать самому)

| Сервис | Что даёт | Цена 2026 |
|---|---|---|
| [ScraperAPI](https://www.scraperapi.com) | Прокси + рендер + капча-solver | $$ |
| [Bright Data Web Unlocker](https://brightdata.com) | Полный антидетект | $$$$ |
| [ZenRows](https://www.zenrows.com) | Антибот API | $$ |
| [Apify](https://apify.com) | Готовые акторы | $$ |
| [firecrawl](https://firecrawl.dev) | LLM-friendly + антидетект | $ + open-source |

**Самостоятельный стек (open-source):**
`curl_cffi` (TLS) + `camoufox` (JS) + residential proxy pool + ротация User-Agent.

---

## ✅ Чеклист "мой парсер устойчив"

- [ ] User-Agent совпадает с реальным Chrome
- [ ] Все Sec-Fetch-* заголовки отправляются
- [ ] TLS-fingerprint проверен на tls.peet.ws → совпадает с Chrome
- [ ] HTTP/2 fingerprint совпадает с Chrome
- [ ] Если используется Playwright — прошёл bot.sannysoft.com
- [ ] Реальный residential/mobile прокси
- [ ] Rate-limit ≤ нормального пользовательского паттерна
- [ ] Cookie живут реалистичное время
- [ ] Есть Referer-цепочки
- [ ] Логирую все 403/429 и автоматически меняю IP

---

## 📚 Ресурсы

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — AI-парсинг, анти-бот инструменты, ML-fingerprinting.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — Python-инструменты, curl_cffi, playwright-stealth.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**

- [curl_cffi](https://github.com/lexiforest/curl_cffi)
- [camoufox](https://github.com/daijro/camoufox)
- [playwright-stealth](https://github.com/AtuboDad/playwright_stealth)
- [patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright)
- [Bot detection collection](https://github.com/niespodd/browser-fingerprinting) — must-read
- 💬 [@pythonl](https://t.me/pythonl)

---

## 🔗 Навигация

⬅️ [Этап 15. Парсинг](./stage-15-parsing.md) · 🏠 [К оглавлению курса](./README.md)
