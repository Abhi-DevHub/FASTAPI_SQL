import requests

# Step 1: Register a new user
register_url = "http://localhost:8000/auth/register"
register_data = {
    "username": "REDX",
    "email": "redx@example.com",
    "password": "redx123"
}
register_response = requests.post(register_url, json=register_data)
print("\nRegister Status Code:", register_response.status_code)
print("\nRegister Response:", register_response.json())

# Step 2: Login to get the access token
login_url = "http://localhost:8000/auth/login"
login_data = {
    "username": "REDX",
    "password": "redx123"
}
login_response = requests.post(login_url, data=login_data)
access_token = login_response.json().get("access_token")
print("\nAccess Token:", access_token)
print("\nLogin Status Code:", login_response.status_code)

# Step 3: Use the token to create a bookmark
bookmark_url = "http://localhost:8000/bookmarks/create"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
bookmark_data = {
    "original_url": "https://www.google.com/search?q=how+to+check+data+in+postgres+gui&sca_esv=41867d5e284fe910&sxsrf=AE3TifMzSP15uo37LwZ7UZSARJkFAcC3BA%3A1752211112273&ei=qJ5waN24EMXt4-EP85a8oQg&ved=0ahUKEwjdrKyHh7SOAxXF9jgGHXMLL4QQ4dUDCBA&uact=5&oq=how+to+check+data+in+postgres+gui&gs_lp=Egxnd3Mtd2l6LXNlcnAiIWhvdyB0byBjaGVjayBkYXRhIGluIHBvc3RncmVzIGd1aTIFECEYoAFI8A1QjgFYpAtwAXgBkAEAmAGiAaABqASqAQMwLjS4AQPIAQD4AQGYAgWgArYEwgIKEAAYsAMY1gQYR8ICBhAAGBYYHpgDAIgGAZAGCJIHAzEuNKAH2xOyBwMwLjS4B7IEwgcDMS40yAcI&sclient=gws-wiz-serp"
}
bookmark_response = requests.post(bookmark_url, json=bookmark_data, headers=headers)
print("\nBookmark Status Code:", bookmark_response.status_code)
print("\nBookmark Response:", bookmark_response.text)
