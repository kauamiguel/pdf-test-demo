import requests

url = "https://api.pdfshift.io/v3/convert/pdf"

payload = { "source": "https://www.google.com" }
headers = {
    "X-API-Key": "",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)