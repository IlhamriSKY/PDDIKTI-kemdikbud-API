# flake8: noqa

# __variables__ with double-quoted values will be available in setup.py
__version__ = "2.0.5"

from .api import api
from .exceptions import (
    PDDIKTIError,
    APIConnectionError,
    APITimeoutError,
    APIRateLimitError,
    APIResponseError,
    ValidationError,
    AuthenticationError
)

__all__ = [
    'api',
    'PDDIKTIError',
    'APIConnectionError', 
    'APITimeoutError',
    'APIRateLimitError',
    'APIResponseError',
    'ValidationError',
    'AuthenticationError'
]
