# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --no-dev --frozen || uv sync --no-dev

COPY src ./src
RUN uv pip install --system --no-deps -e .

FROM python:3.13-slim AS runtime

RUN useradd -m -u 10001 app
WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app
EXPOSE 8000

CMD ["uvicorn", "async_starter.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop"]
