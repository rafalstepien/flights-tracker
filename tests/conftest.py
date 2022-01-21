import pytest
from bs4 import BeautifulSoup

from config_loader.config_loader import config

from tests.utils import read_test_file


@pytest.fixture(autouse=True)
def set_up_test_environment(monkeypatch):
    monkeypatch.setattr(config, "BASE_AZAIR_URL", "https://test-url.com/")


@pytest.fixture
def single_flight_object():
    single_flight_data = read_test_file("example_azair_single_flight.html")
    soup = BeautifulSoup(single_flight_data, "html.parser")
    return soup
