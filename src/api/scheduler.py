"""
Scheduler stub for scheduling posts.
In production, this would use APScheduler to actually schedule posts.
"""
from datetime import datetime
from typing import Optional


def scheduler_stub(post_id: str, publish_date: datetime) -> bool:
    """
    Stub function to schedule a post for future publication.
    
    In production, this would:
    1. Use APScheduler to schedule the job
    2. Store the job ID for later cancellation
    3. Actually publish to Instagram at the scheduled time
    
    Args:
        post_id: The ID of the post to schedule
        publish_date: When to publish the post
        
    Returns:
        True if scheduled successfully (stub always returns True)
    """
    print(f"[SCHEDULER STUB] Scheduled post {post_id} for {publish_date.isoformat()}")
    print(f"[SCHEDULER STUB] In production, APScheduler would handle this")
    return True


def cancel_scheduled_post_stub(post_id: str) -> bool:
    """
    Stub function to cancel a scheduled post.
    
    Args:
        post_id: The ID of the post to cancel
        
    Returns:
        True if cancelled successfully (stub always returns True)
    """
    print(f"[SCHEDULER STUB] Cancelled scheduled post {post_id}")
    return True


def get_scheduled_jobs_stub() -> list:
    """
    Stub function to get all scheduled jobs.
    
    Returns:
        Empty list (stub implementation)
    """
    print("[SCHEDULER STUB] Getting scheduled jobs - none in stub mode")
    return []
