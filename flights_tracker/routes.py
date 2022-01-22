from fastapi import APIRouter, Request, Response
from config_loader.config_loader import config

router = APIRouter()


@router.get("/weekend-flights")
def get_weekend_flights(http_request: Request):
    app = http_request.app
    message = app.weekend_flights_service.process()
    for email_address in config.RECEIVER_EMAIL:
        app.email_sender.send_html_email_message(message, email_address)

    return Response(status_code=200)
