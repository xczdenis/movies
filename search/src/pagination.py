import math
from typing import Generic, Optional, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    count: int
    total_pages: int = Field(default=1)
    next: Optional[int] = Field(default=None)
    prev: Optional[int] = Field(default=None)
    results: list[T]


def paginate(count: int, page_size: int, current_page: int, results=list) -> Page:
    total_pages = 0
    if count > 0:
        total_pages = math.ceil(count / page_size)

    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = None
    if current_page and current_page > 1:
        prev_page = current_page - 1
        if prev_page > total_pages:
            prev_page = total_pages
    return Page(count=count, total_pages=total_pages, next=next_page, prev=prev_page, results=results)
