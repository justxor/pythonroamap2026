# Этап 13. Архитектура и Senior

> 🎯 Проектировать системы, переживающие 5 команд и 3 рефакторинга.
> ⏱ На всю жизнь.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. Гексагональная архитектура](#урок-1-гексагональная-архитектура)
- [Урок 2. DDD основы](#урок-2-ddd-основы)
- [Урок 3. Outbox и Saga](#урок-3-outbox-и-saga)
- [Финальный проект](#финальный-проект)

---

## Урок 1. Гексагональная архитектура

### Идея

**Domain** не зависит ни от чего. **Infrastructure** реализует «порты» (Protocol'ы), определённые в domain. Между ними — **application** слой.

```
┌──── INTERFACES ────┐
│ HTTP / CLI / Kafka │
└──────────┬─────────┘
           ▼
┌──── APPLICATION ────┐
│  use cases / cmds   │
└──────────┬──────────┘
           ▼
┌────── DOMAIN ───────┐
│ pure business logic │
└──────────▲──────────┘
           │ implements ports
┌─── INFRASTRUCTURE ──┐
│ SQLAlchemy / Redis  │
└─────────────────────┘
```

### Порты

```python
# domain/ports.py
from typing import Protocol

class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def find_by_email(self, email: str) -> User | None: ...

class EmailSender(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...
```

### Use case

```python
# application/register_user.py
class RegisterUser:
    def __init__(self, users: UserRepository, mailer: EmailSender) -> None:
        self.users = users
        self.mailer = mailer

    def __call__(self, email: str, password: str) -> User:
        if self.users.find_by_email(email):
            raise DuplicateError()
        user = User.create(email=email, password=password)
        self.users.add(user)
        self.mailer.send(email, "Welcome!", "Hi!")
        return user
```

`RegisterUser` тестируется **без БД и почты** — моки портов.

### Структура

```
src/
  domain/             # без зависимостей наружу
    entities.py
    value_objects.py
    services.py
    events.py
  application/        # use cases
    commands.py
    queries.py
    handlers.py
  infrastructure/     # SQLAlchemy, Redis, Kafka
    repositories.py
    messaging.py
  interfaces/         # FastAPI, CLI, gRPC
    http/
    cli/
  config.py
  main.py
```

---

## Урок 2. DDD основы

### Value Object — immutable, identity-by-value

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: int      # в копейках
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("разные валюты")
        return Money(self.amount + other.amount, self.currency)
```

### Entity — identity-by-id

```python
@dataclass
class User:
    id: int
    email: str
```

Два `User(1, "a@b.c")` и `User(1, "x@y.z")` — один пользователь.

### Aggregate — корень управляющий своими сущностями

```python
class Order:
    def __init__(self, id: int, user_id: int):
        self.id = id
        self.user_id = user_id
        self._items: list[OrderItem] = []

    def add_item(self, product_id: int, qty: int, price: Money) -> None:
        if qty <= 0:
            raise ValueError("qty > 0")
        self._items.append(OrderItem(product_id, qty, price))

    @property
    def total(self) -> Money:
        return sum((i.line_total for i in self._items), Money(0, "USD"))
```

Доступ к `OrderItem` только через `Order` — инвариант агрегата.

### Repository

```python
class OrderRepository(Protocol):
    def get(self, id: int) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

---

## Урок 3. Outbox и Saga

### Проблема

После создания заказа нужно: 1) положить в БД, 2) отправить событие в Kafka, 3) списать деньги. Если упадёт на (2) или (3) — рассинхрон.

### Outbox-паттерн

В **одной транзакции** пишем и сущность, и событие в outbox-таблицу:

```python
async with session.begin():
    session.add(order)
    session.add(OutboxEvent(
        type="OrderCreated",
        payload=order.to_dict(),
    ))
```

Воркер читает outbox и публикует. При падении — перечитает.

### Saga

Распределённая транзакция через цепочку событий + компенсации:

```
[Создать заказ] → [Зарезервировать товар] → [Списать деньги]
        │                  │                       │
        │                  │           если упало:│
        │                  │                       ▼
        │             [Вернуть резерв] ← компенсация
        ↓
   [Отменить заказ] ← компенсация
```

### Idempotency Key

```python
async def create_payment(idempotency_key: str, amount: int):
    cached = await cache.get(f"idem:{idempotency_key}")
    if cached:
        return cached
    payment = await db.create_payment(amount=amount)
    await cache.set(f"idem:{idempotency_key}", payment, ttl=86400)
    return payment
```

### ADR (Architecture Decision Record)

```markdown
# ADR-007: Переход с pandas на Polars
Status: Accepted (2026-03-01)

## Context
pandas медленный на 10M+ строк, теряет память в ETL.

## Decision
Переходим на Polars 1.x для всех ETL-пайплайнов.

## Consequences
+ x10 быстрее, lazy execution
+ Arrow-совместимость с DuckDB
- Команда учит новый API
- Часть legacy придётся переписать
```

---

## Финальный проект. Модульный монолит «маркетплейс»

### Bounded Contexts

- **Users**: регистрация, профиль, аутентификация
- **Catalog**: товары, категории, поиск
- **Orders**: создание/оплата/доставка
- **Payments**: интеграция с провайдером

### Архитектура

- Гексагональная **внутри каждого модуля**.
- Между модулями — только через **events** (in-memory или Kafka).
- Outbox для надёжности.

### Стек

- FastAPI + uvicorn/granian
- SQLAlchemy 2.x async + Alembic + Postgres
- Redis для кеша
- Kafka (или in-memory bus) для событий
- OpenTelemetry + Jaeger
- structlog
- pytest + hypothesis + TestContainers
- Docker + docker-compose

### Требования

- Каждый модуль: domain/, application/, infrastructure/, interfaces/.
- Покрытие тестами ≥ 80%.
- `pyright --strict` проходит.
- README с архитектурной диаграммой.
- 3+ ADR.
- CI на GitHub Actions.

### Бонус

- Распилить на микросервисы (тот же код, разные деплои).
- GraphQL gateway через strawberry.
- Prometheus + Grafana dashboard.

---

## Чеклист и ресурсы

- [ ] Реализовал модульный монолит с разделёнными слоями
- [ ] Написал 3+ ADR в проекте
- [ ] Понимаю trade-off микросервисы vs модульный монолит
- [ ] Использовал Saga / Outbox / Idempotency Key
- [ ] Провёл 5+ чужих code review
- [ ] Могу объяснить архитектуру новичку за 10 минут

Ресурсы:
- 📘 [«Cosmic Python»](https://www.cosmicpython.com/) — лучшая книга по архитектуре Python-приложений (free)
- 📘 [Eric Evans — DDD Reference](https://www.domainlanguage.com/ddd/reference/) — free PDF
- 📘 [Martin Fowler architecture](https://martinfowler.com/architecture/)
- 📝 [microservices.io](https://microservices.io/)
- 🎥 [ArjanCodes — Software Design](https://www.youtube.com/@ArjanCodes/playlists)
- 📘 [ADR templates](https://github.com/joelparkerhenderson/architecture-decision-record)
- 📘 [Designing Data-Intensive Applications](https://dataintensive.net/) — free chapters
- 📘 [12-Factor App](https://12factor.net/)
- 💬 [t.me/pythonl](https://t.me/pythonl) — разборы архитектур

---

🎉 **Если ты дошёл сюда — поздравляю, ты Middle+. Дальше — practice, practice, practice.**

⭐ Поставь звезду репозиторию и подпишись на [t.me/pythonl](https://t.me/pythonl) — там разбирают именно такие проекты.

[← Этап 12](stage-12-devops.md) · [К оглавлению](README.md)
