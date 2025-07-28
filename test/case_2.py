# this is case 2, this case shows a user registering an account, creating a product, and then registering a sale for that product
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

def create_product(token, name, price, stock):
    url = f"{BASE_URL}/api/products/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "productName": name,
        "productPrice": price,
        "productStock": stock
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def register_sale(token, product_id, amount):
    url = f"{BASE_URL}/api/sales/{product_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "soldAmount": amount
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    # Register a new user
    user_data = register_user("testuser2", "test2@example.com", "password456")
    print("User registered:", user_data)
    access_token = user_data.get("accessToken")

    if access_token:
        # Create a product
        product_data = create_product(access_token, "Product A", 15.00, 50)
        print("Product created:", product_data)
        product_id = product_data.get("newProduct", {}).get("productId")

        if product_id:
            # Register a sale
            sale_data = register_sale(access_token, product_id, 5)
            print("Sale registered:", sale_data)
