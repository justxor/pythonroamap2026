# Этап 12. DevOps — Docker, structlog, OpenTelemetry, deploy

> ⏱ Время: 2 недели  
> 🎯 Цель: упаковать приложение в Docker, настроить структурные логи, метрики и трейсы (OpenTelemetry), деплоить через CI/CD, делать healthcheck'и и rolling-обновления.

---

## 📘 Урок 12.1 — Docker за час

```
┌──────────── Dockerfile ────────────┐
│  FROM python:3.13-slim             │
│       ↓                            │
│  COPY pyproject.toml uv.lock /app/ │
│       ↓                            │
│  RUN  uv sync                      │
│       ↓                            │
│  COPY . /app                       │
│       ↓                            │
│  CMD  uvicorn app.main:app         │
└────────────────────────────────────┘
```

**Multi-stage сборка** (минимальный production-образ):

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder
WORKDIR /app
RUN pip install -U uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.13-slim AS runtime
WORKDIR /app
RUN useradd -r -u 1000 app
COPY --from=builder /app/.venv /app/.venv
COPY app ./app
USER app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
HEALTHCHECK --interval=30s CMD curl -fsS http://127.0.0.1:8000/healthz || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**.dockerignore** обязателен:
```
.git
.venv
__pycache__
*.pyc
tests
.env
```

---

## 📘 Урок 12.2 — docker-compose для локальной разработки

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes: { pgdata: {} }
```

```bash
docker compose up --build
```

---

## 📘 Урок 12.3 — Структурные логи (structlog)

Текстовые логи нечитаемы для машин. JSON-логи — стандарт для production.

```bash
uv add structlog
```

```python
# app/logging.py
import logging, structlog, sys

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level)),
    )

log = structlog.get_logger()
```

Использование:
```python
log.info("user_login", user_id=42, ip="1.2.3.4")
# {"event":"user_login","user_id":42,"ip":"1.2.3.4","level":"info","timestamp":"2026-01-15T12:00:00Z"}
```

**Запрещено** логировать пароли, токены, PII. Используй scrubber'ы.

---

## 📘 Урок 12.4 — Корреляция запросов (request_id)

```python
import uuid, structlog
from fastapi import Request

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex
    structlog.contextvars.bind_contextvars(request_id=rid)
    try:
        response = await call_next(request)
    finally:
        structlog.contextvars.clear_contextvars()
    response.headers["x-request-id"] = rid
    return response
```

Теперь все логи в рамках одного запроса автоматически содержат `request_id`.

---

## 📘 Урок 12.5 — OpenTelemetry: трейсы, метрики, логи

OTel — единый стандарт для observability. Один SDK, любой backend (Jaeger, Tempo, DataDog, New Relic).

```bash
uv add opentelemetry-distro opentelemetry-exporter-otlp \
       opentelemetry-instrumentation-fastapi \
       opentelemetry-instrumentation-sqlalchemy \
       opentelemetry-instrumentation-httpx
uv run opentelemetry-bootstrap -a install
```

```python
# app/otel.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
)
tracer = trace.get_tracer(__name__)

@app.get("/work")
def work() -> dict:
    with tracer.start_as_current_span("compute"):
        ...
    return {"ok": True}
```

Запускай рядом локальный коллектор: `otel/opentelemetry-collector` + Jaeger/Tempo для просмотра.

---

## 📘 Урок 12.6 — Метрики и алерты

**RED-метрики** (для сервисов):
- **R**ate — RPS.
- **E**rrors — частота 5xx.
- **D**uration — p50/p95/p99 latency.

**USE-метрики** (для ресурсов):
- **U**tilization, **S**aturation, **E**rrors.

Prometheus + Grafana — бесплатный стандарт. Питон-клиент `prometheus-client` + `/metrics` эндпоинт.

---

## 📘 Урок 12.7 — CI/CD

```yaml
# .github/workflows/release.yml
name: Release
on: { push: { tags: ["v*"] } }
jobs:
  docker:
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

Деплой: GitOps (ArgoCD/FluxCD), либо `kubectl set image`, либо просто `docker compose pull && up -d` для маленьких проектов.

---

## 📘 Урок 12.8 — Секреты

- **Никогда** не коммить секреты. `.env` в `.gitignore`.
- Используй: GitHub Actions Secrets, Doppler, Vault, AWS Secrets Manager, Kubernetes Secrets.
- В коде читай через `pydantic-settings` (этап 9).

---

## 🛠 Упражнения

### Упражнение 12.1 — Multi-stage Dockerfile
Упакуй своё FastAPI-приложение из этапа 9. Образ должен быть < 200 МБ, юзер не root, есть healthcheck.

### Упражнение 12.2 — compose
Подними `app + postgres + redis` через docker-compose. Добавь healthcheck'и для всех.

### Упражнение 12.3 — Structured logs
Подключи structlog к проекту. Добавь middleware с `request_id`. Сделай так, чтобы все логи запроса содержали `request_id`, `user_id` (если есть), `route`.

### Упражнение 12.4 — OpenTelemetry
Подними локально `otel-collector + jaeger` через compose. Инструментируй FastAPI. Сделай 5 запросов и найди их трейсы в Jaeger UI.

---

## ✅ Решение 12.1 (Dockerfile)

См. урок 12.1 — он сразу production-ready. Проверка размера:
```bash
docker build -t app:latest .
docker images app:latest    # SIZE должен быть ~150-200 МБ
docker run --rm -p 8000:8000 app:latest
curl http://localhost:8000/healthz
```

---

## 📚 Бесплатные ресурсы

- 📕 [Docker docs](https://docs.docker.com/) — официально.
- 📕 [Play with Docker](https://labs.play-with-docker.com/) — бесплатная песочница.
- 📕 [12-Factor App](https://12factor.net/) — манифест для production-приложений.
- 📕 [structlog docs](https://www.structlog.org/).
- 📕 [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/).
- 📕 [Distributed Systems Observability — Cindy Sridharan (free PDF)](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/) — бесплатна на сайте автора.
- 📺 [TechWorld with Nana](https://www.youtube.com/@TechWorldwithNana) — Docker и Kubernetes.
- 💬 **Telegram: [@pythonl](https://t.me/pythonl)**.

---

## ☑ Чеклист этапа

- [ ] Многоступенчатый Dockerfile, < 200 МБ, не-root юзер, healthcheck.
- [ ] docker-compose с healthcheck'ами для зависимостей.
- [ ] JSON-логи через structlog с request_id.
- [ ] Трейсы через OpenTelemetry, видны в Jaeger.
- [ ] Метрики Prometheus, дашборд в Grafana.
- [ ] CI собирает образ, CD деплоит на staging.
- [ ] Никаких секретов в репозитории.

---

[⬅ Этап 11](stage-11-data-ml.md) | [📚 Оглавление](README.md) | [Этап 13 ➡](stage-13-architecture.md)
