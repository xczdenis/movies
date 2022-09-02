import json

from elasticsearch import Elasticsearch
from loguru import logger


def create_es_indexes(es_connection: Elasticsearch, indexes: dict):
    """
    Create indexes in Elasticsearch.

    :param es_connection: instance of Elasticsearch
    :param indexes: dict[name_of_index: path_to_index_scheme]

    :return: None
    """
    for index, path_to_scheme in indexes.items():
        if not es_connection.indices.exists(index=index):
            with open(path_to_scheme) as f:
                try:
                    schema = json.load(f)
                except Exception as e:
                    logger.error(e)
                    raise e
                es_connection.indices.create(index=index, body=schema)
