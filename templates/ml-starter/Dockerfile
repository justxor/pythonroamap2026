# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv==0.5.*
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

FROM python:3.13-slim
WORKDIR /app

# non-root user
RUN groupadd -r ml && useradd -r -g ml ml

COPY --from=builder /app/.venv /app/.venv
COPY --chown=ml:ml src ./src
COPY --chown=ml:ml conf ./conf

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

USER ml
EXPOSE 3000
CMD ["bentoml", "serve", "ml_starter.serve:svc", "--port", "3000", "--host", "0.0.0.0"]
