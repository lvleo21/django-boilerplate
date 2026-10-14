#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

postgres_ready() {
python << END
import os
import sys

import psycopg2

url = os.environ.get("DATABASE_URL", "")

# Sem DATABASE_URL de Postgres o Django usa SQLite, então não há o que esperar
if not url.startswith("postgres"):
    sys.exit(0)

try:
    psycopg2.connect(url)
except Exception as e:
    print(f"Unexpected error: {e}")
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