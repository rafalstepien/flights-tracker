import re
from pathlib import Path
from typing import List, Tuple, Union
from jinja2 import Environment, FileSystemLoader
import bs4.element
import httpx
from bs4 import BeautifulSoup

from config_loader.config_loader import config
from flights_tracker.models.weekend_flights import Flight, WhichWay
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
    TEMPLATES_DIR = Path(__file__).resolve().parent / ".." / "templates"

    def process(self):
        with handle_errors(httpx.ReadTimeout):
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
        all_flights = self._process_all_flights(all_flights)
        return self._filter_flights(all_flights)

    @staticmethod
    def prepare_email_message(data: List[Flight]) -> str:
        """
        Create ready-to-send email message from all weekeend flights.

        Args:
            data: List of weekend flights in correct format.

        Returns: Ready-to send e-mail message content.

        """
        env = Environment(loader=FileSystemLoader(WeekendFlightsService.TEMPLATES_DIR))
        template = env.get_template('email_report.html')
        return template.render(flights=data)

    @staticmethod
    def _prepare_url():
        query_params = WeekendFlightsService._get_query_params()
        return f"{config.BASE_AZAIR_URL}?{query_params}"

    @staticmethod
    def send_request(url):
        return httpx.get(
            url,
            timeout=config.TIMEOUT,
        ).text

    @staticmethod
    def _extract_all_flights(data: str) -> bs4.element.ResultSet:
        soup = BeautifulSoup(data, "html.parser")
        return soup.find_all("div", {"class": "result"})

    @staticmethod
    def _process_all_flights(all_flights_data: bs4.element.ResultSet) -> List[Flight]:
        """
        Puts all data to the list as a single Flight() object and returns list of all flights in
        correct format.

        Args:
            all_flights_data: Scraped data about all flights.

        Returns: List of Flight() objects.

        """
        available_flights = []
        for single_flight_div in all_flights_data:
            single_flight_data = WeekendFlightsService._extract_single_flight_data(single_flight_div)
            available_flights.append(Flight(**single_flight_data))
        return available_flights

    @staticmethod
    def _filter_flights(all_flights: List[Flight]) -> List[Flight]:
        """
        Select just flights matching the criteria of weekend flight.

        Args:
            all_flights: Parsed data about all flights.

        Returns:

        """
        just_weekend_flights = []

        for flight in all_flights:
            if WeekendFlightsService.is_weekend_flight(flight):
                just_weekend_flights.append(flight)

        return just_weekend_flights

    @staticmethod
    def is_weekend_flight(flight: Flight) -> bool:
        departure_weekday = flight.flight_there.departure_date[:3].lower()
        comeback_weekday = flight.flight_back.departure_date[:3].lower()
        return departure_weekday in (Weekdays.THURSDAY[:3], Weekdays.FRIDAY[:3]) and comeback_weekday in (Weekdays.SATURDAY[:3], Weekdays.SUNDAY[:3], Weekdays.MONDAY[:3])

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
    def _extract_single_flight_data(single_flight_div: bs4.element.Tag) -> dict:
        """
        Parses HTML data about single flight and returns dictionary in correct format, ready to create Flight() object.

        Args:
            single_flight_div: Data for single flight.

        Returns: Parsed data for single flight.

        """
        there_data = WeekendFlightsService._get_one_way_data(single_flight_div, WhichWay.THERE)
        price_there = WeekendFlightsService._get_element_value(there_data["data"].select("span.subPrice")).replace("€", "")
        back_data = WeekendFlightsService._get_one_way_data(single_flight_div, WhichWay.BACK)
        price_back = WeekendFlightsService._get_element_value(back_data["data"].select("span.subPrice")).replace("€", "")

        return {
            "flight_there": {
                "which_way": WeekendFlightsService._get_element_value(there_data["data"].select("span.caption.tam")),
                "flight_length": there_data["flight_length"],
                "price_euro": price_there,
                "number_of_changes": there_data["number_of_changes"],
                "departure_date": WeekendFlightsService._get_element_value(there_data["data"].select("span.date")),
                "departure_hour": WeekendFlightsService._get_element_value(there_data["data"].select("span.from")[0].select("strong")),
                "departure_airport": {
                    "city": there_data["data"].select("span.from")[0].next_element.next_sibling.text.strip(),
                    "code": there_data["data"]
                    .select("span.from")[0]
                    .next_element.next_sibling.next_element.next_element.text.strip(),
                },
                "arrival_time": there_data["arrival_time"],
                "arrival_airport": {
                    "city": there_data["arrival_airport"],
                    "code": there_data["data"].select("span.to")[0].next_element.next_sibling.next_element.text.strip(),
                },
                "airline": there_data["airline"],
            },
            "flight_back": {
                "which_way": WeekendFlightsService._get_element_value(back_data["data"].select("span.caption.sem")),
                "flight_length": back_data["flight_length"],
                "price_euro": price_back,
                "number_of_changes": back_data["number_of_changes"],
                "departure_date": WeekendFlightsService._get_element_value(back_data["data"].select("span.date")),
                "departure_hour": WeekendFlightsService._get_element_value(back_data["data"].select("span.from")[0].select("strong")),
                "departure_airport": {
                    "city": back_data["data"].select("span.from")[0].next_element.next_sibling.text.strip(),
                    "code": back_data["data"]
                    .select("span.from")[0]
                    .next_element.next_sibling.next_element.next_element.text.strip(),
                },
                "arrival_time": back_data["arrival_time"],
                "arrival_airport": {
                    "city": back_data["arrival_airport"],
                    "code": back_data["data"].select("span.to")[0].next_element.next_sibling.next_element.text.strip(),
                },
                "airline": back_data["airline"],
            },
            "total_price": f"{round(float(price_there) + float(price_back), 2)}"
        }

    @staticmethod
    def _get_one_way_data(single_flight_div: bs4.element.Tag, which_way: WhichWay):
        """
        Extracts data regarding one way flight (there or back) and returns them as a dictionary.

        Args:
            single_flight_div: Data for single flight.
            which_way: If the flight is there or back.

        Returns:
            Data related to flight in one way, there or back.

        """
        if which_way == WhichWay.THERE:
            caption_class = "tam"
            iata_element_number = 0
        else:
            caption_class = "sem"
            iata_element_number = 1

        data = single_flight_div.select(f"p span.caption.{caption_class}")[0].parent
        flight_length, number_of_changes = WeekendFlightsService._get_flight_time_and_changes(data)
        arrival_time, _, arrival_airport = data.select("span.to")[0].next_element.text.strip().partition(" ")
        airline = single_flight_div.select('span[class*="iata"]')[iata_element_number].text
        return {
            "data": data,
            "flight_length": flight_length,
            "number_of_changes": number_of_changes,
            "arrival_time": arrival_time,
            "arrival_airport": arrival_airport,
            "airline": airline,
        }

    @staticmethod
    def _get_flight_time_and_changes(data: bs4.element.Tag) -> Tuple[str, str]:
        """
        Obtains flight time and number of changes from one way flight.
        Args:
            data: Data related to one way flight.

        Returns:
            Time of flight and number of changes.

        """
        time_and_changes = WeekendFlightsService._get_element_value(data.select("span.durcha"))
        pattern_time, pattern_changes = r"\d+:\d+\s", r"\s\d+\s"
        time, changes = re.search(pattern_time, time_and_changes), re.search(pattern_changes, time_and_changes)
        if changes:
            changes = changes.group().strip()
        else:
            changes = "0"
        time = time.group().strip()
        return time, changes

    @staticmethod
    def _get_element_value(element) -> Union[str, None]:
        try:
            return element[0].string
        except (IndexError, AttributeError):
            return None
