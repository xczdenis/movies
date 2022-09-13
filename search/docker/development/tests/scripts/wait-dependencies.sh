#!/bin/sh
set -e

# Redis
echo "\033[94mWaiting the service: \033[97mRedis (url=$REDIS_HOST:$REDIS_PORT)\033[00m"
/wait-for-it.sh $REDIS_HOST:$REDIS_PORT --
echo "\033[01;32mRedis is up!\033[00m"

# Elasticsearch
echo "\033[94mWaiting the service: \033[97mElasticsearch (url=$ELASTIC_HOST:$ELASTIC_PORT)\033[00m"
/wait-for-it.sh $ELASTIC_HOST:$ELASTIC_PORT --
echo "\033[01;32mElasticsearch is up!\033[00m"

# Search-APP
echo "\033[94mWaiting the service: \033[97mSearch-APP (url=$SEARCH_APP_HOST:$$SEARCH_APP_PORT)\033[00m"
/wait-for-it.sh $SEARCH_APP_HOST:$SEARCH_APP_PORT --
echo "\033[01;32mSearch-APP is up!\033[00m"

exec "$@"
