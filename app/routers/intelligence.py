"""
Intelligence Router
====================
API endpoints for the Platform Intelligence system.
Provides cross-platform trend discovery, platform.md generation,
and content recommendations.
"""

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field

from app.models.intelligence import (
    IntelligenceRequest,
    IntelligenceResponse,
    PlatformChoice,
)
from app.models.domain import CreatorDomainProfile, IdentifyDomainRequest
from app.services.platform_intel_service import platform_intel_service
from app.services.domain_service import domain_service, DOMAIN_ARCHETYPES
from app.services.creator_comparator_service import creator_comparator_service

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
    summary="Identify creator domain, niche, and content pillars",
    description="Dynamically identifies any creator's domain, core verticals, target audience psychographics, competitive moat, and domain monologues.",
)
def identify_creator_domain(req: IdentifyDomainRequest):
    return domain_service.get_creator_domain_profile(
        creator_name=req.creator_name,
        niche_hint=req.niche_hint,
        sample_titles=req.sample_titles,
        bio=req.bio,
        language=req.language or "en",
    )


# ──────────────────────────────────────────────
# Compare Any Creator (Dynamic Extraction + Comparison)
# ──────────────────────────────────────────────

class CompareAnyCreatorRequest(BaseModel):
    creator_name: str = Field(..., description="Target creator name (e.g. 'Lex Fridman', 'Veritasium', 'MrBeast')")
    base_creator: Optional[str] = Field("Dhruv Rathee", description="Base creator to benchmark against ('me')")
    niche_hint: Optional[str] = Field(None, description="Optional hint for target creator's domain")
    location: Optional[str] = Field("US", description="Location country code")


@router.post(
    "/compare",
    summary="Compare with any creator across any domain, extracting all 7 dossiers",
    description="Takes input of any creator (no matter what domain), extracts all platform.md files, user.md, hook.md, and creator_comparison.md, and benchmarks against our base creator profile.",
)
@router.post(
    "/compare-any-creator",
    summary="Alias for /compare: enter any creator, extract all platforms.md, user.md, hook.md, and compare with me",
    include_in_schema=False,
)
def compare_any_creator(req: CompareAnyCreatorRequest):
    logger.info(f"[Intelligence] Comparing base={req.base_creator} against target={req.creator_name}")
    return creator_comparator_service.ensure_and_compare_creator(
        target_creator=req.creator_name,
        base_creator=req.base_creator or "Dhruv Rathee",
        niche_hint=req.niche_hint,
        location=req.location or "US"
    )


