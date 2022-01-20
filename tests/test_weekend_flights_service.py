from unittest.mock import Mock

import bs4
import pytest

from flights_tracker.models.weekend_flights import WhichWay
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
    mocker.patch(
        "flights_tracker.services.weekend_flights_service.WeekendFlightsService._get_query_params",
        return_value="query_params",
    )
    assert WeekendFlightsService()._prepare_url() == "https://test-url.com/?query_params"


def test_get_query_params():
    pass


def test_send_request(mocker):
    mocked_get = mocker.patch("httpx.get")
    WeekendFlightsService().send_request("https://test-url.com")
    assert mocked_get.called


def test_extract_all_flights():
    pass


def test_process_all_flights():
    pass


def test_extract_single_flight_data():
    pass


def test_get_one_way_data(single_flight_object):
    expected_data = (
        "There Tue 15/02/22 06:55 Warsaw WMIWarsaw (Modlin) WMI 08:45 Oslo TRFOslo (Torp) TRF 1:50 h / no change\n€5.30"
    )
    expected_flight_length = "1:50"
    expected_number_of_changes = "0"
    expected_arrival_time = "08:45"
    expected_arrival_airport = "Oslo"
    expected_airline = "Ryanair"

    result = WeekendFlightsService._get_one_way_data(single_flight_object, WhichWay.THERE)

    assert result["data"].text == expected_data
    assert result["flight_length"] == expected_flight_length
    assert result["number_of_changes"] == expected_number_of_changes
    assert result["arrival_time"] == expected_arrival_time
    assert result["arrival_airport"] == expected_arrival_airport
    assert result["airline"] == expected_airline


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ("1:20 h / no change", ("1:20", "0")),
        ("1:20 h / 1 change", ("1:20", "1")),
        ("1:20 h / 4 changes", ("1:20", "4")),
    ],
)
def test_get_flight_time_and_changes(mocker, test_input, expected_output):
    mocker.patch(
        "flights_tracker.services.weekend_flights_service.WeekendFlightsService._get_element_value",
        return_value=test_input,
    )
    data = bs4.element.Tag
    data.select = Mock(return_value="")

    assert WeekendFlightsService._get_flight_time_and_changes(data) == expected_output


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ([Mock(string="Test string")], "Test string"),
        ([Mock(spec=[])], None),
        ([], None),
    ],
)
def test_get_element_value(test_input, expected_output):

    assert WeekendFlightsService()._get_element_value(test_input) == expected_output
