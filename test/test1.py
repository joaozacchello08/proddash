# 1. user create a account
# 2. user create a product

from dotenv import load_dotenv
from os import getenv
from faker import Faker
import requests
from json import dumps
load_dotenv()

BASE_URL = "https://proddash.onrender.com/api"
API_KEY = getenv("SECRET_KEY")
fake = Faker("pt_BR")

def create_user() -> dict[str, str]:
    firstName = fake.first_name()
    lastName  = fake.last_name()

    return {
        "email": f"{firstName.lower()}.{lastName.lower()}@{fake.domain_name()}".replace(" ", ""),
        "username": f"{firstName.lower()}_{lastName.lower()}".replace(" ", ""),
        "password": fake.password(20),
        "firstName": firstName,
        "lastName": lastName
    }

if __name__ == "__main__":
    # creating a user
    user_data = create_user()
    response = requests.post(url=f"{BASE_URL}/users/",
                             headers={
                                 "Content-type": "application/json",
                                 "X-API-KEY": API_KEY
                             },
                             json=user_data)
    
    if response.status_code != 201:
        print(f"Error creating user.\nStatus code: {response.status_code}")
        quit()
    
    response_json = response.json()

    print(f"Created user:\n{dumps(response_json["createdUser"], indent=4)}")
    accessToken = response_json["accessToken"]

    # creating a product

