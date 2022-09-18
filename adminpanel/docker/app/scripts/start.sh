#!/bin/sh
if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    echo "\033[94mRun in development mode\033[00m"
    python manage.py runserver $ADMINPANEL_APP_HOST:$ADMINPANEL_APP_PORT
else
    echo "\033[94mRun in production mode mode\033[00m"
    gunicorn -b $ADMINPANEL_APP_HOST:$ADMINPANEL_APP_PORT config.wsgi:application
fi
