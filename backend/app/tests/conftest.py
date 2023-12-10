import asyncio

import pytest
from faker import Faker


@pytest.fixture
def fake() -> Faker:
    return Faker("pt_BR")


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture
# async def app_client() -> AsyncClient:
#     async with AsyncClient(app=app, base_url="http://test") as app_client:
#         yield app_client


# @pytest.fixture
# def mocked_aioresponses():
#     with aioresponses() as mocked_aioresponses:
#         yield mocked_aioresponses


def pytest_sessionfinish(session, exitstatus):
    loop = asyncio.get_event_loop()
    loop.close()
