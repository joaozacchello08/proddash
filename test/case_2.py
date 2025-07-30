# In this case user will create an account and will get logged in automatically, then, will change his dashboard name to "shop stock", will create 5 products and then will open his dashboard

from faker import Faker
import requests

BASE_URL = "http://localhost:8080/api"
fake = Faker("pt_BR")

# Usuário fake
firstName = fake.first_name()
lastName  = fake.last_name()
user_data = {
    "email": f"{firstName.lower()}.{lastName.lower()}@{fake.domain_name()}",
    "username": f"{firstName.lower()}_{lastName.lower().replace(' ', '_')}",
    "password": fake.password(length=20),
    "firstName": firstName,
    "lastName": lastName
}

# Funções da API
def create_user():
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    return [response.status_code, response.json()]

def update_dashboard_name(token: str, new_name: str):
    response = requests.put(f"{BASE_URL}/dashboards/",
                            headers={"Authorization": f"Bearer {token}"},
                            json={"dashboardName": new_name})
    return [response.status_code, response.json()]

def create_product(token: str, name: str, price: float, cost: float, stock: int):
    response = requests.post(f"{BASE_URL}/products/",
                             headers={"Authorization": f"Bearer {token}"},
                             json={
                                 "productName": name,
                                 "productPrice": price,
                                 "productCost": cost,
                                 "productStock": stock
                             })
    return [response.status_code, response.json()]

def get_all_products(token: str):
    response = requests.get(f"{BASE_URL}/products/",
                            headers={"Authorization": f"Bearer {token}"})
    return [response.status_code, response.json()]

# Execução do fluxo
created_user = create_user()
if created_user[0] == 201:
    accessToken = created_user[1]["accessToken"]

    updated_dashboard = update_dashboard_name(accessToken, "shop stock")

    product_names = [
        "Camisa São Paulo II 2025",
        "Tênis Nike Air Max 2025",
        "Garrafa Térmica Stanley 1L",
        "Notebook Dell i7 16GB RAM",
        "Café Especial Orgânico 500g"
    ]

    created_products = []
    for name in product_names:
        status, response = create_product(accessToken, name, price=99.90, cost=30.00, stock=15)
        created_products.append((status, response))
    
    # Carrega todos os produtos do dashboard
    loaded_products = get_all_products(accessToken)

    # Prints de resultados
    print("✅ Usuário criado:", created_user[1]["message"])
    print("✅ Dashboard renomeado:", updated_dashboard[1].get("message", updated_dashboard[1].get("error")))

    for i, (status, resp) in enumerate(created_products):
        print(f"✅ Produto {i+1} criado:", resp.get("message", resp.get("error")))

    print(f"✅ Produtos carregados ({len(loaded_products[1])} encontrados):")
    for prod in loaded_products[1]:
        print(f"  - {prod['productName']} | Estoque: {prod['productStock']} | Preço: R${prod['productPrice']:.2f}")

else:
    print(f"Erro ao criar usuário:\n{created_user[1].get('error', created_user[1])}")
    raise SystemExit("Erro fatal na criação do usuário.")
