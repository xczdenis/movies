#!/bin/sh
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind $SEARCH_APP_HOST:$SEARCH_APP_PORT
