from contextlib import contextmanager

from fastapi import HTTPException, status
from httpx import ReadTimeout


class ErrorHandler:
    @classmethod
    def handle(cls, error):
        if isinstance(error, ReadTimeout):
            ErrorHandler.handle_httpx_error(error)

    @classmethod
    def handle_httpx_error(cls, error):
        # log error in the future
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Data provider was unable to process the request. Please try again for a while.",
        )


@contextmanager
def handle_errors(*expected_errors):
    try:
        yield
    except expected_errors as e:
        ErrorHandler.handle(e)
