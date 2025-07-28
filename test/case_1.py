# this is case 1, this case shows a user registering an account, changing his dashboard to 'shop stock' and creating three products
import requests
import json

BASE_URL = "http://localhost:8080"

def register_user(username, email, password):
    url = f"{BASE_URL}/api/users/"
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    return response.json()

def change_dashboard_name(token, new_name):
    url = f"{BASE_URL}/api/dashboards/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "dashboardName": new_name
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def create_product(token, name, price):
    url = f"{BASE_URL}/api/products/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "productName": name,
        "productPrice": price
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    # Register a new user
    user_data = register_user("testuser1", "test1@example.com", "password123")
    print("User registered:", user_data)
    access_token = user_data.get("accessToken")

    if access_token:
        # Change dashboard name
        dashboard_data = change_dashboard_name(access_token, "shop stock")
        print("Dashboard updated:", dashboard_data)

        # Create three products
        product1 = create_product(access_token, "Product 1", 10.99)
        print("Product 1 created:", product1)
        product2 = create_product(access_token, "Product 2", 20.49)
        print("Product 2 created:", product2)
        product3 = create_product(access_token, "Product 3", 5.99)
        print("Product 3 created:", product3)
