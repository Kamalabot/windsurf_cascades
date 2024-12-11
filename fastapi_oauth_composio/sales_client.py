import requests
from datetime import datetime
from typing import Optional, Dict, List
import json

class SalesAPIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the Sales API client.
        
        Args:
            base_url: The base URL of the API (e.g., "http://localhost:8000")
            api_key: Optional API key for authentication
            token: Optional JWT token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.token = token

        # Automatically check API key or token validity
        if self.api_key:
            self.check_api_key()
        elif self.token:
            self.check_token()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        elif self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def check_api_key(self):
        """Check if the provided API key is valid by listing sales."""
        sales = self.list_sales()
        if sales:
            print("API key is valid.")
        else:
            print("Invalid API key. Please check your API key or server status.")

    def check_token(self):
        """Check if the provided JWT token is valid by listing sales."""
        headers = self._get_headers()  # Get headers with the token
        sales = requests.get(f"{self.base_url}/sales/", headers=headers)
        if sales.status_code == 200:
            print("JWT token is valid.")
        else:
            print("Invalid JWT token. Please check your token or server status.")

    def login(self, email: str, password: str) -> bool:
        """
        Login using email and password to get JWT token.
        
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

    def generate_api_key(self) -> Optional[str]:
        """Generate an API key for the current user."""
        try:
            response = requests.post(
                f"{self.base_url}/users/api-key/",
                headers=self._get_headers()
            )
            if response.status_code == 200:
                api_key = response.json()["api_key"]
                self.api_key = api_key
                return api_key
            return None
        except Exception as e:
            print(f"API key generation failed: {str(e)}")
            return None

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
    api_key = "1VgHFM_oU90Y8c-jl6fxdATRl6TB3UYxy08hmgzw_4o"  # Replace with your API key
    client = SalesAPIClient(base_url="http://localhost:8000", api_key=api_key)
    
    # Check API key by listing sales
    sales = client.list_sales()
    if sales:
        print("Listing all sales:")
        print(json.dumps(sales[:2], indent=2))  # Show first 2 sales
        
        # Get specific sale
        first_sale = client.get_sale(sales[0]["id"])
        if first_sale:
            print("First sale details:")
            print(json.dumps(first_sale, indent=2))
    else:
        print("Failed to list sales. Check API key or server status.")

    # Create a test user
    test_email = "testuser@example.com"
    test_password = "testpassword"
    new_user = client.create_user(test_email, test_password)
    if new_user:
        print("Test user created successfully!")
    else:
        print("Failed to create test user.")

if __name__ == "__main__":
    main()
