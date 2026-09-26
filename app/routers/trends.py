import logging
from typing import Optional
from fastapi import APIRouter, Query, Body

from app.models.trends import TrendsResponse
from app.services.trends_service import trends_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trends", tags=["Live Trends & Hook Angles"])

@router.get("", response_model=TrendsResponse, summary="Get trendy videos/posts for domain across YouTube, Instagram, LinkedIn & X")
def get_trends(
    domain: str = Query("Tech & AI", description="Domain/niche (e.g. 'Tech & AI', 'Finance', 'Productivity', 'Fitness', 'Social Causes')"),
    creator_name: Optional[str] = Query(None, description="Optional creator name to tailor niche hooks"),
    geo: str = Query("US", description="Geographic region code for Google Trends (e.g. 'US', 'GB', 'IN', 'GLOBAL')"),
    limit: int = Query(10, ge=3, le=25, description="Number of trending topics to return per platform")
):
    """
    Fetches live real-world trending content across all 4 major platforms (YouTube, Instagram, LinkedIn, X/Twitter)
    for the specified domain, plus high-velocity trending keywords, viral format templates, and ready-to-record hook angles.
    """
    logger.info(f"Fetching real-time trends for domain: {domain}, geo: {geo}")
    return trends_service.get_realtime_trends(
        creator_name=creator_name,
        domain=domain,
        geo=geo,
        limit=limit
    )

@router.get("/domain", summary="Search domain for trendy videos/posts across YouTube, Instagram, LinkedIn & X")
def search_domain_trends_get(
    domain: str = Query(..., description="Domain/niche (e.g. 'Fitness', 'Gaming', 'Crypto', 'AI Agents', 'Finance', 'Social Causes')"),
    geo: str = Query("US", description="Geographic region code ('US', 'IN', 'GLOBAL')"),
    limit: int = Query(10, ge=3, le=25, description="Number of results per category")
):
    """
    Search any domain to uncover real-time YouTube trending videos, viral Instagram Reels,
    high-authority LinkedIn discussions, viral X/Twitter threads, and high-velocity trending keywords.
    """
    logger.info(f"[TrendsRouter] Searching trends for domain: {domain}, geo: {geo}")
    return trends_service.get_domain_trends(domain=domain, geo=geo, limit=limit)


