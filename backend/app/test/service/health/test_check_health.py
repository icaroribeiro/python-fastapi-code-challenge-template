from test.service.health.test_health_service_fixtures import TestHealthServiceFixtures

from src.service.health import HealthService


class TestCheckHealth(TestHealthServiceFixtures):
    async def test_should_succeed_in_checking_the_health(
        self, health_service: HealthService
    ):
        result = await health_service.check_health()

        assert result
