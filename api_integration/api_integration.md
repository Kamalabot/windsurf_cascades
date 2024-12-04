# JSONPlaceholder API Integration

## About JSONPlaceholder

[JSONPlaceholder](https://jsonplaceholder.typicode.com) is a free online REST API designed for testing and prototyping. It provides a set of common API endpoints that return realistic data, making it perfect for:
- Testing API integrations
- Prototyping applications
- Learning REST API concepts
- Creating example code and documentation

Base URL: `https://jsonplaceholder.typicode.com`

The API is maintained by [Typicode](https://typicode.com) and is widely used by developers worldwide for testing and educational purposes. All data is mock data and will not be permanently modified when using POST, PUT, or DELETE requests.

## JSONPlaceholder API Integration Results

This file contains the results of various API requests to JSONPlaceholder.

## API Endpoints

### GET Requests


#### GET /posts
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
]
```

*Note: Showing first 2 posts for brevity. The API returns 100 posts in total.*

#### GET /posts/1/comments (First Comment)
```json
{
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
}
```

#### GET /users (First User)
```json
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
```

#### GET /todos Request and Response

Command:
```bash
curl -s https://jsonplaceholder.typicode.com/todos | jq '.[0:2]'
```

Response:
```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
  },
  {
    "userId": 1,
    "id": 2,
    "title": "quis ut nam facilis et officia qui",
    "completed": false
  }
]
```

*Note: The command uses `jq '.[0:2]'` to show only the first 2 todos. The API returns 200 todos in total.*

### Posts Grid View

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; padding: 20px; max-width: 1200px; margin: 0 auto;">
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: #333; font-size: 1.2em; margin-bottom: 10px; font-weight: bold;">sunt aut facere repellat provident occaecati excepturi optio reprehenderit</div>
        <div style="color: #666; line-height: 1.5;">quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto</div>
        <div style="color: #888; font-size: 0.9em; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">Post ID: 1 | User ID: 1</div>
    </div>
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: #333; font-size: 1.2em; margin-bottom: 10px; font-weight: bold;">qui est esse</div>
        <div style="color: #666; line-height: 1.5;">est rerum tempore vitae sequi sint nihil reprehenderit dolor beatae ea dolores neque fugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis</div>
        <div style="color: #888; font-size: 0.9em; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">Post ID: 2 | User ID: 1</div>
    </div>
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: #333; font-size: 1.2em; margin-bottom: 10px; font-weight: bold;">ea molestias quasi exercitationem repellat qui ipsa sit aut</div>
        <div style="color: #666; line-height: 1.5;">et iusto sed quo iure voluptatem occaecati omnis eligendi aut ad voluptatem doloribus vel accusantium quis pariatur molestiae porro eius odio et labore et velit aut</div>
        <div style="color: #888; font-size: 0.9em; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">Post ID: 3 | User ID: 1</div>
    </div>
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: #333; font-size: 1.2em; margin-bottom: 10px; font-weight: bold;">eum et est occaecati</div>
        <div style="color: #666; line-height: 1.5;">ullam et saepe reiciendis voluptatem adipisci sit amet autem assumenda provident rerum culpa quis hic commodi nesciunt rem tenetur doloremque ipsam iure</div>
        <div style="color: #888; font-size: 0.9em; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">Post ID: 4 | User ID: 1</div>
    </div>
</div>

### Posts per User Bar Chart

<div style="padding: 20px; max-width: 800px; margin: 0 auto;">
    <h3 style="text-align: center; color: #333;">Number of Posts by User</h3>
    <div style="display: flex; align-items: flex-end; height: 300px; padding: 20px; background: #f5f5f5; border-radius: 8px;">
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #4CAF50; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 1</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #2196F3; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 2</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #FFC107; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 3</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #9C27B0; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 4</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #FF5722; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 5</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #795548; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 6</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #607D8B; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 7</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #E91E63; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 8</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #009688; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 9</div>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; margin: 0 5px;">
            <div style="width: 40px; height: 200px; background: #673AB7; margin-bottom: 10px; position: relative;">
                <div style="position: absolute; top: -25px; width: 100%; text-align: center;">10</div>
            </div>
            <div style="text-align: center;">User 10</div>
        </div>
    </div>
</div>

*Note: Each user has created exactly 10 posts in the system.*

### POST Requests

#### POST /posts

Command:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "title": "foo",
  "body": "bar",
  "userId": 1
}' https://jsonplaceholder.typicode.com/posts
```

Response:
```json
{
  "title": "foo",
  "body": "bar",
  "userId": 1,
  "id": 101
}
```
