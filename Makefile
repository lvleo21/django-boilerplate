build:
	docker compose --env-file .env/.env.$(environment) build

up:
	docker compose --env-file .env/.env.$(environment) up -d

down:
	docker compose --env-file .env/.env.$(environment) down