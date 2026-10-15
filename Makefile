build:
	docker compose --env-file .env/.env.$(env) build

up:
	docker compose --env-file .env/.env.$(env) up -d

down:
	docker compose --env-file .env/.env.$(env) down

createsuperuser:
	docker compose --env-file .env/.env.$(env) exec web python manage.py createsuperuser
init:
	python3 scripts/init_project.py

lint:
	poetry run ruff check .
	poetry run ruff format --check .

format:
	poetry run ruff check --fix .
	poetry run ruff format .

test: test-unit test-integration test-e2e

test-unit:
	poetry run pytest -m unit
	yarn test:unit

test-integration:
	poetry run pytest -m integration
	yarn test:integration

test-e2e:
	yarn test:e2e
