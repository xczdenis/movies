FROM app-search-img

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

ARG HOME_DIR=/app
WORKDIR $HOME_DIR

RUN poetry config virtualenvs.create false \
    && poetry install --only tests

COPY ./search/docker/development/tests/scripts /scripts
RUN chmod -R 777 /scripts

ENTRYPOINT ["/scripts/entrypoint.sh"]
