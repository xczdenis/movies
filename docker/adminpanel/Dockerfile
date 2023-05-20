ARG env=production
ARG img=python:3.11-slim
ARG work_dir=app
ARG pck_name

FROM ${img} as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

ARG env
ARG work_dir
ARG pck_name

WORKDIR ${work_dir}

FROM base as builder

COPY ./docker/scripts /scripts
RUN chmod -R 777 /scripts

COPY ./docker/${pck_name}/scripts /scripts
RUN chmod -R 777 /scripts

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        libpq-dev \
        build-essential \
    && pip install poetry==${POETRY_VERSION} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./

RUN mkdir -p /${work_dir}/src/${pck_name} && touch /${work_dir}/src/${pck_name}/__init__.py \
    && mkdir -p /${work_dir}/src/content && touch /${work_dir}/src/content/__init__.py \
    && mkdir -p /${work_dir}/src/etl && touch /${work_dir}/src/etl/__init__.py

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main,adminpanel


FROM base as final

COPY --from=builder /scripts /scripts
COPY --from=builder /${work_dir}/.venv ./.venv


FROM final as development


FROM final as production

COPY ./src/${pck_name} ./src/${pck_name}


FROM ${env}

ENTRYPOINT ["/scripts/entrypoint.sh"]
