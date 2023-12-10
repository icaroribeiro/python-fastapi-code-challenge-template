from unittest.mock import mock_open, patch
from uuid import uuid4

from faker import Faker
from src.domain.repository.transaction import TransactionRepository
from src.service.transaction import TransactionService
from tests.src.domain.model.transaction_factory import TransactionFactory
from tests.src.service.transaction.test_transaction_service_fixtures import \
    TestTransactionServiceFixtures


class TestSaveTransaction(TestTransactionServiceFixtures):
    def test1(self):
        pass


#     def test_should_succeed_in_saving_transactions(
#         self,
#         file_path: str,
#         transaction_repository: TransactionRepository,
#         transaction_service: TransactionService,
#         fake: Faker,
#     ):
#         file_id = str(uuid4())
#         count = fake.pyint(min_value=1, max_value=1)
#         file_content = "\n".join(
#             "12022-01-15T19:20:30-03:00CURSO DE BEM-ESTAR            0000012750JOSE CARLOS"
#             for _ in range(count)
#         )
#
#         transactions = [TransactionFactory(file_id=file_id) for _ in range(count)]
#
#         transaction_repository.create_transactions.return_value = transactions
#
#         with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
#             result = transaction_service.save_transactions(file_path=file_path)
#
#             assert result == transactions
#             mock_file.asserefresh_token_called_with(file=file_path)
#             transaction_repository.create_transactions.asserefresh_token_called_once_with(
#                 transactions=transactions
#             )
