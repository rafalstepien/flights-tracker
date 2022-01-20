class BaseFlightTrackerError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class FlightTrackerTimeoutError(BaseFlightTrackerError):
    message = "Data provider was unable to process the request"
    status_code = 408
