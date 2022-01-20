from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from config_loader.config_loader import config


@pytest.fixture(autouse=True)
def set_up_test_environment(monkeypatch):
    monkeypatch.setattr(config, "BASE_AZAIR_URL", "https://test-url.com/")


@pytest.fixture
def single_flight_object():
    single_flight_data = read_test_file("example_azair_single_flight.html")
    soup = BeautifulSoup(single_flight_data, "html.parser")
    return soup


def get_test_file_path(filename):
    conftest_path = Path(__file__).resolve().parent
    tests_data_path = conftest_path / "data/"
    return str(tests_data_path / filename)


def read_test_file(filename):
    file_path = get_test_file_path(filename)
    with open(file_path, "r") as f:
        content = f.read()
    return content
