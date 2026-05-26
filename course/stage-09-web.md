# Этап 9. Web — FastAPI, REST, JWT, WebSocket, Dependency Injection

> ⏱ Время: 3 недели  
> 🎯 Цель: спроектировать и реализовать продакшн-готовый REST/WebSocket бэкенд на FastAPI с аутентификацией, валидацией, DI, миграциями, тестами и OpenAPI.

---

## 📘 Урок 9.1 — HTTP за 10 минут

```
Client ──── HTTP/1.1 ────► Server
       │
       ├── метод (GET/POST/PUT/PATCH/DELETE)
       ├── путь (/users/42)
       ├── заголовки (Authorization: Bearer ...)
       └── тело (JSON)

Server ──── статус-код ────► Client
       │
       ├── 2xx OK
       ├── 3xx redirect
       ├── 4xx client error (400 bad req, 401 unauth, 403 forbid, 404 not found, 409 conflict, 422 validation)
       └── 5xx server error
```

**REST-принципы:**
- Ресурсы (`/users`), а не действия (`/getUser`).
- Используем правильные методы (GET идемпотентен, POST — нет).
- Версионирование: `/v1/...` или заголовок `Accept: application/vnd.app.v1+json`.

---

## 📘 Урок 9.2 — Первое приложение FastAPI

```bash
uv add fastapi 'uvicorn[standard]' pydantic-settings httpx
```

```python
# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Tasks API", version="1.0.0")

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    priority: int = Field(default=1, ge=1, le=5)

class TaskOut(TaskIn):
    id: int

_db: dict[int, TaskOut] = {}
_next_id = 0

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create(payload: TaskIn) -> TaskOut:
    global _next_id
    _next_id += 1
    t = TaskOut(id=_next_id, **payload.model_dump())
    _db[t.id] = t
    return t

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get(task_id: int) -> TaskOut:
    from fastapi import HTTPException
    if task_id not in _db: raise HTTPException(404, "not found")
    return _db[task_id]
```

```bash
uv run uvicorn app.main:app --reload
# http://localhost:8000/docs  ← автоматический Swagger
```

---

## 📘 Урок 9.3 — Pydantic v2: валидация на стероидах

```python
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    email: EmailStr
    password: str = Field(min_length=8)
    born: datetime | None = None

    @field_validator("password")
    @classmethod
    def has_digit(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("must contain a digit")
        return v
```

Pydantic v2 на 5-50x быстрее v1 (ядро на Rust — `pydantic-core`).

---

## 📘 Урок 9.4 — Dependency Injection

DI = функция получает свои зависимости из аргументов, а не создаёт их сама. FastAPI делает это через `Depends`.

```python
from typing import Annotated
from fastapi import Depends

def get_db() -> Iterator[Session]:
    s = SessionLocal()
    try: yield s
    finally: s.close()

DbDep = Annotated[Session, Depends(get_db)]

@app.get("/users/{id}")
def read(id: int, db: DbDep) -> UserOut:
    user = db.get(User, id)
    if user is None: raise HTTPException(404)
    return user
```

Преимущество: в тестах подменяешь `get_db` на фейк через `app.dependency_overrides[get_db] = lambda: FakeDb()`.

---

## 📘 Урок 9.5 — Аутентификация с JWT

```bash
uv add python-jose[cryptography] passlib[bcrypt]
```

```python
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET = "change-me"  # читай из переменной окружения!
ALGO = "HS256"
pwd = CryptContext(schemes=["bcrypt"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(p: str) -> str: return pwd.hash(p)
def verify_password(p: str, h: str) -> bool: return pwd.verify(p, h)

def make_token(sub: str, minutes: int = 30) -> str:
    payload = {"sub": sub, "exp": datetime.now(UTC) + timedelta(minutes=minutes)}
    return jwt.encode(payload, SECRET, ALGO)

def current_user(token: Annotated[str, Depends(oauth2)]) -> str:
    try:
        data = jwt.decode(token, SECRET, [ALGO])
    except JWTError:
        raise HTTPException(401, "bad token")
    return data["sub"]
```

```python
@app.get("/me")
def me(user: Annotated[str, Depends(current_user)]) -> dict:
    return {"sub": user}
```

⚠️ **JWT не отзываются**. Делай короткий exp (15 мин) + refresh-токены в БД с возможностью отзыва.

---

## 📘 Урок 9.6 — WebSocket: real-time

