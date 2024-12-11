import requests
from datetime import datetime
import json

BASE_URL = "http://localhost:8000"

def create_user(email: str, password: str):
    response = requests.post(
        f"{BASE_URL}/users/",
        json={"email": email, "password": password}
    )
    print("\nCreate User Response:", response.status_code)
    print(response.json() if response.status_code == 200 else response.text)
    return response.json() if response.status_code == 200 else None

def get_token(email: str, password: str):
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": email, "password": password}
    )
    print("\nGet Token Response:", response.status_code)
    print(response.json() if response.status_code == 200 else response.text)
    return response.json()["access_token"] if response.status_code == 200 else None

def list_sales(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales/", headers=headers)
    print("\nList Sales Response:", response.status_code)
    print(json.dumps(response.json(), indent=2) if response.status_code == 200 else response.text)
    return response.json() if response.status_code == 200 else None

def get_sale(token: str, sale_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales/{sale_id}", headers=headers)
    print("\nGet Sale Response:", response.status_code)
    print(json.dumps(response.json(), indent=2) if response.status_code == 200 else response.text)
    return response.json() if response.status_code == 200 else None

def create_sale(token: str, sale_data: dict):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/sales/", headers=headers, json=sale_data)
    print("\nCreate Sale Response:", response.status_code)
    print(json.dumps(response.json(), indent=2) if response.status_code == 200 else response.text)
    return response.json() if response.status_code == 200 else None

def main():
    # Test user creation and authentication
    email = "test@example.com"
    password = "testpassword123"
    
    print("=== Testing User Creation and Authentication ===")
    user = create_user(email, password)
    token = get_token(email, password)
    
    if not token:
        print("Failed to get token. Exiting...")
        return

    print("\n=== Testing Sales Endpoints ===")
    # List sales
    print("\nListing all sales:")
    sales = list_sales(token)
    
    if sales:
        # Get specific sale
        first_sale_id = sales[0]["id"]
        print(f"\nGetting sale with ID {first_sale_id}:")
        get_sale(token, first_sale_id)
    
    # Create new sale
    new_sale = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "product_name": "Test Product",
        "quantity": 5,
        "unit_price": 19.99,
        "total_amount": 99.95,
        "customer_name": "Test Customer"
    }
    print("\nCreating new sale:")
    create_sale(token, new_sale)

if __name__ == "__main__":
    main()
