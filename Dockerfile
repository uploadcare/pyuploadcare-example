FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY app/ /app/
COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --no-dev --no-install-project

EXPOSE 8000
ENTRYPOINT ["/app/start.sh"]
