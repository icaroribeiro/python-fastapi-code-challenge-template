from enum import Enum


class SalespersonType(str, Enum):
    PRODUCER = "producer"
    AFFILIATE = "affiliate"

    def to_integer(self) -> int:
        if self.value == self.PRODUCER:
            return 1
        if self.value == self.AFFILIATE:
            return 2
