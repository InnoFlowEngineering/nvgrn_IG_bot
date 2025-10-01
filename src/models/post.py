from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UploadType(str, Enum):
    POST = "post"
    REEL = "reel"
    STORY = "story"


class PostType(str, Enum):
    DRESS = "dress"
    EVENT = "event"
    FOLLOW_UP = "follow-up"
    POST_EVENT = "post-event"
    OTHER = "other"


class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"


class Post(BaseModel):
    id: Optional[str] = None
    account: str
    upload_type: UploadType
    post_type: PostType
    event_name: Optional[str] = None
    event_date: Optional[str] = None
    event_location: Optional[str] = None
    context: str
    publish_date: Optional[datetime] = None
    status: PostStatus = PostStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.now)
    flagged: bool = False
    flag_reason: Optional[str] = None
