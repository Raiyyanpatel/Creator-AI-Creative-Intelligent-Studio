"""
Intelligence Router
====================
API endpoints for the Platform Intelligence system.
Provides cross-platform trend discovery, platform.md generation,
and content recommendations.
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Query, Body

from app.models.intelligence import (
    IntelligenceRequest,
    IntelligenceResponse,
    PlatformChoice,
)
from app.services.platform_intel_service import platform_intel_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/intelligence", tags=["Platform Intelligence & Trends"])


@router.post(
    "",
    response_model=IntelligenceResponse,
    summary="Run full cross-platform intelligence scan",
    description="""
Performs a comprehensive trend analysis across selected platforms (YouTube, Instagram, LinkedIn, X/Twitter).

**What it does:**
1. Scrapes live trending content per platform for the creator's niche
2. Discovers domain, location, and global trends with links
3. Generates platform-specific content strategies
4. Produces AI-powered content recommendations
5. Auto-generates `platform_{name}.md` files under `creators/{slug}/`

**Platform Goals:**
- Instagram → Increase Reach
- YouTube → Increase Followers
- LinkedIn → Increase Connections
- X/Twitter → Increase Engagement
    """,
)
def run_intelligence_scan(req: IntelligenceRequest):
    logger.info(
        f"[Intelligence] Running scan for creator={req.creator_name}, "
        f"niche={req.niche}, location={req.location}, "
        f"platforms={[p.value for p in req.platforms]}"
    )
    return platform_intel_service.run_intelligence(req)


@router.get(
    "/quick",
    response_model=IntelligenceResponse,
    summary="Quick intelligence scan via query params",
    description="Lightweight GET endpoint for quick trend scanning without a JSON body.",
)
def quick_intelligence_scan(
    creator_name: str = Query(..., description="Creator's display name"),
    niche: str = Query("Tech & AI", description="Creator's niche/domain"),
    location: str = Query("US", description="Country/region code"),
    platforms: Optional[str] = Query(
        "youtube,instagram,linkedin,x_twitter",
        description="Comma-separated platform names (youtube, instagram, linkedin, x_twitter)",
    ),
):
    platform_list = []
    if platforms:
        for p in platforms.split(","):
            p = p.strip().lower()
            try:
                platform_list.append(PlatformChoice(p))
            except ValueError:
                logger.warning(f"Unknown platform: {p}")

    if not platform_list:
        platform_list = [
            PlatformChoice.YOUTUBE,
            PlatformChoice.INSTAGRAM,
            PlatformChoice.LINKEDIN,
            PlatformChoice.X_TWITTER,
        ]

    req = IntelligenceRequest(
        creator_name=creator_name,
        niche=niche,
        location=location,
        platforms=platform_list,
    )
    return platform_intel_service.run_intelligence(req)


@router.get(
    "/platforms",
    summary="List available platforms and goals",
    description="Returns the list of supported platforms and goal types for the intelligence system.",
)
def list_platforms():
    return {
        "platforms": [p.value for p in PlatformChoice],
        "goals": {
            "instagram": "increase_reach",
            "youtube": "increase_followers",
            "linkedin": "increase_connections",
            "x_twitter": "increase_engagement",
        },
        "description": {
            "youtube": "Find trending videos, Shorts, and topics to increase subscribers",
            "instagram": "Discover trending Reels, hashtags, and posts to maximize reach",
            "linkedin": "Identify viral articles and posts to grow professional connections",
            "x_twitter": "Surface trending threads, hashtags, and topics for engagement",
        },
    }
