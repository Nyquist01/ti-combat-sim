import pytest

from src.main import Dreadnaught


@pytest.fixture
def mock_fleet_1():
    return [Dreadnaught(), Dreadnaught()]
