"""
Platform Intelligence Service
================================
Master orchestrator that scrapes cross-platform trends (YouTube, Instagram,
LinkedIn, X/Twitter), extracts real creator information and footprint,
generates per-platform strategy reports (platform.md), and produces
actionable content recommendations.

Architecture:
  IntelligenceRequest
    → [YT Scraper & Profile Extractor, IG Scraper & Profile Extractor,
       LI Scraper & Profile Extractor, X Scraper & Profile Extractor]
    → Trend Aggregation & Growth Diagnostics
    → Comprehensive platform_{platform}.md Generation
    → IntelligenceResponse with CreatorPlatformProfile & Trend Blocks
"""

import re
import logging
import feedparser
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path
import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.models.intelligence import (
    IntelligenceRequest,
    IntelligenceResponse,
    PlatformTrendsBlock,
    TrendItem,
    ContentRecommendation,
    PlatformChoice,
    GoalType,
    CreatorPlatformProfile,
)
from app.services.instagram_service import instagram_service
from app.services.domain_service import domain_service
from app.services.composio_scraper_service import composio_scraper_service
from app.services.twitter_api_service import twitter_api_service
from app.services.apify_service import apify_service
from app.services.bright_data_service import bright_data_service
from app.services.creator_comparator_service import creator_comparator_service

logger = logging.getLogger(__name__)

# Default platform goals reflecting user growth objectives
DEFAULT_GOALS = {
    "youtube": "increase_subscribers",
    "instagram": "more_views_and_followers",
    "linkedin": "increase_connections",
    "x_twitter": "spread_domain_posts",
}

# Scraping headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


