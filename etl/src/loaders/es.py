from dataclasses import dataclass

from elasticsearch import Elasticsearch
from loaders.interface import ILoader


@dataclass
class ElasticsearchLoader(ILoader):
    connection: Elasticsearch

    def load(self, data):
        success = True
        if data:
            resp = self.connection.bulk(body=data)
            success = not resp["errors"]

        return success
