from dataclasses import dataclass

from loguru import logger

from etl.db_clients.es import ESClient
from etl.loaders.base import Loader


@dataclass
class ElasticsearchLoader(Loader):
    db_client: ESClient

    def load(self, data, **kwargs) -> bool:
        success, resp = self.insert_to_db(data)

        if data and not success and resp:
            index, reason = self.get_index_end_error_reason(resp)
            if reason:
                logger.error(
                    "Unable to insert data into elasticsearch. "
                    "Index: {index}; "
                    "Error: {e}".format(index=index, e=reason)
                )

        return success

    def insert_to_db(self, data) -> tuple[bool, dict | None]:
        success = True
        resp = None
        if data:
            try:
                resp = self.connection.bulk(body=data)
            except Exception as e:
                success = False
                logger.error("Unable to insert data into elasticsearch: {e}".format(e=e))
            else:
                success = not resp["errors"]
                if success:
                    logger.info(
                        "The data was successfully uploaded to elasticsearch. "
                        "Row count: {row_count}".format(row_count=len(data) / 2)
                    )
        return success, resp

    @property
    def connection(self):
        return self.db_client.native_client

    @staticmethod
    def get_index_end_error_reason(resp: dict | None) -> tuple[str, str]:
        index = "unknown"
        reason = ""
        if resp:
            for item in resp.get("items"):
                try:
                    reason = item["index"]["error"]["reason"]
                except KeyError:
                    pass

                try:
                    index = item["index"]["_index"]
                except KeyError:
                    pass
        return index, reason
