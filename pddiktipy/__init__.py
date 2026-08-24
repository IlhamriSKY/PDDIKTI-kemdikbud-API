"""pddiktipy — an unofficial Python client for the PDDIKTI public API."""

# __variables__ with double-quoted values will be available in setup.py
__version__ = "2.1.3"

from .api import api
from .exceptions import (
    APIConnectionError,
    APIRateLimitError,
    APIResponseError,
    APITimeoutError,
    AuthenticationError,
    PDDIKTIError,
    ValidationError,
)

__all__ = [
    "api",
    "PDDIKTIError",
    "APIConnectionError",
    "APITimeoutError",
    "APIRateLimitError",
    "APIResponseError",
    "ValidationError",
    "AuthenticationError",
]
