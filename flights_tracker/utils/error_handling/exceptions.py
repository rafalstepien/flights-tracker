class BaseFlightTrackerError(Exception):

    message = ""
    status_code = 400

    def __init__(self, message: str = None, status_code: int = None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code


class FlightTrackerTimeoutError(BaseFlightTrackerError):

    message = "Data provider was unable to process the request"
    status_code = 408

