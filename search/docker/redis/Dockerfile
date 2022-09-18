ARG env=${ENVIRONMENT:-production}

FROM redis:7-alpine as builder

FROM builder as development
EXPOSE ${EXPOSE_REDIS_PORT:-6379}

FROM builder as production

FROM ${env}
