import logging
from typing import Optional
from fastapi import APIRouter, Query, Body

from app.models.trends import TrendsResponse
from app.services.trends_service import trends_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trends", tags=["Live Trends & Hook Angles"])

@router.get("", response_model=TrendsResponse, summary="Get real-time trends for creator's domain & overall world trends")
def get_trends(
    creator_name: Optional[str] = Query(None, description="Optional creator name to tailor niche hooks"),
    domain: str = Query("Tech & AI", description="Domain/niche (e.g. 'Tech & AI', 'Finance', 'Productivity', 'Fitness')"),
    geo: str = Query("US", description="Geographic region code for Google Trends (e.g. 'US', 'GB', 'IN', 'GLOBAL')"),
    limit: int = Query(10, ge=3, le=25, description="Number of trending topics to return")
):
    """
    Fetches live real-world trending topics from Google Trends RSS and cross-platform feeds.
    Provides niche-specific trends, world trends ('elite + world trends'), viral format templates,
    and ready-to-record hook angles for creators.
    """
    logger.info(f"Fetching real-time trends for domain: {domain}, geo: {geo}")
    return trends_service.get_realtime_trends(
        creator_name=creator_name,
        domain=domain,
        geo=geo,
        limit=limit
    )

@router.post("", response_model=TrendsResponse, summary="Query trends with flexible JSON body")
def post_trends_query(
    creator_name: Optional[str] = Body(None),
    domain: str = Body("Tech & AI"),
    geo: str = Body("US"),
    limit: int = Body(10)
):
    return trends_service.get_realtime_trends(
        creator_name=creator_name,
        domain=domain,
        geo=geo,
        limit=limit
    )
