"""xtapi exceptions."""
from fastapi.exceptions import (
    RequestValidationError as FastAPIRequestValidationError
)


class RequestValidationError(FastAPIRequestValidationError):
    """RequestValidationError"""
