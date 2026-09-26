"""
Viral Video Clipping & On-Device SmolVLM Models
================================================
Schemas for automated viral short detection, context management,
and on-device SmolVLM multimodal visual hook evaluation.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ClipSourceType(str, Enum):
    YOUTUBE = "youtube"
    LIVESTREAM = "livestream"
    LOCAL_FILE = "local_file"
    DIRECT_URL = "direct_url"


class VisualAssessment(BaseModel):
    visual_hook_score: float = Field(..., description="Visual engagement score (0.0 to 10.0) based on facial expression and eye contact")
    facial_expression: str = Field(..., description="Observed facial expression (e.g. 'Shocked / Intense eye contact', 'Passionate debate gesture')")
    face_crop_center_x: float = Field(50.0, description="Recommended horizontal crop center percentage (0-100%) for 9:16 vertical framing")
    active_speaker_identified: bool = Field(True, description="Whether active speaker was confirmed in frame")
    visual_hook_summary: str = Field(..., description="Why the visual frame stops viewer scroll in first 3 seconds")
    keyframe_timestamp: Optional[float] = Field(None, description="Timestamp in seconds of the primary keyframe analyzed")


class ViralClipItem(BaseModel):
    clip_id: str = Field(..., description="Unique clip identifier (e.g. 'clip_1')")
    rank: int = Field(..., description="Virality rank (1 = highest viral potential)")
    start_time: str = Field(..., description="Formatted start timestamp (MM:SS or HH:MM:SS)")
    end_time: str = Field(..., description="Formatted end timestamp (MM:SS or HH:MM:SS)")
    start_seconds: float = Field(..., description="Start offset in seconds")
    end_seconds: float = Field(..., description="End offset in seconds")
    duration_seconds: float = Field(..., description="Total clip duration in seconds")
    virality_score: int = Field(..., description="Composite virality score (0-100)")
    hook_line: str = Field(..., description="The opening 3-second hook that captures attention")
    why_viral: str = Field(..., description="Editorial rationale explaining narrative payoff and audience retention")
    suggested_title: str = Field(..., description="High-CTR title for YouTube Shorts / Instagram Reels")
    suggested_caption: str = Field(..., description="Engagement-optimized caption with call-to-action")
    hashtags: List[str] = Field(default_factory=list, description="Surging hashtags for algorithmic distribution")
    transcript_snippet: str = Field(..., description="Full self-contained transcript snippet for this segment")
    visual_assessment: Optional[VisualAssessment] = Field(None, description="SmolVLM on-device visual analysis")
    recommended_aspect_ratio: str = Field("9:16", description="Target video aspect ratio")


class ClipAnalysisRequest(BaseModel):
    video_url: str = Field(..., description="YouTube URL, live stream replay, or MP4 URL/local path")
    creator_name: Optional[str] = Field("Creator", description="Creator's display name or handle")
    target_duration_seconds: int = Field(50, description="Target short duration in seconds (typically 30-60s)")
    min_virality_score: int = Field(70, description="Minimum score threshold to include in response (0-100)")
    max_clips: int = Field(5, description="Maximum number of top viral clips to return")
    use_on_device_smolvlm: bool = Field(True, description="Enable SmolVLM 2.2B on-device multimodal visual inspection")
    on_device_endpoint: Optional[str] = Field("http://localhost:8080/v1", description="Local on-device endpoint (e.g. iQOO 15 phone or Termux server)")


class ClipAnalysisResponse(BaseModel):
    status: str = Field("success", description="Status of the clipping operation")
    video_title: str = Field(..., description="Extracted video title")
    video_duration: str = Field(..., description="Total duration of the source video")
    source_type: str = Field(..., description="Detected video source type (youtube, livestream, direct_file)")
    signals_used: List[str] = Field(..., description="List of multi-modal signals leveraged for analysis")
    on_device_model: str = Field("SmolVLM-2.2B (Snapdragon 8 Elite)", description="Multimodal model deployed for visual hook verification")
    total_candidates_analyzed: int = Field(..., description="Number of candidate segments evaluated")
    top_viral_clips: List[ViralClipItem] = Field(default_factory=list, description="Ranked viral clips with timestamps")


class ClipToPublishRequest(BaseModel):
    clip: ViralClipItem = Field(..., description="The viral clip item to publish")
    creator_id: str = Field(..., description="Creator identifier")
    platform: str = Field("youtube", description="Target platform ('youtube', 'instagram', 'twitter', 'tiktok')")
    require_human_approval: bool = Field(True, description="Enforce Human-In-The-Loop approval gate in /publish")
