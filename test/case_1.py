# In this case, user will create an account and will be automatically logged in, then, will change his dashboard name to "shop stock", then, will create a product and will register a sale of this product

from faker import Faker
import requests
# from json import dumps

BASE_URL = "http://localhost:8080/api"

fake = Faker("pt_BR")

firstName = fake.first_name()
lastName  = fake.last_name()

user_data = {
    "email": f"{firstName.lower()}.{lastName.lower()}@{fake.domain_name()}",
    "username": f"{firstName.lower()}_{lastName.lower().replace(" ", "_")}",
    "password": f"{fake.password(length=20)}",
    "firstName": firstName,
    "lastName": lastName
}

#region functions
def create_user():
    response = requests.post(url=f"{BASE_URL}/users/",
                             json=user_data)
    
    return [response.status_code, response.json()]

def update_dashboard(accessToken: str, dashboardName: str):
    response = requests.put(url=f"{BASE_URL}/dashboards/",
                            headers={"Authorization": f"Bearer {accessToken}"},
                            json={"dashboardName":dashboardName})
    
    return [response.status_code, response.json()]

def create_product(accessToken: str, name: str, price: float, cost: float, stock: int):
    response = requests.post(url=f"{BASE_URL}/products/",
                             headers={"Authorization": f"Bearer {accessToken}"},
                             json={
                                 "productName": name,
                                 "productPrice": price,
                                 "productCost": cost,
                                 "productStock": stock
                             })
    
    return [response.status_code, response.json()]

def register_sale(accessToken: str, productId: int, soldAmount: int):
    response = requests.post(url=f"{BASE_URL}/sales/{productId}",
                             headers={"Authorization":f"Bearer {accessToken}"},
                             json={"soldAmount":soldAmount})
    
    return [response.status_code, response.json()]
#endregion

created_user = create_user()
if created_user[0] == 201:
    accessToken = created_user[1]["accessToken"]

    updated_dashboard = update_dashboard(accessToken, "shop stock")
    created_product = create_product(accessToken, "Camiseta Corinthians Versão Torcedor I 25/26", 349.99, 10, 20)
    registered_sale = register_sale(accessToken, created_product[1]["product"]["productId"], 2)

    print(created_user[1]["message"])
    print(updated_dashboard[1]["message"] if updated_dashboard[0] == 200 else updated_dashboard[1]["error"])
    print(created_product[1]["message"] if created_product[0] == 201 else created_product[1]["error"])
    print(registered_sale[1]["message"] if registered_sale[0] == 201 else registered_sale[1]["error"])
else:
    print(f"Error:\n{created_user[1]["error"]}")
    raise SystemError("corre negadaaaaa")

# done, this shit is working.
