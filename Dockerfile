# python-alpine with uv
FROM ghcr.io/astral-sh/uv:python3.14-alpine3.23

WORKDIR /app

COPY app/ /app/
COPY pyproject.toml /app/

RUN uv sync --no-dev --no-install-project

EXPOSE 8000
ENTRYPOINT ["/app/start.sh"]
