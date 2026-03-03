# ============================================
# Stage 1 : Builder
# ============================================
FROM python:3.12-slim AS builder

LABEL maintainer="ines.marouani69@gmail.com"
LABEL version="1.0"
LABEL description="Python Frontend (Dash)"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

# ============================================
# Stage 2 : Runtime
# ============================================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY src /app/src
COPY data /app/data

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8050

HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8050 || exit 1

CMD ["python", "src/app.py"]
