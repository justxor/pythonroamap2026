# 21 — Dockerfile review

> Промпт для профессионального ревью Dockerfile для Python-сервиса в 2026.

---

## Промпт

```
Ты — senior DevOps-эксперт по контейнерам и production-безопасности.
Проведи ревью Dockerfile ниже по чеклисту:

1. **Multi-stage**: есть ли разделение builder/runtime? Build-deps в runtime?
2. **Base image**: slim/distroless/chainguard или full? Pinned by digest?
3. **Layer cache**: зависимости копируются раньше кода?
4. **BuildKit**: используются `--mount=type=cache` для pip/uv?
5. **Пакетный менеджер**: pip или uv? `--no-cache-dir` у pip?
6. **Apt-get**: `apt-get update && install && rm -rf /var/lib/apt/lists/*` в одной RUN?
7. **USER**: задан non-root явно? UID >= 10000?
8. **HEALTHCHECK**: присутствует?
9. **CMD/ENTRYPOINT**: exec-форма (JSON array)?
10. **Секреты**: нет ли `ARG`/`ENV` с токенами?
11. **Multi-arch**: поддерживается `$TARGETPLATFORM` где нужно?
12. **WORKDIR**: явно задан?
13. **`.dockerignore`**: упомяни, что нужен (если видишь следы его отсутствия).
14. **Размер и слои**: прикинь, какой размер образа ожидается, сколько слоёв.

Формат ответа:
- Резюме: образ ready/needs-work, ожидаемый размер.
- Находки по пунктам с severity (BLOCKER / HIGH / MEDIUM / LOW).
- Полный переписанный Dockerfile.
- `.dockerignore` и команды сборки.
- Ожидаемое уменьшение размера образа.

--- DOCKERFILE START ---
{paste your Dockerfile here}
--- DOCKERFILE END ---
```

## Связанные материалы

- [Курс по контейнерам](../containers-course.md)
- [Stage 12 — DevOps](../stage-12-devops.md)
