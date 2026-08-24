"""HTTP, crypto and encoding helpers backing the PDDIKTI API client."""

import base64
import binascii
import json
import logging
import time
from typing import Any, Optional, Union

import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from requests.adapters import HTTPAdapter
from requests.utils import requote_uri
from urllib3.util.retry import Retry

from .exceptions import (
    APIConnectionError,
    APIRateLimitError,
    APIResponseError,
    APITimeoutError,
    ValidationError,
)

CLOUDFLARE_HELP = (
    "Blocked by Cloudflare. The upstream now requires a browser-solved "
    "clearance. Fix it one of these ways:\n"
    "  1) Open https://pddikti.kemdiktisaintek.go.id in your browser, "
    "then: api(auto_cookie=True)\n"
    "  2) Copy cf_clearance + User-Agent from DevTools: "
    "api(cf_clearance='...', user_agent='...')\n"
    "  3) Point at a solver proxy: api(base_url='http://localhost:8080/api')"
)

# Upstream status codes that map to a fixed error message.
STATUS_MESSAGES = {
    401: "Authentication failed",
    403: "Access forbidden",
    404: "Endpoint not found",
}

# Base64-obfuscated upstream endpoints, decoded at call time.
BASE_URL = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZC9hcGk="
HOST = "cGRkaWt0aS5rZW1kaWt0aXNhaW50ZWsuZ28uaWQ="
ORIGIN = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZA=="
REFERER = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZC8="
FALLBACK_IP = "MTAzLjQ3LjEzMi4yOQ=="

# How long a looked-up public IP stays valid.
IP_CACHE_SECONDS = 3600

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
)

# AES-256-CBC key/IV used by the upstream for its `*/enc/*` payloads and entity IDs.
AES_KEY = "ecHyOABV9jgO2/+dzE49cfexQpr/H4SiAYWrHLD7PQ0="
AES_IV = "Gu3qsglYJhOOm0eXf6aN2w=="


