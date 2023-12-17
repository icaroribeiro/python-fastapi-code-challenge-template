from test.domain.repository.auth.test_auth_repository_fixtures import (
    TestAuthRepositoryFixtures,
)

from faker import Faker
from sqlalchemy.orm import Session
from src.domain.model.auth import Auth
from src.domain.repository.auth import AuthRepository


class TestCreateAuth(TestAuthRepositoryFixtures):
    async def test_should_return_auth_when_auth_is_registered(
        self,
        auth: Auth,
        auth_repository: AuthRepository,
        fake: Faker,
    ):
        result = await auth_repository.create_auth(auth=auth)

        assert True
