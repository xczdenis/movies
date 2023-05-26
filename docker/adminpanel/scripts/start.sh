#!/bin/sh
. ./scripts/logger.sh


if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    log_info "Run in development mode"
    python src/"${ADMINPANEL_PKG_NAME}"/manage.py runserver "${ADMINPANEL_APP_HOST}":"${ADMINPANEL_APP_PORT}"
else
    log_info "Run in production mode"
    gunicorn -b "${ADMINPANEL_APP_HOST}":"${ADMINPANEL_APP_PORT}" src."${ADMINPANEL_PKG_NAME}".config.wsgi:application
fi
