from typing import List

from flights_tracker.azair_tracker.static import (
    AZairBool,
    CountryCodes,
    Currency,
    IsOneway,
    PolishAirports,
    SearchTypes,
    UnknownParam,
    Weekdays,
)
from flights_tracker.models.weekend_flights import WeekendFlight


class WeekendFlightsService:
    """
    Service for obtaining flights data, processing it and returning as ready-to-send message.
    """

    BASE_AZAIR_URL = "https://www.azair.eu/azfin.php"

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
        request = self._prepare_request()
        return self._send_request(request)

    def _prepare_request(self):
        query_params = self._get_query_params()
        url = f"{WeekendFlightsService.BASE_AZAIR_URL}?{query_params}"
        return url

    def _get_query_params(self) -> str:
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

    def parse_flights_data(self, data: str) -> List[WeekendFlight]:
        """
        Extract just weekend flights and return them correctly formatted.

        Args:
            data: Raw data scraped from website.

        Returns: List of weekend flights in correct format.

        """
        return []

    def prepare_email_message(self, data: List[WeekendFlight]) -> str:
        """
        Create ready-to-send email message from all weekeend flights.

        Args:
            data: List of weekend flights in correct format.

        Returns: Ready-to send e-mail message content.

        """
        return ""
