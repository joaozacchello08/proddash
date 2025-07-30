import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

if __name__ == "__main__":
    BASE_URL = "http://localhost:8080/api"
    API_KEY = getenv("SECRET_KEY")

    data = {
        "email": "xongs@test.com",
        "username": "xongs",
        "password": "xongsLendario123#",
    }

    response = requests.post(url=f"{BASE_URL}/users/",
                             headers={
                                 "X-API-KEY": API_KEY
                             },
                             json=data)
    
    # print(response.json())
    response = requests.get(url=f"{BASE_URL}/users/")
