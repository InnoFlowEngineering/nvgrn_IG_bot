"""
FastAPI application for Instagram Admin Bot.
This is a demo/prerelease version with stub endpoints and in-memory storage.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import uuid

from ..models import Post, PostStatus, PostType, UploadType
from ..utils import check_content_rules
from .scheduler import scheduler_stub
from .store import InMemoryStore

app = FastAPI(
    title="Instagram Admin Bot API",
    description="Demo API for Instagram content management",
    version="0.1.0-prerelease"
)

# In-memory storage
store = InMemoryStore()


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    print("🚀 Instagram Admin Bot API starting up...")
    print("📊 In-memory store initialized")
    print("⏰ Scheduler stub ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 Instagram Admin Bot API shutting down...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Instagram Admin Bot API",
        "version": "0.1.0-prerelease",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "posts_count": len(store.posts)
    }


@app.post("/posts", response_model=Post)
async def create_post(post: Post, background_tasks: BackgroundTasks):
    """
    Create a new post.
    Applies content moderation rules automatically.
    """
    # Generate ID if not provided
    if not post.id:
        post.id = str(uuid.uuid4())
    
    # Check content rules
    should_flag, flag_reason = check_content_rules(post.context)
    if should_flag:
        post.flagged = True
        post.flag_reason = flag_reason
        print(f"⚠️  Post {post.id} flagged: {flag_reason}")
    
    # Store the post
    store.add_post(post)
    
    # Schedule if publish_date is set
    if post.publish_date and post.status == PostStatus.SCHEDULED:
        background_tasks.add_task(scheduler_stub, post.id, post.publish_date)
    
    return post


@app.get("/posts", response_model=List[Post])
async def list_posts(
    status: Optional[PostStatus] = None,
    account: Optional[str] = None
):
    """
    List all posts with optional filtering.
    """
    posts = store.get_posts(status=status, account=account)
    return posts


@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: str):
    """
    Get a specific post by ID.
    """
    post = store.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post_update: Post):
    """
    Update a post.
    """
    existing_post = store.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check content rules on update
    should_flag, flag_reason = check_content_rules(post_update.context)
    if should_flag:
        post_update.flagged = True
        post_update.flag_reason = flag_reason
    
    post_update.id = post_id
    store.update_post(post_id, post_update)
    return post_update


@app.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    """
    Delete a post.
    """
    success = store.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}


@app.post("/webhook")
async def webhook_handler(payload: dict):
    """
    Stub webhook endpoint for Instagram API callbacks.
    In production, this would handle actual Instagram events.
    """
    print(f"[WEBHOOK STUB] Received payload: {payload}")
    
    # Stub processing
    event_type = payload.get("event_type", "unknown")
    
    return {
        "status": "received",
        "event_type": event_type,
        "message": "Webhook stub - no actual processing in prerelease"
    }


@app.post("/posts/{post_id}/publish")
async def publish_post(post_id: str):
    """
    Manually publish a post immediately.
    Stub implementation - no actual Instagram API calls.
    """
    post = store.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.flagged:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot publish flagged post: {post.flag_reason}"
        )
    
    # Stub publish logic
    print(f"[PUBLISH STUB] Publishing post {post_id} to Instagram...")
    
    # Update status
    post.status = PostStatus.POSTED
    store.update_post(post_id, post)
    
    return {
        "message": "Post published successfully (stub)",
        "post_id": post_id
    }


@app.get("/accounts")
async def list_accounts():
    """
    Get list of available Instagram accounts.
    Stub implementation with hardcoded accounts.
    """
    return {
        "accounts": [
            {"id": "account1", "username": "nvgrn_main", "active": True},
            {"id": "account2", "username": "nvgrn_events", "active": True},
            {"id": "account3", "username": "nvgrn_shop", "active": True}
        ]
    }


@app.get("/stats")
async def get_stats():
    """
    Get statistics about posts.
    """
    all_posts = store.get_posts()
    
    stats = {
        "total_posts": len(all_posts),
        "by_status": {},
        "by_type": {},
        "flagged_count": sum(1 for p in all_posts if p.flagged)
    }
    
    for post in all_posts:
        # Count by status
        status_key = post.status.value
        stats["by_status"][status_key] = stats["by_status"].get(status_key, 0) + 1
        
        # Count by type
        type_key = post.post_type.value
        stats["by_type"][type_key] = stats["by_type"].get(type_key, 0) + 1
    
    return stats
