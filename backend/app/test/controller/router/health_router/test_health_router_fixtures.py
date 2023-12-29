from test.controller.test_controller_fixtures import TestControllerFixtures

import pytest


class TestHealthRouterFixtures(TestControllerFixtures):
    @pytest.fixture
    def get_health_endpoint(self) -> str:
        return "/health"
