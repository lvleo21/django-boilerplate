#!/bin/sh

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# exits if any of your variables is not set
set -o nounset

# Deriva as variáveis POSTGRES_* da DATABASE_URL (postgres://user:password@host:port/name)
url="${DATABASE_URL:?DATABASE_URL não definida}"
rest="${url#*://}"
userinfo="${rest%%@*}"
hostpath="${rest#*@}"
dbpath="${hostpath#*/}"

export POSTGRES_USER="${userinfo%%:*}"
export POSTGRES_PASSWORD="${userinfo#*:}"
export POSTGRES_DB="${dbpath%%\?*}"

exec docker-entrypoint.sh "$@"
