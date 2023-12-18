from test.infrastructure.database.test_database_session_manager_fixtures import (
    TestDatabaseSessionManagerFixtures,
)

import pytest
from httpx import AsyncClient

from src.main import app


class TestControllerFixtures(TestDatabaseSessionManagerFixtures):
    @pytest.fixture
    async def app_client(self) -> AsyncClient:
        async with AsyncClient(app=app, base_url="http://test") as app_client:
            yield app_client
