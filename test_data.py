import requests

url = "http://localhost:8000/auth/register"
data = {
    "email": "abhishekhiremathh701@gmail.com",
    "username": "abhishekhiremathh",
    "password": "abhi123"
}
response = requests.post(url, json=data)
print("Status code:", response.status_code)
print("Response text:", response.text)