import urllib.request as urllib
import requests
import base64
from requests.utils import requote_uri

class helper:
    def __init__(self):
        self.url = "aHR0cHM6Ly9wZGRpa3RpLmtlbWRpa2J1ZC5nby5pZC9hcGk="
        self.key = "3ed297db-db1c-4266-8bf4-a89f21c01317"

    def response(self, endpoint):
        """
        Sends a GET request and returns the JSON response.
        """
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.key
        }
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
        headers = {
            'x-api-key': self.key
        }
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

    def endpoint(self):
        """
        Decodes the base64-encoded URL stored in the class.
        """
        return base64.b64decode(self.url).decode('utf-8')

    def with_version(self):
        """
        Appends a version to the decoded URL.
        """
        return self.endpoint() + self.version
