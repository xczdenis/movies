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
    logger.debug("Create elasticsearch indexes")
    for index, path_to_scheme in indexes.items():
        if not es_connection.indices.exists(index=index):
            logger.debug("Create elasticsearch index '%s'" % index)
            try:
                with open(path_to_scheme) as f:
                    try:
                        schema = json.load(f)
                    except Exception as e:
                        logger.error(e)
                        raise e
                    es_connection.indices.create(index=index, body=schema)
                    logger.debug("Elasticsearch index '%s' created successfully" % index)
            except FileNotFoundError:
                logger.error(
                    "{index} index schema file not found ({path})".format(index=index, path=path_to_scheme)
                )
        else:
            logger.debug("Elasticsearch index '%s' already exists" % index)
