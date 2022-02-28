from fastapi import APIRouter, Request, Response

router = APIRouter()


@router.get("/weekend-flights")
def get_weekend_flights(http_request: Request):
    app = http_request.app
    message = app.weekend_flights_service.process()
    app.email_sender.send_html_email_message(message)

    return Response(status_code=200)
