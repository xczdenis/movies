from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Type

from db.constants import LOOKUP_SEP
from db.interface import IAsyncDB
from db.shared import Filter, Term
from elasticsearch import AsyncElasticsearch, NotFoundError
from loguru import logger
from models.mixins import BaseModelWithMeta
from pydantic import BaseModel


class QueryTypes:
    MATCH = "match"


class OccurrenceTypes:
    MUST = "must"
    FILTER = "filter"
    SHOULD = "should"
    MUST_NOT = "must_not"


@dataclass
class Query:
    field: str
    query: str | Query = ""
    operator: str = Term.AND
    query_type: str = QueryTypes.MATCH

    def get_query(self, result_query: dict = None) -> dict:
        result_query = result_query or {}
        if isinstance(self.query, Query):
            result_query.update(
                {
                    "nested": {
                        "path": self.field,
                        "query": self.query.get_query(result_query),
                    }
                }
            )
        else:
            result_query.update(
                {
                    self.query_type: {
                        self.field: {"query": self.query, "operator": self.operator, "fuzziness": "AUTO"}
                    }
                }
            )

        return result_query
        # return {
        #     self.query_type: {
        #         self.field: {"query": self.query, "operator": self.operator, "fuzziness": "AUTO"}
        #     }
        # }


@dataclass
class BooleanClause:
    occurrence_type: str = OccurrenceTypes.MUST
    queries: list[Query] = field(default_factory=list)

    def get_queries(self):
        return {self.occurrence_type: [query.get_query() for query in self.queries]}


@dataclass
class BooleanQuery:
    boolean_clauses: list[BooleanClause] = field(default_factory=list)

    def get_query(self) -> dict:
        query_boolean_clauses = {}
        for boolean_clause in self.boolean_clauses:
            query_boolean_clauses.update(boolean_clause.get_queries())
        return {"query": {"bool": query_boolean_clauses}}


# async def make_request_body_from_kwargs(**kwargs) -> dict:
#     filter = kwargs.get("filter")
#     request_body = None
#     if filter:
#         boolean_clause = BooleanClause()
#         for field_name, value in filter.items():
#             if value:
#                 lookups = field_name.split(LOOKUP_SEP)
#                 if len(lookups) == 1:
#                     boolean_clause.queries.append(Query(field=field_name, query=value))
#                 else:
#                     nested_query = Query(field=".".join(lookups), query=value)
#                     boolean_clause.queries.append(Query(field=lookups[0], query=nested_query))
#
#         if len(boolean_clause.queries) > 0:
#             request_body = BooleanQuery([boolean_clause]).get_query()
#
#     return request_body


def get_occurrence_type_by_term(term: str):
    occurrence_type = OccurrenceTypes.MUST
    if term == Term.OR:
        occurrence_type = OccurrenceTypes.SHOULD
    return occurrence_type


async def make_request_body_from_kwargs(**kwargs) -> dict:
    filter: Filter = kwargs.get("filter")
    request_body = None
    if filter and filter.lookups:
        boolean_clause = BooleanClause(get_occurrence_type_by_term(filter.term))
        for field_name, value in filter.lookups.items():
            if value:
                lookups = field_name.split(LOOKUP_SEP)
                if len(lookups) == 1:
                    boolean_clause.queries.append(Query(field=field_name, query=value))
                else:
                    nested_query = Query(field=".".join(lookups), query=value)
                    boolean_clause.queries.append(Query(field=lookups[0], query=nested_query))

        if len(boolean_clause.queries) > 0:
            request_body = BooleanQuery([boolean_clause]).get_query()

    return request_body


async def get_index_from_model(model: Type[BaseModelWithMeta]) -> Optional[str]:
    index = ""
    try:
        index = model.Meta.index
    except Exception as e:
        logger.error(e)

    if not index:
        logger.info(
            "Unable to get index from model {model}. "
            "Maybe you forget to add class Meta into model {model}.".format(model=model.__name__)
        )

    return index


async def make_model_instance_from_doc(model: Type[BaseModel], doc: dict) -> Optional[BaseModel]:
    source = doc.get("_source")
    if source and isinstance(source, dict):
        _id = source.get("id")
        if _id:
            del source["id"]
            return model(id=doc["_id"], **source)
    return None


class ElasticDB(IAsyncDB):
    def __init__(self, host: str, port: int):
        self.client: AsyncElasticsearch = AsyncElasticsearch(hosts=[f"http://{host}:{port}"])

    async def get(self, model: Type[BaseModel], id: str, **kwargs) -> Optional[BaseModel]:
        model_instance = None
        index = await get_index_from_model(model)
        if index:
            doc_type = kwargs.get("doc_type")
            params = kwargs.get("params")
            headers = kwargs.get("headers")

            try:
                doc = await self.client.get(
                    index=index, id=id, doc_type=doc_type, params=params, headers=headers
                )
            except NotFoundError as e:
                logger.debug(e)
            else:
                model_instance = await make_model_instance_from_doc(model, doc)

        return model_instance

    async def search(self, model: Type[BaseModel], **kwargs) -> tuple[int, list[BaseModel]]:
        page_size = kwargs.get("page_size", 10)
        page = kwargs.get("page", 1)

        total = 0
        objects = []

        index = await get_index_from_model(model)
        if index:
            request_body = await make_request_body_from_kwargs(**kwargs)
            resp = await self.execute_query(
                index=index,
                query="search",
                body=request_body,
                params={
                    "size": page_size,
                    "from": (page - 1) * page_size,
                    "sort": kwargs.get("sort", ""),
                },
            )
            if resp:
                try:
                    total = resp["hits"]["total"]["value"]
                    docs = resp["hits"]["hits"]
                except Exception as e:
                    logger.error(e)
                else:
                    for doc in docs:
                        objects.append(await make_model_instance_from_doc(model, doc))

        return total, objects

    async def count(self, model: Type[BaseModel], **kwargs) -> int:
        resp = {}
        index = await get_index_from_model(model)
        if index:
            request_body = await make_request_body_from_kwargs(**kwargs)
            resp = await self.execute_query(index=index, query="count", body=request_body)

        return resp.get("count", 0)

    async def execute_query(
        self, index: str, query: str, body: Optional[dict] = None, params: Optional[dict] = None
    ) -> Optional[dict]:
        resp = None
        if index:
            try:
                resp = await self.client.transport.perform_request(
                    "POST",
                    f"/{index}/_{query}",
                    params=params,
                    body=body,
                )
            except NotFoundError as e:
                logger.debug(e)

        return resp

    async def close(self):
        await self.client.close()
