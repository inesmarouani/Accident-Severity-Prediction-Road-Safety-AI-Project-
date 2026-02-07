# ============================================
# Image de base
# ============================================
FROM python:3.12-slim

LABEL maintainer="ines.marouani69@gmail.com"
LABEL version="1.0"
LABEL description="Python Frontend (Dash)"

# ============================================
# Dépendances système minimales
# ============================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# ============================================
# Workdir
# ============================================
WORKDIR /app

# ============================================
# Dépendances Python (cache Docker)
# ============================================
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

# ============================================
# Copier le code frontend
# ============================================
COPY src /app/src
COPY data /app/data

# ============================================
# Sécurité : user non-root
# ============================================
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# ============================================
# Runtime
# ============================================
EXPOSE 8050

HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8050 || exit 1

CMD ["uv", "run", "python", "src/app.py"]
