import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    BigInteger,
    Numeric,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class CreatorDB(Base):
    __tablename__ = "creators"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    bio = Column(Text, nullable=True)
    primary_domain = Column(String(100), default="Tech & AI")
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    profiles = relationship("CreatorProfileDB", back_populates="creator", cascade="all, delete-orphan")
    platforms = relationship("CreatorPlatformDB", back_populates="creator", cascade="all, delete-orphan")
    content_items = relationship("ContentItemDB", back_populates="creator", cascade="all, delete-orphan")

class CreatorProfileDB(Base):
    __tablename__ = "creator_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    creator_id = Column(String(36), ForeignKey("creators.id", ondelete="CASCADE"), nullable=False, index=True)
    user_md_content = Column(Text, nullable=False)
    hook_md_content = Column(Text, nullable=False)
    tone_blueprint = Column(JSON, default=dict)
    video_length_analysis = Column(JSON, default=dict)
    video_taxonomy = Column(JSON, default=list)
    thumbnail_strategy = Column(JSON, default=dict)
    frequent_spoken_phrases = Column(JSON, default=list)
    catalog_summary = Column(JSON, default=dict)
    custom_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    creator = relationship("CreatorDB", back_populates="profiles")

class CreatorPlatformDB(Base):
    __tablename__ = "creator_platforms"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    creator_id = Column(String(36), ForeignKey("creators.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False) # youtube, substack, linkedin, twitter
    handle_or_url = Column(String(255), nullable=False)
    is_connected = Column(Boolean, default=True)
    followers_or_subscribers = Column(BigInteger, default=0)
    total_views_or_impressions = Column(BigInteger, default=0)
    total_content_pieces = Column(Integer, default=0)
    avg_engagement_rate = Column(Numeric(5, 2), default=0.00)
    growth_rate_30d = Column(Numeric(5, 2), default=0.00)
    platform_metadata = Column(JSON, default=dict)
    last_synced_at = Column(DateTime(timezone=True), default=utc_now)

    creator = relationship("CreatorDB", back_populates="platforms")

class ContentItemDB(Base):
    __tablename__ = "content_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    creator_id = Column(String(36), ForeignKey("creators.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    external_id = Column(String(255), nullable=True)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    content_format = Column(String(50), nullable=False) # video, short, article, post
    duration_seconds = Column(Integer, default=0)
    view_count = Column(BigInteger, default=0)
    upload_date = Column(String(50), nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    transcript_snippet = Column(Text, nullable=True)
    key_opening_words = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    creator = relationship("CreatorDB", back_populates="content_items")

class TrendsCacheDB(Base):
    __tablename__ = "trends_cache"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    domain = Column(String(100), nullable=False, index=True)
    geo = Column(String(10), default="US")
    world_trends = Column(JSON, default=list)
    niche_trends = Column(JSON, default=list)
    viral_formats = Column(JSON, default=list)
    opportunity_matrix = Column(JSON, default=list)
    fetched_at = Column(DateTime(timezone=True), default=utc_now)

class PublishJobDB(Base):
    __tablename__ = "publish_jobs"

    job_id = Column(String(50), primary_key=True)
    creator_id = Column(String(255), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    content_format = Column(String(50), nullable=False)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    media_urls = Column(JSON, default=list)
    thumbnail_url = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    status = Column(String(50), default="PENDING_APPROVAL", index=True)
    requires_human_approval = Column(Boolean, default=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    reviewer_name = Column(String(255), nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    composio_action = Column(String(100), nullable=True)
    composio_execution_status = Column(String(50), default="WAITING_FOR_HUMAN_APPROVAL")
    composio_output = Column(JSON, nullable=True)
    published_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejected_at = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
