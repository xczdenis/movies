#!/bin/sh
set -e

# Postgres
echo "\033[94mWaiting the service: \033[97mpostgres (url=$POSTGRES_HOST:$POSTGRES_PORT)\033[00m"
/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT --
echo "\033[01;32mPostgres is up!\033[00m"

exec "$@"
