from faker import Faker
from src.domain.repository.transaction import TransactionRepository
from src.service.transaction import TransactionService
from tests.src.service.transaction.test_transaction_service_fixtures import (
    TestTransactionServiceFixtures,
)


class TestListTransactionBalancesBySalespersonType(TestTransactionServiceFixtures):
    def test_should_succeed_in_listing_transactions(
        self,
        file_path: str,
        transaction_repository: TransactionRepository,
        transaction_service: TransactionService,
        fake: Faker,
    ):
        pass
