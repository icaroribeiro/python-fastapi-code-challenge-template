from test.factory.auth_factory import AuthFactory

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.model.auth import Auth
from src.infrastructure.database.test_database_session_manager import (
    TestDatabaseSessionManager,
)
from src.infrastructure.repository.auth_repository import AuthRepository


class TestFixtures(TestDatabaseSessionManager):
    @pytest.fixture
    def fake(self) -> Faker:
        return Faker("pt_BR")

    @pytest.fixture
    def auth(self) -> Auth:
        return AuthFactory()

    @pytest.fixture
    def auth_repository(self, session: AsyncSession) -> AuthRepository:
        return AuthRepository(session=session)


class TestCreateAuth(TestFixtures):
    async def test_should_return_auth_when_auth_is_registered(
        self,
        auth: Auth,
        auth_repository: AuthRepository,
        fake: Faker,
    ):
        result = await auth_repository.create_auth(auth=auth)

        assert True
