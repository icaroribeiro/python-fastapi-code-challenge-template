import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from src.infrastructure.database.test_database_session_manager import (
    TestDatabaseSessionManager,
)
from src.router.dto.health_response_dto import HealthResponseDto


class TestFixtures(TestDatabaseSessionManager):
    @pytest.fixture
    def get_health_endpoint(self) -> str:
        return "/health"


class TestGetHealth(TestFixtures):
    @pytest.fixture
    def endpoint(self, get_health_endpoint: str) -> str:
        return get_health_endpoint

    async def test_returns_health_response_with_true_if_the_application_is_healthy(
        self,
        app_client: AsyncClient,
        endpoint: str,
    ):
        expected_status_code = status.HTTP_200_OK
        expected_json_response = HealthResponseDto(ok=True)

        response = await app_client.get(url=endpoint)

        json_response = response.json()

        assert expected_status_code == response.status_code
        assert jsonable_encoder(expected_json_response) == json_response
