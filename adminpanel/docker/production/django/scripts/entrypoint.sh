#!/bin/sh
set -e

if [ "x$COMPOSE_MODE" = 'xon' ]; then
    echo "\033[94mCOMPOSE_MODE is on\033[00m"
    /scripts/wait-dependencies.sh
    echo "\033[01;32mAll services is up!\033[00m"
fi

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
   python manage.py migrate --noinput
fi

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

exec "$@"
