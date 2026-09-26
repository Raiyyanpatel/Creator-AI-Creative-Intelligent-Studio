import logging
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Body
from app.config import settings
from app.models.profiling import ProfilingRequest, ProfilingResponse
from app.services.youtube_service import youtube_service
from app.services.substack_service import substack_service
from app.services.twitter_service import twitter_service
from app.services.linkedin_service import linkedin_service
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profiling", tags=["Profiling Engine"])

@router.post("", response_model=ProfilingResponse, summary="Analyze creator across all platforms & generate user.md and hook.md")
def analyze_creator_profile(req: ProfilingRequest):
    """
    Ingests real content across YouTube (videos, shorts, transcripts), Substack (articles),
    X/Twitter (posts), and LinkedIn. Analyzes tone, length of videos, video types, thumbnail strategies,
    frequently spoken catchphrases, and generates production-ready `user.md` and `hook.md`.
    """
    creator_name = req.creator_name.strip()
    if not creator_name:
        raise HTTPException(status_code=400, detail="creator_name is required")

    logger.info(f"Initiating full profiling for creator: {creator_name}")
    
    # 1. Ingest YouTube real videos, shorts, and transcripts
    yt_data = youtube_service.fetch_creator_videos(
        creator_name=creator_name,
        channel_url_or_handle=req.youtube_handle_or_url,
        max_videos=req.max_videos_to_analyze
    )

    # 2. Ingest Substack real articles
    sub_data = substack_service.fetch_creator_articles(
        creator_name=creator_name,
        substack_url_or_handle=req.substack_handle_or_url,
        max_articles=req.max_articles_to_analyze
    )

    # 3. Ingest X / Twitter posts
    tw_data = twitter_service.fetch_creator_tweets(
        creator_name=creator_name,
        twitter_handle_or_url=req.twitter_handle_or_url
    )

    # 4. Ingest LinkedIn posts
    li_data = linkedin_service.fetch_creator_posts(
        creator_name=creator_name,
        linkedin_handle_or_url=req.linkedin_handle_or_url
    )

    # 5. Synthesize and generate user.md & hook.md via LLM Service
    profiling_result = llm_service.profile_creator(
        creator_name=creator_name,
        youtube_data=yt_data,
        substack_data=sub_data,
        twitter_data=tw_data,
        linkedin_data=li_data,
        custom_instructions=req.custom_instructions
    )

    platforms_ingested = ["YouTube"]
    if sub_data.get("articles"):
        platforms_ingested.append("Substack")
    if tw_data.get("posts"):
        platforms_ingested.append("X / Twitter")
    platforms_ingested.append("LinkedIn")

    catalog_summary = {
        "youtube_videos_mined": len(yt_data.get("videos", [])),
        "youtube_shorts_mined": yt_data.get("shorts_count", 0),
        "youtube_transcripts_parsed": sum(1 for v in yt_data.get("videos", []) if v.transcript_available),
        "substack_articles_mined": len(sub_data.get("articles", [])),
        "twitter_posts_mined": len(tw_data.get("posts", []))
    }

    return ProfilingResponse(
        status="success",
        creator_name=creator_name,
        creator_slug=profiling_result["creator_slug"],
        analyzed_at=datetime.now(timezone.utc).isoformat(),
        platforms_ingested=platforms_ingested,
        catalog_summary=catalog_summary,
        analysis=profiling_result["analysis"],
        user_md=profiling_result["user_md"],
        hook_md=profiling_result["hook_md"],
        file_paths=profiling_result["file_paths"]
    )

@router.get("/{creator_slug}", summary="Retrieve existing user.md and hook.md for creator")
def get_existing_profile(creator_slug: str):
    """
    Retrieves the generated `user.md` and `hook.md` directly from disk.
    """
    creator_dir = settings.CREATORS_DIR / creator_slug.lower().strip()
    user_md_path = creator_dir / "user.md"
    hook_md_path = creator_dir / "hook.md"

    if not user_md_path.exists() or not hook_md_path.exists():
        raise HTTPException(status_code=404, detail=f"No profile found for '{creator_slug}'. Please run POST /profiling first.")

    with open(user_md_path, "r", encoding="utf-8") as f:
        user_md = f.read()
    with open(hook_md_path, "r", encoding="utf-8") as f:
        hook_md = f.read()

    return {
        "creator_slug": creator_slug,
        "user_md": user_md,
        "hook_md": hook_md,
        "paths": {
            "user_md": str(user_md_path),
            "hook_md": str(hook_md_path)
        }
    }
