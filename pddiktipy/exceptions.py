"""
Custom exceptions for PDDIKTI API wrapper.
"""
from typing import Optional


class PDDIKTIError(Exception):
    """Base exception for PDDIKTI API errors."""
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        super().__init__(self.message)

class APIConnectionError(PDDIKTIError):
    """Raised when there's a connection issue with the API."""

class APITimeoutError(PDDIKTIError):
    """Raised when API request times out."""

class APIRateLimitError(PDDIKTIError):
    """Raised when API rate limit is exceeded."""

class APIResponseError(PDDIKTIError):
    """Raised when API returns an invalid response."""

class ValidationError(PDDIKTIError):
    """Raised when input validation fails."""

class AuthenticationError(PDDIKTIError):
    """Raised when authentication fails."""
