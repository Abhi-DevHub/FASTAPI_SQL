
import requests
import random

first_names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Skyler", "Avery"]
last_names = ["Smith", "Johnson", "Lee", "Brown", "Davis", "Clark", "Lewis", "Walker", "Young", "King"]
websites = [
    "https://www.google.com", "https://www.facebook.com", "https://www.youtube.com", "https://www.twitter.com", "https://www.instagram.com",
    "https://www.wikipedia.org", "https://www.amazon.com", "https://www.linkedin.com", "https://www.microsoft.com", "https://www.apple.com",
    "https://www.netflix.com", "https://www.yahoo.com", "https://www.reddit.com", "https://www.twitch.tv", "https://www.spotify.com",
    "https://www.adobe.com", "https://www.wordpress.com", "https://www.bing.com", "https://www.office.com", "https://www.salesforce.com"
]

register_url = "http://localhost:8000/auth/register"
login_url = "http://localhost:8000/auth/login"
bookmark_url = "http://localhost:8000/bookmarks/create"

for i in range(100):
    # Alternate between single and two-name usernames
    if i % 2 == 0:
        username = random.choice(first_names)
    else:
        username = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"user{i}@example.com"
    password = "123"
    website = random.choice(websites)

    # Register user
    register_data = {"username": username, "email": email, "password": password}
    reg_resp = requests.post(register_url, json=register_data)
    print(f"[{i}] Register: {username} | Status: {reg_resp.status_code}")

    # Login user
    login_data = {"username": username, "password": password}
    login_resp = requests.post(login_url, data=login_data)
    if login_resp.status_code == 200:
        access_token = login_resp.json().get("access_token")
        print(f"[{i}] Login: {username} | Status: {login_resp.status_code}")

        # Create bookmark
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        bookmark_data = {"original_url": website}
        bookmark_resp = requests.post(bookmark_url, json=bookmark_data, headers=headers)
        print(f"[{i}] Bookmark: {website} | Status: {bookmark_resp.status_code}")
    else:
        print(f"[{i}] Login failed for {username} | Status: {login_resp.status_code}")