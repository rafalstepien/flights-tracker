import re
from typing import List, Tuple, Union

import bs4.element
import httpx
from bs4 import BeautifulSoup

from config_loader.config_loader import config
from flights_tracker.models.weekend_flights import Flight
from flights_tracker.static import (
    AZairBool,
    CountryCodes,
    Currency,
    IsOneway,
    PolishAirports,
    SearchTypes,
    UnknownParam,
    Weekdays,
)
from flights_tracker.utils.error_handling.error_handler import handle_errors


class WeekendFlightsService:
    """
    Service for obtaining flights data, processing it and returning as ready-to-send message.
    """

    def process(self):
        data = self.obtain_flights_data()
        data = self.parse_flights_data(data)
        message = self.prepare_email_message(data)
        return message

    def obtain_flights_data(self) -> str:
        """
        Web scrap all flight data and return them as raw text.

        Returns: Flights XML data as string

        """
        request = self._prepare_url()
        return self.send_request(request)

    def parse_flights_data(self, data: str) -> List[Flight]:
        """
        Extract just weekend flights and return them correctly formatted.

        Args:
            data: Raw data scraped from website.

        Returns: List of weekend flights in correct format.

        """
        all_flights = self._extract_all_flights(data)
        return self._process_all_flights(all_flights)

    def prepare_email_message(self, data: List[Flight]) -> str:
        """
        Create ready-to-send email message from all weekeend flights.

        Args:
            data: List of weekend flights in correct format.

        Returns: Ready-to send e-mail message content.

        """
        return ""

    def _prepare_url(self):
        query_params = self._get_query_params()
        return f"{config.BASE_AZAIR_URL}?{query_params}"

    @staticmethod
    def _get_query_params() -> str:
        """
        Fill the query params.

        Returns: String of query params ready to send to AZair.

        """

        srcAirport = "Poland+%5BSZY%5D+%28%2BWMI%2CWAW%2CGDN%2CBZG%2CLCJ%2CLUZ%2CPOZ%2CKRK%2CKTW%2CRZE%2CSZZ%2CWRO%29&"
        srcap = PolishAirports.get_srcap_parameter()
        destination_anywhere = "Anywhere+%5BXXX%5D"
        soonest_depart_date = "2022-02-01"
        latest_arrival_date = "2022-02-28"
        min_days_stay = 2
        max_days_stay = 3
        depmonth = "".join(soonest_depart_date.split("-")[:-1])
        arrmonth = "".join(latest_arrival_date.split("-")[:-1])
        departures = Weekdays.get_departure_for_all_days()
        arrivals = Weekdays.get_arrival_for_all_days()
        minHourStay = "0%3A45"
        maxHourStay = "23%3A20"
        minHourOutbound = "0%3A00"
        maxHourOutbound = "24%3A00"
        minHourInbound = "0%3A00"
        maxHourInbound = "24%3A00"
        adults = 2
        children = 0
        infants = 0
        max_changes = 1

        return (
            f"searchtype={SearchTypes.FLEXI}&"
            f"tp={UnknownParam.ZERO}&"
            f"isOneway={IsOneway.NO}&"
            f"srcAirport={srcAirport}&"
            f"{srcap}&"
            f"srcFreeAirport=&"
            f"srcTypedText=&"
            f"srcFreeTypedText=&"
            f"srcMC={CountryCodes.POLAND}&"
            f"dstAirport={destination_anywhere}&"
            f"anywhere={AZairBool.TRUE}&"
            f"dstTypedText=&"
            f"dstFreeTypedText=&"
            f"dstMC=&"
            f"depmonth={depmonth}&"
            f"depdate={soonest_depart_date}&"
            f"aid={UnknownParam.ZERO}&"
            f"arrmonth={arrmonth}&"
            f"arrdate={latest_arrival_date}&"
            f"minDaysStay={min_days_stay}&"
            f"maxDaysStay={max_days_stay}&"
            f"{departures}&"
            f"{arrivals}&"
            f"samedep={AZairBool.TRUE}&"
            f"samearr={AZairBool.TRUE}&"
            f"minHourStay={minHourStay}&"
            f"maxHourStay={maxHourStay}&"
            f"minHourOutbound={minHourOutbound}&"
            f"maxHourOutbound={maxHourOutbound}&"
            f"minHourInbound={minHourInbound}&"
            f"maxHourInbound={maxHourInbound}&"
            f"autoprice={AZairBool.TRUE}&"
            f"adults={adults}&"
            f"children={children}&"
            f"infants={infants}&"
            f"maxChng={max_changes}&"
            f"currency={Currency.EURO}&"
            f"indexSubmit=Search"
        )

    @staticmethod
    def send_request(url):
        with handle_errors(httpx.ReadTimeout):
            return httpx.get(
                url,
                timeout=config.TIMEOUT,
            ).text

    @staticmethod
    def _extract_all_flights(data: str) -> bs4.element.ResultSet:
        soup = BeautifulSoup(data, "html.parser")
        return soup.find_all("div", {"class": "result"})

    def _process_all_flights(self, all_flights_data: bs4.element.ResultSet) -> List[Flight]:
        available_flights = []
        for single_flight_div in all_flights_data:
            single_flight_data = self._extract_single_flight_data(single_flight_div)
            available_flights.append(Flight(**single_flight_data))
        return available_flights

    def _extract_single_flight_data(self, single_flight_div: bs4.element.Tag) -> dict:
        there_data = single_flight_div.select("p span.caption.tam")[0].parent
        there_flight_length, there_number_of_changes = self._get_flight_time_and_changes(there_data)
        there_arrival_time, _, there_arrival_airport = (
            there_data.select("span.to")[0].next_element.text.strip().partition(" ")
        )
        back_data = single_flight_div.select("p span.caption.sem")[0].parent
        back_flight_length, back_number_of_changes = self._get_flight_time_and_changes(back_data)
        back_arrival_time, _, back_arrival_airport = (
            back_data.select("span.to")[0].next_element.text.strip().partition(" ")
        )
        airline_there = single_flight_div.select('span[class*="iata"]')[0].text
        airline_back = single_flight_div.select('span[class*="iata"]')[0].text
        data = {
            "flight_there": {
                "which_way": self._get_element_value(there_data.select("span.caption.tam")),
                "flight_length": there_flight_length,
                "price_euro": self._get_element_value(there_data.select("span.subPrice")).replace("€", ""),
                "number_of_changes": there_number_of_changes,
                "departure_date": self._get_element_value(there_data.select("span.date")),
                "departure_time": self._get_element_value(there_data.select("span.from")[0].select("strong")),
                "departure_airport": {
                    "city": there_data.select("span.from")[0].next_element.next_sibling.text.strip(),
                    "code": there_data.select("span.from")[
                        0
                    ].next_element.next_sibling.next_element.next_element.text.strip(),
                },
                "arrival_time": there_arrival_time,
                "arrival_airport": {
                    "city": there_arrival_airport,
                    "code": there_data.select("span.to")[0].next_element.next_sibling.next_element.text.strip(),
                },
                "airline": airline_there,
            },
            "flight_back": {
                "which_way": self._get_element_value(back_data.select("span.caption.sem")),
                "flight_length": back_flight_length,
                "price_euro": self._get_element_value(back_data.select("span.subPrice")).replace("€", ""),
                "number_of_changes": back_number_of_changes,
                "departure_date": self._get_element_value(back_data.select("span.date")),
                "departure_time": self._get_element_value(back_data.select("span.from")[0].select("strong")),
                "departure_airport": {
                    "city": back_data.select("span.from")[0].next_element.next_sibling.text.strip(),
                    "code": back_data.select("span.from")[
                        0
                    ].next_element.next_sibling.next_element.next_element.text.strip(),
                },
                "arrival_time": back_arrival_time,
                "arrival_airport": {
                    "city": back_arrival_airport,
                    "code": back_data.select("span.to")[0].next_element.next_sibling.next_element.text.strip(),
                },
                "airline": airline_back,
            },
        }
        return data

    @staticmethod
    def _get_flight_time_and_changes(there_data: bs4.element.Tag) -> Tuple[str, str]:
        time_and_changes = WeekendFlightsService._get_element_value(there_data.select("span.durcha"))
        pattern_time, pattern_changes = r"\d+:\d+\s", r"\s\d+\s"
        time, changes = re.search(pattern_time, time_and_changes), re.search(pattern_changes, time_and_changes)
        if changes:
            changes = changes.group().strip()
        else:
            changes = 0
        time = time.group().strip()
        return time, changes

    @staticmethod
    def _get_element_value(element) -> Union[str, None]:
        try:
            return element[0].string
        except (IndexError, AttributeError):
            return None
