from api_client import JSONPlaceholderClient
import json

def display_results(data, title="Results"):
    """Display the results in a formatted way"""
    print("\n" + "="*50)
    print(f"{title}:")
    print("="*50)
    print(json.dumps(data, indent=2))
    print("="*50 + "\n")

def main():
    client = JSONPlaceholderClient()
    
    # Example 1: Get all posts
    posts = client.get_posts()
    display_results(posts[:3], "First 3 Posts")  # Show only first 3 posts for brevity
    
    # Example 2: Get a specific post
    post = client.get_post(1)
    display_results(post, "Post #1")
    
    # Example 3: Get comments for post #1
    comments = client.get_comments(1)
    display_results(comments[:2], "First 2 Comments for Post #1")
    
    # Example 4: Get users
    users = client.get_users()
    display_results(users[:2], "First 2 Users")

if __name__ == "__main__":
    main()
