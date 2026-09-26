"""
Domain & Niche Intelligence Models
====================================
Pydantic schemas for dynamic creator domain, niche identification,
content pillars, audience psychographics, and domain-tailored monologues.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DomainMonologue(BaseModel):
    title: str = Field(..., description="Monologue archetype title")
    speech: str = Field(..., description="Verbatim spoken monologue text")
    staging_breakdown: str = Field(..., description="Timestamped staging, visual cues, and pacing breakdown")


class DomainAudienceProfile(BaseModel):
    demographics: str = Field(..., description="Target age, professions, location distribution")
    psychographics: str = Field(..., description="Viewer mindset, core pain points, what triggers retention")
    consumption_habits: str = Field(..., description="Average watch time, where they share, discussion style")


class DomainMoat(BaseModel):
    mission: str = Field(..., description="Core purpose / mission in this domain")
    positioning: str = Field(..., description="Unique positioning against competitors")
    competitive_moat: str = Field(..., description="What makes this creator defensible and trusted")


class DomainCadence(BaseModel):
    pitch_modulation: str = Field(..., description="Pitch shifts on key domain reveals")
    micro_pause_timing: str = Field(..., description="Strategic silence intervals")
    articulation_and_pacing: str = Field(..., description="Words per minute and delivery energy")
    inclusive_pronoun_habit: str = Field(..., description="Framing and relationship dynamic")


class CreatorDomainProfile(BaseModel):
    """Full domain intelligence profile for a creator."""
    domain_id: str = Field(..., description="Standardized domain identifier (e.g. 'tech_gadgets', 'personal_finance', 'civic_social_issues')")
    domain_name: str = Field(..., description="Human-readable domain title (e.g. 'Consumer Technology & Future Gadgets')")
    sub_niche: str = Field(..., description="Specific sub-vertical or focus area")
    primary_search_topics: List[str] = Field(
        default_factory=list,
        description="High-velocity search queries for discovering live trends in this domain"
    )
    core_verticals: List[str] = Field(
        default_factory=list,
        description="Core subject pillars the creator covers"
    )
    content_portfolio: List[str] = Field(
        default_factory=list,
        description="Standard content formats produced in this domain"
    )
    investigation_methodology: str = Field(
        ...,
        description="How tests, data, or arguments are researched and verified in this domain"
    )
    audience_profile: DomainAudienceProfile = Field(
        ...,
        description="Audience demographics, psychographics, and viral sharing habits"
    )
    domain_positioning_and_moat: DomainMoat = Field(
        ...,
        description="Strategic mission, niche positioning, and defensibility"
    )
    domain_monologues: Dict[str, DomainMonologue] = Field(
        default_factory=dict,
        description="Domain-specific 45s-60s extended spoken monologue blueprints"
    )
    vocal_cadence_dynamics: DomainCadence = Field(
        ...,
        description="Vocal delivery, pitch trajectory, and pacing dynamics for this domain"
    )
    signature_phrases: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Signature spoken expressions authentic to this domain"
    )
    sample_hooks: List[str] = Field(
        default_factory=list,
        description="High-retention opening hooks for this domain"
    )


class IdentifyDomainRequest(BaseModel):
    creator_name: str = Field(..., description="Creator's display name or handle")
    niche_hint: Optional[str] = Field(None, description="Optional hint about niche if known")
    sample_titles: Optional[List[str]] = Field(None, description="Recent video/post titles to analyze")
    bio: Optional[str] = Field(None, description="Channel or profile bio text")
    language: Optional[str] = Field("en", description="Preferred language for monologues and hooks ('hi', 'en', 'es')")