```python
from fastapi import WebSocket, WebSocketDisconnect

clients: set[WebSocket] = set()

@app.websocket("/ws")
async def ws(socket: WebSocket) -> None:
    await socket.accept()
    clients.add(socket)
    try:
        async for msg in socket.iter_text():
            for c in clients:
                await c.send_text(f"echo: {msg}")
    except WebSocketDisconnect:
        pass
    finally:
        clients.discard(socket)
```

Тестировать руками: `websocat ws://localhost:8000/ws`.

---

## 📘 Урок 9.7 — Конфигурация через Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")
    secret_key: str
    database_url: str = "sqlite:///./app.db"
    debug: bool = False

settings = Settings()  # читает APP_SECRET_KEY, APP_DATABASE_URL...
```

---

## 📘 Урок 9.8 — Тестирование FastAPI

```python
from fastapi.testclient import TestClient
from app.main import app

def test_create_task() -> None:
    with TestClient(app) as c:
        r = c.post("/tasks", json={"title": "buy milk", "priority": 2})
        assert r.status_code == 201
        assert r.json()["id"] > 0

def test_invalid_priority() -> None:
    with TestClient(app) as c:
        r = c.post("/tasks", json={"title": "x", "priority": 99})
        assert r.status_code == 422  # validation
```

Для async-эндпоинтов и WebSocket: `httpx.AsyncClient(transport=ASGITransport(app))`.

---

## 📘 Урок 9.9 — Production-чеклист

- **CORS** через `CORSMiddleware`.
- **Rate-limiting** через `slowapi`.
- **Заголовки безопасности**: HSTS, CSP, X-Frame-Options.
- **Healthcheck** `/healthz` (live) и `/readyz` (ready) — Kubernetes любит это.
- **Структурные логи** (JSON) — этап 12.
- **OpenAPI** живёт в `/openapi.json`. Версионируй контракт.

---

## 🛠 Упражнения

### Упражнение 9.1 — CRUD задач
Реализуй REST API: `POST/GET/PUT/DELETE /tasks`. Храни в памяти. Покрой тестами (4 теста минимум).

### Упражнение 9.2 — Auth
Добавь `/auth/register`, `/auth/login`. Защити `POST /tasks` (только авторизованные). Используй JWT.

### Упражнение 9.3 — WebSocket-чат
Простой чат: подключившиеся видят сообщения друг друга. Бонус: nickname в query-параметре.

### Упражнение 9.4 — DI с подменой
Сделай зависимость `get_clock() -> datetime`. В тестах подмени её, чтобы возвращала фиксированное время.

---

## ✅ Решение 9.4 (DI + override)

```python
# app/deps.py
from datetime import datetime, UTC
def get_clock() -> datetime: return datetime.now(UTC)

# app/main.py
from typing import Annotated
from fastapi import Depends
from .deps import get_clock

@app.get("/now")
def now(t: Annotated[datetime, Depends(get_clock)]) -> dict:
    return {"now": t.isoformat()}

# tests/test_time.py
from datetime import datetime, UTC
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_clock

def test_now_is_fixed() -> None:
    fixed = datetime(2026, 1, 1, tzinfo=UTC)
    app.dependency_overrides[get_clock] = lambda: fixed
    try:
        r = TestClient(app).get("/now")
        assert r.json()["now"].startswith("2026-01-01")
    finally:
        app.dependency_overrides.clear()
```

---

## 📚 Бесплатные ресурсы

- 📕 [FastAPI docs](https://fastapi.tiangolo.com/) — лучшая документация в мире Python.
- 📕 [Pydantic v2 docs](https://docs.pydantic.dev/).
- 📕 [HTTP-спецификация](https://httpwg.org/specs/) — для понимания, что внутри.
- 📕 [JWT.io](https://jwt.io/introduction).
- 📺 [ArjanCodes — FastAPI series](https://www.youtube.com/@ArjanCodes).
- 📺 [TestDriven.io — FastAPI tutorials](https://testdriven.io/blog/topics/fastapi/) (бесплатные статьи).
- 💬 **Telegram: [@pythonl](https://t.me/pythonl)**.

---

## ☑ Чеклист этапа

- [ ] Понимаю HTTP-методы, статусы, идемпотентность.
- [ ] Описываю модели в Pydantic v2 с валидаторами.
- [ ] Использую `Depends` и override в тестах.
- [ ] Реализовал JWT-auth и понимаю риски токенов.
- [ ] Написал WebSocket-эндпоинт.
- [ ] Покрыл API тестами через `TestClient`.
- [ ] Есть `/healthz`, CORS, settings через env.

---

[⬅ Этап 8](stage-08-cpython.md) | [📚 Оглавление](README.md) | [Этап 10 ➡](stage-10-databases.md)
