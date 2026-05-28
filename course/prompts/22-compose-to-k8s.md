# 22 — docker-compose → Kubernetes

> Промпт для конвертации docker-compose в production k8s-манифесты или Helm-чарт.

---

## Промпт

```
Ты — Kubernetes-архитектор с экспертизой в Python-стеке (FastAPI/asyncpg/Postgres/Redis).
Сконвертируй приложенный docker-compose.yml в production-ready k8s-манифесты.

Требования:
1. Каждый сервис → Deployment + Service.
2. Для stateful (DB/Redis) — StatefulSet или вынеси в managed-сервис (укажи в комментарии).
3. **Безопасность**:
   - `runAsNonRoot: true`, UID 10001.
   - `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`.
   - `capabilities.drop: ["ALL"]`.
   - `seccompProfile.type: RuntimeDefault`.
4. **Probes**: startup + liveness + readiness с HTTP-эндпоинтами.
5. **Resources**: requests/limits обязательны.
6. **HPA** по CPU + memory.
7. **Secrets** → `Secret` (не `env` в чистом виде).
8. **ConfigMap** для не-секретных ENV.
9. **NetworkPolicy** ограничивает ingress/egress.
10. **terminationGracePeriodSeconds: 30** + preStop hook.
11. **Labels**: app.kubernetes.io/* recommended labels.
12. **Image**: pinned by tag или digest, `imagePullPolicy: IfNotPresent`.

Формат ответа:
- Список файлов, которые будут созданы.
- Каждый файл полностью (deployment.yaml, service.yaml, secret.yaml, configmap.yaml, hpa.yaml, networkpolicy.yaml, ingress.yaml).
- Краткое объяснение, почему stateful-сервисы лучше managed.
- `kubectl apply` или `kustomization.yaml` поверх.

--- COMPOSE START ---
{paste your docker-compose.yml here}
--- COMPOSE END ---
```

## Связанные материалы

- [Курс по контейнерам — Kubernetes](../containers-course.md#урок-12--kubernetes-для-python)
- [docker-starter template](../../templates/docker-starter/)
