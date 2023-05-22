#!/bin/sh
. ./scripts/logger.sh


if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    log_info "Run in development mode"
    python src/"${ADMINPANEL_PKG_NAME}"/manage.py runserver "${ADMINPANEL_APP_HOST}":"${ADMINPANEL_APP_PORT}"
else
    echo "\033[94mRun in production mode mode\033[00m"
    gunicorn -b "${ADMINPANEL_APP_HOST}":"${ADMINPANEL_APP_PORT}" config.wsgi:application
fi