class helper:  # pylint: disable=invalid-name  # public API name since v1
    """Low-level HTTP/crypto layer shared by every :class:`~pddiktipy.api.api` call."""

    # Kept as class attributes for backwards compatibility: they used to be set
    # on every instance and are read by third-party code as `h.url`, `h.ip`, ...
    url = BASE_URL
    host = HOST
    origin = ORIGIN
    referer = REFERER
    ip = FALLBACK_IP

    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        cf_clearance: Optional[str] = None,
        user_agent: Optional[str] = None,
        auto_cookie: bool = False,
    ):
        """Build the HTTP/crypto layer used by every API call.

        Args:
            base_url: Override the upstream API base URL. Point this at your own
                Cloudflare-solving proxy (FlareSolverr, or a self-hosted wrapper).
                Defaults to the official upstream, which sits behind a Cloudflare
                managed challenge and is unreachable from a plain HTTP client.
            session: Pre-configured requests.Session. Overrides the built-in one.
            cf_clearance: A `cf_clearance` cookie value copied from a real browser
                that has solved the Cloudflare challenge. Must be paired with the
                exact `user_agent` of that browser.
            user_agent: The User-Agent string of the browser that produced
                `cf_clearance` (the cookie is bound to it).
            auto_cookie: If True, read `cf_clearance` (and, where possible, the
                matching User-Agent) from a locally installed browser via
                browser_cookie3. Requires `pip install pddiktipy[auto]` and that
                you have opened https://pddikti.kemdiktisaintek.go.id once.
        """
        self.base_url = base_url.rstrip("/") if base_url else None
        self.cf_clearance = cf_clearance
        self.user_agent = user_agent

        # Setup logging (before anything that may log)
        self.logger = logging.getLogger(__name__)

        if auto_cookie and not cf_clearance:
            found_cookie, found_ua = self._read_browser_clearance()
            self.cf_clearance = found_cookie
            if found_ua and not self.user_agent:
                self.user_agent = found_ua

        # Initialize session with retry strategy
        self._session = session
        self._cached_ip = None
        self._ip_cache_time = 0

    @property
    def session(self) -> requests.Session:
        """Lazy initialization of requests session with retry strategy."""
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

        # Carry the Cloudflare clearance cookie on every request to the upstream.
        if self.cf_clearance:
            self._session.cookies.set(
                "cf_clearance", self.cf_clearance, domain="kemdiktisaintek.go.id"
            )

        return self._session

    def _read_browser_clearance(self):
        """
        Read `cf_clearance` and a matching User-Agent from a local browser.

        Returns (cookie, user_agent), either of which may be None. Never raises:
        a missing browser_cookie3 or an unreadable cookie store just yields None
        so the caller can fall back to an explicit cookie.
        """
        try:
            import browser_cookie3 as bc  # pylint: disable=import-outside-toplevel
        except ImportError:
            self.logger.warning(
                "auto_cookie=True needs browser_cookie3 (pip install pddiktipy[auto])"
            )
            return None, None

        loaders = [
            (bc.chrome, self._detect_chrome_user_agent()),
            (bc.edge, self._detect_chrome_user_agent("Edg")),
            (bc.brave, self._detect_chrome_user_agent()),
            (bc.firefox, None),
        ]
        for loader, ua in loaders:
            try:
                jar = loader(domain_name="kemdiktisaintek.go.id")
            except Exception:  # nosec B112  # pylint: disable=broad-exception-caught
                # browser_cookie3 backends raise anything from OSError to their
                # own BrowserCookieError; any failure just means "try the next".
                continue
            for cookie in jar:
                if cookie.name == "cf_clearance" and cookie.value:
                    self.logger.info("Loaded cf_clearance from %s", loader.__name__)
                    return cookie.value, ua
        self.logger.warning(
            "No cf_clearance found in local browsers. Open "
            "https://pddikti.kemdiktisaintek.go.id once, then retry."
        )
        return None, None

    def _detect_chrome_user_agent(self, brand: str = "Chrome") -> Optional[str]:
        """
        Best-effort Chrome/Edge User-Agent so it matches the cookie's browser.

        cf_clearance is bound to the UA that solved the challenge, so a mismatch
        invalidates it. On Windows we read the installed version from the
        registry; elsewhere we return None and let the default UA apply.
        ponytail: Windows-only version detection; other OSes fall back to default UA.
        """
        try:
            import winreg  # pylint: disable=import-outside-toplevel
            key = (
                r"Software\Microsoft\Edge\BLBeacon"
                if brand == "Edg"
                else r"Software\Google\Chrome\BLBeacon"
            )
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
                version, _ = winreg.QueryValueEx(k, "version")
            major = version.split(".")[0]
            ua = (
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36"
            )
            if brand == "Edg":
                ua += f" Edg/{major}.0.0.0"
            return ua
        except (ImportError, OSError, IndexError):
            return None

    def get_ip(self) -> Optional[str]:
        """
        Return the caller's public IP, cached for an hour.

        Falls back to the last known (or a hard-coded) IP when the lookup fails;
        the value is only used for the upstream's ``X-User-IP`` header.
        """
        now = time.time()
        if self._cached_ip and now - self._ip_cache_time < IP_CACHE_SECONDS:
            return self._cached_ip

        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            response.raise_for_status()
            ip = response.json().get("ip")
            if not ip:
                raise APIResponseError("No IP returned from ipify service")
        except (requests.RequestException, ValueError, APIResponseError) as e:
            self.logger.warning("Could not fetch public IP (%s), using fallback", e)
            return self._cached_ip or self.decodes(FALLBACK_IP)

        self._cached_ip = ip
        self._ip_cache_time = now
        self.logger.debug("IP address retrieved and cached: %s", ip)
        return ip

    def get_headers(self) -> dict:
        """Return the request headers the upstream expects."""
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,mt;q=0.8",
            "Connection": "keep-alive",
            "DNT": "1",
            "Origin": self.decodes(ORIGIN),
            "Referer": self.decodes(REFERER),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.user_agent or DEFAULT_USER_AGENT,
            "X-User-IP": self.get_ip(),
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        # Only pin Host when talking to the official upstream. A custom base_url
        # (local proxy, FlareSolverr wrapper) needs requests to derive its own.
        if not self.base_url:
            headers["Host"] = self.decodes(HOST)

        return headers

    @staticmethod
    def _is_cloudflare_challenge(response: requests.Response) -> bool:
        """A Cloudflare challenge comes back as 403 text/html, not JSON."""
        return (
            "text/html" in response.headers.get("content-type", "")
            or response.headers.get("cf-mitigated") == "challenge"
        )

    def _raise_for_status(self, response: requests.Response, endpoint: str) -> None:
        """Translate a non-2xx upstream response into the matching typed error."""
        code = response.status_code
        if code == 429:
            retry_after = response.headers.get("Retry-After", "60")
            raise APIRateLimitError(
                f"Rate limit exceeded. Retry after {retry_after} seconds",
                status_code=429,
                endpoint=endpoint,
            )
        if code == 403 and not self.base_url and self._is_cloudflare_challenge(response):
            raise APIResponseError(CLOUDFLARE_HELP, status_code=403, endpoint=endpoint)
        if code in STATUS_MESSAGES:
            raise APIResponseError(
                STATUS_MESSAGES[code], status_code=code, endpoint=endpoint
            )
        if 500 <= code < 600:
            raise APIResponseError(
                f"Server error: {code}", status_code=code, endpoint=endpoint
            )
        response.raise_for_status()

    def response(self, endpoint: str, timeout: int = 30) -> Optional[dict]:
        """
        GET the endpoint and return the decoded JSON.

        Raises APITimeoutError, APIConnectionError, APIRateLimitError, or
        APIResponseError depending on the failure.
        """
        if not endpoint:
            raise ValidationError("Endpoint cannot be empty")

        try:
            self.logger.debug("Making request to: %s", endpoint)
            response = self.session.get(
                endpoint, headers=self.get_headers(), timeout=timeout
            )
            self._raise_for_status(response, endpoint)
            try:
                json_data = response.json()
            except ValueError as e:
                raise APIResponseError(
                    f"Invalid JSON response: {e}",
                    status_code=response.status_code,
                    endpoint=endpoint,
                ) from e
            self.logger.debug("Successful response from: %s", endpoint)
            return json_data

        # Our own typed errors (rate limit, forbidden, ...) fall straight through:
        # none of the handlers below catch them.
        except requests.Timeout as e:
            raise APITimeoutError(
                f"Request timeout after {timeout} seconds", endpoint=endpoint
            ) from e
        except requests.ConnectionError as e:
            raise APIConnectionError(f"Connection error: {e}", endpoint=endpoint) from e
        except requests.RequestException as e:
            raise APIResponseError(f"Request failed: {e}", endpoint=endpoint) from e

    def base64_encode_image(self, image_content: bytes) -> str:
        """Encode raw image bytes as a base64 string."""
        return base64.b64encode(image_content).decode('utf-8')

    def fetch_image_as_base64(self, url: str, timeout: int = 30) -> Optional[str]:
        """Fetch an image URL and return it base64-encoded."""
        if not url:
            raise ValidationError("Image URL cannot be empty")

        try:
            self.logger.debug("Fetching image from: %s", url)
            response = self.session.get(
                url, headers=self.get_headers(), timeout=timeout
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                self.logger.warning("Unexpected content type: %s", content_type)

            return self.base64_encode_image(response.content)

        except requests.Timeout as e:
            raise APITimeoutError(
                f"Image request timeout after {timeout} seconds", endpoint=url
            ) from e
        except requests.ConnectionError as e:
            raise APIConnectionError(
                f"Connection error fetching image: {e}", endpoint=url
            ) from e
        except requests.RequestException as e:
            raise APIResponseError(f"Error fetching image: {e}", endpoint=url) from e

    def parse(self, value: Union[str, int, float, Any]) -> str:
        """URL-encode a value, coercing non-strings to str first."""
        if value is None:
            raise ValidationError("Cannot parse None value")

        value = value if isinstance(value, str) else str(value)
        if not value.strip():
            raise ValidationError("Cannot parse empty string")

        try:
            return requote_uri(value)
        except (TypeError, ValueError) as e:
            raise ValidationError(f"Error encoding URL: {e}") from e

    def close(self) -> None:
        """Close the session to free resources."""
        if self._session:
            self._session.close()
            self._session = None
            self.logger.debug("Session closed successfully")

    def decodes(self, string: str) -> str:
        """Decodes the value."""
        return base64.b64decode(string).decode('utf-8')

    def endpoint(self) -> str:
        """Returns the API base URL: the caller's override, or the official upstream."""
        return self.base_url or self.decodes(BASE_URL)

    def decrypt(self, encrypted: str) -> Any:
        """
        Decrypts an AES-256-CBC payload returned by the `*/enc/*` endpoints.

        Upstream wraps these as {"status": ..., "data": "<base64 ciphertext>"}.
        Returns the parsed JSON when the plaintext is JSON, else the raw string.
        Raises ValidationError if the ciphertext is malformed or its padding is
        invalid.
        """
        if not encrypted:
            raise ValidationError("Cannot decrypt empty payload")

        try:
            ciphertext = base64.b64decode(encrypted)
        except (binascii.Error, ValueError) as e:
            raise ValidationError(f"Invalid base64 ciphertext: {e}") from e

        if not ciphertext or len(ciphertext) % 16 != 0:
            raise ValidationError("Ciphertext length is not a multiple of the AES block size")

        decryptor = Cipher(
            algorithms.AES(base64.b64decode(AES_KEY)),
            modes.CBC(base64.b64decode(AES_IV)),
        ).decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        padding = plaintext[-1]
        if not 1 <= padding <= 16 or plaintext[-padding:] != bytes([padding]) * padding:
            raise ValidationError(f"Invalid PKCS7 padding: {padding}")
        plaintext = plaintext[:-padding]

        try:
            return json.loads(plaintext)
        except ValueError:
            return plaintext.decode("utf-8", errors="replace")

    def encrypt_id(self, plain_id: str) -> str:
        """
        Encrypts a plaintext entity ID into the base64 form the upstream expects.

        Only needed when you hold a raw ID; IDs returned by the search endpoints
        are already encrypted and should be passed through unchanged.
        """
        if not plain_id:
            raise ValidationError("Cannot encrypt empty ID")

        data = plain_id.encode()
        padding = 16 - (len(data) % 16)
        data += bytes([padding]) * padding

        encryptor = Cipher(
            algorithms.AES(base64.b64decode(AES_KEY)),
            modes.CBC(base64.b64decode(AES_IV)),
        ).encryptor()
        return base64.b64encode(encryptor.update(data) + encryptor.finalize()).decode()

    def decrypt_id(self, encrypted_id: str) -> str:
        """Decrypts an encrypted entity ID back to its plaintext form."""
        plaintext = self.decrypt(encrypted_id)
        return plaintext if isinstance(plaintext, str) else json.dumps(plaintext)

    def with_version(self, version: str) -> str:
        """Appends a version to the decoded URL."""
        return self.endpoint() + version
