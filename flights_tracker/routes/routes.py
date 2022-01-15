from fastapi import APIRouter, Request, Response

router = APIRouter()


@router.get("/weekend_flights")
def get_weekend_flights(http_request: Request):
    app = http_request.app
    message = app.weekend_flights_service.process()
    app.email_sender.send_email(message)

    return Response(status_code=200)


@router.get("/")
def hello_world():
    return {"message": "Hello world!"}
