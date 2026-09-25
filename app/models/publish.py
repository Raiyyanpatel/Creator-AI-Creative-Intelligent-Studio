from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field

class PlatformType(str, Enum):
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    SUBSTACK = "substack"

class ContentFormat(str, Enum):
    VIDEO = "video"
    SHORT = "short"
    POST = "post"
    THREAD = "thread"
    ARTICLE = "article"

class JobStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

class PublishCreateRequest(BaseModel):
    creator_id: str = Field(..., description="ID or slug of creator (e.g. 'ali-abdaal')")
    platform: PlatformType
    content_format: ContentFormat
    title: Optional[str] = Field(None, description="Title for video/article/short")
    content: str = Field(..., description="Post body text, thread list, or video caption/script")
    media_urls: Optional[List[str]] = Field(default_factory=list, description="Media attachments or video file URLs")
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    scheduled_for: Optional[str] = Field(None, description="ISO timestamp for future scheduled post")
    require_human_approval: bool = Field(True, description="Strictly requires approval before Composio dispatches")

class HumanApprovalRequest(BaseModel):
    reviewer_name: str = Field("Creator Admin", description="Name of person approving")
    feedback: Optional[str] = Field(None, description="Review notes or approval comments")
    override_content: Optional[str] = Field(None, description="Optional edited copy by human reviewer")

class HumanRejectionRequest(BaseModel):
    reviewer_name: str = Field("Creator Admin", description="Name of person rejecting")
    rejection_reason: str = Field(..., description="Why the content was rejected (e.g., brand tone mismatch)")

class PublishJob(BaseModel):
    job_id: str
    creator_id: str
    platform: PlatformType
    content_format: ContentFormat
    title: Optional[str]
    content: str
    media_urls: List[str]
    thumbnail_url: Optional[str]
    tags: List[str]
    status: JobStatus
    requires_human_approval: bool
    created_at: str
    approved_at: Optional[str] = None
    rejected_at: Optional[str] = None
    published_at: Optional[str] = None
    reviewer_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    composio_action: Optional[str] = None
    composio_execution_status: Optional[str] = None
    composio_output: Optional[Dict[str, Any]] = None
    published_url: Optional[str] = None

class PublishResponse(BaseModel):
    status: str
    message: str
    job: PublishJob
