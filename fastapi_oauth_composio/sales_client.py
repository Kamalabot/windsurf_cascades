import requests
from datetime import datetime
from typing import Optional, Dict, List
import json

class SalesAPIClient:
    def __init__(self, base_url: str):
        """
        Initialize the Sales API client.
        
        Args:
            base_url: The base URL of the API (e.g., "http://localhost:8000")
        """
        self.base_url = base_url.rstrip('/')
        self.token = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email: str, password: str) -> bool:
        """
        Login using email and password to get JWT token.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            response = requests.post(
                f"{self.base_url}/token",
                data={"username": email, "password": password}
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                return True
            return False
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def list_sales(self, skip: int = 0, limit: int = 100) -> Optional[List[Dict]]:
        """List all sales."""
        try:
            response = requests.get(
                f"{self.base_url}/sales/",
                params={"skip": skip, "limit": limit},
                headers=self._get_headers()
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"List sales failed: {str(e)}")
            return None

    def get_sale(self, sale_id: int) -> Optional[Dict]:
        """Get a specific sale by ID."""
        try:
            response = requests.get(
                f"{self.base_url}/sales/{sale_id}",
                headers=self._get_headers()
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Get sale failed: {str(e)}")
            return None

    def create_sale(self, sale_data: Dict) -> Optional[Dict]:
        """Create a new sale."""
        try:
            response = requests.post(
                f"{self.base_url}/sales/",
                headers=self._get_headers(),
                json=sale_data
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Create sale failed: {str(e)}")
            return None

    def create_user(self, email: str, password: str) -> Optional[Dict]:
        """Create a new user."""
        try:
            response = requests.post(
                f"{self.base_url}/users/",
                headers=self._get_headers(),
                json={"email": email, "password": password}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Create user failed: {str(e)}")
            return None


def main():
    # Example usage
    client = SalesAPIClient(base_url="http://localhost:8000")
    
    # Example 1: Create a new user (registration)
    print("Example 1: User Registration")
    new_email = "testuser@gmail.com"
    new_password = "1234"
    new_user = client.create_user(new_email, new_password)
    if new_user:
        print(f"Successfully registered user: {new_email}")
    else:
        print("Failed to register new user")
    
    # Example 2: Login Process
    print("\nExample 2: Login Process")
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        print(f"Attempting to login ({email})...")
        if client.login(email, password):
            print("Successfully logged in!")
            break
        else:
            attempt += 1
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"Login failed. {remaining} attempts remaining.")
            else:
                print("Maximum login attempts reached.")
                return
    
    # Only proceed if login was successful
    if client.token:
        print("\nFetching sales data...")
        sales = client.list_sales()
        if sales:
            print("Listing all sales:")
            print(json.dumps(sales[:2], indent=2))  # Show first 2 sales
            
            # Get specific sale
            first_sale = client.get_sale(sales[0]["id"])
            if first_sale:
                print("\nFirst sale details:")
                print(json.dumps(first_sale, indent=2))
        else:
            print("Failed to list sales. Please check your authentication status.")

if __name__ == "__main__":
    main()
