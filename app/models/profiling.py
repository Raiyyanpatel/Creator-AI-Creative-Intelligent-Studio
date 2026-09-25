from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ProfilingRequest(BaseModel):
    creator_name: str = Field(..., description="Creator name or username to profile (e.g. Ali Abdaal, MrBeast, Fireship)")
    youtube_handle_or_url: Optional[str] = Field(None, description="Direct YouTube handle or channel URL")
    substack_handle_or_url: Optional[str] = Field(None, description="Substack publication name, handle, or URL")
    twitter_handle_or_url: Optional[str] = Field(None, description="X / Twitter handle or URL")
    linkedin_handle_or_url: Optional[str] = Field(None, description="LinkedIn profile or creator vanity URL")
    custom_instructions: Optional[str] = Field(None, description="Specific profiling focus (e.g., focus on hook retention, pacing)")
    max_videos_to_analyze: int = Field(8, description="Number of recent videos and shorts to analyze")
    max_articles_to_analyze: int = Field(5, description="Number of recent Substack articles to inspect")

class VideoItem(BaseModel):
    id: str
    title: str
    url: str
    duration_seconds: int
    duration_formatted: str
    is_short: bool
    view_count: Optional[int] = None
    upload_date: Optional[str] = None
    thumbnail_url: Optional[str] = None
    transcript_available: bool = False
    transcript_snippet: Optional[str] = None
    key_opening_words: Optional[str] = None

class ArticleItem(BaseModel):
    title: str
    url: str
    published_date: Optional[str] = None
    word_count: int
    summary: str

class SocialPostItem(BaseModel):
    platform: str
    text: str
    url: Optional[str] = None
    likes: Optional[int] = None
    retweets_or_shares: Optional[int] = None

class FrequentPhrase(BaseModel):
    phrase: str
    count: int
    category: str = Field(..., description="'greeting', 'transition', 'catchphrase', 'call_to_action', or 'emphasis'")
    sample_context: str

class ToneAnalysis(BaseModel):
    primary_tone: str
    energy_level: str
    pacing: str
    vocabulary_style: str
    audience_relationship: str
    key_descriptors: List[str]

class VideoLengthAnalysis(BaseModel):
    average_duration_seconds: float
    average_duration_formatted: str
    shorts_ratio_percentage: float
    long_form_ratio_percentage: float
    recommended_duration_range: str
    pacing_breakdown: str

class ThumbnailStrategy(BaseModel):
    visual_style: str
    facial_expression_patterns: str
    color_palette_dominance: List[str]
    text_density: str
    curiosity_gap_tactics: List[str]

class ProfilingAnalysis(BaseModel):
    tone: ToneAnalysis
    video_length: VideoLengthAnalysis
    video_types: List[str]
    thumbnail_strategy: ThumbnailStrategy
    frequent_spoken_phrases: List[FrequentPhrase]
    post_formats: List[str]
    core_themes: List[str]
    content_strengths: List[str]

class ProfilingResponse(BaseModel):
    status: str = "success"
    creator_name: str
    creator_slug: str
    analyzed_at: str
    platforms_ingested: List[str]
    catalog_summary: Dict[str, Any]
    analysis: ProfilingAnalysis
    user_md: str = Field(..., description="Complete user persona and styling blueprint in Markdown format")
    hook_md: str = Field(..., description="Hook mastery breakdown and formulas in Markdown format")
    file_paths: Dict[str, str] = Field(..., description="Local file paths where user.md and hook.md are saved")
