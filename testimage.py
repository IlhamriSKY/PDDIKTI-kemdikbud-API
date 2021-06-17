import requests

url = "https://api-frontend.kemdikbud.go.id/v2/detail_pt_logo/RTVFNzg2RkItQjhBNy00OUU2LUJBRDgtM0Q4RThFMEE0RUJG"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
