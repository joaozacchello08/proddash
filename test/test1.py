# 1. user create a account
# 2. user create a product

from dotenv import load_dotenv
from os import getenv
from faker import Faker
import requests
from json import dumps
load_dotenv()

#"https://proddash.onrender.com/api"
BASE_URL = ["http://localhost:8080/api", "https://proddash.onrender.com/api"]
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
    BASE_URL = BASE_URL[0] # CHANGE HERE

    # creating a user
    user_data = create_user()
    response = requests.post(url=f"{BASE_URL}/users/",
                             headers={
                                 "Content-type": "application/json",
                                 "X-API-KEY": API_KEY
                             },
                             json=user_data)
    
    response_json = response.json()

    if response.status_code != 201:
        print(f"Error creating user.\nStatus code: {response.status_code}\n{response.text}")
        quit()

    print(f"Created user:\n{dumps(response_json["createdUser"], indent=4)}")
    accessToken = response_json["accessToken"]

    # creating a product
    response = requests.post(url=f"{BASE_URL}/products/",
                             headers={
                                 "Content-type": "application/json",
                                 "X-API-KEY": API_KEY,
                                 "Authorization": f"Bearer {accessToken}"
                             },
                             json={
                                 "productName": "Camiseta",
                                 "productPrice": 200
                             })

    response_json = response.json()
    print(f"Created user:\n{dumps(response_json["product"], indent=4)}")
