# Этап 13. Архитектура — Clean / Hexagonal / DDD, Outbox, Saga, финальный проект

> ⏱ Время: 4 недели  
> 🎯 Цель: проектировать приложения, которые не превращаются в "большой шар грязи" через год. Понимать DDD, гексагональную архитектуру, паттерны интеграции (Outbox, Saga), события и идемпотентность. Завершить курс реальным проектом.

---

## 📘 Урок 13.1 — Зачем нужна архитектура

Симптомы плохой архитектуры:
- Добавить фичу = править 15 файлов.
- Тесты медленные, потому что трогают БД и HTTP.
- Заменить Postgres на что-то другое — переписать половину.
- Бизнес-логика размазана по контроллерам, моделям ORM и шаблонам.

Принципы, которые лечат это:
- **Разделение ответственности** (SoC).
- **Зависимость через интерфейсы** (DIP из SOLID).
- **Бизнес-логика не знает о фреймворке**.

---

## 📘 Урок 13.2 — Гексагональная архитектура (Ports & Adapters)

```
                  ┌──────────────────────────────┐
       HTTP ────► │                              │
       CLI  ────► │      DOMAIN (ядро)           │ ────► PostgresAdapter
       Queue ───► │   - сущности, агрегаты       │ ────► RedisAdapter
       Tests ──► │   - сервисы, use-cases       │ ────► SMTPAdapter
                  │   - порты (интерфейсы)       │
                  └──────────────────────────────┘
                       не знает о фреймворке
```

- **Domain** — pure Python: dataclasses, бизнес-правила. Никакого FastAPI/SQLAlchemy.
- **Ports** — интерфейсы (Protocol), которые домен требует от внешнего мира.
- **Adapters** — реализации портов: PostgresUserRepository, FastAPIController, ...
- **Зависимости направлены внутрь**: домен ничего не импортирует из адаптеров.

---

## 📘 Урок 13.3 — Структура проекта

```
app/
├── domain/          # ядро: сущности, value objects, события
│   ├── user.py
│   ├── order.py
│   └── events.py
├── application/     # use-cases (бизнес-операции)
│   ├── create_order.py
│   └── ports.py     # интерфейсы репозиториев и сервисов
├── infrastructure/  # адаптеры
│   ├── db/          # SQLAlchemy
│   ├── http/        # внешние API клиенты
│   └── queue/       # rabbitmq/kafka
├── interfaces/      # вход: FastAPI controllers, CLI
│   └── api/
└── main.py          # composition root: связываем всё
```

---

## 📘 Урок 13.4 — DDD: язык, агрегаты, события

**Ubiquitous Language** — разработчики и бизнес говорят одними словами. `Order`, а не `OrderRow`.

**Агрегат** = граница консистентности. Внутри агрегата всё меняется в одной транзакции, между агрегатами — через события.

```python
# domain/order.py
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

@dataclass
class OrderLine:
    sku: str
    qty: int
    price: Decimal

@dataclass
class Order:
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID
    lines: list[OrderLine] = field(default_factory=list)
    status: str = "draft"
    events: list["DomainEvent"] = field(default_factory=list, repr=False)

    def add(self, line: OrderLine) -> None:
        if self.status != "draft":
            raise ValueError("cannot modify confirmed order")
        self.lines.append(line)

    def confirm(self) -> None:
        if not self.lines:
            raise ValueError("empty order")
        self.status = "confirmed"
        self.events.append(OrderConfirmed(order_id=self.id))
```

---

## 📘 Урок 13.5 — Use-case и порты

```python
# application/ports.py
from typing import Protocol
from uuid import UUID
from app.domain.order import Order

class OrderRepository(Protocol):
    async def get(self, id_: UUID) -> Order | None: ...
    async def save(self, order: Order) -> None: ...

class EventPublisher(Protocol):
    async def publish(self, event: object) -> None: ...

# application/confirm_order.py
from dataclasses import dataclass

@dataclass
class ConfirmOrder:
    orders: OrderRepository
    publisher: EventPublisher

    async def __call__(self, order_id: UUID) -> None:
        order = await self.orders.get(order_id)
        if order is None: raise LookupError("order not found")
        order.confirm()
        await self.orders.save(order)
        for ev in order.events:
            await self.publisher.publish(ev)
        order.events.clear()
```

Use-case не знает ни про БД, ни про брокер. Тесты на use-case — без БД, моки порт через `InMemoryOrderRepository`.

---

## 📘 Урок 13.6 — Outbox: надёжная публикация событий

**Проблема:** записал в БД и упал — событие в Kafka не ушло. Записал в Kafka и упал — данные в БД не сохранены. **Двух-фазный коммит не работает в продакшне.**

**Решение — Outbox:**

```
┌─ транзакция ──────────────────────────┐
│  UPDATE orders SET status='confirmed' │
│  INSERT INTO outbox(event)  ←         │
└───────────────────────────────────────┘
                  │
                  ▼
   ┌────── relay (отдельный процесс) ───────┐
   │  SELECT * FROM outbox WHERE !sent      │
   │  for each: publish → mark sent         │
   └────────────────────────────────────────┘
```

```sql
CREATE TABLE outbox (
    id          BIGSERIAL PRIMARY KEY,
    aggregate   TEXT NOT NULL,
    type        TEXT NOT NULL,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    sent_at     TIMESTAMPTZ
);
CREATE INDEX idx_outbox_unsent ON outbox(id) WHERE sent_at IS NULL;
```

Гарантирует **at-least-once** доставку. Получатель должен быть **идемпотентным** (см. 13.8).

---

## 📘 Урок 13.7 — Saga: распределённые транзакции

Когда операция захватывает несколько сервисов, классическая транзакция невозможна. Используют **сагу** — последовательность шагов с компенсациями.

