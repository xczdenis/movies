from celery import Celery

from etl.config.settings import redis_config

celery_app = Celery(
    "etl",
    broker="redis://{host}:{port}/0".format(host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT),
    include=["etl.periodic_tasks"],
)

celery_app.conf.beat_schedule = {
    "sqlite_to_pg": {"task": "etl.periodic_tasks.start_etl_sqlite_to_pg", "schedule": 30.0},
}

if __name__ == "__main__":
    celery_app.start()
