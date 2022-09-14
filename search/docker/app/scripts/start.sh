#!/bin/sh
if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    echo "\033[94mRun in development mode\033[00m"
    python main.py
else
    echo "\033[94mRun in production mode mode\033[00m"
    gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind $SEARCH_APP_HOST:$SEARCH_APP_PORT
fi
