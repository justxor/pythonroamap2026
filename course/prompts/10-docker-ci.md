# 🐳 Промпт 10 — Dockerfile / GitHub Actions

> Используй когда: нужно упаковать приложение или настроить CI.

---

```
[CONTEXT]
Python 3.13, uv для зависимостей.
Приложение: <FastAPI на uvicorn / CLI / воркер / ...>
Зависимости в pyproject.toml + uv.lock.

[TASK]
<«Напиши production-Dockerfile» / «Настрой GitHub Actions для PR» / ...>

[RULES для Dockerfile]
- Multi-stage build (builder + runtime).
- Базовый образ: python:3.13-slim.
- Не-root юзер.
- COPY pyproject.toml uv.lock — отдельным слоем для кеширования.
- HEALTHCHECK обязательно (если есть HTTP).
- Финальный образ < 200 МБ.
- .dockerignore с .git, .venv, __pycache__, tests.

[RULES для CI]
- На каждый PR: ruff check, ruff format --check, pyright, pytest с coverage.
- Matrix по версиям Python (3.13, 3.14).
- Кеш для uv (actions/cache@v4 или setup-uv@v3 cache).
- Тайм-аут на job (≤ 15 мин).
- Никаких секретов в логах.

[LENS]
1) **Файлы** целиком (Dockerfile / workflow.yml / .dockerignore).
2) **Чеклист проверки** — что прогнать локально перед push.
3) **Возможные улучшения** — что бы добавил на v2 (Trivy-скан, SBOM, ...).
```
