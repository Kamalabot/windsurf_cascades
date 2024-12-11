# FastAPI Sales API with OAuth2 and API Key Authentication

This project implements a FastAPI server with both OAuth2 and API key authentication options for accessing a sales database through multiple endpoints.

## Project Structure
```
fastapi_oauth_composio/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── auth.py
├── sales_client.py
├── test_client.py
├── requirements.txt
└── instructions.md
```

## Features

1. Dual Authentication Methods:
   - OAuth2 Authentication with JWT tokens
   - API Key Authentication
2. SQLAlchemy database integration
3. CRUD operations for sales data
4. Secure password hashing
5. Python client library for easy API integration

## API Endpoints

1. `/users/` - POST: Create new user account
2. `/users/api-key/` - POST: Generate API key for authenticated user
3. `/token` - POST: Get access token (login)
4. `/sales/` - GET: List all sales (requires authentication)
5. `/sales/{sale_id}` - GET: Get specific sale details (requires authentication)
6. `/sales/` - POST: Create new sale entry (requires authentication)

## Authentication Methods

### 1. JWT Token Authentication
- Create a user account
- Obtain JWT token using email/password
- Include token in Authorization header: `Bearer <token>`

### 2. API Key Authentication
- Create a user account
- Login and generate API key
- Include API key in header: `X-API-Key: <api_key>`

## Authentication Functions

The `auth.py` file contains several functions that handle authentication for the FastAPI application:

1. **`verify_password(plain_password, hashed_password)`**: Verifies a plain password against a hashed password using the configured hashing algorithm.

2. **`get_password_hash(password)`**: Returns the hashed version of a given password.

3. **`get_user(db: Session, email: str)`**: Retrieves a user from the database by their email address.

4. **`authenticate_user(db: Session, email: str, password: str)`**: Authenticates a user by verifying their email and password. Returns the user object if successful, otherwise returns `False`.

5. **`create_access_token(data: dict, expires_delta: Optional[timedelta] = None)`**: Creates a JWT access token with an expiration time. The token includes the provided data.

6. **`generate_api_key()`**: Generates a secure random API key for user authentication.

7. **`get_api_key(api_key: str = Depends(api_key_header), db: Session = Depends(get_db))`**: Validates the provided API key by checking if it exists in the database and is associated with an active user.

8. **`get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))`**: Retrieves the current user based on the provided JWT token. Raises an exception if the token is invalid or expired.

9. **`get_current_user_or_api_key(api_key_user: models.User = Depends(get_api_key), token_user: models.User = Depends(get_current_user))`**: Checks for either a valid API key or JWT token to authenticate the user. Returns the user object if either method is valid, otherwise raises an exception.

These functions provide a comprehensive authentication mechanism for the FastAPI application, allowing for both API key and JWT token authentication.

## Database Schema

Sales Table:
- id: Integer (Primary Key)
- date: Date
- product_name: String
- quantity: Integer
- unit_price: Float
- total_amount: Float
- customer_name: String

Users Table:
- id: Integer (Primary Key)
- email: String (Unique)
- hashed_password: String
- is_active: Integer
- api_key: String (Unique)
- api_key_created_at: DateTime

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

4. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Using the Python Client

The project includes a Python client library (`sales_client.py`) that provides an easy way to interact with the API:

```python
from sales_client import SalesAPIClient

# Create client instance
client = SalesAPIClient("http://localhost:8000")

# Option 1: Use email/password authentication
client.login("user@example.com", "password123")

# Option 2: Use API key authentication
client = SalesAPIClient("http://localhost:8000", api_key="your-api-key")

# Use the client
sales = client.list_sales()
sale = client.get_sale(1)
new_sale = client.create_sale({
    "date": "2024-12-11",
    "product_name": "Test Product",
    "quantity": 5,
    "unit_price": 19.99,
    "total_amount": 99.95,
    "customer_name": "Test Customer"
})
```

## API Usage Examples

1. Create a new user:
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"password123"}'
```

2. Get access token:
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

3. Generate API key:
```bash
curl -X POST "http://localhost:8000/users/api-key/" \
  -H "Authorization: Bearer <your_jwt_token>"
```

4. List sales using API key:
```bash
curl -X GET "http://localhost:8000/sales/" \
  -H "X-API-Key: <your_api_key>"
```

5. Create new sale using API key:
```bash
curl -X POST "http://localhost:8000/sales/" \
  -H "X-API-Key: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-12-11",
    "product_name": "Test Product",
    "quantity": 5,
    "unit_price": 19.99,
    "total_amount": 99.95,
    "customer_name": "Test Customer"
  }'

```
