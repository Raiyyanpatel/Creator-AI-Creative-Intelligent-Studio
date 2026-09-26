"""
Viral Video Clipping & SmolVLM Router
=====================================
FastAPI routes for automated video clipping, on-device SmolVLM visual verification,
and direct handoff to the /publish Human-In-The-Loop queue.
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query

from app.models.clipping import (
    ClipAnalysisRequest,
    ClipAnalysisResponse,
    ClipToPublishRequest,
    ViralClipItem
)
from app.models.publish import (
    PublishCreateRequest,
    PublishResponse,
    PlatformType,
    ContentFormat
)
from app.services.clipping_service import clipping_service
from app.services.smolvlm_service import smolvlm_service
from app.services.composio_service import composio_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clipping", tags=["Viral Video Clipping & On-Device SmolVLM"])


@router.post("/analyze", response_model=ClipAnalysisResponse, summary="Analyze video for viral short clips with context management & SmolVLM")
def analyze_video_for_clips(req: ClipAnalysisRequest):
    """
    Ingests any video (YouTube, live stream, or direct MP4), extracts timed transcript
    and retention signals, resolves context and dangling pronouns, executes on-device
    SmolVLM visual hook verification, and returns ranked viral shorts with exact timestamps.
    """
    try:
        return clipping_service.analyze_video(req)
    except Exception as e:
        logger.error(f"[Clipping] Analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to analyze video for clipping: {str(e)}")


@router.post("/to-publish", response_model=PublishResponse, summary="Handoff viral clip to /publish Human Approval Queue")
def send_clip_to_publish_queue(req: ClipToPublishRequest):
    """
    Converts a chosen viral clip directly into a PublishJob inside the /publish
    Human-In-The-Loop approval queue. Reviewers can approve or reject before Composio
    dispatches it to YouTube Shorts, Instagram Reels, or TikTok.
    """
    try:
        # Map target platform
        platform_map = {
            "youtube": PlatformType.YOUTUBE,
            "instagram": PlatformType.TWITTER, # Fallback to social stream
            "twitter": PlatformType.TWITTER,
            "tiktok": PlatformType.YOUTUBE
        }
        chosen_platform = platform_map.get(req.platform.lower(), PlatformType.YOUTUBE)

        # Build publishing request
        full_content = (
            f"🎬 {req.clip.suggested_title}\n\n"
            f"{req.clip.suggested_caption}\n\n"
            f"⏱️ Timestamp: {req.clip.start_time} - {req.clip.end_time} ({req.clip.duration_seconds}s)\n\n"
            f"🎣 Opening Hook: \"{req.clip.hook_line}\"\n\n"
            f"{' '.join(req.clip.hashtags)}"
        )

        pub_req = PublishCreateRequest(
            creator_id=req.creator_id,
            platform=chosen_platform,
            content_format=ContentFormat.SHORT if chosen_platform == PlatformType.YOUTUBE else ContentFormat.POST,
            title=req.clip.suggested_title,
            content=full_content,
            tags=req.clip.hashtags,
            require_human_approval=req.require_human_approval
        )

        job = composio_service.create_publish_job(pub_req)
        return PublishResponse(
            status="success",
            message=f"Viral clip '{req.clip.suggested_title}' ({req.clip.start_time}-{req.clip.end_time}) dispatched to Human Approval Queue as Job {job.job_id}!",
            job=job
        )
    except Exception as e:
        logger.error(f"[Clipping] Error creating publish job: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to hand off clip to publish queue: {str(e)}")


@router.get("/status", summary="Check on-device SmolVLM health & connectivity on iQOO 15")
def check_on_device_status(endpoint: Optional[str] = Query(None, description="Optional custom IP/port for iQOO 15")):
    """
    Pings the on-device SmolVLM server running on the Snapdragon 8 Elite (iQOO 15).
    Verifies NPU acceleration readiness and model availability.
    """
    return smolvlm_service.check_on_device_health(endpoint)
