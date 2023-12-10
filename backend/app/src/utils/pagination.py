import math
from typing import Any, List, Optional

from src.domain.model.pagination import Pagination


def build_pagination(
    pagination: Pagination, total_records: int, records: List[Any]
) -> Pagination:
    pagination.total_records = total_records

    pagination.total_pages = math.ceil(
        float(total_records) / float(pagination.get_page_size())
    )

    pagination.records = [
        record.to_dict(rules=("-created_at", "-updated_at"))
        if hasattr(record, "to_dict")
        else record
        for record in records
    ]

    if (pagination.page_number * pagination.page_size) < pagination.total_records:
        next_page = f"page_number={pagination.page_number + 1}"
        pagination.next_page = next_page
    else:
        pagination.next_page = None

    return pagination


def build_next_page(
    url_path: str, url_query: str, next_page: Optional[str]
) -> Optional[str]:
    if not next_page:
        return None

    page_number_query = f"{next_page}"

    query_values = []
    if len(url_query) > 0:
        for value in url_query.split("&"):
            if not value.startswith("page_number"):
                query_values.append(value)

    if len(query_values) > 0:
        page_number_query = page_number_query + "&"

    return f"{url_path}?{page_number_query}" + "&".join(query_values)
