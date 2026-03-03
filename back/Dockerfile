# ============================================
# Stage 1 : Builder — installe les dépendances
# ============================================
FROM python:3.12-slim AS builder

LABEL maintainer="ines.marouani69@gmail.com"
LABEL version="1.0"
LABEL description="FastAPI backend - Accident Severity"

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Dépendances Python (cache Docker)
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

# ============================================
# Stage 2 : Runtime — image finale légère
# ============================================
FROM python:3.12-slim AS runtime

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Dépendances runtime uniquement (pas build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier uniquement le venv buildé depuis le stage builder
COPY --from=builder /app/.venv /app/.venv

# Copier le code
COPY app /app/app
COPY models_trained /app/models_trained

# Sécurité : user non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Runtime
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
