"""
Content moderation rules for Instagram admin bot.
Rules:
1. No replies to negative comments/refunds - flag and hide
2. No competitor mentions - flag
3. Detect conflicts - flag
"""
import re
from typing import Tuple, Optional


# Predefined lists for content moderation
NEGATIVE_KEYWORDS = [
    'refund', 'money back', 'scam', 'fraud', 'terrible', 'worst', 
    'horrible', 'awful', 'disappointed', 'waste', 'never again'
]

COMPETITOR_KEYWORDS = [
    'competitor1', 'competitor2', 'competitor3',  # Replace with actual competitor names
    'other brand', 'alternative', 'instead of'
]

CONFLICT_KEYWORDS = [
    'controversy', 'lawsuit', 'dispute', 'complaint', 'violation',
    'issue', 'problem', 'concern'
]


def check_content_rules(content: str) -> Tuple[bool, Optional[str]]:
    """
    Check content against encoding rules.
    
    Args:
        content: The text content to check
        
    Returns:
        Tuple of (should_flag, reason)
    """
    content_lower = content.lower()
    
    # Check for negative/refund keywords
    for keyword in NEGATIVE_KEYWORDS:
        if keyword in content_lower:
            return True, f"Contains negative/refund keyword: '{keyword}'. No replies allowed, content hidden."
    
    # Check for competitor mentions
    for keyword in COMPETITOR_KEYWORDS:
        if keyword in content_lower:
            return True, f"Contains competitor mention: '{keyword}'. Flagged for review."
    
    # Check for conflict indicators
    for keyword in CONFLICT_KEYWORDS:
        if keyword in content_lower:
            return True, f"Contains conflict keyword: '{keyword}'. Flagged for review."
    
    return False, None


def hide_comment(comment_id: str) -> bool:
    """
    Stub function to hide a comment.
    In production, this would call Instagram API.
    """
    # Stub implementation
    print(f"[STUB] Hiding comment: {comment_id}")
    return True


def flag_content(content_id: str, reason: str) -> bool:
    """
    Stub function to flag content for review.
    In production, this would update the database.
    """
    # Stub implementation
    print(f"[STUB] Flagging content {content_id}: {reason}")
    return True
