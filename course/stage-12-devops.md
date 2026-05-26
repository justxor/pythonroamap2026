# Этап 12. DevOps и продакшн

> 🎯 Довести Python-сервис до prod: Docker, конфиги, логи, метрики, CI/CD.
> ⏱ 3 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. Docker (multi-stage + uv)](#урок-1-docker-multi-stage--uv)
- [Урок 2. structlog и pydantic-settings](#урок-2-structlog-и-pydantic-settings)
- [Урок 3. OpenTelemetry](#урок-3-opentelemetry)
- [Упражнение](#упражнение)

---

## Урок 1. Docker (multi-stage + uv)

### Простой Dockerfile (плохо)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "-m", "src.app"]
```

Минусы: огромный образ, нет кеша слоёв.

### Multi-stage + uv (правильно 2026)

```dockerfile
# syntax=docker/dockerfile:1.9
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.13-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src ./src
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
USER 1000
CMD ["python", "-m", "src.app"]
```

Результат: ~150-200 МБ, зависимости в кешируемом слое, non-root.

### .dockerignore

```
__pycache__
*.pyc
.venv
.git
.pytest_cache
.ruff_cache
tests
docs
```

### docker-compose для разработки

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - DB_URL=postgresql+asyncpg://u:p@db:5432/app
    depends_on: [db, redis]

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: u
      POSTGRES_PASSWORD: p
      POSTGRES_DB: app
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  db_data:
```

---

## Урок 2. structlog и pydantic-settings

### pydantic-settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    db_url: str
    redis_url: str = "redis://localhost"
    debug: bool = False

settings = Settings()
```

### structlog — JSON-логи

```python
import structlog
import logging

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

log = structlog.get_logger()
log.info("user.signup", user_id=42, plan="pro")
# {"event":"user.signup","user_id":42,"plan":"pro","level":"info","timestamp":"..."}
```

### Контекст запроса (request_id)

```python
from uuid import uuid4

@app.middleware("http")
async def add_request_id(request, call_next):
    rid = str(uuid4())
    structlog.contextvars.bind_contextvars(request_id=rid)
    response = await call_next(request)
    structlog.contextvars.clear_contextvars()
    return response
```

Все логи в рамках запроса автоматически содержат `request_id`.

---

## Урок 3. OpenTelemetry

```bash
uv add opentelemetry-api opentelemetry-sdk        opentelemetry-instrumentation-fastapi        opentelemetry-exporter-otlp
```

### Инициализация

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

resource = Resource.create({"service.name": "my-api"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317")))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)
```

### Авто-инструментирование FastAPI

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor.instrument_app(app)
```

### Свои спаны

```python
@app.get("/process")
def process():
    with tracer.start_as_current_span("validate"):
        ...
    with tracer.start_as_current_span("db.query"):
        ...
    return {"ok": True}
```

### Просмотр

- Jaeger: `docker run -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one`
- Grafana Tempo (prod).

---

## Упражнение. Задеплоить FastAPI

Возьми API из этапа 9 и:

1. Multi-stage Dockerfile с uv.
2. docker-compose с Postgres, Redis, Jaeger.
3. pydantic-settings + structlog + OpenTelemetry.
4. Health endpoint `/healthz`.
5. README с инструкцией: `docker compose up` → API на :8000, Jaeger на :16686.

Бонус: pre-commit + GitHub Actions CI, pip-audit, bandit.

---

## Чеклист и ресурсы

- [ ] Multi-stage Docker < 200 МБ
- [ ] Настроен CI: lint + typecheck + test + build
- [ ] structlog с JSON-форматом
- [ ] Понимаю span, trace, контекст распространения
- [ ] OpenTelemetry → Jaeger работает
- [ ] Знаю HPA в Kubernetes

Ресурсы:
- 📘 [12-Factor App](https://12factor.net/) — must-read
- 📘 [Docker Get Started](https://docs.docker.com/get-started/)
- 📘 [Kubernetes basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- 🎥 [TechWorld with Nana](https://www.youtube.com/@TechWorldwithNana)
- 📘 [structlog docs](https://www.structlog.org/)
- 📘 [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- 📝 [Hynek Schlawack](https://hynek.me/articles/)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 11](stage-11-data-ml.md) · [К оглавлению](README.md) · [Этап 13 →](stage-13-architecture.md)
