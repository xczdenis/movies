#!/bin/sh
set -e

if [ "x$COMPOSE_MODE" = 'xon' ]; then
    echo "\033[94mCOMPOSE_MODE is on\033[00m"
    /scripts/wait-dependencies.sh
    echo "\033[01;32mAll services is up!\033[00m"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

/scripts/start.sh

exec "$@"
