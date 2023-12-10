from sqlalchemy.orm import Session
from src.service.health import HealthService
from tests.src.service.health.test_health_service_fixtures import (
    TestHealthServiceFixtures,
)


class TestCheckHealth(TestHealthServiceFixtures):
    def test_should_succeed_in_checking_the_health(self, health_service: HealthService):
        result = health_service.check_health()

        assert result

    def test_should_fail_with_500_if_an_exception_is_throw_when_checking_if_the_database_is_alive(
        self, health_service: HealthService, session: Session
    ):
        session.execute.return_value = None

        result = health_service.check_health()

        assert not result
