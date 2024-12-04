import requests
import json

class JSONPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    @staticmethod
    def get_posts():
        """Fetch all posts from the API"""
        response = requests.get(f"{JSONPlaceholderClient.BASE_URL}/posts")
        return response.json()

    @staticmethod
    def get_post(post_id):
        """Fetch a specific post by ID"""
        response = requests.get(f"{JSONPlaceholderClient.BASE_URL}/posts/{post_id}")
        return response.json()

    @staticmethod
    def get_comments(post_id):
        """Fetch comments for a specific post"""
        response = requests.get(f"{JSONPlaceholderClient.BASE_URL}/posts/{post_id}/comments")
        return response.json()

    @staticmethod
    def get_users():
        """Fetch all users"""
        response = requests.get(f"{JSONPlaceholderClient.BASE_URL}/users")
        return response.json()

    @staticmethod
    def get_todos():
        """Fetch all todos"""
        response = requests.get(f"{JSONPlaceholderClient.BASE_URL}/todos")
        return response.json()
