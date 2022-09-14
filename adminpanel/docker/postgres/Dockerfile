ARG env=${ENVIRONMENT:-production}

FROM postgres:14.3-alpine as builder

COPY ./adminpanel/docker/postgres/init /docker-entrypoint-initdb.d/

FROM builder as development
EXPOSE 5432

FROM builder as production

FROM ${env}
