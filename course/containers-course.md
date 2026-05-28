# 🐳 Курс по контейнерам и оркестрации для Python 2026

> Глубокий курс по Docker, BuildKit, multi-stage, distroless, безопасности контейнеров, docker compose, Kubernetes и Helm для Python-сервисов в 2026.

---

## 📚 Бесплатные ресурсы

- 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — AI/ML, деплой моделей в контейнерах.
- 🐍 [t.me/pythonl](https://t.me/pythonl) — рубрики «задача дня», разборы Dockerfile.
- 📚 [Папка супер-полезных Python ресурсов](https://t.me/addlist/8vDUwYRGujRmZjFi) — целая подборка каналов.

---

## 🎯 Кому и зачем

Курс для тех, кто:
- пишет Dockerfile «по старинке» и получает образ на 1.5 ГБ вместо 150 МБ;
- не понимает, зачем BuildKit, cache mounts и multi-stage;
- хочет собирать образы быстро и сложные multi-arch;
- строит production-деплой в Kubernetes с health-probes, HPA, secrets;
- хочет проходить security-сканы (trivy, grype) без блокеров.

---

## 🗺️ Содержание

| #   | Урок                                                                       | Ключевые концепции                  |
| --- | -------------------------------------------------------------------------- | ---------------------------------- |
| 01  | [Контейнеры в 2026](#урок-01--контейнеры-в-2026)                              | OCI, runc, containerd, BuildKit    |
| 02  | [Dockerfile основы](#урок-02--dockerfile-основы)                            | FROM, RUN, COPY, layers            |
| 03  | [BuildKit и cache mounts](#урок-03--buildkit-и-cache-mounts)                | --mount, secrets, ssh              |
| 04  | [Multi-stage для Python](#урок-04--multi-stage-для-python)                   | builder, runtime, slim images      |
| 05  | [uv и контейнеры](#урок-05--uv-и-контейнеры)                                  | uv sync, lock, prod deps           |
| 06  | [Distroless и chainguard](#урок-06--distroless-и-chainguard)                | non-root, no shell, CVE-free       |
| 07  | [Multi-arch сборка](#урок-07--multi-arch-сборка)                              | buildx, QEMU, manifest list        |
| 08  | [Безопасность образов](#урок-08--безопасность-образов)                         | trivy, grype, SBOM, cosign         |
| 09  | [docker compose](#урок-09--docker-compose)                                | services, healthcheck, profiles    |
| 10  | [Networking и volumes](#урок-10--networking-и-volumes)                      | bridge, host, tmpfs, named volumes |
| 11  | [Logs, metrics, tracing](#урок-11--logs-metrics-tracing)                    | stdout, OTel, sidecar              |
| 12  | [Kubernetes для Python](#урок-12--kubernetes-для-python)                    | Deployment, Service, probes        |
| 13  | [Helm и charts](#урок-13--helm-и-charts)                                   | values.yaml, templates             |
| 14  | [Антипаттерны](#урок-14--антипаттерны)                                  | root user, fat images, latest tag  |
| 15  | [Production-чеклист](#урок-15--production-чеклист)                         | reproducibility, supply chain      |

---


## Урок 01 — Контейнеры в 2026

**Что такое контейнер на самом деле:**
- **OCI image** — tarball слоёв + JSON-манифест (image spec).
- **OCI runtime** (`runc`, `crun`) — запускает процесс в namespaces + cgroups.
- **containerd / podman** — высокоуровневый демон, управляющий runtime'ом.
- **Docker Engine** — wrapper над containerd + BuildKit + CLI.

В 2026 production-стек обычно такой:
- **Сборка:** `docker buildx` (BuildKit) или `podman build`.
- **Запуск локально:** `docker compose`.
- **Прод:** Kubernetes (k8s) с containerd.

> Образ — это **не виртуалка**. Это файловая система + метаданные. Изоляция — на уровне ядра хоста.

---

## Урок 02 — Dockerfile основы

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**Что не так в этом примере:**
1. Нет multi-stage → build-deps попадают в образ.
2. `COPY . .` инвалидирует кэш на любое изменение кода.
3. Запуск от `root`.
4. `pip` вместо `uv` — медленно.
5. Нет healthcheck, нет non-root user.

**Правила layer-кэша:**
- Меняющиеся файлы (`COPY src/`) — **в конце**.
- Зависимости (`pyproject.toml`/`requirements.txt`) — **в начале**.
- `RUN` с `apt-get update && apt-get install ... && rm -rf /var/lib/apt/lists/*` — одна команда.

---

## Урок 03 — BuildKit и cache mounts

BuildKit включён по умолчанию в Docker 23+. Даёт:
- параллельные стейджи;
- `--mount=type=cache` для pip/uv-кэша между билдами;
- `--mount=type=secret` для безопасной передачи токенов;
- `--mount=type=ssh` для приватных git-репо.

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS deps

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev
```

**Secrets — никогда не через ARG/ENV:**

```dockerfile
RUN --mount=type=secret,id=pypi_token \
    pip install --index-url "https://$(cat /run/secrets/pypi_token)@pypi.internal/simple/" my-private-pkg
```

Сборка: `docker buildx build --secret id=pypi_token,src=./token .`

---

## Урок 04 — Multi-stage для Python

**Канонический паттерн 2026:**

```dockerfile
# syntax=docker/dockerfile:1.7

# === Stage 1: builder ===
FROM python:3.13-slim AS builder

ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY src ./src
RUN uv pip install --no-deps -e .

# === Stage 2: runtime ===
FROM python:3.13-slim AS runtime

RUN useradd -m -u 10001 -s /usr/sbin/nologin app
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Результат:** образ ~120-180 МБ вместо 1.2 ГБ.

---

## Урок 05 — uv и контейнеры

`uv` ускоряет сборку в 10-100× относительно pip:

```dockerfile
FROM python:3.13-slim AS builder

# uv ставится 1 raw-байт, без python-пакета
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
```

**Лайфхаки:**
- `--no-install-project` на первом sync — кэширует только deps.
- `UV_LINK_MODE=copy` — для cross-layer переноса `.venv`.
- `UV_COMPILE_BYTECODE=1` — pyc заранее, быстрее cold start.

---

## Урок 06 — Distroless и chainguard

**Distroless** (Google) — образ без shell, package manager, libc-tools. Только runtime.

```dockerfile
FROM python:3.13-slim AS builder
# ... сборка venv ...

FROM gcr.io/distroless/python3-debian12:nonroot AS runtime
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
ENV PYTHONPATH=/app/src
USER nonroot
ENTRYPOINT ["/app/.venv/bin/python", "-m", "app.main"]
```

**Chainguard Images** (2026 — фактический стандарт для production):
- `cgr.dev/chainguard/python:latest` — wolfi-based.
- 0 CVE на момент релиза.
- SBOM + cosign подпись из коробки.
- Безсhell, nonroot по умолчанию.

```dockerfile
FROM cgr.dev/chainguard/python:latest-dev AS builder
# ...
FROM cgr.dev/chainguard/python:latest
COPY --from=builder /venv /venv
ENTRYPOINT ["/venv/bin/python", "-m", "app"]
```

---

## Урок 07 — Multi-arch сборка

В 2026 каждый сервис должен собираться под `linux/amd64` **и** `linux/arm64` (Mac M-series, AWS Graviton, ARM-ноды k8s).

```bash
docker buildx create --use --name multi
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/me/app:1.0 \
  --push .
```

**В Dockerfile** учитывай платформу:

```dockerfile
FROM --platform=$BUILDPLATFORM python:3.13-slim AS builder
ARG TARGETPLATFORM
ARG TARGETARCH
RUN echo "Building for $TARGETPLATFORM"
```

**Подводный камень:** native wheels (numpy, lxml, asyncpg) должны быть в индексе для обеих arch. Иначе билд под arm64 будет компилировать из исходников по 20 минут.

---

## Урок 08 — Безопасность образов

**Слои защиты:**

1. **Base image:** distroless или chainguard, pinned by digest:
   ```dockerfile
   FROM python:3.13-slim@sha256:abc123...
   ```
2. **Vulnerability scan:**
   ```bash
   trivy image --severity HIGH,CRITICAL ghcr.io/me/app:1.0
   grype ghcr.io/me/app:1.0
   ```
3. **SBOM:**
   ```bash
   syft ghcr.io/me/app:1.0 -o spdx-json > sbom.json
   docker buildx build --sbom=true --provenance=true ...
   ```
4. **Подпись (cosign + Sigstore):**
   ```bash
   cosign sign --yes ghcr.io/me/app:1.0
   cosign verify ghcr.io/me/app:1.0 --certificate-identity=...
   ```
5. **Принудительная политика в k8s:** `kyverno` / `OPA Gatekeeper` блокируют неподписанные образы.

---

## Урок 09 — docker compose

```yaml
services:
  api:
    build: .
    env_file: .env
    ports: ["8000:8000"]
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_started }
    restart: unless-stopped
    deploy:
      resources:
        limits: { cpus: "1.0", memory: 512M }

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s

  redis:
    image: redis:7-alpine
    command: redis-server --save "" --appendonly no

volumes:
  pgdata:
```

**`profiles` для опциональных сервисов:**

```yaml
services:
  jaeger:
    profiles: [observability]
    image: jaegertracing/all-in-one:latest
```

`docker compose --profile observability up`

---

## Урок 10 — Networking и volumes

**Networking:**
- `bridge` (default) — изолированная подсеть, DNS по имени сервиса.
- `host` — общий сетевой namespace (только Linux, опасно для prod).
- `none` — никакой сети (CI-задачи).

**Volumes:**
- `named` — `pgdata:/var/lib/postgresql/data` — Docker управляет жизненным циклом.
- `bind` — `./code:/app` — для разработки, никогда в проде.
- `tmpfs` — RAM-only, для секретов на время работы контейнера.

```yaml
services:
  app:
    tmpfs:
      - /tmp:size=100M,mode=1777
```

**Правило production:** stateful данные → managed-сервис (RDS, ElastiCache), не volume.

---

## Урок 11 — Logs, metrics, tracing

**Логи:**
- Пиши в `stdout`/`stderr` (12-factor). Docker подхватит сам.
- JSON-формат: `structlog` + `JSONRenderer`.
- Drivers: `json-file` (default), `journald`, `fluentd`, `awslogs`.

```yaml
services:
  api:
    logging:
      driver: json-file
      options: { max-size: "10m", max-file: "3" }
```

**Метрики:**
- `prometheus_client` экспортирует `/metrics`.
- В k8s: `ServiceMonitor` для Prometheus Operator.

**Tracing:**
- OpenTelemetry SDK + `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Sidecar `otel-collector` или DaemonSet.

---

## Урок 12 — Kubernetes для Python

**Минимальный Deployment + Service:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: api }
spec:
  replicas: 3
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: api
          image: ghcr.io/me/app:1.0
          ports: [{ containerPort: 8000 }]
          env:
            - name: DATABASE_URL
              valueFrom: { secretKeyRef: { name: db, key: url } }
          resources:
            requests: { cpu: 100m, memory: 256Mi }
            limits:   { cpu: 1,    memory: 512Mi }
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 10
          readinessProbe:
            httpGet: { path: /ready, port: 8000 }
            periodSeconds: 5
          startupProbe:
            httpGet: { path: /health, port: 8000 }
            failureThreshold: 30
            periodSeconds: 2
---
apiVersion: v1
kind: Service
metadata: { name: api }
spec:
  selector: { app: api }
  ports: [{ port: 80, targetPort: 8000 }]
```

**HPA для autoscaling:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api }
spec:
  scaleTargetRef: { kind: Deployment, name: api, apiVersion: apps/v1 }
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
```

---

## Урок 13 — Helm и charts

Helm — пакетный менеджер k8s. Структура чарта:

```
chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── _helpers.tpl
└── charts/        # subcharts (postgresql, redis)
```

`values.yaml`:

```yaml
image:
  repository: ghcr.io/me/app
  tag: "1.0"
  pullPolicy: IfNotPresent

replicaCount: 3

resources:
  requests: { cpu: 100m, memory: 256Mi }
  limits:   { cpu: 1,    memory: 512Mi }

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPU: 70

env:
  LOG_LEVEL: INFO

postgresql:
  enabled: true
  auth: { database: app, username: app }
```

Релизы: `helm upgrade --install api ./chart -f values.prod.yaml --namespace prod --create-namespace`.

**В 2026 чаще используют ArgoCD / FluxCD** поверх Helm — GitOps вместо CLI.

---

## Урок 14 — Антипаттерны

**❌ `FROM python:3.13`** (full image, 1+ ГБ) → ✅ `python:3.13-slim` или distroless.

**❌ `USER root`** (или не указан = root) → ✅ `USER 10001:10001` + `runAsNonRoot: true`.

**❌ `COPY . .` в начале** → cache breaks on every change → ✅ сначала `pyproject.toml`, потом код.

**❌ Секреты в `ENV` / `ARG`** → видны в `docker history` → ✅ `--mount=type=secret` или k8s Secrets.

**❌ `latest` тег в production** → невоспроизводимо → ✅ semver + digest `@sha256:...`.

**❌ `apt-get install` без `rm -rf /var/lib/apt/lists/*`** → лишние 50 МБ.

**❌ Запуск под supervisord / pid 1 = bash** → сигналы не доходят → ✅ `exec` форма CMD: `CMD ["python", "-m", "app"]`.

**❌ `docker run --privileged`** в проде → ✅ capabilities только что нужно.

**❌ Volume с кодом в production** → ✅ только в dev.

**❌ Нет `.dockerignore`** → весь `.git`, `.venv`, `__pycache__` идут в build context.

---

## Урок 15 — Production-чеклист

- [ ] Multi-stage Dockerfile, runtime-stage без build-deps.
- [ ] Base image pinned by digest (`@sha256:...`).
- [ ] `USER` non-root + `runAsNonRoot: true` в k8s.
- [ ] `.dockerignore` исключает `.git`, `.venv`, тесты.
- [ ] `HEALTHCHECK` в Dockerfile + livenessProbe/readinessProbe в k8s.
- [ ] BuildKit cache mounts для uv/pip.
- [ ] Multi-arch сборка (amd64 + arm64).
- [ ] Trivy/grype в CI, fail on HIGH+.
- [ ] SBOM (`syft`) + cosign-подпись в registry.
- [ ] Логи в stdout как JSON.
- [ ] Метрики `/metrics` (Prometheus).
- [ ] OTel-трейсинг включён.
- [ ] Resource limits (cpu/memory) в k8s.
- [ ] HPA или KEDA для autoscale.
- [ ] NetworkPolicy ограничивает egress.
- [ ] PodSecurityStandard: `restricted`.
- [ ] Образ < 200 МБ для FastAPI-сервиса.
- [ ] Cold start < 3 сек.

---

## 🏋️ Упражнения

1. Возьми свой существующий Dockerfile, уменьши размер образа в 5+ раз через multi-stage + slim/distroless.
2. Напиши `docker buildx` команду для multi-arch сборки FastAPI-сервиса.
3. Прогони `trivy image` на популярном `python:3.13` и на `cgr.dev/chainguard/python:latest` — сравни CVE.
4. Собери Dockerfile с BuildKit cache mounts для `uv` — измерь время повторной сборки.
5. Напиши `docker-compose.yml` для FastAPI + Postgres + Redis + Jaeger с healthchecks и profiles.
6. Напиши минимальный Helm-чарт для FastAPI-сервиса (Deployment + Service + HPA + ConfigMap + Secret).
7. Сделай GitHub Actions workflow: build → trivy scan → sign with cosign → push.
8. Реализуй graceful shutdown в Python-приложении и убедись, что k8s preStop hook + terminationGracePeriodSeconds работают корректно.

---

## 📚 Бесплатные ресурсы

**📌 Telegram (в порядке полезности для контейнеров):**
1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — деплой ML/AI в контейнерах.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — разборы Dockerfile, задачи дня.
3. 📚 [Папка Python-ресурсов](https://t.me/addlist/8vDUwYRGujRmZjFi) — целая подборка.

**Документация:**
- [Docker docs](https://docs.docker.com/)
- [BuildKit docs](https://docs.docker.com/build/buildkit/)
- [Kubernetes docs](https://kubernetes.io/docs/home/)
- [Helm docs](https://helm.sh/docs/)
- [Chainguard Images](https://images.chainguard.dev/)
- [Distroless](https://github.com/GoogleContainerTools/distroless)

**Инструменты:**
- [trivy](https://github.com/aquasecurity/trivy) — vulnerability scanner.
- [grype](https://github.com/anchore/grype) — альтернатива trivy.
- [syft](https://github.com/anchore/syft) — SBOM generator.
- [cosign](https://github.com/sigstore/cosign) — image signing.
- [dive](https://github.com/wagoodman/dive) — анализ слоёв образа.
- [hadolint](https://github.com/hadolint/hadolint) — Dockerfile linter.
- [k9s](https://k9scli.io/) — terminal UI для k8s.

**Лучшие туториалы:**
- [Docker official getting started](https://docs.docker.com/get-started/)
- [Kubernetes the Hard Way (Kelsey Hightower)](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Play with Docker](https://labs.play-with-docker.com/) — браузерная песочница.
- [Killercoda Kubernetes](https://killercoda.com/kubernetes) — интерактивные лаборатории.

---

## ⏭️ Что дальше

- 🚀 [Stage 12 — DevOps](stage-12-devops.md) — CI/CD, observability, k8s в деталях.
- 🌊 [Курс по асинхронности](async-course.md) — async-сервисы в контейнерах.
- 🌐 [Stage 09 — Web](stage-09-web.md) — FastAPI в production.
- 📦 [Template: docker-starter](../templates/docker-starter/) — production-ready шаблон.

[← К содержанию курса](README.md)
