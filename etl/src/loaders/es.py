from dataclasses import dataclass

from elasticsearch import Elasticsearch
from loaders.interface import ILoader
from loguru import logger


@dataclass
class ElasticsearchLoader(ILoader):
    connection: Elasticsearch

    def load(self, data) -> bool:
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

        if data and not success and resp:
            reason = ""
            index = "unknown"
            for item in resp.get("items"):
                try:
                    reason = item["index"]["error"]["reason"]
                except KeyError:
                    pass

                try:
                    index = item["index"]["_index"]
                except KeyError:
                    pass

                if reason != "":
                    logger.error(
                        "Unable to insert data into elasticsearch. "
                        "Index: {index}; "
                        "Error: {e}".format(index=index, e=reason)
                    )
                    break

        return success
