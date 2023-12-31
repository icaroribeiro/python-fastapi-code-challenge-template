from unittest.mock import MagicMock

import pytest
from faker import Faker

from src.infrastructure.repository.auth_repository import AuthRepository
from src.service.auth_service import AuthService


class TestFixtures:
    @pytest.fixture
    def fake(self) -> Faker:
        return Faker()

    @pytest.fixture
    def auth_repository(self) -> AuthRepository:
        return MagicMock(spec=AuthRepository)

    @pytest.fixture
    def auth_service(
        self,
        auth_repository: AuthRepository,
    ) -> AuthService:
        return AuthService(
            auth_repository=auth_repository,
        )


class TestSaveAuth(TestFixtures):
    def test_1(
        self,
        auth_repository: AuthRepository,
        auth_service: AuthService,
        fake: Faker,
    ):
        pass
