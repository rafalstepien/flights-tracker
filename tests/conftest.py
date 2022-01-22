import pytest
from bs4 import BeautifulSoup

from config_loader.config_loader import config

from tests.utils import read_test_file


@pytest.fixture(autouse=True)
def set_up_test_environment(monkeypatch):
    monkeypatch.setattr(config, "BASE_AZAIR_URL", "https://test-url.com/")


@pytest.fixture
def single_flight_beautiful_soup_object():
    single_flight_data = read_test_file("example_azair_single_flight.html")
    soup = BeautifulSoup(single_flight_data, "html.parser")
    return soup


@pytest.fixture
def single_flight_parsed_data():
    return {
        "flight_there": {
            "which_way": "There",
            "flight_length": "1:50",
            "price_euro": "5.30",
            "number_of_changes": "0",
            "departure_date": "Tue 15/02/22",
            "departure_hour": "06:55",
            "departure_airport": {
                "city": "Warsaw",
                "code": "WMI"
            },
            "arrival_time": "08:45",
            "arrival_airport": {
                "city": "Oslo",
                "code": "TRF"
            },
            "airline": "Ryanair",
        },
        "flight_back": {
            "which_way": "Back",
            "flight_length": "1:50",
            "price_euro": "5.21",
            "number_of_changes": "0",
            "departure_date": "Fri 18/02/22",
            "departure_hour": "09:05",
            "departure_airport": {
                "city": "Oslo",
                "code": "TRF"
            },
            "arrival_time": "10:55",
            "arrival_airport": {
                "city": "Warsaw",
                "code": "WMI"
            },
            "airline": "Ryanair",
        },
    }
