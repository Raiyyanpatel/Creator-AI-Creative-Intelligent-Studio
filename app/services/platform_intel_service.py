"""
Platform Intelligence Service
================================
Master orchestrator that scrapes cross-platform trends (YouTube, Instagram,
LinkedIn, X/Twitter), generates per-platform strategy reports (platform.md),
and produces AI-powered content recommendations.

Architecture:
  IntelligenceRequest → [YT Scraper, IG Scraper, LI Scraper, X Scraper]
                       → Trend Aggregation
                       → platform.md Generation
                       → IntelligenceResponse
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
        recommendations: List[ContentRecommendation] = []
        md_files: Dict[str, str] = {}

        goals = req.goals or {}
        handles = req.platform_handles or {}

        for platform in req.platforms:
            pname = platform.value
            goal = goals.get(pname, DEFAULT_GOALS.get(pname, "increase_reach"))
            # Ensure goal is a plain string, not an enum
            if hasattr(goal, "value"):
                goal = goal.value
            handle = handles.get(pname, req.creator_name)

            logger.info(f"[Intel] Scanning {pname} for creator={req.creator_name}, niche={req.niche}, location={req.location}")

            if platform == PlatformChoice.YOUTUBE:
                block = self._scan_youtube(req.niche, req.location, handle, goal)
            elif platform == PlatformChoice.INSTAGRAM:
                block = self._scan_instagram(req.niche, req.location, handle, goal)
            elif platform == PlatformChoice.LINKEDIN:
                block = self._scan_linkedin(req.niche, req.location, handle, goal)
            elif platform == PlatformChoice.X_TWITTER:
                block = self._scan_x_twitter(req.niche, req.location, handle, goal)
            else:
                continue

            platform_blocks.append(block)

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
            # Attach file paths to blocks
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
            platform_trends=platform_blocks,
            top_recommendations=recommendations[:10],
            platform_md_files=md_files,
            summary=summary,
        )

    # ──────────────────────────────────────────────
    # YouTube Scanner
    # ──────────────────────────────────────────────

    def _scan_youtube(self, niche: str, location: str, handle: str, goal: str) -> PlatformTrendsBlock:
        domain_trends = self._youtube_search_trending(niche, location, limit=8)
        global_trends = self._youtube_trending_feed(location, limit=6)
        location_trends = self._youtube_search_trending(f"{niche} {location}", location, limit=5)

        hashtags = self._youtube_trending_hashtags(niche)

        strategy = self._youtube_strategy(niche, goal)

        return PlatformTrendsBlock(
            platform="youtube",
            goal=goal,
            domain_trends=domain_trends,
            location_trends=location_trends,
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy=strategy,
        )

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
    # Instagram Scanner
    # ──────────────────────────────────────────────

    def _scan_instagram(self, niche: str, location: str, handle: str, goal: str) -> PlatformTrendsBlock:
        # Hashtag trends
        hashtag_data = instagram_service.fetch_trending_hashtags_for_niche(niche, location)
        hashtags = [h["tag"] for h in hashtag_data]

        # Trending reels
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

        # Google Trends as global signal for Instagram content
        global_trends = self._google_trends_rss(location, limit=5, platform_label="instagram")

        # Strategy
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
            domain_trends=domain_trends,
            location_trends=[],
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy="\n".join(strategy_lines),
        )

    # ──────────────────────────────────────────────
    # LinkedIn Scanner
    # ──────────────────────────────────────────────

    def _scan_linkedin(self, niche: str, location: str, handle: str, goal: str) -> PlatformTrendsBlock:
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
            domain_trends=domain_trends,
            location_trends=[],
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy=strategy,
        )

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
    # X (Twitter) Scanner
    # ──────────────────────────────────────────────

    def _scan_x_twitter(self, niche: str, location: str, handle: str, goal: str) -> PlatformTrendsBlock:
        domain_trends = self._x_niche_trends(niche, location)
        global_trends = self._google_trends_rss(location, limit=5, platform_label="x_twitter")

        # Attempt scraping trending topics from X/Twitter
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
            domain_trends=domain_trends,
            location_trends=[],
            global_trends=global_trends,
            hashtag_trends=hashtags,
            content_strategy=strategy,
        )

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
            f"# {platform_display} Intelligence Report: {creator_name}",
            f"> **Niche**: {niche} | **Location**: {location} | **Goal**: {goal_display}",
            f"> Generated by Creator AI Engine — {now}",
            "",
            "---",
            "",
        ]

        # Domain/Niche Trends
        lines.append(f"## 🔥 {niche} Trending on {platform_display}")
        lines.append("")
        if block.domain_trends:
            for t in block.domain_trends:
                url_part = f" — [Link]({t.url})" if t.url else ""
                views_part = f" | {t.views_or_engagement}" if t.views_or_engagement else ""
                creator_part = f" by **{t.creator_handle}**" if t.creator_handle else ""
                lines.append(f"{t.rank}. **{t.title}**{creator_part}{views_part}{url_part}")
                if t.why_trending:
                    lines.append(f"   - _Why Trending_: {t.why_trending}")
                if t.suggested_angle:
                    lines.append(f"   - _Suggested Angle_: {t.suggested_angle}")
                lines.append("")
        else:
            lines.append("_No domain-specific trends discovered. Try broadening the niche or check API keys._")
            lines.append("")

        # Location Trends
        if block.location_trends:
            lines.append(f"## 📍 Location Trends ({location})")
            lines.append("")
            for t in block.location_trends:
                url_part = f" — [Link]({t.url})" if t.url else ""
                lines.append(f"{t.rank}. **{t.title}**{url_part}")
                lines.append("")

        # Global Trends
        lines.append("## 🌍 Global Trends (Cross-Platform Signal)")
        lines.append("")
        if block.global_trends:
            for t in block.global_trends:
                lines.append(f"{t.rank}. **{t.title}** — {t.views_or_engagement or 'Trending'}")
                if t.suggested_angle:
                    lines.append(f"   - _Angle_: {t.suggested_angle}")
                lines.append("")
        else:
            lines.append("_No global trends captured._")
            lines.append("")

        # Trending Hashtags
        if block.hashtag_trends:
            lines.append(f"## # Trending Hashtags for {platform_display}")
            lines.append("")
            lines.append(" ".join(block.hashtag_trends))
            lines.append("")

        # Content Strategy
        if block.content_strategy:
            lines.append("## 🎯 Content Strategy")
            lines.append("")
            lines.append(block.content_strategy)
            lines.append("")

        # AI Recommendations
        if recommendations:
            lines.append("## 💡 AI-Powered Content Recommendations")
            lines.append("")
            for idx, rec in enumerate(recommendations, 1):
                lines.append(f"### Recommendation {idx}: {rec.topic}")
                lines.append(f"- **Content Type**: {rec.content_type}")
                lines.append(f"- **Hook**: _{rec.hook}_")
                lines.append(f"- **Why Now**: {rec.why_now}")
                if rec.best_posting_time:
                    lines.append(f"- **Best Posting Time**: {rec.best_posting_time}")
                if rec.hashtags:
                    lines.append(f"- **Hashtags**: {' '.join(rec.hashtags[:6])}")
                lines.append("")

        lines.append("---")
        lines.append(f"_Report generated by Creator AI Engine for **{creator_name}** on {now}_")

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
            f"Analyzed {total_trends} trending items across {len(blocks)} platforms "
            f"({platforms_str}) for {creator_name} in the '{niche}' niche. "
            f"Platform-specific strategy reports and content recommendations have been generated. "
            f"Check the platform.md files for detailed trend links and action plans."
        )


platform_intel_service = PlatformIntelService()
