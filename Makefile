run-main:
	poetry run python src/fig_data_challenge/main.py
test:
	poetry run pytest

setup:
	poetry install
	poetry run pre-commit install

makemigration:
	alembic revision

migrate:
	alembic upgrade head