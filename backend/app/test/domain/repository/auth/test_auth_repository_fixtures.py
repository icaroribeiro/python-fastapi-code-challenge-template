from test.factory.auth_factory import AuthFactory
from test.infrastructure.database.test_database_session_manager_fixtures import (
    TestDatabaseSessionManagerFixtures,
)

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.model.auth import Auth
from src.domain.repository.auth import AuthRepository


class TestAuthRepositoryFixtures(TestDatabaseSessionManagerFixtures):
    @pytest.fixture
    def auth(self) -> Auth:
        return AuthFactory()

    @pytest.fixture
    def auth_repository(self, session: AsyncSession) -> AuthRepository:
        return AuthRepository(session=session)
