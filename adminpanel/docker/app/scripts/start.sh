#!/bin/sh
if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    echo "\033[94mRun in development mode\033[00m"
    python manage.py runserver 0.0.0.0:8000
else
    echo "\033[94mRun in production mode mode\033[00m"
    gunicorn -b 0.0.0.0:8000 config.wsgi:application
fi
