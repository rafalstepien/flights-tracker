from fastapi import FastAPI

from flights_tracker.azair_tracker.services.weekend_flights_service import WeekendFlightsService
from flights_tracker.email_sender.email_sender import EmailSender


class AZairTracker(FastAPI):
    weekend_flights_service = WeekendFlightsService()
    email_sender = EmailSender()
