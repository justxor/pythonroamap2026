# Этап 9. Веб-разработка

> 🎯 Собрать production-ready API: авторизация, БД, тесты, Swagger.
> ⏱ 4–5 недель.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. FastAPI с нуля](#урок-1-fastapi-с-нуля)
- [Урок 2. Dependency Injection](#урок-2-dependency-injection)
- [Урок 3. JWT-авторизация](#урок-3-jwt-авторизация)
- [Урок 4. WebSocket](#урок-4-websocket)
- [Финальный проект](#финальный-проект)

---

## Урок 1. FastAPI с нуля

```bash
uv add fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Tasks API")

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

DB: dict[int, Task] = {}

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(DB.values())

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task) -> Task:
    DB[task.id] = task
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    if task_id not in DB:
        raise HTTPException(404, "not found")
    return DB[task_id]
```

```bash
uvicorn main:app --reload
# http://localhost:8000/docs — готовый Swagger
```

### Async-эндпоинты

```python
import httpx

@app.get("/proxy")
async def proxy(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        return {"status": r.status_code, "size": len(r.content)}
```

---

## Урок 2. Dependency Injection

```python
from fastapi import Depends

def get_config():
    return {"api_key": "secret"}

@app.get("/")
def home(cfg: dict = Depends(get_config)):
    return cfg
```

### Цепочка зависимостей

```python
from fastapi import Header, HTTPException

def auth_token(authorization: str = Header()) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "no token")
    return authorization.removeprefix("Bearer ")

def current_user(token: str = Depends(auth_token)) -> dict:
    return {"id": 1, "token": token}

@app.get("/me")
def me(user: dict = Depends(current_user)):
    return user
```

### yield-зависимости

```python
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/users")
def list_users(db = Depends(get_db)):
    return db.query(User).all()
```

### Lifespan

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await aioredis.from_url("redis://localhost")
    yield
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
```

---

## Урок 3. JWT-авторизация

```bash
uv add pyjwt passlib[bcrypt]
```

### Пароли

```python
from passlib.hash import bcrypt

hashed = bcrypt.hash("MyP@ssword")
assert bcrypt.verify("MyP@ssword", hashed)
```

### JWT

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET = "super-secret"
ALGO = "HS256"

def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGO])
```

### В FastAPI

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def current_user(token: str = Depends(oauth2)) -> int:
    try:
        payload = decode_token(token)
        return int(payload["sub"])
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid token")

@app.get("/me")
def me(user_id: int = Depends(current_user)):
    return {"user_id": user_id}
```

### В проде

- `SECRET` — только из ENV.
- Подумай о refresh-токенах.
- HTTPS обязателен.

---

## Урок 4. WebSocket

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def ws_echo(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text(f"echo: {msg}")
    except Exception:
        await ws.close()
```

---

## Финальный проект

**Task Tracker API**:

1. `POST /auth/register` — регистрация
2. `POST /auth/login` — выдача JWT
3. `GET /tasks` — мои задачи (JWT)
4. `POST/PATCH/DELETE /tasks` — CRUD
5. SQLite или Postgres
6. Тесты pytest + httpx
7. Логирование, обработка ошибок
8. README с инструкцией запуска

Бонус: Docker, OpenTelemetry, rate-limiting Redis.

---

## Чеклист и ресурсы

- [ ] Запустил FastAPI с авторизацией, БД, Swagger
- [ ] Понимаю WSGI vs ASGI
- [ ] Знаю, что делает CORS
- [ ] Реализовал rate-limiting
- [ ] WebSocket-эндпоинт работает
- [ ] Завернул API в Docker

Ресурсы:
- 📘 [FastAPI docs](https://fastapi.tiangolo.com/) — образцовая документация
- 📘 [Litestar](https://docs.litestar.dev/)
- 📘 [Django docs](https://docs.djangoproject.com/) + [Django Girls (RU)](https://tutorial.djangogirls.org/ru/)
- 🎥 [ArjanCodes FastAPI](https://www.youtube.com/@ArjanCodes/search?query=fastapi)
- 📝 [TestDriven.io blog](https://testdriven.io/blog/)
- 📘 [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- 📘 [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 8](stage-08-cpython.md) · [К оглавлению](README.md) · [Этап 10 →](stage-10-databases.md)
