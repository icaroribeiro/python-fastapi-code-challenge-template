from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session
from src.service.health import HealthService


class TestHealthServiceFixtures:
    @pytest.fixture
    def session(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def health_service(self, session: Session) -> HealthService:
        return HealthService(session=session)
