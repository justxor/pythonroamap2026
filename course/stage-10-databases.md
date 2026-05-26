# Этап 10. Базы данных и ORM

> 🎯 Уверенно писать SQL, читать EXPLAIN, использовать SQLAlchemy 2.x.
> ⏱ 3 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. SQL основы](#урок-1-sql-основы)
- [Урок 2. SQLAlchemy 2.x async](#урок-2-sqlalchemy-2x-async)
- [Урок 3. Alembic-миграции](#урок-3-alembic-миграции)
- [Упражнение](#упражнение)

---

## Урок 1. SQL основы

### SELECT, WHERE, ORDER, LIMIT

```sql
SELECT id, email, created_at
FROM users
WHERE created_at > '2026-01-01'
ORDER BY created_at DESC
LIMIT 10;
```

### JOIN

```sql
SELECT u.email, o.id AS order_id, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.created_at > '2026-01-01';
```

Виды: `INNER JOIN` (пересечение), `LEFT JOIN` (все слева), `FULL OUTER JOIN` (все).

### GROUP BY + агрегаты

```sql
SELECT user_id, COUNT(*) AS orders_count, SUM(total) AS revenue
FROM orders
WHERE created_at > '2026-01-01'
GROUP BY user_id
HAVING COUNT(*) > 5
ORDER BY revenue DESC;
```

### Оконные функции

```sql
-- Накопительная сумма
SELECT user_id, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total
FROM payments;

-- Рейтинг
SELECT user_id, amount, RANK() OVER (ORDER BY amount DESC) AS rank
FROM payments;
```

### EXPLAIN

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@b.c';
```

Что смотреть: `Seq Scan` (медленно) vs `Index Scan` (быстро), стратегии JOIN (Hash/Nested Loop).

### Индексы

```sql
CREATE INDEX users_email_idx ON users (email);
CREATE INDEX users_email_lower_idx ON users (LOWER(email));   -- функциональный
```

---

## Урок 2. SQLAlchemy 2.x async

```bash
uv add sqlalchemy[asyncio] asyncpg
```

### Модели

```python
from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total: Mapped[float]
    user: Mapped[User] = relationship(back_populates="orders")
```

### Async session

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://u:p@localhost/db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
```

### CRUD

```python
from sqlalchemy import select

async def create_user(email: str) -> User:
    async with SessionLocal() as s:
        user = User(email=email)
        s.add(user)
        await s.commit()
        await s.refresh(user)
        return user

async def find_user(email: str) -> User | None:
    async with SessionLocal() as s:
        result = await s.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

### N+1 проблема

```python
from sqlalchemy.orm import selectinload

# ✅ загрузка orders одним запросом
stmt = select(User).options(selectinload(User.orders))
```

---

## Урок 3. Alembic-миграции

```bash
uv add alembic
uv run alembic init -t async migrations
```

В `migrations/env.py`:

```python
from src.models import Base
target_metadata = Base.metadata
```

В `alembic.ini`:

```ini
sqlalchemy.url = postgresql+asyncpg://u:p@localhost/db
```

### Автогенерация

```bash
uv run alembic revision --autogenerate -m "create users"
uv run alembic upgrade head
uv run alembic downgrade -1
```

### Правила

- Всегда **просматривай** автогенерированную миграцию.
- Большие данные мигрируй пачками.
- Всегда умей `downgrade`.

---

## Упражнение

User → Order → OrderItem

Создать модели + функции:

1. `async def create_order(user_id, items)` — одна транзакция.
2. `async def user_revenue(user_id)` — сумма по пользователю.
3. `async def top_users(n)` — топ N по выручке (использовать JOIN + GROUP BY + ORDER BY).

Требования: SQLAlchemy 2.x async, Alembic, pytest + sqlite (для CI) или TestContainers Postgres.

---

## Чеклист и ресурсы

- [ ] Пишу JOIN-ы и оконные функции без подсказок
- [ ] Читаю EXPLAIN ANALYZE
- [ ] Настроены Alembic-миграции
- [ ] Async SQLAlchemy 2.x в проекте
- [ ] Знаю когда нужен индекс
- [ ] Различаю уровни изоляции транзакций

Ресурсы:
- 📘 [SQLAlchemy 2.x docs](https://docs.sqlalchemy.org/en/20/) — пройти tutorial
- 📘 [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- 📘 [«Use the Index, Luke!»](https://use-the-index-luke.com/) — free book
- 📘 [Mode SQL Tutorial](https://mode.com/sql-tutorial/)
- 🎮 [SQLBolt](https://sqlbolt.com/)
- 📘 [Alembic docs](https://alembic.sqlalchemy.org/)
- 📘 [Designing Data-Intensive Applications (free chapters)](https://dataintensive.net/)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 9](stage-09-web.md) · [К оглавлению](README.md) · [Этап 11 →](stage-11-data-ml.md)
