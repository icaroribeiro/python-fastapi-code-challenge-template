from unittest.mock import MagicMock

import pytest
from faker import Faker
from src.domain.repository.transaction import TransactionRepository
from src.service.transaction import TransactionService


class TestTransactionServiceFixtures:
    @pytest.fixture
    def fake(self) -> Faker:
        return Faker()

    @pytest.fixture
    def file_path(self) -> str:
        return "/file.txt"

    @pytest.fixture
    def transaction_repository(self) -> TransactionRepository:
        return MagicMock(spec=TransactionRepository)

    @pytest.fixture
    def transaction_service(
        self,
        transaction_repository: TransactionRepository,
    ) -> TransactionService:
        return TransactionService(
            transaction_repository=transaction_repository,
        )

    # def _build_file_content_from_transactions(
    #     self, file_id: str, line: str
    # ) -> Transaction:
    #     transaction = Transaction()
    #     transaction.id = str(uuid4())
    #     transaction.type = (
    #         self._validate_numeric_string(
    #             field_name="type", line_number=line_number, value=line[0]
    #         ),
    #     )
    #     transaction.date = (
    #         self._validate_datetime_string(
    #             field_name="date", line_number=line_number, value=line[1:26]
    #         ),
    #     )
    #     transaction.product = line[26:56].rstrip(" ")
    #     transaction.value = (
    #         float(
    #             "{:.2f}".format(
    #                 self._validate_numeric_string(
    #                     field_name="value",
    #                     line_number=line_number,
    #                     value=line[56:66],
    #                 )
    #                 / 100.0
    #             )
    #         ),
    #     )
    #     transaction.salesperson = line[66:86].rstrip(" ")
    #     transaction.file_id = file_id
    #     return transaction
