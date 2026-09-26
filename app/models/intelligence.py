"""
Platform Intelligence Models
=============================
Pydantic schemas for the cross-platform trend discovery and
platform.md generation system.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class PlatformChoice(str, Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    X_TWITTER = "x_twitter"


class GoalType(str, Enum):
    INCREASE_REACH = "increase_reach"
    INCREASE_FOLLOWERS = "increase_followers"
    INCREASE_SUBSCRIBERS = "increase_subscribers"
    MORE_VIEWS_AND_FOLLOWERS = "more_views_and_followers"
    INCREASE_CONNECTIONS = "increase_connections"
    SPREAD_DOMAIN_POSTS = "spread_domain_posts"
    INCREASE_ENGAGEMENT = "increase_engagement"
    BRAND_AUTHORITY = "brand_authority"


# ──────────────────────────────────────────────
# Request
# ──────────────────────────────────────────────

class IntelligenceRequest(BaseModel):
    creator_name: str = Field(..., description="Creator's display name or handle")
    niche: Optional[str] = Field("auto", description="Creator's primary niche/domain (e.g. 'Tech & Gadgets', 'Finance & Investing', 'Social Causes', 'Productivity', or 'auto' for automatic detection)")
    causes_or_topics: Optional[List[str]] = Field(
        None,
        description="Creator's specific causes or topics of work (e.g. ['Environmental Crisis', 'Civic Awareness', 'Public Policy']) to find trends related to their work rather than personal news"
    )
    language: Optional[str] = Field(
        None,
        description="Creator's native spoken language code (e.g. 'hi' for Hindi/Hinglish, 'en' for English, 'es' for Spanish). Auto-detected if omitted."
    )
    location: str = Field("US", description="Country/region code for location-based trends (e.g. 'US', 'IN', 'GB')")
    platforms: List[PlatformChoice] = Field(
        default=[PlatformChoice.YOUTUBE, PlatformChoice.INSTAGRAM, PlatformChoice.LINKEDIN, PlatformChoice.X_TWITTER],
        description="Which platforms to investigate. Only the specified platforms will be queried."
    )
    platform_handles: Optional[Dict[str, str]] = Field(
        None,
        description="Optional handles per platform, e.g. {'youtube': '@dhruvrathee', 'instagram': 'dhruvrathee', 'linkedin': 'dhruvrathee', 'x_twitter': 'dhruv_rathee'}"
    )
    goals: Optional[Dict[str, Any]] = Field(
        None,
        description="Per-platform goals (e.g. {'youtube': 'increase_subscribers', 'instagram': 'more_views_and_followers'})"
    )
    generate_platform_md: bool = Field(True, description="Whether to auto-generate platform.md files")
    generate_user_hook_md: bool = Field(True, description="Whether to generate/update user.md and hook.md in the creator's native language based on the investigated apps")


# ──────────────────────────────────────────────
# Creator Platform Profile
# ──────────────────────────────────────────────

class CreatorPlatformProfile(BaseModel):
    """Real creator information extracted from a specific platform."""
    platform: str
    handle: str
    profile_url: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    follower_or_sub_count: Optional[str] = None
    following_count: Optional[str] = None
    total_posts_or_videos: Optional[str] = None
    verified: bool = False
    recent_content: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Recent posts/videos/threads extracted from this creator's profile"
    )
    growth_gap_analysis: Optional[str] = None


# ──────────────────────────────────────────────
# Trend Items
# ──────────────────────────────────────────────

class TrendItem(BaseModel):
    """A single trending content piece discovered on a platform."""
    rank: int
    title: str
    url: Optional[str] = None
    platform: str
    content_type: str = Field(..., description="e.g. 'video', 'reel', 'post', 'article', 'thread'")
    views_or_engagement: Optional[str] = None
    published_date: Optional[str] = None
    creator_handle: Optional[str] = None
    why_trending: Optional[str] = None
    relevance_to_niche: Optional[str] = None
    suggested_angle: Optional[str] = None
    hashtags: List[str] = []
    thumbnail_url: Optional[str] = None


class PlatformTrendsBlock(BaseModel):
    """All trends and creator profile discovered for a single platform."""
    platform: str
    goal: Optional[str] = None
    creator_profile: Optional[CreatorPlatformProfile] = Field(
        None,
        description="Extracted real creator profile information on this platform"
    )
    domain_trends: List[TrendItem] = Field(default_factory=list, description="Niche/domain-specific trending content")
    location_trends: List[TrendItem] = Field(default_factory=list, description="Location/region trending content")
    global_trends: List[TrendItem] = Field(default_factory=list, description="Global/worldwide trending content")
    hashtag_trends: List[str] = Field(default_factory=list, description="Currently trending hashtags for this platform")
    content_strategy: Optional[str] = None
    platform_md_path: Optional[str] = None


class ContentRecommendation(BaseModel):
    """AI-generated content recommendation based on trends."""
    platform: str
    content_type: str
    topic: str
    hook: str
    why_now: str
    estimated_reach: Optional[str] = None
    hashtags: List[str] = []
    best_posting_time: Optional[str] = None


# ──────────────────────────────────────────────
# Response
# ──────────────────────────────────────────────

class IntelligenceResponse(BaseModel):
    creator_name: str
    niche: str
    location: str
    analyzed_at: str
    platforms_analyzed: List[str]
    creator_profiles: Dict[str, CreatorPlatformProfile] = Field(
        default_factory=dict,
        description="Map of platform -> extracted creator profile data"
    )
    platform_trends: List[PlatformTrendsBlock]
    top_recommendations: List[ContentRecommendation] = []
    platform_md_files: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of platform -> file path for generated platform.md files"
    )
    detected_language: Optional[str] = Field(None, description="Creator's detected or specified spoken language")
    identified_domain: Optional[str] = Field(None, description="Creator's identified domain/niche name")
    domain_profile: Optional[Dict[str, Any]] = Field(None, description="Structured domain and audience profile")
    user_md_path: Optional[str] = Field(None, description="Path to generated user.md")
    hook_md_path: Optional[str] = Field(None, description="Path to generated hook.md")
    summary: Optional[str] = None

