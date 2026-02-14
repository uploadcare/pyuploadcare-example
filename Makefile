format:
	uv run black .
	uv run isort .

lint:
	uv run black --check .
	uv run isort --check .
	uv run flake8 .
	uv run mypy --namespace-packages --show-error-codes ./app

docker-up:
	docker compose up
