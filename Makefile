build:
	docker compose --env-file .env/.env.$(env) build

up:
	docker compose --env-file .env/.env.$(env) up -d

down:
	docker compose --env-file .env/.env.$(env) down

createsuperuser:
	docker compose --env-file .env/.env.$(env) exec web python manage.py createsuperuser