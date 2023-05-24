FROM python:3.11-slim

RUN pip install elasticsearch[async]

COPY ../docker/tests/scripts ./scripts
COPY ./docker/tests/scripts ./scripts
RUN chmod -R 777 ./scripts

ENTRYPOINT ["./scripts/entrypoint.sh"]
