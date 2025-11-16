#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except Exception as e:
    print(f"Unexpected error: {e}")
    print(f"Database connection details:")
    print(f"  dbname: {'${DB_NAME}'}")
    print(f"  user: {'${DB_USER}'}")
    print(f"  password: {'${DB_PASSWORD}'}")
    print(f"  host: {'${DB_HOST}'}")
    print(f"  port: {'${DB_PORT}'}")
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

exec "$@"