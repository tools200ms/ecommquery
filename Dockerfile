# ---------- Builder stage ----------
FROM python:3.13-slim AS builder

ENV POETRY_VERSION=2.2.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# System deps needed for building wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /app

# Copy only dependency files first (for caching)
COPY pyproject.toml poetry.lock ./

# Install prod dependencies only
RUN poetry install --only main --no-root

# ---------- Runtime stage ----------
FROM python:3.13-slim AS runtime
#ENV APP_NAME="ecommquery"

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./task/main.py main.py

# Copy application code
COPY ecommquery/ ecommquery/

COPY conf/ conf/

RUN touch stash.json && chown -R appuser:appuser stash.json
RUN mkdir -p logs && chown -R appuser:appuser logs

USER appuser

CMD ["python", "main.py"]
