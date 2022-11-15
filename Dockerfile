FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false || true && poetry install

EXPOSE 8000
ENTRYPOINT /app/start.sh
