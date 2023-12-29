from test.service.auth_service.test_auth_service_fixtures import \
    TestAuthServiceFixtures

from faker import Faker
from src.domain.repository.auth_repository import AuthRepository
from src.service.auth_service import AuthService


class TestSaveAuth(TestAuthServiceFixtures):
    def test_1(
        self,
        auth_repository: AuthRepository,
        auth_service: AuthService,
        fake: Faker,
    ):
        pass
