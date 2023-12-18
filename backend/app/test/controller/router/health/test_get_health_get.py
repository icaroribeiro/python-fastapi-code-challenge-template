from test.controller.router.health.test_health_router_fixtures import (
    TestHealthRouterFixtures,
)

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from src.controller.model.health import HealthResponse


class TestGetHealthGet(TestHealthRouterFixtures):
    @pytest.fixture
    def endpoint(self, get_health_endpoint: str) -> str:
        return get_health_endpoint

    async def test_get_status_should_succeed_in_getting_the_status(
        self,
        app_client: AsyncClient,
        endpoint: str,
    ):
        expected_status_code = status.HTTP_200_OK
        expected_json_response = HealthResponse(ok=True)

        response = await app_client.get(url=endpoint)

        json_response = response.json()

        assert expected_status_code == response.status_code
        assert jsonable_encoder(expected_json_response) == json_response
