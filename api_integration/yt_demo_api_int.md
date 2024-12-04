# JSONPlaceholder API Integration Documentation

JSONPlaceholder is a free fake REST API for testing and prototyping. This document provides a detailed analysis of its endpoints and example responses.

## Base URL
```
https://jsonplaceholder.typicode.com
```

## Available Endpoints

### 1. Posts
#### GET /posts
Retrieves all posts

**Curl Command:**
```bash
curl https://jsonplaceholder.typicode.com/posts
```

**Example Response:**
```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  },
  {
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
  }
  // ... (98 more items)
]
```

Note: The actual response contains 100 posts. Above is a truncated version showing the first 2 posts for brevity.

#### GET /posts/{id}
Retrieves a specific post

**Example Response:**
```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati",
  "body": "quia et suscipit suscipit recusandae consequuntur"
}
```

#### POST /posts
Create a new post

**Curl Command:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"test_title","body":"test body","userId":5}' \
  https://jsonplaceholder.typicode.com/posts
```

**Request Body:**
```json
{
  "title": "test_title",
  "body": "test body",
  "userId": 5
}
```

**Response:**
```json
{
  "title": "test_title",
  "body": "test body",
  "userId": 5,
  "id": 101
}
```

Note: The API will simulate the creation of a new post and return the created object with an ID, but it won't actually be persisted to the server.

### 2. Comments
#### GET /comments
Retrieves all comments

**Example Response:**
```json
[
  {
    "postId": 1,
    "id": 1,
    "name": "id labore ex et quam laborum",
    "email": "Eliseo@gardner.biz",
    "body": "laudantium enim quasi est quidem magnam"
  }
]
```

#### GET /posts/{id}/comments
Retrieves comments for a specific post

**Example Response:**
```json
[
  {
    "postId": 1,
    "id": 1,
    "name": "id labore ex et quam laborum",
    "email": "Eliseo@gardner.biz",
    "body": "laudantium enim quasi est quidem magnam"
  }
]
```

### 3. Users
#### GET /users
Retrieves all users

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }
]
```

### 4. Todos
#### GET /todos
Retrieves all todos

**Example Response:**
```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
  }
]
```

### 5. Albums
#### GET /albums
Retrieves all albums

**Example Response:**
```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "quidem molestiae enim"
  }
]
```

### 6. Photos
#### GET /photos
Retrieves all photos

**Example Response:**
```json
[
  {
    "albumId": 1,
    "id": 1,
    "title": "accusamus beatae ad facilis cum similique qui sunt",
    "url": "https://via.placeholder.com/600/92c952",
    "thumbnailUrl": "https://via.placeholder.com/150/92c952"
  }
]
```

## Common Operations

### Filtering
You can filter resources using query parameters:
```
GET /posts?userId=1
GET /comments?postId=1
```

### Nested Resources
Access nested resources using:
```
GET /posts/1/comments
GET /albums/1/photos
GET /users/1/albums
```

### HTTP Methods Supported
- GET: Retrieve resources
- POST: Create resources
- PUT: Update resources
- PATCH: Partially update resources
- DELETE: Remove resources

### Response Codes
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Authentication
No authentication is required to use the JSONPlaceholder API.

## Rate Limiting
There are no rate limits, but the service is intended for testing and prototyping only.

## Notes
- All POST, PUT, PATCH, and DELETE requests are faked and will not persist
- The API returns placeholder data that follows a consistent schema
- All requests return JSON data
- Cross-Origin Resource Sharing (CORS) is enabled
