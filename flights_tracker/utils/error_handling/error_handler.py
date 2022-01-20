from contextlib import contextmanager

from httpx import ReadTimeout

from flights_tracker.utils.error_handling.exceptions import FlightTrackerTimeoutError


class ErrorHandler:
    @classmethod
    def handle(cls, error):
        if isinstance(error, ReadTimeout):
            ErrorHandler.handle_httpx_error(error)

    @classmethod
    def handle_httpx_error(cls, error):
        # log error in the future
        raise FlightTrackerTimeoutError


@contextmanager
def handle_errors(*expected_errors):
    try:
        yield
    except expected_errors as e:
        ErrorHandler.handle(e)
