# 🌐 Промпт 06 — Спроектировать REST/FastAPI-эндпоинт

> Используй когда: добавляешь новый эндпоинт и хочешь, чтобы он сразу был production-ready.

---

```
[CONTEXT]
FastAPI 0.115+, Pydantic v2, SQLAlchemy 2.x async, JWT-auth.
Доменная сущность: <Order / User / Post / ...>
Уже существуют: <какие эндпоинты на эту сущность уже есть>

[TASK]
Спроектируй эндпоинт: <словесное описание, например «создать заказ»>.

[RULES]
- REST: правильный метод (POST/GET/PUT/PATCH/DELETE), правильный URL (/orders, не /createOrder).
- Pydantic-схемы отдельно для In и Out (никаких ORM-моделей наружу).
- Статус-коды: 200/201/204/400/401/403/404/409/422.
- Авторизация через Depends(current_user) если нужна.
- Идемпотентность: если POST — Idempotency-Key header.
- Логирование критичных действий через structlog с request_id.
- OpenAPI: tags, summary, response_model.
- Ошибки через HTTPException с понятным detail.

[LENS]
1) **API-контракт** (request/response примеры в JSON).
2) **Pydantic-схемы** (In / Out / ошибка).
3) **Сигнатура эндпоинта** (def + Depends).
4) **Use-case** (если архитектура из stage-13 — отдельный класс).
5) **Тесты** (TestClient: happy + 4xx).
6) **Открытые вопросы** — что мне уточнить у продакта/архитектора.
```
