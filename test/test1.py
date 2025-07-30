from dotenv import load_dotenv
from os import getenv
load_dotenv()
API_KEY=getenv("SECRET_KEY")

from requests import post
from json import dumps

BASE_URL = "http://127.0.0.1:8000/api"

user_data = {
    "email": "test@test.com",
    "username": "xester",
    "password": "xester123!"
}

response = post(url=f"{BASE_URL}/users/",
                headers={
                    "Content-type": "application/json",
                    "X-API-KEY": API_KEY
                },
                json=user_data)

print(dumps(response.json(), indent=4))