class PlatformIntelService:
    """Orchestrates cross-platform trend discovery and platform.md generation."""

    # ──────────────────────────────────────────────
    # Public entry point
    # ──────────────────────────────────────────────

    def run_intelligence(self, req: IntelligenceRequest) -> IntelligenceResponse:
        """Main entry: runs only requested platform scrapers, audits footprint, generates reports & user/hook dossiers."""
        now = datetime.now(timezone.utc).isoformat()

        # 1. Dynamically identify creator's domain/niche and work pillars
        domain_profile = domain_service.get_creator_domain_profile(
            creator_name=req.creator_name,
            niche_hint=req.niche,
            sample_titles=None,
            bio=None,
            language=req.language or "en",
        )
        effective_niche = domain_profile.domain_name if (req.niche in ["auto", "", None]) else req.niche
        causes_or_topics = req.causes_or_topics if req.causes_or_topics else domain_profile.primary_search_topics

        logger.info(
            f"[Intel] Dynamically identified domain for '{req.creator_name}': "
            f"'{domain_profile.domain_name}' ({domain_profile.domain_id}). Primary search topics: {causes_or_topics}"
        )

        platform_blocks: List[PlatformTrendsBlock] = []
        creator_profiles_dict: Dict[str, CreatorPlatformProfile] = {}
        recommendations: List[ContentRecommendation] = []
        md_files: Dict[str, str] = {}

        goals = req.goals or {}
        handles = req.platform_handles or {}

        # Investigate ONLY requested platforms
        for platform in req.platforms:
            pname = platform.value
            raw_goal = goals.get(pname, DEFAULT_GOALS.get(pname, "increase_subscribers"))
            goal = raw_goal.value if hasattr(raw_goal, "value") else str(raw_goal)
            handle = handles.get(pname, req.creator_name)

            logger.info(f"[Intel] Investigating {pname} for creator={req.creator_name}, handle={handle}, domain={domain_profile.domain_name}, causes={causes_or_topics}")

            if platform == PlatformChoice.YOUTUBE:
                block = self._scan_youtube(req.creator_name, effective_niche, req.location, handle, goal, causes_or_topics)
            elif platform == PlatformChoice.INSTAGRAM:
                block = self._scan_instagram(req.creator_name, effective_niche, req.location, handle, goal, causes_or_topics)
            elif platform == PlatformChoice.LINKEDIN:
                block = self._scan_linkedin(req.creator_name, effective_niche, req.location, handle, goal, causes_or_topics)
            elif platform == PlatformChoice.X_TWITTER:
                block = self._scan_x_twitter(req.creator_name, effective_niche, req.location, handle, goal, causes_or_topics)
            else:
                continue

            platform_blocks.append(block)
            if block.creator_profile:
                creator_profiles_dict[pname] = block.creator_profile

            # Generate content recommendations in creator's native language
            recs = self._generate_recommendations(block, effective_niche, pname, goal, req.language)
            recommendations.extend(recs)

        # Generate platform.md files if requested
        if req.generate_platform_md:
            md_files = self._generate_all_platform_md(
                creator_name=req.creator_name,
                niche=effective_niche,
                location=req.location,
                blocks=platform_blocks,
                recommendations=recommendations,
            )
            for block in platform_blocks:
                if block.platform in md_files:
                    block.platform_md_path = md_files[block.platform]

        # Always generate / update user.md and hook.md from investigated platforms
        user_md_path_str: Optional[str] = None
        hook_md_path_str: Optional[str] = None
        detected_lang_str: Optional[str] = None
        comparison_path: Optional[str] = None

        if req.generate_user_hook_md:
            try:
                from app.services.llm_service import llm_service
                from app.services.youtube_service import youtube_service

                yt_data = None
                if PlatformChoice.YOUTUBE in req.platforms:
                    yt_handle = handles.get("youtube", req.creator_name)
                    yt_data = youtube_service.fetch_creator_videos(
                        creator_name=req.creator_name,
                        channel_url_or_handle=yt_handle,
                        max_videos=5
                    )

                ig_data = None
                if PlatformChoice.INSTAGRAM in req.platforms:
                    ig_prof = creator_profiles_dict.get("instagram")
                    if ig_prof and ig_prof.recent_content:
                        ig_data = {"posts": ig_prof.recent_content}

                tw_data = None
                if PlatformChoice.X_TWITTER in req.platforms:
                    tw_prof = creator_profiles_dict.get("x_twitter")
                    if tw_prof and tw_prof.recent_content:
                        tw_data = {"posts": tw_prof.recent_content}

                li_data = None
                if PlatformChoice.LINKEDIN in req.platforms:
                    li_prof = creator_profiles_dict.get("linkedin")
                    if li_prof and li_prof.recent_content:
                        li_data = {"posts": li_prof.recent_content}

                causes_str = ", ".join(causes_or_topics) if causes_or_topics else effective_niche
                prof_res = llm_service.profile_creator(
                    creator_name=req.creator_name,
                    youtube_data=yt_data or {},
                    instagram_data=ig_data,
                    twitter_data=tw_data,
                    linkedin_data=li_data,
                    custom_instructions=f"Focus on creator's domain and work pillars: {causes_str}",
                    language=req.language,
                    niche=effective_niche
                )
                user_md_path_str = prof_res["file_paths"]["user_md"]
                hook_md_path_str = prof_res["file_paths"]["hook_md"]
                detected_lang_str = prof_res.get("detected_language")

                # Generate creator_comparison.md benchmarking against top domain peers
                slug = req.creator_name.lower().replace(" ", "_")
                creator_dir = str(settings.CREATORS_DIR / slug)
                comparison_path = creator_comparator_service.generate_creator_comparison_md(
                    base_creator=req.creator_name,
                    output_dir=creator_dir
                )
                logger.info(f"[Intel] Successfully generated user.md, hook.md & creator_comparison.md for {req.creator_name} in {detected_lang_str} ({domain_profile.domain_name})")
            except Exception as e:
                logger.warning(f"[Intel] Error generating dossiers: {e}")

        # Compute comparative intelligence for all top creators of this domain
        domain_key = getattr(domain_profile, 'domain_id', 'civic_social_issues')
        top_leaders = creator_comparator_service.get_top_creators_for_domain(domain_key)
        domain_top_creators: List[Dict[str, Any]] = []
        domain_leader_comparisons: List[Dict[str, Any]] = []
        for leader in top_leaders:
            l_name = leader.get("name", "")
            if l_name.lower().strip() == req.creator_name.lower().strip():
                continue
            domain_top_creators.append({
                "name": l_name,
                "handle": leader.get("handle", ""),
                "subscribers": leader.get("subscribers", ""),
                "cross_platform_reach": leader.get("cross_platform_reach", ""),
                "core_style": leader.get("core_style", ""),
                "hook_archetype": leader.get("hook_archetype", "")
            })
            try:
                comp_res = creator_comparator_service.compare_creators(base_creator=req.creator_name, competitor=l_name)
                domain_leader_comparisons.append({
                    "leader_name": l_name,
                    "leader_handle": leader.get("handle", ""),
                    "leader_subscribers": leader.get("subscribers", ""),
                    "core_style": leader.get("core_style", ""),
                    "how_they_differ": comp_res.get("content_differences", []),
                    "how_to_improve": comp_res.get("content_improvement_playbook", []),
                    "speech_differences": comp_res.get("speech_differences", []),
                    "user_advantages": comp_res.get("user_advantages", [])
                })
            except Exception as e:
                logger.debug(f"Leader comparison error for {l_name}: {e}")

        from app.services.trends_service import trends_service
        trending_keywords = trends_service.extract_trending_keywords(domain_profile.domain_name, limit=12)

        summary = self._generate_summary(req.creator_name, effective_niche, platform_blocks)

        return IntelligenceResponse(
            creator_name=req.creator_name,
            niche=effective_niche,
            location=req.location,
            analyzed_at=now,
            platforms_analyzed=[p.value for p in req.platforms],
            creator_profiles=creator_profiles_dict,
            platform_trends=platform_blocks,
            top_recommendations=recommendations[:10],
            platform_md_files=md_files,
            detected_language=detected_lang_str,
            identified_domain=domain_profile.domain_name,
            domain_profile=domain_profile.model_dump(),
            user_md_path=user_md_path_str,
            hook_md_path=hook_md_path_str,
            creator_comparison_md_path=comparison_path,
            domain_top_creators=domain_top_creators,
            domain_leader_comparisons=domain_leader_comparisons,
            trending_keywords=trending_keywords,
            summary=summary,
        )

    # ──────────────────────────────────────────────
    # YouTube Scanner & Creator Extractor
    # ──────────────────────────────────────────────

    def _scan_youtube(
        self, creator_name: str, niche: str, location: str, handle: str, goal: str, causes_or_topics: Optional[List[str]] = None
    ) -> PlatformTrendsBlock:
        # 1. Extract creator-specific profile info
        creator_profile = self._extract_youtube_creator_profile(creator_name, handle, niche)

        # 2. Discover trending videos in creator's WORK / CAUSES / DOMAIN (NOT creator's name!)
        cause_query = causes_or_topics[0] if causes_or_topics else niche
        domain_trends = self._youtube_search_trending(cause_query, location, limit=8)
        global_trends = self._youtube_trending_feed(location, limit=6)
        location_trends = self._youtube_search_trending(f"{cause_query} {location}", location, limit=5)

        hashtags = self._youtube_trending_hashtags(cause_query)
        strategy = self._youtube_strategy(niche, goal)

        return PlatformTrendsBlock(
            platform="youtube",
            goal=goal,
            creator_profile=creator_profile,
            domain_trends=domain_trends,
            location_trends=location_trends,
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy=strategy,
        )

    def _extract_youtube_creator_profile(
        self, creator_name: str, handle: str, niche: str
    ) -> CreatorPlatformProfile:
        """Extracts authentic YouTube channel metrics and recent uploads using YouTube API v3 or yt-dlp."""
        clean_handle = handle.replace("@", "").strip() if handle else creator_name.strip()
        profile = CreatorPlatformProfile(
            platform="youtube",
            handle=f"@{clean_handle}",
            profile_url=f"https://www.youtube.com/@{clean_handle}",
            display_name=creator_name,
        )

        # 1. Primary: Scrape YouTube channel & video uploads via Composio
        try:
            comp_res = composio_scraper_service.scrape_youtube_channel(clean_handle, max_videos=5)
            if comp_res and comp_res.get("videos"):
                profile.display_name = comp_res.get("channel_title", creator_name)
                profile.bio = comp_res.get("description", "")
                profile.follower_or_sub_count = comp_res.get("subscriber_count")
                profile.total_posts_or_videos = comp_res.get("total_videos")
                profile.verified = True
                for v in comp_res.get("videos", []):
                    profile.recent_content.append({
                        "title": v.get("title", ""),
                        "url": v.get("url"),
                        "published_at": v.get("published_at", ""),
                        "thumbnail": v.get("thumbnail"),
                        "content_type": "video",
                        "source": "composio"
                    })
        except Exception as e:
            logger.debug(f"Composio YouTube scrape notice: {e}")

        # 2. Secondary fallback: YouTube Data API v3
        api_key = settings.YOUTUBE_API_KEY
        if api_key and not profile.recent_content:
            try:
                # 1. Query channels endpoint by forHandle
                url = "https://www.googleapis.com/youtube/v3/channels"
                with httpx.Client(timeout=8.0) as client:
                    res = client.get(url, params={
                        "part": "snippet,statistics,contentDetails",
                        "forHandle": clean_handle,
                        "key": api_key,
                    })
                    item = None
                    if res.status_code == 200:
                        items = res.json().get("items", [])
                        if items:
                            item = items[0]

                    # If not found by forHandle, try searching channel
                    if not item:
                        search_url = "https://www.googleapis.com/youtube/v3/search"
                        s_res = client.get(search_url, params={
                            "part": "snippet",
                            "q": clean_handle or creator_name,
                            "type": "channel",
                            "maxResults": 1,
                            "key": api_key
                        })
                        if s_res.status_code == 200:
                            s_items = s_res.json().get("items", [])
                            if s_items:
                                cid = s_items[0].get("id", {}).get("channelId")
                                if cid:
                                    c_res = client.get(url, params={
                                        "part": "snippet,statistics,contentDetails",
                                        "id": cid,
                                        "key": api_key
                                    })
                                    if c_res.status_code == 200:
                                        c_items = c_res.json().get("items", [])
                                        if c_items:
                                            item = c_items[0]

                    if item:
                        snippet = item.get("snippet", {})
                        stats = item.get("statistics", {})
                        content_details = item.get("contentDetails", {})

                        profile.display_name = snippet.get("title", creator_name)
                        profile.bio = snippet.get("description", "")
                        sub_cnt = stats.get("subscriberCount")
                        profile.follower_or_sub_count = f"{int(sub_cnt):,} subscribers" if sub_cnt else None
                        vid_cnt = stats.get("videoCount")
                        profile.total_posts_or_videos = f"{int(vid_cnt):,} videos" if vid_cnt else None
                        custom_url = snippet.get("customUrl")
                        profile.profile_url = f"https://www.youtube.com/{custom_url}" if custom_url else f"https://www.youtube.com/@{clean_handle}"
                        profile.verified = True

                        # Fetch recent videos from uploads playlist
                        uploads_playlist = content_details.get("relatedPlaylists", {}).get("uploads")
                        if uploads_playlist:
                            pl_res = client.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
                                "part": "snippet",
                                "playlistId": uploads_playlist,
                                "maxResults": 5,
                                "key": api_key
                            })
                            if pl_res.status_code == 200:
                                for p_item in pl_res.json().get("items", []):
                                    p_snip = p_item.get("snippet", {})
                                    vid_id = p_snip.get("resourceId", {}).get("videoId", "")
                                    profile.recent_content.append({
                                        "title": p_snip.get("title", ""),
                                        "url": f"https://www.youtube.com/watch?v={vid_id}" if vid_id else None,
                                        "published_at": p_snip.get("publishedAt", ""),
                                        "thumbnail": p_snip.get("thumbnails", {}).get("high", {}).get("url"),
                                        "content_type": "video"
                                    })
            except Exception as e:
                logger.warning(f"YouTube channel profile extraction error: {e}")

        # Fallback to local youtube_service if empty
        if not profile.recent_content:
            try:
                from app.services.youtube_service import youtube_service
                yt_res = youtube_service.fetch_creator_videos(creator_name, handle, max_videos=3)
                for v in yt_res.get("videos", []):
                    profile.recent_content.append({
                        "title": v.title,
                        "url": v.url,
                        "views": f"{v.view_count:,} views" if v.view_count else None,
                        "duration": v.duration_formatted,
                        "hook": v.key_opening_words,
                        "content_type": "short" if v.is_short else "video"
                    })
                if not profile.follower_or_sub_count and yt_res.get("metadata", {}).get("subscriber_count"):
                    profile.follower_or_sub_count = f"{yt_res['metadata']['subscriber_count']:,} subscribers"
            except Exception as e:
                logger.debug(f"YouTube service fallback error: {e}")

        profile.growth_gap_analysis = (
            f"YouTube Channel has {profile.follower_or_sub_count or 'growing audience'} with {profile.total_posts_or_videos or 'an active video catalog'}. "
            f"To accelerate subscriber growth in '{niche}', prioritize 30-60 second Shorts targeting searchable 'How-to' queries, "
            f"and optimize the first 5 seconds with pattern-interrupt hooks to increase watch-through rate."
        )
        return profile

    @staticmethod
    def _normalize_country_code(location: Optional[str]) -> str:
        """Normalizes location strings like 'India', 'United States', 'UK' into valid ISO-3166-1 alpha-2 codes."""
        if not location or not location.strip():
            return "US"
        loc = location.strip().lower()
        mapping = {
            "india": "IN", "in": "IN",
            "united states": "US", "usa": "US", "us": "US", "america": "US",
            "united kingdom": "GB", "uk": "GB", "great britain": "GB", "england": "GB", "gb": "GB",
            "canada": "CA", "ca": "CA",
            "australia": "AU", "au": "AU",
            "germany": "DE", "deutschland": "DE", "de": "DE",
            "france": "FR", "fr": "FR",
            "spain": "ES", "es": "ES",
            "brazil": "BR", "br": "BR",
            "japan": "JP", "jp": "JP",
            "south korea": "KR", "korea": "KR", "kr": "KR",
            "uae": "AE", "united arab emirates": "AE", "dubai": "AE", "ae": "AE",
            "singapore": "SG", "sg": "SG",
            "indonesia": "ID", "id": "ID",
            "pakistan": "PK", "pk": "PK",
            "bangladesh": "BD", "bd": "BD",
            "russia": "RU", "ru": "RU",
            "italy": "IT", "it": "IT",
            "mexico": "MX", "mx": "MX",
            "netherlands": "NL", "nl": "NL",
            "south africa": "ZA", "za": "ZA",
            "nigeria": "NG", "ng": "NG",
            "philippines": "PH", "ph": "PH",
        }
        if loc in mapping:
            return mapping[loc]
        if len(loc) == 2 and loc.isalpha():
            return loc.upper()
        return "US"

    def _youtube_search_trending(self, query: str, location: str, limit: int = 8) -> List[TrendItem]:
        """Uses YouTube Data API v3 or Google News RSS fallback to search for trending videos in a niche."""
        api_key = settings.YOUTUBE_API_KEY
        items: List[TrendItem] = []

        if api_key:
            try:
                region = self._normalize_country_code(location)
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "order": "viewCount",
                    "regionCode": region,
                    "maxResults": limit,
                    "key": api_key,
                }
                with httpx.Client(timeout=10.0) as client:
                    res = client.get(url, params=params)
                    if res.status_code == 200:
                        data = res.json()
                        for rank, item in enumerate(data.get("items", [])[:limit], 1):
                            snippet = item.get("snippet", {})
                            vid_id = item.get("id", {}).get("videoId", "")
                            items.append(TrendItem(
                                rank=rank,
                                title=snippet.get("title", ""),
                                url=f"https://www.youtube.com/watch?v={vid_id}" if vid_id else None,
                                platform="youtube",
                                content_type="video",
                                published_date=snippet.get("publishedAt", ""),
                                creator_handle=snippet.get("channelTitle", ""),
                                why_trending=f"High view velocity in '{query}' search results",
                                relevance_to_niche=f"Directly related to {query}",
                                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url"),
                            ))
            except Exception as e:
                logger.debug(f"YouTube API search error: {e}")

        # Fallback to Google News RSS for YouTube videos if API returned empty
        if not items:
            try:
                rss_q = f"{query} site:youtube.com"
                rss_url = f"https://news.google.com/rss/search?q={rss_q.replace(' ', '+')}&hl=en"
                feed = feedparser.parse(rss_url)
                for rank, entry in enumerate(feed.entries[:limit], 1):
                    title = entry.get("title", "").replace("- YouTube", "").strip()
                    items.append(TrendItem(
                        rank=rank,
                        title=title,
                        url=entry.get("link", ""),
                        platform="youtube",
                        content_type="video",
                        published_date=entry.get("published", ""),
                        creator_handle=entry.get("source", {}).get("title", ""),
                        why_trending=f"Trending topic in '{query}'",
                        relevance_to_niche=f"Directly related to {query}",
                    ))
            except Exception as e:
                logger.debug(f"YouTube RSS fallback failed: {e}")

        return items

    def _youtube_trending_feed(self, location: str, limit: int = 6) -> List[TrendItem]:
        """Fetches YouTube's official trending feed via API, with Google News RSS fallback."""
        api_key = settings.YOUTUBE_API_KEY
        items: List[TrendItem] = []
        region = self._normalize_country_code(location)

        if api_key:
            try:
                url = "https://www.googleapis.com/youtube/v3/videos"
                params = {
                    "part": "snippet,statistics",
                    "chart": "mostPopular",
                    "regionCode": region,
                    "maxResults": limit,
                    "key": api_key,
                }
                with httpx.Client(timeout=10.0) as client:
                    res = client.get(url, params=params)
                    if res.status_code == 200:
                        data = res.json()
                        for rank, vid in enumerate(data.get("items", [])[:limit], 1):
                            snippet = vid.get("snippet", {})
                            stats = vid.get("statistics", {})
                            items.append(TrendItem(
                                rank=rank,
                                title=snippet.get("title", ""),
                                url=f"https://www.youtube.com/watch?v={vid.get('id', '')}",
                                platform="youtube",
                                content_type="video",
                                views_or_engagement=f"{int(stats.get('viewCount', 0)):,} views",
                                published_date=snippet.get("publishedAt", ""),
                                creator_handle=snippet.get("channelTitle", ""),
                                why_trending="YouTube Trending chart (official)",
                                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url"),
                            ))
            except Exception as e:
                logger.warning(f"YouTube trending feed API failed: {e}")

        # Fallback to Google News RSS for global/regional YouTube trending if API fails or quota exceeded
        if not items:
            try:
                rss_q = f"trending videos site:youtube.com"
                rss_url = f"https://news.google.com/rss/search?q={rss_q.replace(' ', '+')}&hl=en"
                feed = feedparser.parse(rss_url)
                for rank, entry in enumerate(feed.entries[:limit], 1):
                    title = entry.get("title", "").replace("- YouTube", "").strip()
                    items.append(TrendItem(
                        rank=rank,
                        title=title,
                        url=entry.get("link", ""),
                        platform="youtube",
                        content_type="video",
                        published_date=entry.get("published", ""),
                        creator_handle=entry.get("source", {}).get("title", "YouTube Trending"),
                        why_trending=f"High velocity trend in {region}",
                        relevance_to_niche="Popular video",
                    ))
            except Exception as e:
                logger.debug(f"YouTube trending feed RSS fallback failed: {e}")

        return items

    def _youtube_trending_hashtags(self, niche: str) -> List[str]:
        niche_lower = niche.lower()
        base = ["#Shorts", "#Trending", "#Viral"]
        if any(kw in niche_lower for kw in ["tech", "ai", "code", "dev"]):
            return base + ["#TechTube", "#AIExplained", "#CodingTutorial", "#TechReview", "#LearnToCode"]
        elif any(kw in niche_lower for kw in ["fitness", "gym", "workout"]):
            return base + ["#FitnessTube", "#GymLife", "#WorkoutMotivation", "#HealthyLiving"]
        elif any(kw in niche_lower for kw in ["finance", "money", "invest"]):
            return base + ["#MoneyTube", "#InvestingTips", "#FinancialFreedom", "#StockMarket"]
        return base + [f"#{niche.replace(' ', '')}", "#ContentCreator", "#YouTube"]

    def _youtube_strategy(self, niche: str, goal: str) -> str:
        return (
            f"**YouTube Strategy for '{niche}' (Core Goal: 👥 Increase Subscribers)**\n"
            f"• Publish 2-3 Shorts weekly directly converting to long-form deep-dives via related video links to maximize new subscriber acquisition\n"
            f"• Opening 0-5s: Deliver instant high-clarity hook stating the exact truth/system without rambling intro greetings\n"
            f"• Mid-roll Subscribe Anchor: Insert verbal and visual subscribe prompt at the peak curiosity climax (minute 4-6) when value is highest\n"
            f"• End Screens & Pinned Comment: Direct viewer to a curated 3-part playlist to trigger binge-watching loops (the #1 subscriber growth driver)\n"
            f"• Search-Optimized Titles: Combine the core civic/domain problem + provocative curiosity question (e.g. 'The Real Truth Behind [Issue]')\n"
            f"• High-CTR Thumbnails: High contrast, maximum 3 words, expressive direct gaze, single clear focal evidence object"
        )

    # ──────────────────────────────────────────────
    # Instagram Scanner & Creator Extractor
    # ──────────────────────────────────────────────

    def _scan_instagram(
        self, creator_name: str, niche: str, location: str, handle: str, goal: str, causes_or_topics: Optional[List[str]] = None
    ) -> PlatformTrendsBlock:
        creator_profile = self._extract_instagram_creator_profile(creator_name, handle, niche)

        cause_query = causes_or_topics[0] if causes_or_topics else niche
        hashtag_data = instagram_service.fetch_trending_hashtags_for_niche(cause_query, location)
        hashtags = [h["tag"] for h in hashtag_data]

        domain_trends = []
        # 1. Option A: Scrape real-time domain Reels via Bright Data
        try:
            bright_trends = bright_data_service.scrape_instagram_reels(cause_query, location, limit=6)
            if bright_trends:
                domain_trends.extend(bright_trends)
        except Exception as e:
            logger.debug(f"Bright Data Instagram reels notice: {e}")

        # 2. Option B: Scrape real-time domain-relevant posts/reels via Apify
        if len(domain_trends) < 5:
            try:
                apify_trends = apify_service.scrape_instagram_trends(cause_query, location, limit=6)
                if apify_trends:
                    domain_trends.extend(apify_trends)
            except Exception as e:
                logger.debug(f"Apify Instagram trend notice: {e}")

        # 2. Supplementary/Fallback: Ensure at least 5 rich domain Reels are always returned
        if len(domain_trends) < 5:
            queries_to_try = causes_or_topics[:3] if causes_or_topics else [cause_query]
            for c_q in queries_to_try:
                if len(domain_trends) >= 6:
                    break
                reels_data = instagram_service.fetch_trending_reels_for_niche(c_q, location)
                for reel in reels_data:
                    if len(domain_trends) >= 6:
                        break
                    if not any(d.title == reel.get("title") for d in domain_trends):
                        domain_trends.append(TrendItem(
                            rank=len(domain_trends) + 1,
                            title=reel.get("title", f"Trending {c_q} Reel"),
                            url=reel.get("url"),
                            platform="instagram",
                            content_type="reel",
                            why_trending=f"Discovered via {reel.get('source', 'Instagram Explore')}",
                            relevance_to_niche=f"Directly relevant to {c_q}",
                            hashtags=[h["tag"] for h in hashtag_data[:5]],
                        ))

        location_reels_data = instagram_service.fetch_trending_reels_for_niche(f"{cause_query} {location}", location)
        location_trends = []
        for idx, reel in enumerate(location_reels_data[:5], 1):
            location_trends.append(TrendItem(
                rank=idx,
                title=reel.get("title", f"Viral {location} Reel"),
                url=reel.get("url"),
                platform="instagram",
                content_type="reel",
                why_trending=f"Trending in {location}",
                relevance_to_niche=f"Location viral reel ({location})"
            ))

        global_trends = self._google_trends_rss(location, limit=5, platform_label="instagram")

        strategy_lines = [
            f"**Instagram Strategy for '{niche}' (Core Goal: 🚀 Get More Views & Followers)**",
            f"• Reels-First Distribution: Allocate 80% of production to 7-15s fast-looping Reels to trigger the Explore algorithm",
            f"• Visual Accessibility: 80% of users watch without sound — use high-contrast kinetic subtitles and bold hook text overlays in 0-2s",
            f"• Trending Sound Adoption: Layer emerging trending audio at 5-10% volume behind spoken audio within 24h of release",
            f"• Follower Conversion CTA: Conclude with a clear reason to follow: 'Follow for daily ground-reality breakdowns and unbiased facts'",
            f"• Optimal Posting Windows: 6:00 PM - 8:30 PM (peak mobile leisure hours)",
        ]

        return PlatformTrendsBlock(
            platform="instagram",
            goal=goal,
            creator_profile=creator_profile,
            domain_trends=domain_trends,
            location_trends=location_trends,
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy="\n".join(strategy_lines),
        )

    def _extract_instagram_creator_profile(
        self, creator_name: str, handle: str, niche: str
    ) -> CreatorPlatformProfile:
        """Extracts public Instagram follower stats, bio, and recent post snippets."""
        clean_handle = handle.replace("@", "").strip() if handle else re.sub(r'[^a-zA-Z0-9._]', '', creator_name.lower())
        profile = CreatorPlatformProfile(
            platform="instagram",
            handle=f"@{clean_handle}",
            profile_url=f"https://www.instagram.com/{clean_handle}/",
            display_name=creator_name,
        )

        # 1. Option A: Try Bright Data Profile Dataset
        try:
            bd_prof = bright_data_service.scrape_instagram_profile(clean_handle)
            if bd_prof:
                profile.display_name = bd_prof.get("full_name") or creator_name
                profile.bio = bd_prof.get("biography") or profile.bio
                profile.follower_or_sub_count = bd_prof.get("followers_count")
                profile.following_count = bd_prof.get("following_count")
                profile.total_posts_or_videos = bd_prof.get("total_posts")
                profile.verified = bd_prof.get("verified", False)
        except Exception as e:
            logger.debug(f"Bright Data profile notice: {e}")

        # 2. Option B: Scrape authentic Instagram profile metrics, verified status, and latest posts via Apify
        if not profile.follower_or_sub_count:
            try:
                apify_prof = apify_service.scrape_instagram_profile(clean_handle)
                if apify_prof:
                    profile.display_name = apify_prof.get("full_name") or creator_name
                    profile.bio = apify_prof.get("biography") or profile.bio
                    profile.follower_or_sub_count = apify_prof.get("followers_count")
                    profile.following_count = apify_prof.get("following_count")
                    profile.total_posts_or_videos = apify_prof.get("total_posts")
                    profile.verified = apify_prof.get("verified", False)
                    profile.profile_url = apify_prof.get("profile_url", profile.profile_url)
                    if apify_prof.get("recent_content"):
                        profile.recent_content.extend(apify_prof["recent_content"])
            except Exception as e:
                logger.debug(f"Apify Instagram profile scrape notice: {e}")

        # 2. Secondary: Try Composio Instagram connected account scraping
        if not profile.recent_content:
            try:
                comp_ig = composio_scraper_service.scrape_instagram_profile(clean_handle)
                if comp_ig and comp_ig.get("recent_posts"):
                    for p in comp_ig["recent_posts"]:
                        profile.recent_content.append({
                            "caption": p.get("caption", ""),
                            "url": p.get("url"),
                            "content_type": "post_or_reel",
                            "source": "composio"
                        })
            except Exception as e:
                logger.debug(f"Composio Instagram scrape notice: {e}")

        # 3. Tertiary fallback: DuckDuckGo public snippet & Google News
        if not profile.follower_or_sub_count:
            try:
                ddg_url = "https://html.duckduckgo.com/html/"
                query = f"site:instagram.com/{clean_handle}"
                with httpx.Client(timeout=8.0) as client:
                    r = client.post(ddg_url, data={"q": query}, headers=HEADERS)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, "html.parser")
                        for a in soup.find_all("div", class_="result"):
                            snip_el = a.find("a", class_="result__snippet")
                            if not snip_el:
                                continue
                            snip = snip_el.get_text(strip=True)

                            m = re.search(r"([0-9\.,MKkmb]+)\s+Followers[,\s]+([0-9\.,MKkmb]+)\s+Following[,\s]+([0-9\.,MKkmb]+)\s+Posts", snip, re.I)
                            if m and not profile.follower_or_sub_count:
                                profile.follower_or_sub_count = f"{m.group(1)} followers"
                                profile.following_count = f"{m.group(2)} following"
                                profile.total_posts_or_videos = f"{m.group(3)} posts"
                                bio_m = re.search(r'"([^"]+)"', snip)
                                if bio_m:
                                    profile.bio = bio_m.group(1)

                            post_m = re.search(r"([0-9\.,MKkmb]+)\s+likes?,\s+([0-9\.,MKkmb]+)\s+comments?\s+-\s+([^:]+)\s*:\s*\"([^\"]+)\"", snip, re.I)
                            if post_m:
                                profile.recent_content.append({
                                    "likes": post_m.group(1),
                                    "comments": post_m.group(2),
                                    "meta": post_m.group(3).strip(),
                                    "caption": post_m.group(4).strip(),
                                    "content_type": "post_or_reel"
                                })
            except Exception as e:
                logger.debug(f"Instagram profile extraction error: {e}")

        if not profile.recent_content:
            try:
                q = f"{creator_name} instagram reel OR viral"
                feed_url = f"https://news.google.com/rss/search?q={q.replace(' ', '+')}&hl=en"
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:
                    profile.recent_content.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "published_at": entry.get("published", ""),
                        "content_type": "reel_mention"
                    })
            except Exception:
                pass

        profile.growth_gap_analysis = (
            f"Instagram presence ({profile.handle}): Currently has {profile.follower_or_sub_count or 'an established presence'}. "
            f"To maximize viral reach in '{niche}', shift 70% of production to 7-15s Reels using trending audio within 24 hours of release, "
            f"and include clear on-screen text hooks for the 80% of viewers watching without audio."
        )
        return profile

    # ──────────────────────────────────────────────
    # LinkedIn Scanner & Creator Extractor
    # ──────────────────────────────────────────────

    def _scan_linkedin(
        self, creator_name: str, niche: str, location: str, handle: str, goal: str, causes_or_topics: Optional[List[str]] = None
    ) -> PlatformTrendsBlock:
        creator_profile = self._extract_linkedin_creator_profile(creator_name, handle, niche)
        cause_query = causes_or_topics[0] if causes_or_topics else niche
        
        domain_trends = []
        # 1. Primary: Scrape real-time domain discussions via Apify LinkedIn actor
        try:
            apify_li = apify_service.scrape_linkedin_trends(cause_query, location, limit=6)
            if apify_li:
                domain_trends.extend(apify_li)
        except Exception as e:
            logger.debug(f"Apify LinkedIn trend notice: {e}")

        # 2. Supplementary/Fallback: Google News for LinkedIn articles
        if not domain_trends:
            domain_trends = self._linkedin_trending_articles(cause_query, location)

        global_trends = self._google_trends_rss(location, limit=5, platform_label="linkedin")
        hashtags = self._linkedin_trending_hashtags(cause_query)

        strategy = (
            f"**LinkedIn Strategy for '{niche}' (Core Goal: 🤝 Increase Reach & Connections, Spread Domain Insights)**\n"
            f"• High-Authority Domain Posts: Share 3-5x/week breaking down critical issues in '{cause_query}' with objective data\n"
            f"• High-Converting Hook: First 2 lines before 'see more' must highlight an urgent industry problem or surprising statistic\n"
            f"• Connection Multiplier: End every post with an open question prompting professionals to comment, triggering 2nd-degree feed distribution\n"
            f"• Document/PDF Carousels: Convert detailed research into 5-8 slide visual breakdowns (achieves 3x greater dwell time)\n"
            f"• Targeted Networking: Engage thoughtfully on 10 top creators/industry voices in '{cause_query}' daily to drive organic profile visits\n"
            f"• Optimal Posting Times: 7:30-8:30 AM or 5:00-6:00 PM (local timezone)"
        )

        return PlatformTrendsBlock(
            platform="linkedin",
            goal=goal,
            creator_profile=creator_profile,
            domain_trends=domain_trends,
            location_trends=[],
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy=strategy,
        )

    def _extract_linkedin_creator_profile(
        self, creator_name: str, handle: str, niche: str
    ) -> CreatorPlatformProfile:
        """Extracts public LinkedIn professional details and recent publications."""
        clean_vanity = handle.replace("@", "").strip() if handle else re.sub(r'[^a-zA-Z0-9-]', '-', creator_name.lower())
        if "linkedin.com/in/" in clean_vanity:
            clean_vanity = clean_vanity.split("linkedin.com/in/")[-1].split("/")[0]

        profile = CreatorPlatformProfile(
            platform="linkedin",
            handle=clean_vanity,
            profile_url=f"https://www.linkedin.com/in/{clean_vanity}",
            display_name=creator_name,
        )

        # 1. Primary: Try Composio LinkedIn connected account scraping
        try:
            comp_li = composio_scraper_service.scrape_linkedin_profile(clean_vanity)
            if comp_li:
                profile.display_name = comp_li.get("full_name", creator_name)
                profile.bio = comp_li.get("headline", "")
                profile.profile_url = comp_li.get("profile_url", profile.profile_url)
                profile.verified = True
        except Exception as e:
            logger.debug(f"Composio LinkedIn scrape notice: {e}")

        try:
            q = f"site:linkedin.com {creator_name or clean_vanity}"
            feed_url = f"https://news.google.com/rss/search?q={q.replace(' ', '+')}&hl=en"
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:4]:
                title = entry.get("title", "").replace("- LinkedIn", "").strip()
                link = entry.get("link", "")
                pub = entry.get("published", "")
                profile.recent_content.append({
                    "title": title,
                    "url": link,
                    "published_at": pub,
                    "content_type": "post_or_article"
                })
                if not profile.bio and (" - " in title or " | " in title):
                    profile.bio = title
        except Exception as e:
            logger.debug(f"LinkedIn profile extraction error: {e}")

        profile.growth_gap_analysis = (
            f"LinkedIn presence: Focused on '{niche}' domain leadership. "
            f"To accelerate connections and professional reach, convert key long-form takeaways into 5-7 slide PDF Carousels, "
            f"and start posts with a contrarian 1-sentence hook before revealing actionable steps."
        )
        return profile

    def _linkedin_trending_articles(self, niche: str, location: str) -> List[TrendItem]:
        """Scrapes Google News for LinkedIn-relevant trending content in the niche."""
        items: List[TrendItem] = []
        try:
            query = f"{niche} linkedin trending {location} site:linkedin.com"
            search_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-{location[:2].upper()}"
            feed = feedparser.parse(search_url)
            for rank, entry in enumerate(feed.entries[:6], 1):
                items.append(TrendItem(
                    rank=rank,
                    title=entry.get("title", ""),
                    url=entry.get("link", ""),
                    platform="linkedin",
                    content_type="article",
                    published_date=entry.get("published", ""),
                    creator_handle=entry.get("source", {}).get("title", ""),
                    why_trending="Trending in Google News for LinkedIn",
                    relevance_to_niche=f"Relevant to {niche}",
                ))
        except Exception as e:
            logger.debug(f"LinkedIn article scraping failed: {e}")
        return items

    def _linkedin_trending_hashtags(self, niche: str) -> List[str]:
        niche_lower = niche.lower()
        base = ["#LinkedInCreator", "#ContentCreator", "#PersonalBrand"]
        if any(kw in niche_lower for kw in ["tech", "ai", "software", "code"]):
            return base + ["#AI", "#MachineLearning", "#TechLeadership", "#StartupFounder", "#Innovation"]
        elif any(kw in niche_lower for kw in ["finance", "money", "invest"]):
            return base + ["#FinTech", "#InvestmentStrategy", "#WealthManagement", "#Finance"]
        elif any(kw in niche_lower for kw in ["fitness", "health"]):
            return base + ["#WellnessCoach", "#HealthTech", "#CorporateWellness"]
        return base + [f"#{niche.replace(' ', '')}", "#ThoughtLeadership", "#GrowthMindset"]

    # ──────────────────────────────────────────────
    # X (Twitter) Scanner & Creator Extractor
    # ──────────────────────────────────────────────

    def _scan_x_twitter(
        self, creator_name: str, niche: str, location: str, handle: str, goal: str, causes_or_topics: Optional[List[str]] = None
    ) -> PlatformTrendsBlock:
        creator_profile = self._extract_x_creator_profile(creator_name, handle, niche)
        cause_query = causes_or_topics[0] if causes_or_topics else niche
        domain_trends = self._x_niche_trends(cause_query, location)
        global_trends = self._google_trends_rss(location, limit=5, platform_label="x_twitter")
        hashtags = self._x_trending_hashtags(cause_query)

        strategy = (
            f"**X (Twitter) Strategy for '{niche}' (Core Goal: 🌐 Increase Reach & Spread Domain Awareness)**\n"
            f"• Daily Domain Drops: Post 2-3 single-punch insights or infographics daily discussing key developments in '{cause_query}'\n"
            f"• High-Impact Viral Threads: Publish 1 weekly 5-8 tweet deep-dive on a pressing cause topic optimized for bookmark saves\n"
            f"• Pattern-Interrupt Opening Hook: Strong declarative statement challenging a common narrative, backed by immediate evidence\n"
            f"• Community & Connections: Quote-tweet trending discussions in '{cause_query}', tagging relevant researchers or organizations\n"
            f"• Clear Domain Spread CTA: Conclude threads asking viewers to Retweet/Repost if they believe this issue needs public visibility"
        )

        return PlatformTrendsBlock(
            platform="x_twitter",
            goal=goal,
            creator_profile=creator_profile,
            domain_trends=domain_trends,
            location_trends=[],
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy=strategy,
        )

    def _extract_x_creator_profile(
        self, creator_name: str, handle: str, niche: str
    ) -> CreatorPlatformProfile:
        """Extracts authentic X/Twitter metrics, followers, and recent tweets via Twitter API v2 with Bearer Token."""
        clean_handle = handle.replace("@", "").strip() if handle else re.sub(r'[^a-zA-Z0-9_]', '', creator_name.lower())
        if "x.com/" in clean_handle or "twitter.com/" in clean_handle:
            clean_handle = clean_handle.split("/")[-1].replace("@", "")

        return twitter_api_service.extract_creator_profile(creator_name, clean_handle, niche)

    def _x_niche_trends(self, niche: str, location: str) -> List[TrendItem]:
        """Discovers trending X/Twitter discussions via Twitter API v2 with Bearer Token, with RSS fallback."""
        return twitter_api_service.search_domain_tweets(niche, location, limit=8)

    def _x_trending_hashtags(self, niche: str) -> List[str]:
        niche_lower = niche.lower()
        base = ["#XPost", "#Thread", "#Viral"]
        if any(kw in niche_lower for kw in ["tech", "ai", "software", "code"]):
            return base + ["#AITwitter", "#TechTwitter", "#BuildInPublic", "#IndieHacker", "#DevCommunity"]
        elif any(kw in niche_lower for kw in ["finance", "money", "invest", "crypto"]):
            return base + ["#FinTwit", "#CryptoTwitter", "#Bitcoin", "#StockMarket", "#DeFi"]
        elif any(kw in niche_lower for kw in ["fitness", "health"]):
            return base + ["#FitTwitter", "#HealthTwitter", "#GymMotivation"]
        return base + [f"#{niche.replace(' ', '')}", "#ContentCreator"]

    # ──────────────────────────────────────────────
    # Shared Helpers
    # ──────────────────────────────────────────────

    def _google_trends_rss(self, geo: str, limit: int = 5, platform_label: str = "") -> List[TrendItem]:
        """Fetches Google Trends RSS as a global trend signal."""
        items: List[TrendItem] = []
        try:
            url = f"https://trends.google.com/trending/rss?geo={geo[:2].upper()}"
            feed = feedparser.parse(url)
            for rank, entry in enumerate(feed.entries[:limit], 1):
                title = getattr(entry, "title", "Trending Topic")
                traffic = getattr(entry, "ht_approx_traffic", "100K+ searches")
                items.append(TrendItem(
                    rank=rank,
                    title=title.title(),
                    platform=platform_label or "global",
                    content_type="trending_topic",
                    views_or_engagement=traffic,
                    published_date=getattr(entry, "published", "Today"),
                    why_trending="Google Trends Real-Time RSS",
                    suggested_angle=f"Create a '{title}' hot-take or explainer from your {platform_label} perspective",
                ))
        except Exception as e:
            logger.debug(f"Google Trends RSS failed: {e}")
        return items

    def _recent_date_iso(self) -> str:
        """Returns ISO date for 7 days ago (for YouTube API publishedAfter)."""
        from datetime import timedelta
        d = datetime.now(timezone.utc) - timedelta(days=7)
        return d.strftime("%Y-%m-%dT00:00:00Z")

    # ──────────────────────────────────────────────
    # Recommendations Engine
    # ──────────────────────────────────────────────

    def _generate_recommendations(
        self,
        block: PlatformTrendsBlock,
        niche: str,
        platform: str,
        goal: str,
        language: Optional[str] = None,
    ) -> List[ContentRecommendation]:
        """Generates actionable content recommendations from discovered domain, global, and location trends in creator's native language."""
        from app.services.language_service import language_service

        # Resolve language code ('hi', 'es', 'en')
        text_samples = [t.title for t in block.domain_trends]
        if block.creator_profile and block.creator_profile.recent_content:
            text_samples.extend([str(c.get("title") or c.get("text") or c.get("caption") or "") for c in block.creator_profile.recent_content])
        
        creator_name = block.creator_profile.display_name if block.creator_profile else ""
        lang_code = language_service.detect_language(creator_name, text_samples, requested_language=language)
        lang_pack = language_service.get_language_pack(lang_code)
        native_hooks = lang_pack.get("hooks", [])

        recs: List[ContentRecommendation] = []

        # 1. Domain Trends Recommendations (Focus: Creator's work / causes / domain)
        content_types = {
            "youtube": "video",
            "instagram": "reel",
            "linkedin": "post",
            "x_twitter": "thread",
        }
        content_type = content_types.get(platform, "post")

        for idx, trend in enumerate(block.domain_trends[:3]):
            if lang_code == "hi":
                hook_options = [
                    f"क्या आपने कभी सोचा है कि '{trend.title}' के पीछे की असली सच्चाई क्या है?",
                    f"सच तो यह है कि '{trend.title}' के बारे में 99% लोग गलत सोचते हैं...",
                    f"'{trend.title}' का पूरा सच: डेटा और आधिकारिक सबूतों के साथ विश्लेषण।"
                ]
                hook = hook_options[idx % len(hook_options)]
            elif lang_code == "es":
                hook_options = [
                    f"¿Alguna vez te has preguntado cuál es la verdadera razón detrás de '{trend.title}'?",
                    f"La verdad oculta sobre '{trend.title}' que nadie se atreve a decir en voz alta.",
                    f"El 99% de las personas están equivocadas sobre '{trend.title}'..."
                ]
                hook = hook_options[idx % len(hook_options)]
            else:
                hook_options = [
                    f"The hidden truth about '{trend.title}' that nobody in {niche} is talking about.",
                    f"What if everything you've been told about '{trend.title}' is completely backwards?",
                    f"Here is the single data point that changed my entire perspective on '{trend.title}'."
                ]
                hook = hook_options[idx % len(hook_options)]

            # Platform-tailored rationale
            if platform == "youtube":
                why_now = "High-intent searchable domain trend — optimized to convert viewers into new subscribers"
            elif platform == "instagram":
                why_now = "High-velocity domain issue — visual hook engineered to maximize explore views & profile followers"
            elif platform == "linkedin":
                why_now = "Authoritative domain insight — structured to drive reach, comments, and high-value professional connections"
            elif platform == "x_twitter":
                why_now = "Urgent domain development — crafted as a bookmark-optimized thread to spread domain awareness"
            else:
                why_now = trend.why_trending or "High-relevance trending topic in creator's domain"

            recs.append(ContentRecommendation(
                platform=platform,
                content_type=content_type,
                topic=trend.title,
                hook=hook,
                why_now=why_now,
                hashtags=trend.hashtags or block.hashtag_trends[:5],
                best_posting_time=self._best_time_for_platform(platform),
            ))

        # 2. Global Trends Recommendation (Cross-niche bridge to capture massive search volume)
        for trend in block.global_trends[:1]:
            if lang_code == "hi":
                global_hook = f"पूरी दुनिया में '{trend.title}' की चर्चा है — लेकिन हमारे {niche} पर इसका क्या असर होगा? आइए सच जानते हैं।"
            elif lang_code == "es":
                global_hook = f"Todo el mundo está hablando de '{trend.title}'. Esto es lo que realmente significa para {niche}."
            else:
                global_hook = f"Everyone is talking about '{trend.title}'. Here's the critical breakdown for {niche}."

            recs.append(ContentRecommendation(
                platform=platform,
                content_type="hot_take" if platform in ["youtube", "instagram"] else "analysis",
                topic=f"{trend.title} × {niche}",
                hook=global_hook,
                why_now="Global viral phenomenon — ride mainstream momentum to expand reach beyond core follower base",
                hashtags=block.hashtag_trends[:5],
                best_posting_time=self._best_time_for_platform(platform),
            ))

        # 3. Location Trends Recommendation (Specifically for YouTube & Instagram)
        if platform in ["youtube", "instagram"] and block.location_trends:
            for trend in block.location_trends[:1]:
                if lang_code == "hi":
                    loc_hook = f"ग्राउंड रियलिटी: '{trend.title}' को लेकर जमीनी स्तर पर क्या हालात हैं? देखिए यह खास रिपोर्ट।"
                elif lang_code == "es":
                    loc_hook = f"La realidad local sobre '{trend.title}'. Un análisis urgente sobre el terreno."
                else:
                    loc_hook = f"The ground reality behind '{trend.title}' that mainstream local coverage is missing."

                recs.append(ContentRecommendation(
                    platform=platform,
                    content_type="video" if platform == "youtube" else "reel",
                    topic=trend.title,
                    hook=loc_hook,
                    why_now="Regional trending velocity — triggers location-based algorithmic feed distribution for rapid views and subs",
                    hashtags=block.hashtag_trends[:5],
                    best_posting_time=self._best_time_for_platform(platform),
                ))

        # 4. Trending Keyword Recommendation (Leveraging high-velocity domain search terms)
        from app.services.trends_service import trends_service
        trending_kws = trends_service.extract_trending_keywords(niche, limit=5)
        if trending_kws:
            primary_kw = trending_kws[0]
            if lang_code == "hi":
                kw_hook = f"क्या आपको पता है कि '{primary_kw}' का नया बदलाव {niche} में सब कुछ बदलने वाला है?"
            elif lang_code == "es":
                kw_hook = f"El giro inesperado con '{primary_kw}' que transformará {niche} este año."
            else:
                kw_hook = f"Why the sudden surge around '{primary_kw}' changes everything for {niche} in 2026..."

            recs.append(ContentRecommendation(
                platform=platform,
                content_type=content_type,
                topic=f"Trending Keyword Deep Dive: {primary_kw}",
                hook=kw_hook,
                why_now=f"High-velocity domain trending keyword in {niche} — optimal search and retention catalyst",
                hashtags=[f"#{primary_kw.replace(' ', '')}"] + (block.hashtag_trends[:4] if block.hashtag_trends else []),
                best_posting_time=self._best_time_for_platform(platform),
            ))

        return recs

    def _best_time_for_platform(self, platform: str) -> str:
        times = {
            "youtube": "2:00 PM - 4:00 PM (local timezone)",
            "instagram": "6:00 AM or 7:00 PM",
            "linkedin": "7:30 AM - 8:30 AM",
            "x_twitter": "8:00 AM - 10:00 AM",
        }
        return times.get(platform, "9:00 AM")

    # ──────────────────────────────────────────────
    # Platform.md Generator
    # ──────────────────────────────────────────────

    def _generate_all_platform_md(
        self,
        creator_name: str,
        niche: str,
        location: str,
        blocks: List[PlatformTrendsBlock],
        recommendations: List[ContentRecommendation],
    ) -> Dict[str, str]:
        """Generates a platform.md file for each analyzed platform."""
        creator_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", creator_name.lower().strip())
        creator_dir = settings.CREATORS_DIR / creator_slug
        creator_dir.mkdir(parents=True, exist_ok=True)

        md_files: Dict[str, str] = {}

        for block in blocks:
            md_content = self._render_platform_md(
                creator_name=creator_name,
                niche=niche,
                location=location,
                block=block,
                recommendations=[r for r in recommendations if r.platform == block.platform],
            )
            filename = f"platform_{block.platform}.md"
            filepath = creator_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)
            md_files[block.platform] = str(filepath)
            logger.info(f"[Intel] Generated {filepath}")

        return md_files

    def _render_platform_md(
        self,
        creator_name: str,
        niche: str,
        location: str,
        block: PlatformTrendsBlock,
        recommendations: List[ContentRecommendation],
    ) -> str:
        """Renders a single platform.md markdown document."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        platform_display = {
            "youtube": "YouTube",
            "instagram": "Instagram",
            "linkedin": "LinkedIn",
            "x_twitter": "X (Twitter)",
        }.get(block.platform, block.platform.title())

        goal_display = {
            "increase_reach": "📈 Increase Reach",
            "increase_followers": "👥 Increase Followers",
            "increase_subscribers": "👥 Increase Subscribers",
            "more_views_and_followers": "🚀 More Views & Followers",
            "increase_connections": "🤝 Increase Connections",
            "spread_domain_posts": "🌐 Spread Domain Posts",
            "increase_engagement": "💬 Increase Engagement",
            "brand_authority": "👑 Build Brand Authority",
        }.get(block.goal or "", block.goal or "General Growth")

        lines = [
            f"# {platform_display} Intelligence & Strategy Report: {creator_name}",
            f"> **Domain / Niche**: `{niche}` | **Location**: `{location}` | **Primary Goal**: **{goal_display}**",
            f"> **Engine**: Creator AI Intelligence Suite | **Audited At**: {now}",
            "",
            "---",
            "",
        ]

        # 1. Creator Profile Audit Section
        profile = block.creator_profile
        lines.append(f"## 👤 Creator Footprint & Profile Audit")
        if profile:
            lines.append(f"- **Official Handle**: [{profile.handle}]({profile.profile_url})")
            if profile.follower_or_sub_count:
                lines.append(f"- **Audience Size**: **{profile.follower_or_sub_count}**")
            if profile.total_posts_or_videos:
                lines.append(f"- **Published Volume**: {profile.total_posts_or_videos}")
            if profile.bio:
                clean_bio = profile.bio.replace("\n", " ").strip()[:200]
                lines.append(f"- **Profile Positioning / Bio**: _{clean_bio}_")
            lines.append("")

            if profile.recent_content:
                lines.append(f"### 🎬 Recent Content & Hooks Analyzed")
                for idx, c in enumerate(profile.recent_content[:4], 1):
                    title = c.get("title") or c.get("text") or c.get("caption") or "Recent Post"
                    url = c.get("url")
                    views = c.get("views") or (f"{c.get('likes')} likes, {c.get('comments')} comments" if c.get('likes') else "")
                    hook = c.get("hook")

                    url_str = f" — [View Original]({url})" if url else ""
                    views_str = f" ({views})" if views else ""
                    lines.append(f"{idx}. **{title[:90]}**{views_str}{url_str}")
                    if hook:
                        lines.append(f"   - _Spoken Hook Opening_: \"{hook}\"")
                lines.append("")

            if profile.growth_gap_analysis:
                lines.append("### 📊 Performance Diagnostic & Growth Gap")
                lines.append(f"> ⚡ **Diagnostic**: {profile.growth_gap_analysis}")
                lines.append("")
        else:
            lines.append(f"- **Handle**: @{creator_name.lower()}")
            lines.append(f"- **Status**: Profile initialized for cross-platform expansion.")
            lines.append("")

        lines.append("---")
        lines.append("")

        # 2. Domain/Niche Trends
        lines.append(f"## 🔥 High-Velocity {niche} Trends on {platform_display}")
        lines.append("")
        if block.domain_trends:
            for t in block.domain_trends:
                url_part = f" — [Watch / View Content]({t.url})" if t.url else ""
                views_part = f" | `{t.views_or_engagement}`" if t.views_or_engagement else ""
                creator_part = f" by **{t.creator_handle}**" if t.creator_handle else ""
                lines.append(f"{t.rank}. **{t.title}**{creator_part}{views_part}{url_part}")
                if t.why_trending:
                    lines.append(f"   - _Why Trending_: {t.why_trending}")
                if t.suggested_angle:
                    lines.append(f"   - _Suggested Creator Angle_: {t.suggested_angle}")
                lines.append("")
        else:
            lines.append("_No domain-specific trends discovered. Expand query scope or check network._")
            lines.append("")

        # 3. Location Trends
        if block.location_trends:
            lines.append(f"## 📍 Location Trends ({location})")
            lines.append("")
            for t in block.location_trends:
                url_part = f" — [Link]({t.url})" if t.url else ""
                lines.append(f"{t.rank}. **{t.title}**{url_part}")
                lines.append("")

        # 4. Global Trends
        lines.append("## 🌍 Global Trend Signals (Cross-Platform Momentum)")
        lines.append("")
        if block.global_trends:
            for t in block.global_trends:
                lines.append(f"{t.rank}. **{t.title}** — {t.views_or_engagement or 'Trending'}")
                if t.suggested_angle:
                    lines.append(f"   - _Crossover Opportunity_: {t.suggested_angle}")
                lines.append("")
        else:
            lines.append("_No global trends captured._")
            lines.append("")

        # 5. Trending Hashtags
        if block.hashtag_trends:
            lines.append(f"## # High-Converting Hashtags for {platform_display}")
            lines.append("")
            lines.append("`" + " ".join(block.hashtag_trends) + "`")
            lines.append("")

        # 6. Content Strategy
        if block.content_strategy:
            lines.append(f"## 🎯 Actionable Platform Strategy ({goal_display})")
            lines.append("")
            lines.append(block.content_strategy)
            lines.append("")

        # 7. AI Recommendations
        if recommendations:
            lines.append("## 💡 Ready-to-Post Content Blueprints (Next 5 Pieces)")
            lines.append("")
            for idx, rec in enumerate(recommendations, 1):
                lines.append(f"### Blueprint {idx}: {rec.topic}")
                lines.append(f"- **Format**: `{rec.content_type.upper()}`")
                lines.append(f"- **Hook / Opening Line**: _{rec.hook}_")
                lines.append(f"- **Why Now (Trend Driver)**: {rec.why_now}")
                if rec.best_posting_time:
                    lines.append(f"- **Optimal Posting Window**: {rec.best_posting_time}")
                if rec.hashtags:
                    lines.append(f"- **Tags**: {' '.join(rec.hashtags[:6])}")
                lines.append("")

        lines.append("---")
        lines.append(f"_Authored by Creator AI Studio • All rights reserved • Generated for **{creator_name}**_")

        return "\n".join(lines)

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────

    def _generate_summary(
        self,
        creator_name: str,
        niche: str,
        blocks: List[PlatformTrendsBlock],
    ) -> str:
        total_trends = sum(
            len(b.domain_trends) + len(b.global_trends) + len(b.location_trends)
            for b in blocks
        )
        platforms_str = ", ".join(
            {"youtube": "YouTube", "instagram": "Instagram", "linkedin": "LinkedIn", "x_twitter": "X"}.get(b.platform, b.platform)
            for b in blocks
        )
        return (
            f"Successfully audited creator footprint and extracted {total_trends} trending items across {len(blocks)} platforms "
            f"({platforms_str}) for {creator_name} in '{niche}'. "
            f"Tailored platform.md reports with growth diagnostics, real trend links, and content blueprints have been generated."
        )


platform_intel_service = PlatformIntelService()
