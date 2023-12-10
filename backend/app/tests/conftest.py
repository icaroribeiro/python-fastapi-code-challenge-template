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


def pytest_sessionfinish(session, exitstatus):
    loop = asyncio.get_event_loop()
    loop.close()
