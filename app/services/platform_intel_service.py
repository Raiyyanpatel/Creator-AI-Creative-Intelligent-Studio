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

logger = logging.getLogger(__name__)

# Default platform goals when user doesn't specify
DEFAULT_GOALS = {
    "instagram": "increase_reach",
    "youtube": "increase_followers",
    "linkedin": "increase_connections",
    "x_twitter": "increase_engagement",
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
        """Main entry: runs all platform scrapers, generates reports, returns response."""
        now = datetime.now(timezone.utc).isoformat()

        platform_blocks: List[PlatformTrendsBlock] = []
        creator_profiles_dict: Dict[str, CreatorPlatformProfile] = {}
        recommendations: List[ContentRecommendation] = []
        md_files: Dict[str, str] = {}

        goals = req.goals or {}
        handles = req.platform_handles or {}

        for platform in req.platforms:
            pname = platform.value
            raw_goal = goals.get(pname, DEFAULT_GOALS.get(pname, "increase_reach"))
            goal = raw_goal.value if hasattr(raw_goal, "value") else str(raw_goal)
            handle = handles.get(pname, req.creator_name)

            logger.info(f"[Intel] Extracting {pname} for creator={req.creator_name}, handle={handle}, niche={req.niche}")

            if platform == PlatformChoice.YOUTUBE:
                block = self._scan_youtube(req.creator_name, req.niche, req.location, handle, goal)
            elif platform == PlatformChoice.INSTAGRAM:
                block = self._scan_instagram(req.creator_name, req.niche, req.location, handle, goal)
            elif platform == PlatformChoice.LINKEDIN:
                block = self._scan_linkedin(req.creator_name, req.niche, req.location, handle, goal)
            elif platform == PlatformChoice.X_TWITTER:
                block = self._scan_x_twitter(req.creator_name, req.niche, req.location, handle, goal)
            else:
                continue

            platform_blocks.append(block)
            if block.creator_profile:
                creator_profiles_dict[pname] = block.creator_profile

            # Generate content recommendations for this platform
            recs = self._generate_recommendations(block, req.niche, pname, goal)
            recommendations.extend(recs)

        # Generate platform.md files if requested
        if req.generate_platform_md:
            md_files = self._generate_all_platform_md(
                creator_name=req.creator_name,
                niche=req.niche,
                location=req.location,
                blocks=platform_blocks,
                recommendations=recommendations,
            )
            for block in platform_blocks:
                if block.platform in md_files:
                    block.platform_md_path = md_files[block.platform]

        summary = self._generate_summary(req.creator_name, req.niche, platform_blocks)

        return IntelligenceResponse(
            creator_name=req.creator_name,
            niche=req.niche,
            location=req.location,
            analyzed_at=now,
            platforms_analyzed=[p.value for p in req.platforms],
            creator_profiles=creator_profiles_dict,
            platform_trends=platform_blocks,
            top_recommendations=recommendations[:10],
            platform_md_files=md_files,
            summary=summary,
        )

    # ──────────────────────────────────────────────
    # YouTube Scanner & Creator Extractor
    # ──────────────────────────────────────────────

    def _scan_youtube(
        self, creator_name: str, niche: str, location: str, handle: str, goal: str
    ) -> PlatformTrendsBlock:
        # 1. Extract creator-specific profile info
        creator_profile = self._extract_youtube_creator_profile(creator_name, handle, niche)

        # 2. Discover trending videos in niche, global, and location
        domain_trends = self._youtube_search_trending(niche, location, limit=8)
        global_trends = self._youtube_trending_feed(location, limit=6)
        location_trends = self._youtube_search_trending(f"{niche} {location}", location, limit=5)

        hashtags = self._youtube_trending_hashtags(niche)
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

        api_key = settings.YOUTUBE_API_KEY
        if api_key:
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

    def _youtube_search_trending(self, query: str, location: str, limit: int = 8) -> List[TrendItem]:
        """Uses YouTube Data API v3 to search for trending videos in a niche."""
        api_key = settings.YOUTUBE_API_KEY
        items: List[TrendItem] = []
        if not api_key:
            return items

        try:
            region = location[:2].upper() if location else "US"
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": self._recent_date_iso(),
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
            logger.error(f"YouTube trending search failed: {e}")
        return items

    def _youtube_trending_feed(self, location: str, limit: int = 6) -> List[TrendItem]:
        """Fetches YouTube's official trending feed via API."""
        api_key = settings.YOUTUBE_API_KEY
        items: List[TrendItem] = []
        if not api_key:
            return items
        try:
            region = location[:2].upper() if location else "US"
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
            logger.error(f"YouTube trending feed failed: {e}")
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
            f"**YouTube Strategy for '{niche}' (Goal: {goal})**\n"
            f"• Post 2-3 Shorts/week + 1 long-form/week for maximum algorithmic surface area\n"
            f"• First 30 seconds are critical — use pattern-interrupt hooks\n"
            f"• Optimize titles for search: include primary keyword + emotional trigger\n"
            f"• Use end screens & pinned comments to drive subscriptions\n"
            f"• Engage with comments in first 60 minutes (boosts recommendations)\n"
            f"• Thumbnail: high-contrast, 3-word max, expressive face close-up"
        )

    # ──────────────────────────────────────────────
    # Instagram Scanner & Creator Extractor
    # ──────────────────────────────────────────────

    def _scan_instagram(
        self, creator_name: str, niche: str, location: str, handle: str, goal: str
    ) -> PlatformTrendsBlock:
        # 1. Extract creator-specific profile info
        creator_profile = self._extract_instagram_creator_profile(creator_name, handle, niche)

        # 2. Discover trending hashtags and reels
        hashtag_data = instagram_service.fetch_trending_hashtags_for_niche(niche, location)
        hashtags = [h["tag"] for h in hashtag_data]

        reels_data = instagram_service.fetch_trending_reels_for_niche(niche, location)
        domain_trends = []
        for idx, reel in enumerate(reels_data, 1):
            domain_trends.append(TrendItem(
                rank=idx,
                title=reel.get("title", f"Trending {niche} Reel"),
                url=reel.get("url"),
                platform="instagram",
                content_type="reel",
                why_trending=f"Discovered via {reel.get('source', 'Instagram Explore')}",
                relevance_to_niche=f"Directly relevant to {niche}",
                hashtags=[h["tag"] for h in hashtag_data[:5]],
            ))

        global_trends = self._google_trends_rss(location, limit=5, platform_label="instagram")

        strategy_data = instagram_service.get_reel_strategy(niche, goal)
        strategy_lines = [
            f"**Instagram Strategy for '{niche}' (Goal: {goal})**",
            f"• Optimal Reel Length: {strategy_data.get('optimal_length', '7-15s')}",
            f"• Best Posting Times: {', '.join(strategy_data.get('best_posting_times', []))}",
            f"• Caption Strategy: {strategy_data.get('caption_strategy', '')}",
            f"• Audio Strategy: {strategy_data.get('audio_strategy', '')}",
        ]
        for tactic in strategy_data.get("engagement_tactics", [])[:4]:
            strategy_lines.append(f"• {tactic}")

        return PlatformTrendsBlock(
            platform="instagram",
            goal=goal,
            creator_profile=creator_profile,
            domain_trends=domain_trends,
            location_trends=[],
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
        self, creator_name: str, niche: str, location: str, handle: str, goal: str
    ) -> PlatformTrendsBlock:
        creator_profile = self._extract_linkedin_creator_profile(creator_name, handle, niche)
        domain_trends = self._linkedin_trending_articles(niche, location)
        global_trends = self._google_trends_rss(location, limit=5, platform_label="linkedin")
        hashtags = self._linkedin_trending_hashtags(niche)

        strategy = (
            f"**LinkedIn Strategy for '{niche}' (Goal: {goal})**\n"
            f"• Post 3-5x/week — LinkedIn's algorithm strongly favors consistent posters\n"
            f"• Ideal post format: Short hook line → whitespace → 3-5 insight bullets → CTA question\n"
            f"• Document/carousel posts get 3x more reach than text-only\n"
            f"• Comment on 10-15 posts in your niche daily (drive profile views → follows)\n"
            f"• Best posting times: 7:30-8:30 AM or 5:00-6:00 PM (local timezone)\n"
            f"• Use 3-5 hashtags max (LinkedIn penalizes hashtag stuffing)\n"
            f"• Video posts get 5x engagement — especially under 90 seconds\n"
            f"• Newsletter feature: launch a LinkedIn Newsletter for subscriber lock-in"
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
        self, creator_name: str, niche: str, location: str, handle: str, goal: str
    ) -> PlatformTrendsBlock:
        creator_profile = self._extract_x_creator_profile(creator_name, handle, niche)
        domain_trends = self._x_niche_trends(niche, location)
        global_trends = self._google_trends_rss(location, limit=5, platform_label="x_twitter")
        hashtags = self._x_trending_hashtags(niche)

        strategy = (
            f"**X (Twitter) Strategy for '{niche}' (Goal: {goal})**\n"
            f"• Tweet 3-5x/day — X rewards high-frequency, high-engagement accounts\n"
            f"• Thread format: Hook tweet → 4-7 value tweets → CTA (retweet/bookmark)\n"
            f"• Optimal engagement times: 8-10 AM, 12-1 PM, 5-6 PM (target timezone)\n"
            f"• Use quote tweets to join trending conversations in your niche\n"
            f"• Image/video tweets get 2.5x more engagement than text-only\n"
            f"• Long-form posts (X Premium): use for deep-dive thought pieces\n"
            f"• Engage with top 20 accounts in your niche daily (comment, not just like)\n"
            f"• Spaces: host weekly 30-min Spaces for community + authority building"
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
        """Extracts X/Twitter handle, recent tweets, and viral threads."""
        clean_handle = handle.replace("@", "").strip() if handle else re.sub(r'[^a-zA-Z0-9_]', '', creator_name.lower())
        if "x.com/" in clean_handle or "twitter.com/" in clean_handle:
            clean_handle = clean_handle.split("/")[-1].replace("@", "")

        profile = CreatorPlatformProfile(
            platform="x_twitter",
            handle=f"@{clean_handle}",
            profile_url=f"https://x.com/{clean_handle}",
            display_name=creator_name,
        )

        # Attempt syndication timeline fetch
        try:
            syn_url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{clean_handle}"
            with httpx.Client(timeout=5.0) as client:
                r = client.get(syn_url, headers=HEADERS)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")
                    for art in soup.find_all("article")[:4]:
                        txt = art.get_text(" ", strip=True)
                        if txt:
                            profile.recent_content.append({
                                "text": txt[:250],
                                "url": f"https://x.com/{clean_handle}",
                                "content_type": "tweet"
                            })
        except Exception:
            pass

        # Fallback to Google News RSS
        if not profile.recent_content:
            try:
                q = f"{creator_name or clean_handle} tweet OR thread"
                feed_url = f"https://news.google.com/rss/search?q={q.replace(' ', '+')}&hl=en"
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:4]:
                    profile.recent_content.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "published_at": entry.get("published", ""),
                        "content_type": "tweet_mention"
                    })
            except Exception as e:
                logger.debug(f"X profile extraction fallback error: {e}")

        profile.growth_gap_analysis = (
            f"X footprint (@{clean_handle}): High opportunity in '{niche}' by publishing 1 signature thread weekly "
            f"optimized for bookmark saves (which algorithmically boosts account authority 5x over retweets), "
            f"supported by daily observational commentary."
        )
        return profile

    def _x_niche_trends(self, niche: str, location: str) -> List[TrendItem]:
        """Discovers X/Twitter trending content via Google News RSS for the niche."""
        items: List[TrendItem] = []
        try:
            query = f"{niche} viral twitter thread {location}"
            search_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en"
            feed = feedparser.parse(search_url)
            for rank, entry in enumerate(feed.entries[:6], 1):
                items.append(TrendItem(
                    rank=rank,
                    title=entry.get("title", ""),
                    url=entry.get("link", ""),
                    platform="x_twitter",
                    content_type="thread",
                    published_date=entry.get("published", ""),
                    creator_handle=entry.get("source", {}).get("title", ""),
                    why_trending="Trending in Google News for X/Twitter",
                    relevance_to_niche=f"Relevant to {niche}",
                ))
        except Exception as e:
            logger.debug(f"X trending scrape failed: {e}")
        return items

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
    ) -> List[ContentRecommendation]:
        """Generates actionable content recommendations from discovered trends."""
        recs: List[ContentRecommendation] = []

        # Pick top domain trends
        for trend in block.domain_trends[:3]:
            content_types = {
                "youtube": "video",
                "instagram": "reel",
                "linkedin": "post",
                "x_twitter": "thread",
            }
            recs.append(ContentRecommendation(
                platform=platform,
                content_type=content_types.get(platform, "post"),
                topic=trend.title,
                hook=f"The hidden truth about '{trend.title}' that nobody in {niche} is talking about.",
                why_now=trend.why_trending or "Currently trending in your niche",
                hashtags=trend.hashtags or block.hashtag_trends[:5],
                best_posting_time=self._best_time_for_platform(platform),
            ))

        # Pick top global trend and create a niche crossover
        for trend in block.global_trends[:1]:
            recs.append(ContentRecommendation(
                platform=platform,
                content_type="hot_take",
                topic=f"{trend.title} × {niche}",
                hook=f"Everyone is talking about '{trend.title}'. Here's what it means for {niche}.",
                why_now="Global trending topic — high search volume right now",
                hashtags=block.hashtag_trends[:5],
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
            "increase_connections": "🤝 Increase Connections",
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
