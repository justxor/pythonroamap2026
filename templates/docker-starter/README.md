# 🐳 docker-starter

Production-ready шаблон для Python-сервиса: multi-stage Dockerfile, BuildKit cache, distroless runtime, k8s-манифесты, security-scan, CI.

## Ключевые решения

| Область          | Инструмент                                |
| ---------------- | ------------------------------------------ |
| Python           | 3.13-slim в builder, distroless в runtime  |
| Package manager  | `uv` (в 10-100× быстрее pip)               |
| Build            | BuildKit + cache mounts                    |
| Multi-arch       | linux/amd64 + linux/arm64 (buildx)         |
| Security         | trivy + cosign + SBOM (syft)               |
| Orchestration    | docker compose (local), k8s (prod)         |
| Charts           | Helm                                       |
| CI               | GitHub Actions                             |

## Структура

```
docker-starter/
├── Dockerfile             # multi-stage, distroless runtime
├── .dockerignore
├── docker-compose.yml     # local dev (api + db + redis)
├── docker-compose.prod.yml
├── pyproject.toml         # FastAPI demo сервис
├── src/app/
│   ├── __init__.py
│   └── main.py
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
├── chart/                 # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── _helpers.tpl
└── .github/workflows/
    └── docker.yml         # build + scan + sign + push
```

## Quickstart

```bash
# local dev
docker compose up --build

# production build (multi-arch)
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/me/app:1.0 --push .

# k8s deploy
kubectl apply -f k8s/
# или helm
helm upgrade --install app ./chart -f chart/values.yaml
```

## Цифры результата

- Размер образа: ~120 МБ (vs 1.2 ГБ без multi-stage).
- Cold start: < 2 сек.
- CVE (trivy HIGH+): 0 на chainguard-base.
- Повторная сборка: < 15 сек (с cache).

## Чеклист

- [ ] Base image запиннен по digest.
- [ ] `USER` non-root (10001).
- [ ] HEALTHCHECK в Dockerfile + probes в k8s.
- [ ] Resource limits заданы.
- [ ] `.dockerignore` исключает `.git`, `.venv`, тесты.
- [ ] CI сканирует trivy + grype.
- [ ] Образ подписан cosign.
- [ ] SBOM приложен к relase’у.

## Куда дальше

- 🐳 [Курс по контейнерам](../../course/containers-course.md)
- 🚀 [Stage 12 — DevOps](../../course/stage-12-devops.md)
