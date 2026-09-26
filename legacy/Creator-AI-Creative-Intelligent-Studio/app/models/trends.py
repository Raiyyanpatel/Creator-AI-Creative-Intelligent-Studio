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
    creator_name: Optional[str]
    domain: str
    geo: str
    fetched_at: str
    niche_trends: List[TrendingItem]
    world_trends: List[TrendingItem]
    viral_formats: List[FormatTrend]
    content_opportunity_matrix: List[Dict[str, Any]]
