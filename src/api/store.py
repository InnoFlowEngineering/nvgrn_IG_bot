"""
In-memory storage for posts.
This is a simple demonstration - in production, use a proper database.
"""
from typing import Dict, List, Optional
from ..models import Post, PostStatus


class InMemoryStore:
    """Simple in-memory storage for posts."""
    
    def __init__(self):
        self.posts: Dict[str, Post] = {}
    
    def add_post(self, post: Post) -> Post:
        """Add a new post to the store."""
        if post.id:
            self.posts[post.id] = post
        return post
    
    def get_post(self, post_id: str) -> Optional[Post]:
        """Get a post by ID."""
        return self.posts.get(post_id)
    
    def get_posts(
        self,
        status: Optional[PostStatus] = None,
        account: Optional[str] = None
    ) -> List[Post]:
        """Get all posts with optional filtering."""
        posts = list(self.posts.values())
        
        if status:
            posts = [p for p in posts if p.status == status]
        
        if account:
            posts = [p for p in posts if p.account == account]
        
        # Sort by created_at descending
        posts.sort(key=lambda x: x.created_at, reverse=True)
        
        return posts
    
    def update_post(self, post_id: str, post: Post) -> Optional[Post]:
        """Update an existing post."""
        if post_id in self.posts:
            self.posts[post_id] = post
            return post
        return None
    
    def delete_post(self, post_id: str) -> bool:
        """Delete a post by ID."""
        if post_id in self.posts:
            del self.posts[post_id]
            return True
        return False
