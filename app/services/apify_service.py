"""
Apify Service
=============
Integrates Apify Actors to scrape verified profile information and trending posts
across Instagram and LinkedIn:
  - Instagram Profile Scraper: `apify~instagram-profile-scraper`
  - Instagram Posts/Reels Scraper: `apify~instagram-scraper`
  - LinkedIn Post Search: `harvestapi~linkedin-post-search`

All calls run synchronously against Apify's REST API with strict timeouts
and fallback protection.
"""

import re
import logging
from typing import List, Dict, Any, Optional
import httpx

from app.config import settings
from app.models.intelligence import TrendItem, CreatorPlatformProfile

logger = logging.getLogger(__name__)


class ApifyService:
    """Encapsulates Apify API actor executions for Instagram and LinkedIn."""

    BASE_URL = "https://api.apify.com/v2"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, "APIFY_API_KEY", "")

    def _get_api_key(self) -> str:
        return self.api_key or getattr(settings, "APIFY_API_KEY", "")

    # ──────────────────────────────────────────────
    # Instagram Scrapers
    # ──────────────────────────────────────────────

    def scrape_instagram_profile(self, handle: str) -> Optional[Dict[str, Any]]:
        """
        Scrapes authentic Instagram profile metrics and latest posts via apify~instagram-profile-scraper.
        Returns profile dictionary or None on failure.
        """
        key = self._get_api_key()
        if not key:
            logger.debug("[Apify] No APIFY_API_KEY configured; skipping Apify Instagram profile scraper.")
            return None

        clean_handle = re.sub(r'[^a-zA-Z0-9._]', '', handle.replace("@", "").strip().lower())
        if not clean_handle:
            return None

        actor_id = "apify~instagram-profile-scraper"
        url = f"{self.BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"

        try:
            with httpx.Client(timeout=25.0) as client:
                res = client.post(
                    url,
                    params={"token": key},
                    json={"usernames": [clean_handle]},
                )
                if res.status_code in [200, 201]:
                    items = res.json()
                    if isinstance(items, list) and len(items) > 0:
                        data = items[0]
                        # Verify we got real data
                        if data.get("error") or not data.get("username"):
                            logger.warning(f"[Apify] Instagram profile scraper returned error or empty for {clean_handle}")
                            return None

                        followers = data.get("followersCount")
                        following = data.get("followsCount")
                        posts_cnt = data.get("postsCount")

                        recent_content = []
                        for post in data.get("latestPosts", [])[:8]:
                            caption = post.get("caption", "") or ""
                            # Short title from first line of caption
                            first_line = caption.split("\n")[0].strip() if caption else ""
                            post_type = "reel" if (post.get("productType") == "clips" or post.get("type") == "Video") else "post"
                            
                            views_or_eng = None
                            if post.get("videoViewCount"):
                                views_or_eng = f"{int(post['videoViewCount']):,} views"
                            elif post.get("likesCount"):
                                views_or_eng = f"{int(post['likesCount']):,} likes"

                            recent_content.append({
                                "id": post.get("id"),
                                "title": first_line[:120] if first_line else "Instagram Post",
                                "caption": caption,
                                "url": post.get("url"),
                                "likes": post.get("likesCount"),
                                "comments": post.get("commentsCount"),
                                "views": post.get("videoViewCount"),
                                "engagement": views_or_eng,
                                "published_at": post.get("timestamp", ""),
                                "thumbnail": post.get("displayUrl"),
                                "content_type": post_type,
                                "source": "apify",
                            })

                        return {
                            "username": data.get("username"),
                            "full_name": data.get("fullName") or clean_handle,
                            "biography": data.get("biography", ""),
                            "profile_url": data.get("url") or f"https://www.instagram.com/{clean_handle}/",
                            "followers_count": f"{int(followers):,} followers" if followers is not None else None,
                            "following_count": f"{int(following):,} following" if following is not None else None,
                            "total_posts": f"{int(posts_cnt):,} posts" if posts_cnt is not None else None,
                            "verified": bool(data.get("verified", False)),
                            "profile_pic_url": data.get("profilePicUrlHD") or data.get("profilePicUrl"),
                            "recent_content": recent_content,
                        }
                else:
                    logger.warning(f"[Apify] Instagram profile scraper failed with HTTP {res.status_code}: {res.text[:200]}")
        except Exception as e:
            logger.warning(f"[Apify] Exception running Instagram profile scraper: {e}")

        return None

    def scrape_instagram_trends(self, query: str, location: str = "", limit: int = 5) -> List[TrendItem]:
        """
        Scrapes trending posts/reels for a domain topic via apify~instagram-scraper using hashtag exploration.
        """
        key = self._get_api_key()
        if not key:
            return []

        # Convert query to valid hashtag format
        tag = re.sub(r'[^a-zA-Z0-9]', '', query.lower())
        if not tag:
            tag = "viral"

        actor_id = "apify~instagram-scraper"
        url = f"{self.BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"

        payload = {
            "directUrls": [f"https://www.instagram.com/explore/tags/{tag}/"],
            "resultsType": "posts",
            "resultsLimit": limit,
        }

        items: List[TrendItem] = []
        try:
            with httpx.Client(timeout=25.0) as client:
                res = client.post(url, params={"token": key}, json=payload)
                if res.status_code in [200, 201]:
                    posts = res.json()
                    if isinstance(posts, list):
                        for rank, p in enumerate(posts[:limit], 1):
                            caption = p.get("caption") or ""
                            first_line = caption.split("\n")[0].strip() if caption else f"Trending #{tag} Instagram Post"
                            p_type = "reel" if (p.get("productType") == "clips" or p.get("type") == "Video") else "post"
                            
                            likes = p.get("likesCount", 0)
                            comments = p.get("commentsCount", 0)
                            eng_str = None
                            if likes or comments:
                                eng_str = f"{likes:,} likes, {comments:,} comments"

                            items.append(TrendItem(
                                rank=rank,
                                title=first_line[:120],
                                url=p.get("url") or f"https://www.instagram.com/explore/tags/{tag}/",
                                platform="instagram",
                                content_type=p_type,
                                views_or_engagement=eng_str,
                                published_date=p.get("timestamp", ""),
                                creator_handle=p.get("ownerUsername") or f"#{tag}",
                                why_trending=f"Top-ranking post under #{tag} explore feed",
                                relevance_to_niche=f"Directly tagged in {query} domain",
                                hashtags=p.get("hashtags", [])[:5],
                                thumbnail_url=p.get("displayUrl"),
                            ))
                else:
                    logger.warning(f"[Apify] Instagram posts scraper returned HTTP {res.status_code}")
        except Exception as e:
            logger.warning(f"[Apify] Exception running Instagram trend scraper: {e}")

        return items

    # ──────────────────────────────────────────────
    # LinkedIn Scraper
    # ──────────────────────────────────────────────

    def scrape_linkedin_trends(self, query: str, location: str = "", limit: int = 5) -> List[TrendItem]:
        """
        Scrapes real-time trending LinkedIn posts discussing the domain topic via harvestapi~linkedin-post-search.
        """
        key = self._get_api_key()
        if not key:
            return []

        clean_query = query.strip()
        if not clean_query:
            clean_query = "technology"

        actor_id = "harvestapi~linkedin-post-search"
        url = f"{self.BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"

        payload = {
            "searchQueries": [clean_query],
            "maxPosts": limit,
        }

        items: List[TrendItem] = []
        try:
            with httpx.Client(timeout=25.0) as client:
                res = client.post(url, params={"token": key}, json=payload)
                if res.status_code in [200, 201]:
                    posts = res.json()
                    if isinstance(posts, list):
                        for rank, p in enumerate(posts[:limit], 1):
                            content = p.get("content") or p.get("text") or ""
                            first_sentence = content.split("\n")[0].strip() if content else f"LinkedIn discussion on {clean_query}"
                            # Trim title to readable length
                            title = first_sentence[:120] if first_sentence else f"LinkedIn post on {clean_query}"
                            
                            author_info = p.get("author", {})
                            author_name = author_info.get("name") or author_info.get("headline") or "LinkedIn Member"
                            
                            # Engagement metrics
                            reactions = p.get("engagement", {}).get("totalReactions") or len(p.get("reactionIds", []))
                            comments = p.get("engagement", {}).get("totalComments") or len(p.get("commentIds", []))
                            eng_str = f"{reactions:,} reactions, {comments:,} comments" if (reactions or comments) else None

                            # Posted date handling (can be dict or str)
                            raw_posted = p.get("postedAt")
                            if isinstance(raw_posted, dict):
                                posted_date = raw_posted.get("date") or raw_posted.get("postedAgoText") or ""
                            else:
                                posted_date = str(raw_posted or "")

                            post_url = p.get("linkedinUrl") or p.get("shareLinkedinUrl") or "https://www.linkedin.com"

                            items.append(TrendItem(
                                rank=rank,
                                title=title,
                                url=post_url,
                                platform="linkedin",
                                content_type="post",
                                views_or_engagement=eng_str,
                                published_date=posted_date,
                                creator_handle=author_name,
                                why_trending=f"High-engagement LinkedIn post on '{clean_query}'",
                                relevance_to_niche=f"Direct professional discussion in {clean_query}",
                            ))
                else:
                    logger.warning(f"[Apify] LinkedIn post search returned HTTP {res.status_code}")
        except Exception as e:
            logger.warning(f"[Apify] Exception running LinkedIn post search: {e}")

        return items


apify_service = ApifyService()
