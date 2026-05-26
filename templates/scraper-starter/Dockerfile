# Multi-stage Docker build for scraper-starter (Python 3.13 + uv)

FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1

# Install deps first for cache
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system .

# Copy source
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system .


# Runtime stage
FROM python:3.13-slim AS runtime

RUN useradd -m -u 1001 scraper
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/scraper /usr/local/bin/scraper
COPY src ./src

RUN mkdir -p /app/data && chown -R scraper:scraper /app
USER scraper

ENTRYPOINT ["scraper"]
CMD ["--help"]
