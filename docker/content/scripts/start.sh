#!/bin/sh
. ./scripts/logger.sh

. ./.venv/bin/activate

#!/bin/sh
if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    log_info "Run in development mode"
    python ./src/"${CONTENT_PKG_NAME}"/main.py
else
    log_info "Run in production mode"
    gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "${CONTENT_APP_HOST}":"${CONTENT_APP_PORT}"
fi
