from faker import Faker
from src.domain.repository.auth import AuthRepository
from src.service.auth import AuthService
from tests.src.service.auth.test_auth_service_fixtures import TestAuthServiceFixtures


class TestSignIn(TestAuthServiceFixtures):
    def test_1(
        self,
        auth_repository: AuthRepository,
        auth_service: AuthService,
        fake: Faker,
    ):
        pass
