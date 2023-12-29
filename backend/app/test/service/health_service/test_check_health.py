from test.service.health_service.test_health_service_fixtures import (
    TestHealthServiceFixtures,
)

from src.service.health_service import HealthService


class TestCheckHealth(TestHealthServiceFixtures):
    async def test_should_succeed_in_checking_the_health(
        self, health_service: HealthService
    ):
        result = await health_service.check_health()

        assert result
