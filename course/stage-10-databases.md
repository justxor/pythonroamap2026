# Этап 10. Базы данных — SQL, SQLAlchemy 2.x async, Alembic, миграции, тюнинг

> ⏱ Время: 3 недели  
> 🎯 Цель: уверенно проектировать схемы, писать SQL, использовать SQLAlchemy 2.x в async-стиле, делать миграции через Alembic, понимать индексы, транзакции и план запроса.

---

## 📘 Урок 10.1 — SQL за час

```sql
-- DDL: схема
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email       VARCHAR(255) NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE posts (
    id        BIGSERIAL PRIMARY KEY,
    user_id   BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title     TEXT   NOT NULL,
    body      TEXT
);

-- DML: данные
INSERT INTO users(email) VALUES ('a@b.c') RETURNING id;

-- Чтение
SELECT u.email, COUNT(p.id) AS n_posts
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id
HAVING COUNT(p.id) > 0
ORDER BY n_posts DESC
LIMIT 10;
```

**Шпаргалка JOIN:**
```
A INNER  B  — только пересечение
A LEFT   B  — все A + совпавшие B (отсутствие = NULL)
A RIGHT  B  — все B + совпавшие A
A FULL   B  — всё
```

---

## 📘 Урок 10.2 — Нормальные формы (1NF/2NF/3NF) и денормализация

- **1NF**: атомарность. Не храни `tags = "a,b,c"` строкой.
- **2NF**: нет частичной зависимости от части составного ключа.
- **3NF**: нет транзитивной зависимости (атрибут зависит от ключа, а не от другого атрибута).

В реальном мире иногда **денормализуют** ради скорости чтения (например, кешируют `posts_count` в `users`).

---

## 📘 Урок 10.3 — Индексы и план запроса

```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 42 ORDER BY created_at DESC LIMIT 10;
```

- B-tree — дефолтный, для =, <, >, ORDER BY, LIKE 'abc%'.
- GIN — JSON, массивы, полнотекстовый поиск.
- Hash — только =, обычно не нужен.
- **Композитные** индексы работают только с префиксом колонок.

**Правило:** индекс ускоряет чтение, замедляет запись. Без замеров — не добавляй.

---

## 📘 Урок 10.4 — Транзакции и уровни изоляции

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- или ROLLBACK;
```

**ACID:** Atomicity, Consistency, Isolation, Durability.

**Уровни изоляции (Postgres дефолт = Read Committed):**
| Уровень | Грязное чтение | Неповт. чтение | Фантомы |
|---|---|---|---|
| Read Uncommitted | да | да | да |
| Read Committed | нет | да | да |
| Repeatable Read | нет | нет | да* |
| Serializable | нет | нет | нет |

* В Postgres RR уже без фантомов (snapshot isolation).

---

## 📘 Урок 10.5 — SQLAlchemy 2.x: Core vs ORM

```bash
uv add 'sqlalchemy[asyncio]' asyncpg
```

```python
# app/db.py
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase): ...

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

engine = create_async_engine("postgresql+asyncpg://u:p@localhost/app", echo=False, pool_size=10)
Session = async_sessionmaker(engine, expire_on_commit=False)
```

---

## 📘 Урок 10.6 — Запросы 2.x в стиле `select()`

```python
from sqlalchemy import select, func

async def top_users(limit: int = 10) -> list[tuple[str, int]]:
    async with Session() as s:
        stmt = (
            select(User.email, func.count(Post.id).label("n"))
            .join(Post, Post.user_id == User.id, isouter=True)
            .group_by(User.id)
            .order_by(func.count(Post.id).desc())
            .limit(limit)
        )
        return list(await s.execute(stmt))
```

**Главный анти-паттерн: N+1 запрос.** Лечится через `selectinload` / `joinedload`:

```python
from sqlalchemy.orm import selectinload

