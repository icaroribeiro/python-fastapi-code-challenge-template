import pytest
from faker import Faker
from httpx import AsyncClient

from src.main import app


@pytest.fixture
def fake() -> Faker:
    return Faker("pt_BR")


@pytest.fixture
async def app_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as app_client:
        yield app_client


def pytest_sessionfinish(session, exitstatus):
    pass
