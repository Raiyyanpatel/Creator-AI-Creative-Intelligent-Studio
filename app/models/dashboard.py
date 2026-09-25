from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PlatformMetricDetail(BaseModel):
    platform: str
    connected: bool
    handle_or_name: str
    followers_or_subscribers: int
    total_views_or_impressions: int
    total_content_pieces: int
    avg_engagement_rate_percent: float
    growth_rate_30d_percent: float
    recent_performance: str
    top_content: List[Dict[str, Any]] = []

class AppEngagementMetrics(BaseModel):
    total_scripts_generated: int = 14
    total_hooks_created: int = 42
    pending_approval_posts: int = 3
    approved_posts: int = 8
    published_via_composio: int = 19
    publishing_success_rate: float = 98.4

class ChartDataPoint(BaseModel):
    label: str
    youtube_views: int
    social_engagement: int
    substack_reads: int

class DashboardResponse(BaseModel):
    creator_name: str
    timeframe: str
    overall_reach: int
    overall_engagement_rate: float
    platforms: Dict[str, PlatformMetricDetail]
    app_platform_metrics: AppEngagementMetrics
    charts: Dict[str, Any] = Field(..., description="Ready-to-render data structures for React Native charts")
    executive_summary: str
    key_recommendations: List[str]
