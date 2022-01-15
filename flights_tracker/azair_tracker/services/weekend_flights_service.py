from typing import List

from flights_tracker.models.weekend_flights import WeekendFlight


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
        return ""

    def parse_flights_data(self, data: str) -> List[WeekendFlight]:
        """
        Extract just weekend flights and return them correctly formatted.

        Args:
            data: Raw data scraped from website.

        Returns: List of weekend flights in correct format.

        """
        return [WeekendFlight()]

    def prepare_email_message(self, data: List[WeekendFlight]) -> str:
        """
        Create ready-to-send email message from all weekeend flights.

        Args:
            data: List of weekend flights in correct format.

        Returns: Ready-to send e-mail message content.

        """
        return ""


