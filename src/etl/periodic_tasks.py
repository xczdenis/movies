from etl.celery import celery_app
from etl.pg_to_es import load_data as load_data_from_pg_to_es
from etl.sqlite_to_pg import load_data as load_data_from_sqlite_to_pg


@celery_app.task
def start_etl_sqlite_to_pg():
    load_data_from_sqlite_to_pg()


@celery_app.task
def start_etl_pg_to_es():
    load_data_from_pg_to_es()
