import requests
import dotenv
import os
import json

dotenv.load_dotenv()

key = os.getenv("SECRET_KEY")

# create user
resp = requests.post(url="http://localhost:6969/api/users/",
                     headers={
                         "Content-type": "application/json",
                         "X-API-KEY": key
                     },
                     json={
                         "email": "xongs@test.com",
                         "username": "xongs",
                         "password": "xester123"
                     }
)
resp = resp.json()
accessToken = resp["accessToken"]
# print(json.dumps(resp, indent=4))

resp = requests.get(url="http://localhost:6969/api/users/",
                    headers={
                        "X-API-KEY": key,
                        "Authorization": f"Bearer {accessToken}"
                    })

resp = resp.json()
print(json.dumps(resp, indent=4))
