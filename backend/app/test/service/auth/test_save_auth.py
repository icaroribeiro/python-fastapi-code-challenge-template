from test.service.auth.test_auth_service_fixtures import TestAuthServiceFixtures

from faker import Faker
from src.domain.repository.auth import AuthRepository
from src.service.auth import AuthService


class TestSaveAuth(TestAuthServiceFixtures):
    def test_1(
        self,
        auth_repository: AuthRepository,
        auth_service: AuthService,
        fake: Faker,
    ):
        pass
