import urllib.request as urllib
import requests
import base64
import logging
import time
from requests.utils import requote_uri
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Union, Any
from .exceptions import (
    APIConnectionError, APITimeoutError, APIRateLimitError, 
    APIResponseError, ValidationError
)

class helper:
    def __init__(self):
        self.url = "aHR0cHM6Ly9hcGktcGRkaWt0aS5rZW1kaWt0aXNhaW50ZWsuZ28uaWQ="
        self.host = "YXBpLXBkZGlrdGkua2VtZGlrdGlzYWludGVrLmdvLmlk"
        self.origin = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZA=="
        self.referer = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZC8="
        self.ip = "MTAzLjQ3LjEzMi4yOQ=="
        
        # Initialize session with retry strategy
        self._session = None
        self._cached_ip = None
        self._ip_cache_time = 0
        self._ip_cache_duration = 3600  # Cache IP for 1 hour
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    @property
    def session(self) -> requests.Session:
        """Lazy initialization of requests session with retry strategy"""
        if self._session is None:
            self._session = requests.Session()
            
            # Retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS"]
            )
            
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)
            
        return self._session
        
    def get_ip(self) -> Optional[str]:
        """
        Retrieves the public IP address with caching and better error handling.
        """
        current_time = time.time()
        
        # Return cached IP if still valid
        if (self._cached_ip and 
            current_time - self._ip_cache_time < self._ip_cache_duration):
            return self._cached_ip
            
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            response.raise_for_status()
            ip = response.json().get("ip")
            
            if not ip:
                raise APIResponseError("No IP returned from ipify service")
            
            # Cache the IP
            self._cached_ip = ip
            self._ip_cache_time = current_time
            self.logger.debug(f"IP address retrieved and cached: {ip}")
            return ip
            
        except requests.Timeout:
            self.logger.warning("Timeout getting IP address, using fallback")
            fallback_ip = self.decodes(self.ip)
            return self._cached_ip or fallback_ip
            
        except requests.RequestException as e:
            self.logger.warning(f"Error fetching IP: {e}, using fallback")
            fallback_ip = self.decodes(self.ip)
            return self._cached_ip or fallback_ip
        
        except Exception as e:
            self.logger.error(f"Unexpected error getting IP: {e}")
            fallback_ip = self.decodes(self.ip)
            return self._cached_ip or fallback_ip

    def get_headers(self) -> dict:
        """
        Returns a single header dictionary for requests.
        """
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,mt;q=0.8",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": self.decodes(self.host),
            "Origin": self.decodes(self.origin),
            "Referer": self.decodes(self.referer),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "X-User-IP": self.get_ip(),
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

    def response(self, endpoint: str, timeout: int = 30) -> Optional[dict]:
        """
        Sends a GET request and returns the JSON response with comprehensive error handling.
        
        Args:
            endpoint: The API endpoint URL
            timeout: Request timeout in seconds
            
        Returns:
            JSON response or None if error occurs
            
        Raises:
            APIConnectionError: For connection issues
            APITimeoutError: For timeout issues  
            APIRateLimitError: For rate limit issues
            APIResponseError: For invalid responses
        """
        if not endpoint:
            raise ValidationError("Endpoint cannot be empty")
            
        headers = self.get_headers()
        
        try:
            self.logger.debug(f"Making request to: {endpoint}")
            response = self.session.get(endpoint, headers=headers, timeout=timeout)
            
            # Handle different HTTP status codes
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After', '60')
                raise APIRateLimitError(
                    f"Rate limit exceeded. Retry after {retry_after} seconds",
                    status_code=429,
                    endpoint=endpoint
                )
            elif response.status_code == 401:
                raise APIResponseError(
                    "Authentication failed",
                    status_code=401,
                    endpoint=endpoint
                )
            elif response.status_code == 403:
                raise APIResponseError(
                    "Access forbidden",
                    status_code=403,
                    endpoint=endpoint
                )
            elif response.status_code == 404:
                raise APIResponseError(
                    "Endpoint not found",
                    status_code=404,
                    endpoint=endpoint
                )
            elif 500 <= response.status_code < 600:
                raise APIResponseError(
                    f"Server error: {response.status_code}",
                    status_code=response.status_code,
                    endpoint=endpoint
                )
            
            response.raise_for_status()
            
            try:
                json_data = response.json()
                self.logger.debug(f"Successful response from: {endpoint}")
                return json_data
            except ValueError as e:
                raise APIResponseError(
                    f"Invalid JSON response: {str(e)}",
                    status_code=response.status_code,
                    endpoint=endpoint
                )
                
        except requests.Timeout:
            raise APITimeoutError(
                f"Request timeout after {timeout} seconds",
                endpoint=endpoint
            )
        except requests.ConnectionError as e:
            raise APIConnectionError(
                f"Connection error: {str(e)}",
                endpoint=endpoint
            )
        except requests.RequestException as e:
            raise APIResponseError(
                f"Request failed: {str(e)}",
                endpoint=endpoint
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in response(): {e}")
            raise APIResponseError(
                f"Unexpected error: {str(e)}",
                endpoint=endpoint
            )

    def base64_encode_image(self, image_content: bytes) -> str:
        """
        Encodes binary image content to a base64 string.

        Args:
            image_content (bytes): The binary content of the image.

        Returns:
            str: Base64-encoded string of the image.
        """
        return base64.b64encode(image_content).decode('utf-8')

    def fetch_image_as_base64(self, url: str, timeout: int = 30) -> Optional[str]:
        """
        Fetches an image from the given URL and returns it as a base64-encoded string.

        Args:
            url (str): URL of the image.
            timeout (int): Request timeout in seconds.

        Returns:
            Optional[str]: Base64-encoded image string or None if an error occurs.
            
        Raises:
            APIConnectionError: For connection issues
            APITimeoutError: For timeout issues
            ValidationError: For invalid input
        """
        if not url:
            raise ValidationError("Image URL cannot be empty")
            
        headers = self.get_headers()
        try:
            self.logger.debug(f"Fetching image from: {url}")
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # Validate content type
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                self.logger.warning(f"Unexpected content type: {content_type}")
            
            return self.base64_encode_image(response.content)
            
        except requests.Timeout:
            raise APITimeoutError(
                f"Image request timeout after {timeout} seconds",
                endpoint=url
            )
        except requests.ConnectionError as e:
            raise APIConnectionError(
                f"Connection error fetching image: {str(e)}",
                endpoint=url
            )
        except requests.RequestException as e:
            raise APIResponseError(
                f"Error fetching image: {str(e)}",
                endpoint=url
            )
        except Exception as e:
            self.logger.error(f"Unexpected error fetching image: {e}")
            raise APIResponseError(
                f"Unexpected error fetching image: {str(e)}",
                endpoint=url
            )

    def parse(self, value: Union[str, int, float, Any]) -> str:
        """
        Encodes a value into a valid URL format.
        Automatically converts non-strings to strings with validation.
        
        Args:
            value: The value to parse (string, int, float, etc.)
            
        Returns:
            URL-encoded string
            
        Raises:
            ValidationError: For invalid input values
        """
        if value is None:
            raise ValidationError("Cannot parse None value")
            
        # Convert to string if input is not a string
        if not isinstance(value, str):
            try:
                value = str(value)
            except Exception as e:
                raise ValidationError(f"Cannot convert value to string: {e}")
        
        # Basic validation
        if not value.strip():
            raise ValidationError("Cannot parse empty string")
            
        try:
            return requote_uri(value)
        except Exception as e:
            raise ValidationError(f"Error encoding URL: {e}")
    
    def close(self) -> None:
        """
        Close the session to free resources.
        """
        if self._session:
            self._session.close()
            self._session = None
            self.logger.debug("Session closed successfully")
    
    def decodes(self, string: str) -> str:
        """
        Decodes the value.
        """
        return base64.b64decode(string).decode('utf-8')

    def endpoint(self) -> str:
        """
        Decodes the URL stored in the class.
        """
        return self.decodes(self.url)

    def with_version(self, version: str) -> str:
        """
        Appends a version to the decoded URL.
        """
        return self.endpoint() + version
