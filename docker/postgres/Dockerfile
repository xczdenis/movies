ARG img=postgres:14.3-alpine

FROM ${img}

COPY ./docker/postgres/init /docker-entrypoint-initdb.d/
COPY ./docker/scripts /scripts

