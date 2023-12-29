from unittest.mock import MagicMock

import pytest
from faker import Faker
from src.domain.repository.auth_repository import AuthRepository
from src.service.auth_service import AuthService


class TestAuthServiceFixtures:
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
