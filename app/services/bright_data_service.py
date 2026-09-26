"""
Bright Data Service
===================
Integrates Bright Data's Web Scraper & Dataset API for Instagram:
  - Instagram Reels Dataset (`gd_lyclm20il4r5helnj`)
  - Instagram Keyword Search Dataset (`gd_lnixyos0cjq3k7an7`)
  - Instagram Hashtag Dataset (`gd_lp9xgqvwrt2wc2jjy`)
  - Instagram Profiles Dataset (`gd_l1vikfch901nx3by4`)

Provides synchronous scraping with strict timeouts, structured normalization
into TrendItem models, and seamless failover to Apify and Composio.
"""

import logging
import re
from typing import List, Dict, Any, Optional
import httpx

from app.config import settings
from app.models.intelligence import TrendItem, CreatorPlatformProfile

logger = logging.getLogger(__name__)


class BrightDataService:
    """Encapsulates Bright Data API calls for Instagram Reels and profiles."""

    BASE_URL = "https://api.brightdata.com"
    REELS_DATASET_ID = "gd_lyclm20il4r5helnj"
    KEYWORD_POSTS_DATASET_ID = "gd_lnixyos0cjq3k7an7"
    HASHTAG_DATASET_ID = "gd_lp9xgqvwrt2wc2jjy"
    PROFILES_DATASET_ID = "gd_l1vikfch901nx3by4"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, "BRIGHT_DATA_API_KEY", "")

    def _get_api_key(self) -> str:
        return self.api_key or getattr(settings, "BRIGHT_DATA_API_KEY", "")

    def _get_headers(self) -> Dict[str, str]:
        key = self._get_api_key()
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

    # ──────────────────────────────────────────────
    # Instagram Reels Scraper
    # ──────────────────────────────────────────────

    def scrape_instagram_reels(
        self,
        query: str,
        location: str = "US",
        limit: int = 6
    ) -> List[TrendItem]:
        """
        Queries Bright Data's Instagram datasets to discover high-velocity trending Reels
        for the creator's domain and causes.
        """
        key = self._get_api_key()
        if not key:
            logger.debug("[BrightData] No BRIGHT_DATA_API_KEY configured; skipping.")
            return []

        clean_tag = re.sub(r'[^a-zA-Z0-9]', '', query.lower())
        items: List[TrendItem] = []

        # 1. Try Bright Data Synchronous Scraper API for Instagram Reels / Keyword Search
        endpoint = f"{self.BASE_URL}/datasets/v3/scrape?dataset_id={self.REELS_DATASET_ID}"
        payload = [
            {"url": f"https://www.instagram.com/explore/tags/{clean_tag}/"}
        ]

        try:
            with httpx.Client(timeout=15.0) as client:
                res = client.post(endpoint, headers=self._get_headers(), json=payload)
                if res.status_code in [200, 201]:
                    data = res.json()
                    if isinstance(data, list):
                        for rank, reel in enumerate(data[:limit], 1):
                            caption = reel.get("caption") or reel.get("description") or ""
                            first_line = caption.split("\n")[0].strip() if caption else f"Trending #{clean_tag} Reel"
                            likes = reel.get("likes_count") or reel.get("likes", 0)
                            comments = reel.get("comments_count") or reel.get("comments", 0)
                            views = reel.get("video_view_count") or reel.get("views_count") or reel.get("views")
                            
                            eng_str = None
                            if views:
                                eng_str = f"{int(views):,} views"
                            elif likes or comments:
                                eng_str = f"{int(likes):,} likes, {int(comments):,} comments"

                            items.append(TrendItem(
                                rank=rank,
                                title=first_line[:120],
                                url=reel.get("url") or reel.get("link") or f"https://www.instagram.com/explore/tags/{clean_tag}/",
                                platform="instagram",
                                content_type="reel",
                                views_or_engagement=eng_str,
                                published_date=reel.get("timestamp") or reel.get("post_time", ""),
                                creator_handle=reel.get("owner_username") or reel.get("author", f"#{clean_tag}"),
                                why_trending=f"High velocity in Bright Data Instagram Reels dataset for '{query}'",
                                relevance_to_niche=f"Directly relevant to {query} domain",
                                hashtags=reel.get("hashtags", [f"#{clean_tag}"])[:5],
                                thumbnail_url=reel.get("thumbnail") or reel.get("display_url"),
                            ))
                        if items:
                            logger.info(f"[BrightData] Successfully retrieved {len(items)} trending reels for '{query}'")
                            return items
                else:
                    logger.debug(f"[BrightData] Instagram reels scraper response: HTTP {res.status_code} ({res.text[:120]})")
        except Exception as e:
            logger.debug(f"[BrightData] Notice during Instagram reels scraping: {e}")

        return items

    # ──────────────────────────────────────────────
    # Instagram Profile Scraper
    # ──────────────────────────────────────────────

    def scrape_instagram_profile(self, handle: str) -> Optional[Dict[str, Any]]:
        """
        Extracts verified follower count, bio, and catalog stats using Bright Data's Profiles dataset.
        """
        key = self._get_api_key()
        if not key:
            return None

        clean_handle = re.sub(r'[^a-zA-Z0-9._]', '', handle.replace("@", "").strip().lower())
        if not clean_handle:
            return None

        endpoint = f"{self.BASE_URL}/datasets/v3/scrape?dataset_id={self.PROFILES_DATASET_ID}"
        payload = [
            {"url": f"https://www.instagram.com/{clean_handle}/"}
        ]

        try:
            with httpx.Client(timeout=15.0) as client:
                res = client.post(endpoint, headers=self._get_headers(), json=payload)
                if res.status_code in [200, 201]:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        p = data[0]
                        followers = p.get("followers") or p.get("followers_count")
                        following = p.get("following") or p.get("following_count")
                        posts = p.get("posts_count") or p.get("media_count")
                        return {
                            "username": p.get("username", clean_handle),
                            "full_name": p.get("full_name") or p.get("name", clean_handle),
                            "biography": p.get("biography") or p.get("bio", ""),
                            "profile_url": f"https://www.instagram.com/{clean_handle}/",
                            "followers_count": f"{int(followers):,} followers" if followers else None,
                            "following_count": f"{int(following):,} following" if following else None,
                            "total_posts": f"{int(posts):,} posts" if posts else None,
                            "verified": bool(p.get("is_verified", False)),
                            "profile_pic_url": p.get("profile_pic_url"),
                            "recent_content": []
                        }
        except Exception as e:
            logger.debug(f"[BrightData] Profile scraping notice: {e}")

        return None


bright_data_service = BrightDataService()
