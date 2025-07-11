import requests

url = "http://localhost:8000/auth/login"
data = {
    "username": "abhishekhiremathh",
    "password": "abhi123"
}

response = requests.post(url, data=data)
print("Status code:", response.status_code)
print("Response:", response.text)