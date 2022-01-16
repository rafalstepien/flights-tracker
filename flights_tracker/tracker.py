import uvicorn
from fastapi import FastAPI

from email_sender.service.email_sender import EmailSender
from flights_tracker.routes import router
from flights_tracker.services.weekend_flights_service import WeekendFlightsService


class FlightsTracker(FastAPI):
    weekend_flights_service = WeekendFlightsService()
    email_sender = EmailSender()


app = FlightsTracker()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
