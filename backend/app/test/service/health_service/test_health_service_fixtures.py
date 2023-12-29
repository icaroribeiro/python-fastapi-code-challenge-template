from test.infrastructure.database.test_database_session_manager_fixtures import (
    TestDatabaseSessionManagerFixtures,
)

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.health_service import HealthService


class TestHealthServiceFixtures(TestDatabaseSessionManagerFixtures):
    @pytest.fixture
    def health_service(self, session: AsyncSession) -> HealthService:
        return HealthService(session=session)
