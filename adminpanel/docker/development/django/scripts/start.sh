#!/bin/sh
set -e

if [ "x$COMPOSE_MODE" = 'xon' ]; then
    echo COMPOSE_MODE is on
    /wait-dependencies.sh
    echo Postgres is up!
fi

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
   python manage.py migrate --noinput
fi

python manage.py collectstatic --noinput

exec "$@"
