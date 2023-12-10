import os
from datetime import datetime
from typing import List, Optional

from fastapi.logger import logger

from src.domain.model.pagination import Pagination
from src.domain.model.transaction import Transaction
from src.domain.repository.transaction import TransactionRepository
from src.infrastructure import application_settings
from src.utils.api_exceptions import InvalidFileFormatException, ServerErrorException
from src.utils.pagination import build_pagination


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
    ):
        self.transaction_repository = transaction_repository

    async def save_transactions(self, in_file_path: str) -> List[Transaction]:
        transactions = []

        file_id = (os.path.basename(in_file_path).split("/")[-1])[16:52]

        max_line_length = int(application_settings.max_line_length)

        with open(file=in_file_path, mode="rb") as out_file:
            for line_number, line in enumerate(out_file):
                decoded_line = line.decode("utf-8").strip()

                if len(decoded_line) > max_line_length:
                    logger.warning(
                        msg=f"Invalid line length={len(decoded_line)} at line={line_number}"
                    )
                    raise InvalidFileFormatException(
                        extra=f"Invalid line length={len(decoded_line)} at line={line_number}"
                    )
                elif len(decoded_line) < max_line_length:
                    decoded_line = self._append_empty_string_to_line(
                        max_line_length=max_line_length, line=decoded_line
                    )

                transactions.append(
                    self._build_transaction(
                        file_id=file_id, line_number=line_number, line=decoded_line
                    )
                )
        return await self.transaction_repository.create_transactions(
            transactions=transactions
        )

    async def list_transactions(
        self, page_number: int, page_size: int
    ) -> Optional[Pagination]:
        pagination = Pagination(page_number=page_number, page_size=page_size)

        offset = pagination.get_offset()

        limit = pagination.get_page_size()

        total_records = await self.transaction_repository.count_transactions()

        if not total_records:
            logger.error(msg="Total of transaction records is None")
            raise ServerErrorException(extra="Total of transaction records is None")

        records = await self.transaction_repository.read_transactions(
            offset=offset, limit=limit
        )
        if not records:
            logger.error("List of transaction records is None")
            raise ServerErrorException("List of transaction records is None")

        return build_pagination(
            pagination=pagination, total_records=total_records, records=records
        )

    async def list_transaction_balances_by_salesperson_type(
        self, salesperson_type: int, page_number: int, page_size: int
    ) -> Optional[Pagination]:
        pagination = Pagination(page_number=page_number, page_size=page_size)
        offset = pagination.get_offset()
        limit = pagination.get_page_size()

        total_records = await self.transaction_repository.count_transaction_balances_by_salesperson_type(
            salesperson_type=salesperson_type
        )

        if not total_records:
            logger.error(
                "Total of transaction balances by salesperson type records is None"
            )
            raise ServerErrorException(
                "Total of transaction balances by salesperson type records is None"
            )

        records = await self.transaction_repository.read_transaction_balances_by_salesperson_type(
            salesperson_type=salesperson_type,
            offset=offset,
            limit=limit,
        )
        if not records:
            logger.error(
                "List of transaction balances by salesperson type records is None"
            )
            raise ServerErrorException(
                "List of transaction balances by salesperson type records is None"
            )

        return build_pagination(
            pagination=pagination, total_records=total_records, records=records
        )

    @staticmethod
    def _append_empty_string_to_line(max_line_length: int, line: str) -> str:
        empty_string = ""
        number_of_chars = range(max_line_length - len(line))
        for _ in number_of_chars:
            line = line + empty_string
        return line

    def _build_transaction(
        self, file_id: str, line_number: int, line: str
    ) -> Transaction:
        transaction = Transaction()
        transaction.type = self._validate_numeric_string(
            field_name="type", line_number=line_number, value=line[0]
        )
        transaction.date = self._validate_datetime_string(
            field_name="date", line_number=line_number, value=line[1:26]
        )
        transaction.product = line[26:56].rstrip(" ")
        transaction.value = float(
            "{:.2f}".format(
                self._validate_numeric_string(
                    field_name="value",
                    line_number=line_number,
                    value=line[56:66],
                )
                / 100.0
            )
        )
        transaction.salesperson = line[66:86].rstrip(" ")
        transaction.file_id = file_id
        return transaction

    @staticmethod
    def _validate_numeric_string(field_name: str, line_number: int, value: str) -> int:
        try:
            return int(value.lstrip("0"))
        except (Exception,):
            logger.warning(
                msg=f"Invalid value={value} of field={field_name} at line={line_number}"
            )
            raise InvalidFileFormatException(
                extra=f"Invalid value={value} of field={field_name} at line={line_number}"
            )

    @staticmethod
    def _validate_datetime_string(
        field_name: str, line_number: int, value: str
    ) -> datetime:
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        try:
            return datetime.strptime(value, date_format).replace(tzinfo=None)
        except (Exception,):
            logger.warning(
                msg=f"Invalid value={value} of field={field_name} at line={line_number}"
            )
            raise InvalidFileFormatException(
                extra=f"Invalid value={value} of field={field_name} at line={line_number}"
            )
