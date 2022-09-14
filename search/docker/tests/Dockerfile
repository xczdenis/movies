ARG env=${ENVIRONMENT:-production}

FROM app-search-img as builder

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

ARG HOME_DIR=/app
WORKDIR $HOME_DIR

RUN poetry config virtualenvs.create false \
    && poetry install --only tests

COPY ./search/docker/tests/scripts /scripts
RUN chmod -R 777 /scripts

FROM builder as development

FROM builder as production
COPY ./search/src .

FROM ${env}

ENTRYPOINT ["/scripts/entrypoint.sh"]
