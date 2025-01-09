import urllib.request as urllib
import requests
import base64
from requests.utils import requote_uri

class helper:
    def __init__(self):
        self.url = "aHR0cHM6Ly9hcGktcGRkaWt0aS5rZW1kaWt0aXNhaW50ZWsuZ28uaWQ="
        self.host = "YXBpLXBkZGlrdGkua2VtZGlrdGlzYWludGVrLmdvLmlk"
        self.origin = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZA=="
        self.referer = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa3Rpc2FpbnRlay5nby5pZC8="
        self.ip = "MTAzLjQ3LjEzMi4yOQ=="
        
    def get_ip(self):
        """
        Retrieves the public IP address of the machine.
        """
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            return response.json().get("ip")
        except requests.RequestException as e:
            print(f"Error fetching IP: {e}")
            return self.decodes(self.ip)

    def get_headers(self):
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

    def response(self, endpoint):
        """
        Sends a GET request and returns the JSON response.
        """
        headers = self.get_headers()
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def base64_encode_image(self, image_content: bytes) -> str:
        """
        Encodes binary image content to a base64 string.

        Args:
            image_content (bytes): The binary content of the image.

        Returns:
            str: Base64-encoded string of the image.
        """
        return base64.b64encode(image_content).decode('utf-8')

    def fetch_image_as_base64(self, url: str) -> str:
        """
        Fetches an image from the given URL and returns it as a base64-encoded string.

        Args:
            url (str): URL of the image.

        Returns:
            Optional[str]: Base64-encoded image string or None if an error occurs.
        """
        headers = self.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            return self.base64_encode_image(response.content)
        except requests.RequestException as e:
            print(f"Error fetching image: {e}")
            return None

    def parse(self, string):
        """
        Encodes a string into a valid URL format.
        """
        return requote_uri(string)
    
    def decodes(self, string):
        """
        Decodes the value.
        """
        return base64.b64decode(string).decode('utf-8')

    def endpoint(self):
        """
        Decodes the URL stored in the class.
        """
        return self.decodes(self.url)

    def with_version(self, version):
        """
        Appends a version to the decoded URL.
        """
        return self.endpoint() + version
