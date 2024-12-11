import requests
from datetime import datetime
from typing import Optional, Dict, List
import json

class SalesAPIKeyClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the Sales API client with API key authentication.
        
        Args:
            base_url: The base URL of the API (e.g., "http://localhost:8000")
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def set_api_key(self, api_key: str):
        """Set the API key for authentication."""
        self.api_key = api_key

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


def generate_api_key(base_url: str, email: str, password: str) -> Optional[str]:
    """
    Helper function to generate an API key using email/password authentication.
    
    Args:
        base_url: The base URL of the API
        email: User's email
        password: User's password
        
    Returns:
        Optional[str]: API key if successful, None otherwise
    """
    from sales_client import SalesAPIClient
    
    # Create a regular client to login and generate API key
    client = SalesAPIClient(base_url=base_url)
    
    # Login with credentials
    if not client.login(email, password):
        print("Failed to login with credentials.")
        return None
    
    # Generate API key
    try:
        response = requests.post(
            f"{base_url}/users/api-key/",
            headers={"Authorization": f"Bearer {client.token}"}
        )
        if response.status_code == 200:
            return response.json()["api_key"]
        print(f"Failed to generate API key: {response.status_code}")
        return None
    except Exception as e:
        print(f"Failed to generate API key: {str(e)}")
        return None


def main():
    base_url = "http://localhost:8000"
    email = "testuser@gmail.com"
    password = "1234"
    
    # Step 1: Generate API key
    print(f"Generating API key for user: {email}")
    api_key = generate_api_key(base_url, email, password)
    
    if not api_key:
        print("Failed to generate API key. Exiting.")
        return
    
    print(f"Successfully generated API key: {api_key}")
    
    # Step 2: Create API key client and test endpoints
    client = SalesAPIKeyClient(base_url=base_url, api_key=api_key)
    
    # Test listing sales
    print("\nTesting sales listing...")
    sales = client.list_sales(limit=2)
    if sales:
        print("Successfully retrieved sales:")
        print(json.dumps(sales, indent=2))
        
        # Test getting specific sale
        if len(sales) > 0:
            sale_id = sales[0]["id"]
            print(f"\nTesting get sale (ID: {sale_id})...")
            sale = client.get_sale(sale_id)
            if sale:
                print("Successfully retrieved sale details:")
                print(json.dumps(sale, indent=2))
    
    # Test creating a new sale
    print("\nTesting sale creation...")
    new_sale = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "product_name": "Test Product",
        "quantity": 1,
        "unit_price": 99.99,
        "total_amount": 99.99,
        "customer_name": "API Key Test Customer"
    }
    
    created_sale = client.create_sale(new_sale)
    if created_sale:
        print("Successfully created new sale:")
        print(json.dumps(created_sale, indent=2))


if __name__ == "__main__":
    main()
