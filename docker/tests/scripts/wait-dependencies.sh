#!/bin/sh
set -e

. ./scripts/colors.sh
. ./scripts/logger.sh
. ./scripts/helpers.sh


check_service "Redis" "${REDIS_HOST}" "${REDIS_PORT}"
check_service "Elasticsearch" "${ELASTIC_HOST}" "${ELASTIC_PORT}"

log_success "All services is up!"
echo ""

exec "$@"
