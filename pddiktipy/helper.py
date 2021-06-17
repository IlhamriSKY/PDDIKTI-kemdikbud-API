import urllib.request as urllib
import json
import requests
import base64

# Encode
from requests.utils import requote_uri
# from urllib.parse import quote

class helper(object):
	def __init__(self):
		self.url = "aHR0cHM6Ly9hcGktZnJvbnRlbmQua2VtZGlrYnVkLmdvLmlkLw=="
		self.version = "v2"

	def response(self, endpoint):
		response = urllib.urlopen(endpoint)
		data = json.loads(response.read())
		return data

	def post(self, endpoint, payload):
		headers = {
			'Content-Type': 'text/plain'
		}
		response = requests.post(endpoint, data = payload)
		return (response.json())

	def get(self, endpoint, payload):
		headers = {
			'Content-Type': 'text/plain'
		}
		response = requests.get(endpoint, data = payload)
		return (response.json())

	def get_text(self, endpoint):
		payload = {}
		response = requests.get(endpoint, data = payload)
		return (response.text)

	def parse(self, string):
		url = requote_uri(string)
		return url

	def base64_decode(self, string):
		response = base64.b64decode(string)
		return response.decode('utf-8')

	def base64_encode(self, string):
		response = base64.b64encode(string)
		return response.decode('utf-8')

	def endpoint(self):
		endpoint = base64.b64decode(self.url).decode()
		return endpoint

	def withversion(self):
		endpoint = base64.b64decode(self.url).decode()
		return endpoint+self.version