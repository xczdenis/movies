from etl.db_clients.base import DatabaseClient


class DatabaseClientContextManager:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    def __enter__(self):
        self.db_client.connect()
        return self.db_client

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.db_client.close()
