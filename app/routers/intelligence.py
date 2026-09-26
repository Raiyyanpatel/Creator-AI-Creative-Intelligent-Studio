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
from app.models.domain import CreatorDomainProfile, IdentifyDomainRequest
from app.services.platform_intel_service import platform_intel_service
from app.services.domain_service import domain_service, DOMAIN_ARCHETYPES

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
    causes_or_topics: Optional[str] = Query(None, description="Comma-separated topics or causes of creator's work (e.g. 'Social Causes, Public Policy')"),
    language: Optional[str] = Query(None, description="Creator's native spoken language code (e.g. 'hi', 'en', 'es')"),
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

    causes_list = [c.strip() for c in causes_or_topics.split(",") if c.strip()] if causes_or_topics else None

    req = IntelligenceRequest(
        creator_name=creator_name,
        niche=niche,
        causes_or_topics=causes_list,
        language=language,
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
            "youtube": "increase_subscribers",
            "instagram": "more_views_and_followers",
            "linkedin": "increase_connections",
            "x_twitter": "spread_domain_posts",
        },
        "description": {
            "youtube": "Discover trending domain + global + location videos and Shorts to increase subscribers",
            "instagram": "Identify trending domain + global + location viral Reels to get more views and followers",
            "linkedin": "Surface high-authority domain discussions to increase reach and build professional connections",
            "x_twitter": "Discover domain trends and viral threads to spread domain posts and increase reach",
        },
    }


@router.get(
    "/domains",
    summary="List recognized domain archetypes",
    description="Returns all pre-built creator domains, sub-niches, and core content verticals.",
)
def list_domain_archetypes():
    result = []
    for dom_id, d in DOMAIN_ARCHETYPES.items():
        result.append({
            "domain_id": dom_id,
            "domain_name": d["domain_name"],
            "sub_niche": d["sub_niche"],
            "core_verticals": d["core_verticals"],
            "primary_search_topics": d["primary_search_topics"],
            "methodology": d["investigation_methodology"]
        })
    return {"domains": result, "total": len(result)}


@router.post(
    "/identify-domain",
    response_model=CreatorDomainProfile,
    summary="Identify creator domain, niche, and content pillars (POST)",
    description="Dynamically identifies any creator's domain, core verticals, target audience psychographics, competitive moat, and domain monologues.",
)
def identify_creator_domain_post(req: IdentifyDomainRequest):
    return domain_service.get_creator_domain_profile(
        creator_name=req.creator_name,
        niche_hint=req.niche_hint,
        sample_titles=req.sample_titles,
        bio=req.bio,
        language=req.language or "en",
    )


@router.get(
    "/identify-domain",
    response_model=CreatorDomainProfile,
    summary="Identify creator domain, niche, and content pillars (GET)",
    description="Lightweight query endpoint to quickly identify a creator's domain and niche.",
)
def identify_creator_domain_get(
    creator_name: str = Query(..., description="Creator's display name or handle"),
    niche_hint: Optional[str] = Query(None, description="Optional hint about niche if known"),
    language: Optional[str] = Query("en", description="Target spoken language ('hi', 'en', 'es')"),
):
    return domain_service.get_creator_domain_profile(
        creator_name=creator_name,
        niche_hint=niche_hint,
        sample_titles=None,
        bio=None,
        language=language or "en",
    )
