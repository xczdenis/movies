FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DJANGO_ENV=development

ARG HOME_DIR=/app
WORKDIR $HOME_DIR

COPY ./adminpanel/docker/wait-for-it.sh /wait-for-it.sh
RUN chmod a+x /wait-for-it.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev=3.9.2-3 \
        libpq-dev=13.7-0+deb11u1 \
        build-essential=12.9 \
    && pip install --no-cache-dir poetry==1.2.0rc2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /
RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY ./adminpanel/docker/local/django/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# COPY ./adminpanel /adminpanel1

# ENTRYPOINT ["/entrypoint.sh"]