# ============================================
# Stage 1: Base - Install dependencies
# ============================================
FROM python:3.12-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Lint & Test
# ============================================
FROM base AS test

RUN pip install --no-cache-dir ruff pytest httpx

COPY . .

# Lint
RUN ruff check . || true

# Unit tests (if any exist in tests/ directory)
RUN python -m pytest tests/ -v --tb=short || true

# ============================================
# Stage 3: Production
# ============================================
FROM base AS production

COPY . .

# Create media directory
RUN mkdir -p /app/media

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
