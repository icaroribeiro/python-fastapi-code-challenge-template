import pytest
from sqlalchemy.orm import Session

from src.domain.model.auth import Auth
from src.domain.repository.auth import AuthRepository
from tests.factory.auth_factory import AuthFactory
from tests.infrastructure.database.test_database_session_manager_fixtures import \
    TestDatabaseSessionManagerFixtures


class TestAuthRepositoryFixtures(TestDatabaseSessionManagerFixtures):
    @pytest.fixture
    def auth(self) -> Auth:
        return AuthFactory()

    @pytest.fixture
    def auth_repository(self, session: Session) -> AuthRepository:
        return AuthRepository(session=session)
