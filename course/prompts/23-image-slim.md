# 23 — Сокращение Docker-образа

> Промпт для радикального уменьшения размера Python-образа с 1+ ГБ до ~120 МБ.

---

## Промпт

```
Ты — эксперт по оптимизации Docker-образов Python-сервисов.
Цель: уменьшить размер приложенного образа под production.

Стратегия (применяй в таком порядке):

1. **Multi-stage**: вынеси build-deps в builder, в runtime — только venv + код.
2. **Base образ**: выбери по возрастающей агрессивности:
   - python:3.13-slim (~150 МБ)
   - python:3.13-alpine (внимание: musl, не все wheels)
   - gcr.io/distroless/python3-debian12:nonroot (~50 МБ)
   - cgr.dev/chainguard/python:latest (лучший в 2026)
3. **pip → uv**: установка в 10-100× быстрее.
4. **BuildKit cache mounts** для uv/pip-кэша.
5. **Squash layers**: объединяй RUN и чисти кэши в том же слое.
6. **Чистка**:
   - apt-get clean && rm -rf /var/lib/apt/lists/*
   - __pycache__, *.pyc вырезать (или PYTHONDONTWRITEBYTECODE=1 + UV_COMPILE_BYTECODE=1 выборочно).
   - Удалить тесты и docs из установленных пакетов.
7. **.dockerignore**: исключи .git, .venv, tests, docs, *.md.
8. **Wheel-стратегия**: определи, какие пакеты тянут wheels (numpy/torch/lxml) и не нужны ли onnx-версии вместо полных.
9. **Анализ dive**: укажи топ-3 самых тяжёлых слоёв и что в них.

Дано:
- Текущий Dockerfile.
- Текущий размер образа (docker images).
- pyproject.toml/requirements.txt.

Формат ответа:
1. Диагноз: что жрёт место (топ-3 слоёв).
2. Новый Dockerfile (с комментариями объясняющими каждый шаг).
3. Новый .dockerignore.
4. Ожидаемый размер + сравнение.
5. Риски (alpine/musl, distroless без shell, etc).

--- DOCKERFILE START ---
{paste your Dockerfile here}
--- DOCKERFILE END ---

--- PYPROJECT START ---
{paste pyproject.toml here}
--- PYPROJECT END ---
```

## Связанные материалы

- [Курс по контейнерам — Multi-stage](../containers-course.md#урок-04--multi-stage-для-python)
- [Distroless и chainguard](../containers-course.md#урок-06--distroless-и-chainguard)