```
Заказ:
  1. Резерв товара     ── ошибка ──► (нечего откатывать)
  2. Списать деньги    ── ошибка ──► отменить резерв
  3. Создать доставку  ── ошибка ──► вернуть деньги, отменить резерв
  4. Подтвердить заказ
```

Два стиля:
- **Orchestration** — отдельный сервис-дирижёр шлёт команды.
- **Choreography** — сервисы реагируют на события друг друга.

---

## 📘 Урок 13.8 — Идемпотентность

Идемпотентная операция — повторный вызов с теми же параметрами не меняет результат.

```python
async def credit(account_id: UUID, amount: Decimal, idem_key: str) -> None:
    async with session.begin():
        if await session.scalar(select(IdempotencyKey).where(...)):
            return                            # уже обработано
        session.add(IdempotencyKey(key=idem_key))
        await session.execute(update(Account).where(...).values(balance=Account.balance + amount))
```

Клиент шлёт уникальный `Idempotency-Key` в HTTP-заголовке (Stripe-style).

---

## 📘 Урок 13.9 — CQRS (когда нужно)

**Command** меняет состояние, ничего не возвращает (или id).  
**Query** читает, ничего не меняет.

Иногда полезно держать **разные модели для записи и чтения** — write-модель оптимизирована под бизнес-правила, read-модель — под UI/отчёты. Не нужно сразу на все проекты, только когда чтение и запись по-разному масштабируются.

---

## 🛠 Финальный проект

**Mini-Marketplace** — собери проект, использующий навыки всего курса.

### Требования
1. **Backend** на FastAPI: пользователи, товары, заказы, корзина.
2. **Auth** через JWT (этап 9).
3. **БД** Postgres + SQLAlchemy 2.x async + Alembic (этап 10).
4. **Архитектура**: domain / application / infrastructure / interfaces (этап 13).
5. **События** через Outbox: при подтверждении заказа в outbox пишется `OrderConfirmed`, отдельный воркер шлёт в очередь (Redis Streams или RabbitMQ).
6. **Idempotency-Key** на `POST /orders`.
7. **Тесты**: unit (домен и use-cases) + integration (через TestClient) + property-based на критичную функцию (этап 7).
8. **Структурные логи** + OpenTelemetry-трейсы (этап 12).
9. **Docker** + docker-compose (этап 12).
10. **CI**: ruff + pyright + pytest на каждом PR (этапы 0, 7, 12).
11. **README** с архитектурной диаграммой, инструкцией по запуску, описанием эндпоинтов.

### Этапы реализации (4 недели)
- **Неделя 1**: домен + use-cases + in-memory репозитории + unit-тесты.
- **Неделя 2**: SQLAlchemy + Alembic + FastAPI-эндпоинты + integration-тесты.
- **Неделя 3**: outbox + воркер + idempotency + JWT-auth.
- **Неделя 4**: structlog + OTel + Docker + CI + README.

---

## ✅ Скелет проекта (фрагмент)

```python
# app/main.py — composition root
from fastapi import FastAPI
from app.infrastructure.db import Session
from app.infrastructure.db.order_repo import SqlOrderRepository
from app.infrastructure.queue.outbox_publisher import OutboxPublisher
from app.application.confirm_order import ConfirmOrder
from app.interfaces.api.orders import make_router

def create_app() -> FastAPI:
    app = FastAPI()
    async def session_factory(): 
        async with Session() as s: yield s
    # композим зависимости в точке входа, нигде больше
    app.include_router(make_router(
        confirm_order=lambda s: ConfirmOrder(
            orders=SqlOrderRepository(s),
            publisher=OutboxPublisher(s),
        )
    ))
    return app

app = create_app()
```

---

## 📚 Бесплатные ресурсы

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**

- 📕 [Architecture Patterns with Python — Cosmic Python (free online)](https://www.cosmicpython.com/) — главная книга про DDD/Hexagonal в Python.
- 📕 [Domain-Driven Design Reference — Eric Evans (free PDF)](https://www.domainlanguage.com/ddd/reference/).
- 📕 [Microservices.io — Chris Richardson](https://microservices.io/patterns/) — Outbox, Saga, CQRS.
- 📕 [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) — каталог паттернов.
- 📺 [Code Opinion (Derek Comartin)](https://www.youtube.com/@CodeOpinion) — современная архитектура.
- 📺 [GOTO Conferences — DDD talks](https://www.youtube.com/@GOTOConferences).
- 💬 **Telegram: [@pythonl](https://t.me/pythonl)**.

---

## ☑ Чеклист этапа

- [ ] Разделяю код на domain / application / infrastructure / interfaces.
- [ ] Домен не импортирует фреймворк и ORM.
- [ ] Use-cases получают зависимости через порты (Protocol).
- [ ] Понимаю, что такое агрегат и граница консистентности.
- [ ] Реализовал Outbox для надёжной публикации событий.
- [ ] Сделал `Idempotency-Key` на критичных эндпоинтах.
- [ ] Финальный проект задеплоен и работает.

---

# 🎉 Поздравляю!

Если ты дошёл до конца — у тебя есть **полный набор**, чтобы устроиться Python-разработчиком в 2026 году, делать pet-проекты, контрибьютить в open source и постоянно расти.

**Что дальше:**
- 🧠 Делай свои pet-проекты и публикуй на GitHub.
- 📝 Веди технический блог — лучший способ закрепить знания.
- 🌍 Контрибьють в open source (FastAPI, Polars, SQLAlchemy всегда нуждаются в помощи).
- 💼 Иди на собеседования. Большинство компаний оценивают как раз то, что в этом курсе.

---

[⬅ Этап 12](stage-12-devops.md) | [📚 Оглавление](README.md) | [🏠 Главная README](../README.md)
