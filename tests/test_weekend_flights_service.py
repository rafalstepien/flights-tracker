import pytest
from unittest.mock import Mock

from flights_tracker.services.weekend_flights_service import WeekendFlightsService


def test_weekend_flights_service():
    pass


def test_obtain_flights_data():
    pass


def test_parse_flights_data():
    pass


def test_prepare_email_message():
    pass


def test_prepare_url(mocker):
    mocker.patch("flights_tracker.services.weekend_flights_service.WeekendFlightsService._get_query_params", return_value="query_params")
    assert WeekendFlightsService()._prepare_url() == "https://test-url.com/?query_params"


def test_get_query_params():
    pass


def test_send_request(mocker):
    mocked_get = mocker.patch('httpx.get')
    WeekendFlightsService().send_request("https://test-url.com")
    assert mocked_get.called


def test_extract_all_flights():
    pass


def test_process_all_flights():
    pass


def test_extract_single_flight_data():
    pass


def test_get_flight_time_and_changes():
    pass


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ([Mock(string="Test string")], "Test string"),
        ([Mock(spec=[])], None),
        ([], None),
    ]
)
def test_get_element_value(test_input, expected_output):

    assert WeekendFlightsService()._get_element_value(test_input) == expected_output
