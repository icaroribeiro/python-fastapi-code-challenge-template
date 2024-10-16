import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.test_database_session_manager import (
    TestDatabaseSessionManager,
)
from src.service.health_service import HealthService


class TestFixtures(TestDatabaseSessionManager):
    @pytest.fixture
    def health_service(self, session: AsyncSession) -> HealthService:
        return HealthService(session=session)


class TestCheckHealth(TestFixtures):
    async def test_returns_true_when_application_is_healthy(
        self, health_service: HealthService
    ):
        result = await health_service.check_health()

        assert result
