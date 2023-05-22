PAGINATED_RESPONSE_STRUCTURE = {
    "count": int,
    "total_pages": int,
    "next": int | None,
    "prev": int | None,
    "results": list,
}
