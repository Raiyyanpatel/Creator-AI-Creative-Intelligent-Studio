from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TrendingItem(BaseModel):
    rank: int
    title: str
    traffic_volume: str
    source: str = "Google Trends Live / YouTube Realtime"
    category: str
    published_or_trending_since: str
    news_headlines: List[str] = []
    relevance_to_creator: str
    hook_angles: List[str] = Field(..., description="Actionable opening hooks to create content around this trend")

class FormatTrend(BaseModel):
    format_name: str
    virality_score: int = Field(..., ge=1, le=100)
    ideal_length: str
    platform_fit: List[str]
    why_it_works: str
    structure_template: str

class TrendsResponse(BaseModel):
    creator_name: Optional[str] = None
    domain: str
    geo: str
    fetched_at: str
    youtube_trending: List[Dict[str, Any]] = Field(default_factory=list, description="Trending videos and Shorts in this domain")
    instagram_trending: List[Dict[str, Any]] = Field(default_factory=list, description="Viral Instagram Reels and posts in this domain")
    linkedin_trending: List[Dict[str, Any]] = Field(default_factory=list, description="High-engagement LinkedIn discussions and carousels in this domain")
    x_twitter_trending: List[Dict[str, Any]] = Field(default_factory=list, description="Viral X / Twitter tweets and threads in this domain")
    trending_keywords: List[str] = Field(default_factory=list, description="High-velocity search and discussion keywords in this domain")
    velocity_topics: List[Dict[str, Any]] = Field(default_factory=list, description="Surging search queries and industry velocity topics")
    niche_trends: List[TrendingItem] = Field(default_factory=list)
    world_trends: List[TrendingItem] = Field(default_factory=list)
    viral_formats: List[FormatTrend] = Field(default_factory=list)
    content_opportunity_matrix: List[Dict[str, Any]] = Field(default_factory=list)

