import pytest
from src.infrastructure.jwt.jwt_auth import JWTAuth
from tests.src.infrastructure.jwt.test_jwt_fixtures import TestJWTFixtures


class TestJWTAuthFixtures(TestJWTFixtures):
    @pytest.fixture()
    def jwt_auth(self) -> JWTAuth:
        return JWTAuth()