stmt = select(User).options(selectinload(User.posts))
```

---

## 📘 Урок 10.7 — Миграции через Alembic

```bash
uv add alembic
uv run alembic init -t async alembic
```

Отредактируй `alembic/env.py`: укажи `target_metadata = Base.metadata` и URL из настроек.

```bash
uv run alembic revision --autogenerate -m "add users"
uv run alembic upgrade head
uv run alembic downgrade -1
```

**Правила:**
- Каждую миграцию ревьюй вручную — autogenerate ошибается.
- Большие миграции делай в несколько шагов (add column nullable → backfill → set not null).
- Для CI: проверяй, что `alembic check` чист.

---

## 📘 Урок 10.8 — Пулы соединений и тюнинг

- Pool size: `(CPU cores * 2) + spindles` для PG. Для async-приложения часто 10-20.
- `pool_pre_ping=True` — проверка соединения перед использованием.
- `statement_timeout` на стороне БД, чтобы зависшие запросы не висели вечно.
- `pgbouncer` (transaction mode) — must-have в продакшне.

---

## 📘 Урок 10.9 — Когда не SQL: Redis, key-value

- **Кеш** (TTL): `redis.set(key, value, ex=60)`.
- **Rate limit**: `INCR` + `EXPIRE`.
- **Очереди**: `LPUSH`/`BRPOP` или Redis Streams.
- **Pub/Sub**: чаты, уведомления.

⚠️ Redis — не основная БД. Данные в памяти, persistence настраивается.

---

## 🛠 Упражнения

### Упражнение 10.1 — Схема блога
Спроектируй: `users`, `posts`, `tags`, `post_tags` (many-to-many). Напиши DDL.

### Упражнение 10.2 — Запросы
К схеме из 10.1 напиши:
1. Все посты с тегом "python".
2. Топ-10 авторов по числу постов за последние 30 дней.
3. Посты без тегов.

### Упражнение 10.3 — SQLAlchemy + Alembic
Опиши `User/Post/Tag` через 2.x ORM. Создай первую миграцию. Накатить. Откатить.

### Упражнение 10.4 — N+1
Сделай эндпоинт `GET /users`, возвращающий юзеров со списком их постов. Сначала с N+1, потом исправь через `selectinload`. Замерь время на 1000 юзеров × 10 постов.

---

## ✅ Решение 10.2 (запросы)

```sql
-- 1) Посты с тегом "python"
SELECT p.* FROM posts p
JOIN post_tags pt ON pt.post_id = p.id
JOIN tags t       ON t.id = pt.tag_id
WHERE t.name = 'python';

-- 2) Топ-10 авторов за 30 дней
SELECT u.email, COUNT(p.id) AS n
FROM users u
JOIN posts p ON p.user_id = u.id
WHERE p.created_at >= now() - INTERVAL '30 days'
GROUP BY u.id
ORDER BY n DESC
LIMIT 10;

-- 3) Посты без тегов
SELECT p.* FROM posts p
LEFT JOIN post_tags pt ON pt.post_id = p.id
WHERE pt.tag_id IS NULL;
```

## ✅ Решение 10.4 (selectinload)

```python
# Плохо — N+1
async def bad() -> list[dict]:
    async with Session() as s:
        users = (await s.scalars(select(User))).all()
        return [{"id": u.id, "posts": [p.title for p in u.posts]} for u in users]  # каждый u.posts — отдельный запрос

# Хорошо — один JOIN + один SELECT IN (...)
async def good() -> list[dict]:
    async with Session() as s:
        users = (await s.scalars(select(User).options(selectinload(User.posts)))).all()
        return [{"id": u.id, "posts": [p.title for p in u.posts]} for u in users]
```

---

## 📚 Бесплатные ресурсы

- 📕 [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — лучшее по SQL.
- 📕 [SQLAlchemy 2.0 docs](https://docs.sqlalchemy.org/) — раздел "Unified Tutorial".
- 📕 [Alembic docs](https://alembic.sqlalchemy.org/).
- 📕 [Use the Index, Luke!](https://use-the-index-luke.com/) — про индексы, лучшая бесплатная книга.
- 📕 [PostgreSQL Exercises](https://pgexercises.com/) — тренажёр SQL.
- 📺 [ArjanCodes — SQLAlchemy 2.0](https://www.youtube.com/@ArjanCodes).
- 💬 **Telegram: [@pythonl](https://t.me/pythonl)**.

---

## ☑ Чеклист этапа

- [ ] Пишу SQL: JOIN, GROUP BY, оконные функции.
- [ ] Понимаю EXPLAIN ANALYZE и могу прочитать план.
- [ ] Знаю когда нужен индекс (и когда нет).
- [ ] Различаю уровни изоляции, понимаю аномалии.
- [ ] Использую SQLAlchemy 2.x в async-стиле.
- [ ] Решаю N+1 через `selectinload`/`joinedload`.
- [ ] Делаю миграции через Alembic, ревьюю их вручную.

---

[⬅ Этап 9](stage-09-web.md) | [📚 Оглавление](README.md) | [Этап 11 ➡](stage-11-data-ml.md)
