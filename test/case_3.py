# this is case 3, this case shows a user registering an account, creating a product, and then updating the product's information
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

def update_product(token, product_id, new_name, new_price):
    url = f"{BASE_URL}/api/products/{product_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "productName": new_name,
        "productPrice": new_price
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    # Register a new user
    user_data = register_user("testuser3", "test3@example.com", "password789")
    print("User registered:", user_data)
    access_token = user_data.get("accessToken")

    if access_token:
        # Create a product
        product_data = create_product(access_token, "Old Product Name", 99.99)
        print("Product created:", product_data)
        product_id = product_data.get("newProduct", {}).get("productId")

        if product_id:
            # Update the product
            updated_product_data = update_product(access_token, product_id, "New Product Name", 109.99)
            print("Product updated:", updated_product_data)
