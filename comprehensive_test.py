#!/usr/bin/env python3
"""
Comprehensive test script for Instagram Admin Bot.
Tests all major functionality.
"""
import requests
import json
from datetime import datetime, timedelta


API_URL = "http://localhost:8000"


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_fail(text):
    """Print failure message."""
    print(f"❌ {text}")


def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")


def test_basic_endpoints():
    """Test basic API endpoints."""
    print_header("Test 1: Basic Endpoints")
    
    # Test root
    try:
        response = requests.get(f"{API_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "Instagram Admin Bot API" in data["message"]
        print_success("Root endpoint working")
    except Exception as e:
        print_fail(f"Root endpoint failed: {e}")
        return False
    
    # Test health
    try:
        response = requests.get(f"{API_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print_success("Health endpoint working")
    except Exception as e:
        print_fail(f"Health endpoint failed: {e}")
        return False
    
    # Test accounts
    try:
        response = requests.get(f"{API_URL}/accounts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["accounts"]) == 3
        print_success("Accounts endpoint working")
    except Exception as e:
        print_fail(f"Accounts endpoint failed: {e}")
        return False
    
    return True


def test_content_moderation():
    """Test content moderation rules."""
    print_header("Test 2: Content Moderation Rules")
    
    test_cases = [
        {
            "content": "Beautiful new dress collection!",
            "should_flag": False,
            "name": "Normal content"
        },
        {
            "content": "I want a refund this is terrible",
            "should_flag": True,
            "name": "Refund keyword"
        },
        {
            "content": "Check out competitor1 instead",
            "should_flag": True,
            "name": "Competitor mention"
        },
        {
            "content": "There's a lawsuit about this",
            "should_flag": True,
            "name": "Conflict keyword"
        }
    ]
    
    passed = 0
    for test_case in test_cases:
        try:
            post_data = {
                "account": "nvgrn_main",
                "upload_type": "post",
                "post_type": "other",
                "context": test_case["content"],
                "status": "draft"
            }
            
            response = requests.post(f"{API_URL}/posts", json=post_data)
            assert response.status_code == 200
            
            result = response.json()
            flagged = result.get("flagged", False)
            
            if flagged == test_case["should_flag"]:
                print_success(f"{test_case['name']}: correctly flagged={flagged}")
                passed += 1
            else:
                print_fail(f"{test_case['name']}: expected flagged={test_case['should_flag']}, got {flagged}")
            
        except Exception as e:
            print_fail(f"{test_case['name']} test failed: {e}")
    
    print_info(f"Passed {passed}/{len(test_cases)} moderation tests")
    return passed == len(test_cases)


def test_crud_operations():
    """Test CRUD operations on posts."""
    print_header("Test 3: CRUD Operations")
    
    # Create
    try:
        post_data = {
            "account": "nvgrn_main",
            "upload_type": "post",
            "post_type": "dress",
            "context": "Test post for CRUD operations",
            "status": "draft"
        }
        
        response = requests.post(f"{API_URL}/posts", json=post_data)
        assert response.status_code == 200
        created_post = response.json()
        post_id = created_post["id"]
        print_success(f"Created post with ID: {post_id[:8]}...")
    except Exception as e:
        print_fail(f"Create operation failed: {e}")
        return False
    
    # Read
    try:
        response = requests.get(f"{API_URL}/posts/{post_id}")
        assert response.status_code == 200
        retrieved_post = response.json()
        assert retrieved_post["id"] == post_id
        print_success(f"Retrieved post: {post_id[:8]}...")
    except Exception as e:
        print_fail(f"Read operation failed: {e}")
        return False
    
    # Update
    try:
        updated_data = retrieved_post.copy()
        updated_data["context"] = "Updated test post"
        
        response = requests.put(f"{API_URL}/posts/{post_id}", json=updated_data)
        assert response.status_code == 200
        updated_post = response.json()
        assert updated_post["context"] == "Updated test post"
        print_success(f"Updated post: {post_id[:8]}...")
    except Exception as e:
        print_fail(f"Update operation failed: {e}")
        return False
    
    # Delete
    try:
        response = requests.delete(f"{API_URL}/posts/{post_id}")
        assert response.status_code == 200
        
        # Verify deleted
        response = requests.get(f"{API_URL}/posts/{post_id}")
        assert response.status_code == 404
        print_success(f"Deleted post: {post_id[:8]}...")
    except Exception as e:
        print_fail(f"Delete operation failed: {e}")
        return False
    
    return True


def test_scheduling():
    """Test post scheduling."""
    print_header("Test 4: Post Scheduling")
    
    try:
        future_date = (datetime.now() + timedelta(hours=1)).isoformat()
        
        post_data = {
            "account": "nvgrn_events",
            "upload_type": "post",
            "post_type": "event",
            "event_name": "Test Event",
            "event_date": "2024-12-31",
            "event_location": "Test Location",
            "context": "Scheduled post test",
            "publish_date": future_date,
            "status": "scheduled"
        }
        
        response = requests.post(f"{API_URL}/posts", json=post_data)
        assert response.status_code == 200
        
        scheduled_post = response.json()
        assert scheduled_post["status"] == "scheduled"
        assert scheduled_post["publish_date"] is not None
        
        print_success(f"Created scheduled post for: {scheduled_post['publish_date'][:16]}")
        
        # Verify it appears in scheduled list
        response = requests.get(f"{API_URL}/posts?status=scheduled")
        assert response.status_code == 200
        scheduled_posts = response.json()
        
        assert any(p["id"] == scheduled_post["id"] for p in scheduled_posts)
        print_success(f"Scheduled post appears in list ({len(scheduled_posts)} total)")
        
        return True
        
    except Exception as e:
        print_fail(f"Scheduling test failed: {e}")
        return False


def test_filtering():
    """Test post filtering."""
    print_header("Test 5: Post Filtering")
    
    try:
        # Create posts with different statuses and accounts
        posts_to_create = [
            {"account": "nvgrn_main", "status": "draft"},
            {"account": "nvgrn_events", "status": "draft"},
            {"account": "nvgrn_main", "status": "posted"},
        ]
        
        for post_config in posts_to_create:
            post_data = {
                "account": post_config["account"],
                "upload_type": "post",
                "post_type": "other",
                "context": f"Test post for {post_config['account']} {post_config['status']}",
                "status": post_config["status"]
            }
            response = requests.post(f"{API_URL}/posts", json=post_data)
            assert response.status_code == 200
        
        print_success("Created test posts with different statuses/accounts")
        
        # Test status filtering
        response = requests.get(f"{API_URL}/posts?status=draft")
        draft_posts = response.json()
        assert all(p["status"] == "draft" for p in draft_posts)
        print_success(f"Status filtering works: {len(draft_posts)} draft posts")
        
        # Test account filtering
        response = requests.get(f"{API_URL}/posts?account=nvgrn_main")
        main_posts = response.json()
        assert all(p["account"] == "nvgrn_main" for p in main_posts)
        print_success(f"Account filtering works: {len(main_posts)} nvgrn_main posts")
        
        return True
        
    except Exception as e:
        print_fail(f"Filtering test failed: {e}")
        return False


def test_statistics():
    """Test statistics endpoint."""
    print_header("Test 6: Statistics")
    
    try:
        response = requests.get(f"{API_URL}/stats")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_posts" in stats
        assert "by_status" in stats
        assert "by_type" in stats
        assert "flagged_count" in stats
        
        print_success(f"Statistics endpoint working")
        print_info(f"  Total posts: {stats['total_posts']}")
        print_info(f"  Flagged posts: {stats['flagged_count']}")
        print_info(f"  By status: {stats['by_status']}")
        
        return True
        
    except Exception as e:
        print_fail(f"Statistics test failed: {e}")
        return False


def test_webhook():
    """Test webhook endpoint."""
    print_header("Test 7: Webhook (Stub)")
    
    try:
        webhook_data = {
            "event_type": "post_published",
            "post_id": "test123",
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.post(f"{API_URL}/webhook", json=webhook_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["status"] == "received"
        
        print_success("Webhook endpoint accepting payloads")
        
        return True
        
    except Exception as e:
        print_fail(f"Webhook test failed: {e}")
        return False


def main():
    """Run all tests."""
    print_header("Instagram Admin Bot - Comprehensive Test Suite")
    print_info(f"Testing API at: {API_URL}")
    
    try:
        # Quick connectivity check
        requests.get(f"{API_URL}/health", timeout=2)
    except:
        print_fail("Cannot connect to API!")
        print_info("Please start the API with: python3 run_api.py")
        return
    
    results = []
    
    # Run all tests
    results.append(("Basic Endpoints", test_basic_endpoints()))
    results.append(("Content Moderation", test_content_moderation()))
    results.append(("CRUD Operations", test_crud_operations()))
    results.append(("Scheduling", test_scheduling()))
    results.append(("Filtering", test_filtering()))
    results.append(("Statistics", test_statistics()))
    results.append(("Webhook", test_webhook()))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'='*70}\n")
    
    if passed == total:
        print_success("All tests passed! 🎉")
        print_info("The Instagram Admin Bot is working correctly.")
    else:
        print_fail(f"{total - passed} test(s) failed")
        print_info("Please check the output above for details.")


if __name__ == "__main__":
    main()
