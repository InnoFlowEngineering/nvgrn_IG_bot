#!/usr/bin/env python3
"""
Demo script for Instagram Admin Bot.
This script demonstrates the API functionality without the UI.
"""
import requests
import json
from datetime import datetime, timedelta


API_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_api():
    """Demonstrate the API functionality."""
    print_section("Instagram Admin Bot - API Demo")
    
    # 1. Check health
    print("1. Checking API health...")
    response = requests.get(f"{API_URL}/health")
    print(f"   Response: {response.json()}")
    
    # 2. Get accounts
    print("\n2. Getting available accounts...")
    response = requests.get(f"{API_URL}/accounts")
    print(f"   Accounts: {json.dumps(response.json(), indent=2)}")
    
    # 3. Create a regular post
    print("\n3. Creating a regular post...")
    post_data = {
        "account": "nvgrn_main",
        "upload_type": "post",
        "post_type": "dress",
        "context": "Check out our new summer dress collection! Perfect for any occasion. #fashion #style",
        "status": "draft"
    }
    response = requests.post(f"{API_URL}/posts", json=post_data)
    post1 = response.json()
    print(f"   Created post: {post1['id']}")
    print(f"   Flagged: {post1.get('flagged', False)}")
    
    # 4. Create a post with negative content (should be flagged)
    print("\n4. Creating a post with negative content (should be flagged)...")
    post_data = {
        "account": "nvgrn_events",
        "upload_type": "post",
        "post_type": "other",
        "context": "Some customers are asking for refunds but this is a terrible situation.",
        "status": "draft"
    }
    response = requests.post(f"{API_URL}/posts", json=post_data)
    post2 = response.json()
    print(f"   Created post: {post2['id']}")
    print(f"   Flagged: {post2.get('flagged', False)}")
    if post2.get('flagged'):
        print(f"   Reason: {post2.get('flag_reason')}")
    
    # 5. Create a scheduled post
    print("\n5. Creating a scheduled post...")
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    post_data = {
        "account": "nvgrn_shop",
        "upload_type": "reel",
        "post_type": "event",
        "event_name": "Summer Fashion Show",
        "event_date": "2024-07-15",
        "event_location": "Downtown Gallery",
        "context": "Join us for our exclusive summer fashion show! See the latest trends.",
        "publish_date": future_date,
        "status": "scheduled"
    }
    response = requests.post(f"{API_URL}/posts", json=post_data)
    post3 = response.json()
    print(f"   Created scheduled post: {post3['id']}")
    print(f"   Publish date: {post3.get('publish_date')}")
    
    # 6. List all posts
    print("\n6. Listing all posts...")
    response = requests.get(f"{API_URL}/posts")
    posts = response.json()
    print(f"   Total posts: {len(posts)}")
    for post in posts:
        print(f"   - {post['id'][:8]}... | {post['account']} | {post['status']} | Flagged: {post.get('flagged', False)}")
    
    # 7. Get statistics
    print("\n7. Getting statistics...")
    response = requests.get(f"{API_URL}/stats")
    stats = response.json()
    print(f"   Stats: {json.dumps(stats, indent=2)}")
    
    # 8. Test webhook (stub)
    print("\n8. Testing webhook (stub)...")
    webhook_payload = {
        "event_type": "post_published",
        "post_id": "test123",
        "timestamp": datetime.now().isoformat()
    }
    response = requests.post(f"{API_URL}/webhook", json=webhook_payload)
    print(f"   Webhook response: {response.json()}")
    
    print_section("Demo Complete!")
    print("✅ All API endpoints tested successfully")
    print("\nTo see the UI, run: python3 run_ui.py")


if __name__ == "__main__":
    try:
        demo_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API")
        print("Please start the API server first: python3 run_api.py")
        print("Then run this demo script again.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
