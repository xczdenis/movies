ARG env=${ENVIRONMENT:-production}

FROM docker.io/elastic/elasticsearch:7.7.0 as builder

FROM builder as development
EXPOSE ${EXPOSE_ELASTIC_PORT:-9200}

FROM builder as production

FROM ${env}
