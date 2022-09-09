from fastapi import Query
from pydantic import BaseModel, Field


class PaginateModel(BaseModel):
    page_size: int = Field(
        default=Query(10, alias="page[size]", description="Items amount on page", ge=1, le=100),
    )
    page: int = Field(
        default=Query(1, alias="page[number]", description="Page number for pagination", ge=1),
    )


class SortModel(BaseModel):
    sort: str = Field(
        Query(
            "",
            description="Sorting fields (A comma-separated list of 'field'[:'direction(=asc|desc)]' pairs. "
            "Example: 'rating', or 'rating:desc')",
        ),
    )
