#!/bin/bash

# Output file
MD_FILE="api_integration.md"
BASE_URL="https://jsonplaceholder.typicode.com"

# Function to append content to the markdown file
append_to_md() {
    echo -e "$1" >> "$MD_FILE"
}

# Clear existing content after the header
sed -i '/## API Endpoints/q' "$MD_FILE"
append_to_md "\n### GET Requests\n"

# GET /posts
append_to_md "\n#### GET /posts (First Post)\n\`\`\`json"
curl -s "${BASE_URL}/posts/1" | jq '.' >> "$MD_FILE"
append_to_md "\`\`\`"

# GET /comments for a post
append_to_md "\n#### GET /posts/1/comments (First Comment)\n\`\`\`json"
curl -s "${BASE_URL}/posts/1/comments" | jq '.[0]' >> "$MD_FILE"
append_to_md "\`\`\`"

# GET /users
append_to_md "\n#### GET /users (First User)\n\`\`\`json"
curl -s "${BASE_URL}/users/1" | jq '.' >> "$MD_FILE"
append_to_md "\`\`\`"

# POST example
append_to_md "\n### POST Requests\n"
append_to_md "\n#### POST /posts\n\`\`\`json"
curl -s -X POST "${BASE_URL}/posts" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }' | jq '.' >> "$MD_FILE"
append_to_md "\`\`\`"

echo "API requests completed and results saved to $MD_FILE"
