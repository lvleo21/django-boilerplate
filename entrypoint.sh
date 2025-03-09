#!/bin/sh



# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     until pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
#         sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# Dependencies
if [ "$ENVIRONMENT" != "local" ]; then
    echo "Installing production dependencies"
    poetry install
else
    echo "Installing development dependencies"
    poetry install --with dev
fi

# Makemigrations
if [ "$ENVIRONMENT" = "local" ]; then
    echo "Running makemigrations"
    poetry run python manage.py makemigrations
fi

# Apply database migrations
poetry run python manage.py migrate

# Collect Static
if [ "$ENVIRONMENT" = "local" ]; then
    echo "Collecting static files"
    poetry run python manage.py collectstatic --noinput
fi

# Running server
if [ "$ENVIRONMENT" = "local" ]; then
    echo "Starting development server"
    exec poetry run python manage.py runserver 0.0.0.0:8000
else
    echo "Starting production server"
    exec poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi

exec "$@"
