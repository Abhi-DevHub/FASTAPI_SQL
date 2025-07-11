# "id":"99e3b1-d594-4b9e-acd9-d19bc6568fa3"


import requests

bookmark_id = "99e3b1-d594-4b9e-acd9-d19bc6568fa3"
headers = {"Authorization": f"Bearer {access_token}"}
url = f"http://localhost:8000/bookmarks/get/{bookmark_id}"

response = requests.get(url, headers=headers)
print(response.json())