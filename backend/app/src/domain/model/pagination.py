from typing import Any, List

from pydantic import BaseModel

from src.infrastructure import application_settings


class Pagination(BaseModel):
    page_number: int = 0
    page_size: int = 0
    total_pages: int = None
    total_records: int = None
    records: List[Any] = None
    next_page: str = None

    def get_offset(self) -> int:
        return (self.get_page_number() - 1) * self.get_page_size()

    def get_page_number(self) -> int:
        if self.page_number <= 0:
            self.page_number = int(application_settings.minimum_page_number)

        return self.page_number

    def get_page_size(self) -> int:
        if self.page_size <= 0:
            self.page_size = int(application_settings.minimum_page_size)

        if self.page_size > 100:
            self.page_size = int(application_settings.maximum_page_size)

        return self.page_size
