from pydantic import BaseModel

PAGE_NUMBER_DESCRIPTION = "The number of the page"

PAGE_SIZE_DESCRIPTION = "The size of the page"


class BasePaginationResponse(BaseModel):
    page_number: int
    page_size: int
    total_pages: int
    total_records: int
    next_page: str
