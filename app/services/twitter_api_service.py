import os
import re
import logging
from typing import List, Dict, Any, Optional
import httpx
import feedparser
from bs4 import BeautifulSoup

from app.config import settings
from app.models.intelligence import TrendItem, CreatorPlatformProfile

logger = logging.getLogger(__name__)

class TwitterApiService:
    """
    Direct integration with Twitter API v2 using the configured TWITTER_BEARER_TOKEN.
    Provides authentic live tweet searches, trending domain discussions,
    and verified creator profile statistics (followers, tweet counts, metrics).
    """

    BASE_URL = "https://api.twitter.com/2"

    def __init__(self):
        self.bearer_token = settings.TWITTER_BEARER_TOKEN or os.environ.get("TWITTER_BEARER_TOKEN", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "User-Agent": "CreatorAIStudio/2.0"
        }

    # ──────────────────────────────────────────────
    # Search Domain Tweets (Trending Discussions)
    # ──────────────────────────────────────────────

    def search_domain_tweets(self, query: str, location: str = "US", limit: int = 8) -> List[TrendItem]:
        """
        Searches recent viral/popular tweets in creator's domain/niche via Twitter API v2.
        """
        items: List[TrendItem] = []

        if self.bearer_token:
            try:
                # Build search query targeting authentic domain posts (excluding retweets)
                # Twitter API syntax: multi-word phrases require all words; extract top 2 core keywords
                stop_words = {"review", "shootout", "teardown", "guide", "tutorial", "video", "the", "and", "for", "with", "how", "what"}
                words = [w for w in re.findall(r'[a-zA-Z0-9]+', query) if len(w) > 2 and w.lower() not in stop_words]
                if words:
                    core_term = " ".join(words[:2])
                    clean_q = f"({core_term}) -is:retweet"
                else:
                    clean_q = f"{query} -is:retweet"
                url = f"{self.BASE_URL}/tweets/search/recent"
                params = {
                    "query": clean_q,
                    "max_results": min(max(limit, 10), 50),
                    "tweet.fields": "public_metrics,created_at,author_id,entities",
                    "expansions": "author_id",
                    "user.fields": "username,name,verified"
                }

                with httpx.Client(timeout=10.0) as client:
                    res = client.get(url, headers=self._headers(), params=params)
                    if res.status_code == 200:
                        data = res.json()
                        raw_tweets = data.get("data", [])
                        users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}

                        # Sort by like_count + retweet_count to surface the most viral posts
                        def engagement_score(t):
                            m = t.get("public_metrics", {})
                            return m.get("like_count", 0) + (m.get("retweet_count", 0) * 2)

                        sorted_tweets = sorted(raw_tweets, key=engagement_score, reverse=True)

                        for rank, t in enumerate(sorted_tweets[:limit], 1):
                            tid = t.get("id")
                            text = t.get("text", "")
                            author = users.get(t.get("author_id"), {})
                            uname = author.get("username", "x_user")
                            metrics = t.get("public_metrics", {})

                            likes = metrics.get("like_count", 0)
                            rts = metrics.get("retweet_count", 0)
                            impressions = metrics.get("impression_count", 0)
                            bookmarks = metrics.get("bookmark_count", 0)

                            engagement_str = f"{likes:,} likes, {rts:,} retweets"
                            if impressions > 0:
                                engagement_str += f", {impressions:,} views"

                            items.append(TrendItem(
                                rank=rank,
                                title=text[:140] + ("..." if len(text) > 140 else ""),
                                url=f"https://x.com/{uname}/status/{tid}",
                                platform="x_twitter",
                                content_type="tweet",
                                views_or_engagement=engagement_str,
                                published_date=t.get("created_at", ""),
                                creator_handle=f"@{uname}",
                                why_trending=f"High engagement on X/Twitter ({likes} likes, {rts} RTs, {bookmarks} bookmarks)",
                                relevance_to_niche=f"Trending discussion in '{query}'",
                            ))
                        logger.info(f"[TwitterAPI] Discovered {len(items)} trending tweets for '{query}' via Twitter API v2.")
                    elif res.status_code == 429:
                        logger.warning("[TwitterAPI] Rate limit reached on Twitter API v2. Falling back to RSS.")
                    else:
                        logger.warning(f"[TwitterAPI] Search returned HTTP {res.status_code}: {res.text[:200]}")
            except Exception as e:
                logger.warning(f"[TwitterAPI] Tweet search error: {e}")

        # Fallback to Google News RSS if API returned empty
        if not items:
            try:
                rss_q = f"{query} viral twitter thread OR tweet {location}"
                rss_url = f"https://news.google.com/rss/search?q={rss_q.replace(' ', '+')}&hl=en"
                feed = feedparser.parse(rss_url)
                for rank, entry in enumerate(feed.entries[:limit], 1):
                    items.append(TrendItem(
                        rank=rank,
                        title=entry.get("title", ""),
                        url=entry.get("link", ""),
                        platform="x_twitter",
                        content_type="thread",
                        published_date=entry.get("published", ""),
                        creator_handle=entry.get("source", {}).get("title", "X/Twitter"),
                        why_trending="Trending in Google News for X/Twitter",
                        relevance_to_niche=f"Relevant to {query}",
                    ))
            except Exception as e:
                logger.debug(f"[TwitterAPI] RSS fallback error: {e}")

        return items

    # ──────────────────────────────────────────────
    # Extract Creator Profile
    # ──────────────────────────────────────────────

    def extract_creator_profile(self, creator_name: str, handle: str, niche: str) -> CreatorPlatformProfile:
        """
        Pulls authentic profile statistics (followers, following, bio, verified status)
        and recent posts directly using Twitter API v2.
        """
        clean_handle = handle.replace("@", "").strip() if handle else re.sub(r'[^a-zA-Z0-9_]', '', creator_name.lower())
        if "x.com/" in clean_handle or "twitter.com/" in clean_handle:
            clean_handle = clean_handle.split("/")[-1].replace("@", "")

        profile = CreatorPlatformProfile(
            platform="x_twitter",
            handle=f"@{clean_handle}",
            profile_url=f"https://x.com/{clean_handle}",
            display_name=creator_name,
        )

        user_id = None
        if self.bearer_token:
            try:
                # 1. Fetch User Data by Username
                u_url = f"{self.BASE_URL}/users/by/username/{clean_handle}"
                params = {"user.fields": "public_metrics,description,verified,profile_image_url,name"}
                with httpx.Client(timeout=10.0) as client:
                    u_res = client.get(u_url, headers=self._headers(), params=params)
                    if u_res.status_code == 200:
                        u_data = u_res.json().get("data", {})
                        user_id = u_data.get("id")
                        profile.display_name = u_data.get("name", creator_name)
                        profile.bio = u_data.get("description", "")
                        profile.verified = bool(u_data.get("verified"))

                        metrics = u_data.get("public_metrics", {})
                        followers = metrics.get("followers_count")
                        following = metrics.get("following_count")
                        tweets = metrics.get("tweet_count")

                        if followers is not None:
                            profile.follower_or_sub_count = f"{followers:,} followers"
                        if following is not None:
                            profile.following_count = f"{following:,} following"
                        if tweets is not None:
                            profile.total_posts_or_videos = f"{tweets:,} tweets"

                        # 2. Fetch User Recent Tweets
                        if user_id:
                            tw_url = f"{self.BASE_URL}/users/{user_id}/tweets"
                            tw_params = {
                                "max_results": 5,
                                "tweet.fields": "public_metrics,created_at",
                                "exclude": "retweets"
                            }
                            tw_res = client.get(tw_url, headers=self._headers(), params=tw_params)
                            if tw_res.status_code == 200:
                                for t in tw_res.json().get("data", []):
                                    m = t.get("public_metrics", {})
                                    profile.recent_content.append({
                                        "id": t.get("id"),
                                        "text": t.get("text", "")[:280],
                                        "url": f"https://x.com/{clean_handle}/status/{t.get('id')}",
                                        "likes": m.get("like_count", 0),
                                        "retweets": m.get("retweet_count", 0),
                                        "bookmarks": m.get("bookmark_count", 0),
                                        "impressions": m.get("impression_count", 0),
                                        "created_at": t.get("created_at"),
                                        "content_type": "tweet"
                                    })
                        logger.info(f"[TwitterAPI] Successfully fetched profile & recent tweets for @{clean_handle} via Twitter API v2.")
            except Exception as e:
                logger.warning(f"[TwitterAPI] Profile fetch error for @{clean_handle}: {e}")

        # Web / RSS fallback if API returned no recent content
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
            except Exception:
                pass

        profile.growth_gap_analysis = (
            f"X footprint (@{clean_handle}): Account currently has {profile.follower_or_sub_count or 'an engaged audience'}. "
            f"To maximize reach in '{niche}', publish 1 weekly signature deep-dive thread optimized for bookmark saves "
            f"(which the X algorithm weights 5x higher than retweets for feed distribution), backed by 2-3 daily short observations."
        )
        return profile

twitter_api_service = TwitterApiService()
