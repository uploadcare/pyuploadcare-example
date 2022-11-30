format:
	poetry run black .
	poetry run isort .

lint:
	poetry run black --check .
	poetry run isort --check .
	poetry run flake8 .
	poetry run mypy --namespace-packages --show-error-codes ./app
