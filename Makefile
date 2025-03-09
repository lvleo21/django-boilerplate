build:
	docker-compose -f docker-compose.yml up --build

down:
	docker-compose -f docker-compose.yml down

hard-down:
 	docker-compose -f docker-compose.yml down --volumes --remove-orphans

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

run:
	poetry run python manage.py runserver 0.0.0.0:8000