import pytest
from faker import Faker


@pytest.fixture
def fake() -> Faker:
    return Faker("pt_BR")


def pytest_sessionfinish(session, exitstatus):
    pass
