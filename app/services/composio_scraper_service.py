import os
import re
import logging
from typing import List, Dict, Any, Optional

from app.config import settings
from app.models.profiling import VideoItem

logger = logging.getLogger(__name__)

class ComposioScraperService:
    """
    Leverages Composio's authenticated tool ecosystem and active connected accounts
    to scrape creator profiles, channel uploads, and professional footprint for
    YouTube, LinkedIn, and Instagram.
    """

    def __init__(self):
        self.api_key = settings.COMPOSIO_API_KEY or os.environ.get("COMPOSIO_API_KEY", "")
        self.client = None
        self.connected_accounts: Dict[str, str] = {}
        self.user_id: Optional[str] = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            logger.info("[ComposioScraper] No COMPOSIO_API_KEY configured.")
            return

        try:
            from composio import Composio
            self.client = Composio(api_key=self.api_key)
            # Discover active connected accounts and user_id
            accs = self.client.connected_accounts.list()
            for item in getattr(accs, "items", []):
                slug = getattr(item.toolkit, "slug", "") if hasattr(item, "toolkit") else ""
                acc_id = getattr(item, "id", "")
                status = getattr(item, "status", "")
                uid = getattr(item, "user_id", None)
                if status == "ACTIVE" and slug:
                    self.connected_accounts[slug] = acc_id
                    if uid and not self.user_id:
                        self.user_id = uid

            logger.info(
                f"[ComposioScraper] Initialized Composio client. "
                f"Active accounts: {list(self.connected_accounts.keys())}, User ID: {self.user_id}"
            )
        except Exception as e:
            logger.warning(f"[ComposioScraper] Initialization warning: {e}")

    # ──────────────────────────────────────────────
    # YouTube via Composio
    # ──────────────────────────────────────────────

    def scrape_youtube_channel(self, handle_or_name: str, max_videos: int = 5) -> Optional[Dict[str, Any]]:
        """
        Uses Composio's YouTube toolkit to fetch channel ID, metadata, and recent uploads.
        """
        if not self.client or "youtube" not in self.connected_accounts or not self.user_id:
            logger.debug("[ComposioScraper] YouTube account not available in Composio.")
            return None

        clean_handle = handle_or_name.replace("https://www.youtube.com/", "").replace("youtube.com/", "").strip()
        if not clean_handle.startswith("@"):
            clean_handle = f"@{clean_handle}"

        try:
            acc_id = self.connected_accounts["youtube"]
            
            # 1. Resolve channel ID via handle
            cid_res = self.client.tools.execute(
                slug="YOUTUBE_GET_CHANNEL_ID_BY_HANDLE",
                arguments={"channel_handle": clean_handle},
                connected_account_id=acc_id,
                user_id=self.user_id,
                dangerously_skip_version_check=True,
            )

            channel_id = None
            if cid_res.get("successful") and cid_res.get("data", {}).get("items"):
                channel_id = cid_res["data"]["items"][0].get("id")

            if not channel_id:
                logger.debug(f"[ComposioScraper] Could not resolve channel ID for {clean_handle}")
                return None

            # 2. Fetch channel recent uploads playlist items
            vids_res = self.client.tools.execute(
                slug="YOUTUBE_LIST_CHANNEL_VIDEOS",
                arguments={"channel_id": channel_id, "max_results": max_videos},
                connected_account_id=acc_id,
                user_id=self.user_id,
                dangerously_skip_version_check=True,
            )

            videos_data = []
            channel_title = handle_or_name
            channel_desc = ""

            if vids_res.get("successful") and vids_res.get("data", {}).get("items"):
                for it in vids_res["data"]["items"]:
                    snip = it.get("snippet", {})
                    channel_title = snip.get("channelTitle", channel_title)
                    channel_desc = snip.get("description", "")
                    vid_id = snip.get("resourceId", {}).get("videoId")
                    if not vid_id:
                        continue
                    
                    title = snip.get("title", "")
                    pub = snip.get("publishedAt", "")
                    thumbs = snip.get("thumbnails", {})
                    thumb_url = (
                        thumbs.get("maxres", {}).get("url")
                        or thumbs.get("high", {}).get("url")
                        or thumbs.get("default", {}).get("url")
                    )

                    videos_data.append({
                        "id": vid_id,
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={vid_id}",
                        "published_at": pub,
                        "thumbnail": thumb_url,
                        "description": channel_desc[:250],
                        "source": "composio_youtube_tool"
                    })

            # 3. Get channel statistics
            stats_res = self.client.tools.execute(
                slug="YOUTUBE_GET_CHANNEL_STATISTICS",
                arguments={"channel_id": channel_id},
                connected_account_id=acc_id,
                user_id=self.user_id,
                dangerously_skip_version_check=True,
            )

            subscriber_count = None
            total_videos = None
            if stats_res.get("successful") and stats_res.get("data", {}).get("items"):
                st = stats_res["data"]["items"][0].get("statistics", {})
                subs = st.get("subscriberCount")
                if subs:
                    subscriber_count = f"{int(subs):,} subscribers"
                vids = st.get("videoCount")
                if vids:
                    total_videos = f"{int(vids):,} videos"

            logger.info(f"[ComposioScraper] Successfully scraped YouTube channel '{channel_title}' via Composio ({len(videos_data)} videos).")
            return {
                "channel_id": channel_id,
                "channel_title": channel_title,
                "handle": clean_handle,
                "subscriber_count": subscriber_count,
                "total_videos": total_videos,
                "description": channel_desc,
                "videos": videos_data,
                "source": "composio"
            }

        except Exception as e:
            logger.warning(f"[ComposioScraper] YouTube scrape error: {e}")
            return None

    # ──────────────────────────────────────────────
    # LinkedIn via Composio
    # ──────────────────────────────────────────────

    def scrape_linkedin_profile(self, handle_or_name: str) -> Optional[Dict[str, Any]]:
        """
        Uses Composio's LinkedIn toolkit to fetch profile metadata, headline, and posts.
        """
        if not self.client or "linkedin" not in self.connected_accounts or not self.user_id:
            logger.debug("[ComposioScraper] LinkedIn account not available in Composio.")
            return None

        try:
            acc_id = self.connected_accounts["linkedin"]
            
            # Fetch user profile info
            info_res = self.client.tools.execute(
                slug="LINKEDIN_GET_MY_INFO",
                arguments={},
                connected_account_id=acc_id,
                user_id=self.user_id,
                dangerously_skip_version_check=True,
            )

            if info_res.get("successful") and info_res.get("data"):
                data = info_res["data"]
                first_name = data.get("localizedFirstName") or data.get("firstName", {}).get("localized", {}).get("en_US", "")
                last_name = data.get("localizedLastName") or data.get("lastName", {}).get("localized", {}).get("en_US", "")
                full_name = f"{first_name} {last_name}".strip() or handle_or_name
                headline = data.get("localizedHeadline") or data.get("headline", {}).get("localized", {}).get("en_US", "")
                vanity = data.get("vanityName", handle_or_name)
                profile_url = data.get("profileUrl") or f"https://www.linkedin.com/in/{vanity}"

                logger.info(f"[ComposioScraper] Successfully scraped LinkedIn profile '{full_name}' via Composio.")
                return {
                    "full_name": full_name,
                    "headline": headline,
                    "vanity_name": vanity,
                    "profile_url": profile_url,
                    "source": "composio"
                }

        except Exception as e:
            logger.warning(f"[ComposioScraper] LinkedIn scrape error: {e}")

        return None

    # ──────────────────────────────────────────────
    # Instagram via Composio
    # ──────────────────────────────────────────────

    def scrape_instagram_profile(self, handle_or_name: str) -> Optional[Dict[str, Any]]:
        """
        Uses Composio's Instagram toolkit to inspect active user media and insights.
        """
        if not self.client or "instagram" not in self.connected_accounts or not self.user_id:
            logger.debug("[ComposioScraper] Instagram account not available in Composio.")
            return None

        try:
            acc_id = self.connected_accounts["instagram"]
            media_res = self.client.tools.execute(
                slug="INSTAGRAM_GET_IG_USER_MEDIA",
                arguments={"fields": "id,caption,media_type,media_url,permalink,timestamp"},
                connected_account_id=acc_id,
                user_id=self.user_id,
                dangerously_skip_version_check=True,
            )

            if media_res.get("successful") and media_res.get("data", {}).get("data"):
                posts = []
                for p in media_res["data"]["data"][:5]:
                    posts.append({
                        "id": p.get("id"),
                        "caption": p.get("caption", ""),
                        "url": p.get("permalink"),
                        "media_type": p.get("media_type", "IMAGE"),
                        "published_at": p.get("timestamp"),
                        "source": "composio"
                    })
                return {
                    "handle": handle_or_name,
                    "recent_posts": posts,
                    "source": "composio"
                }
        except Exception as e:
            logger.debug(f"[ComposioScraper] Instagram scrape notice: {e}")

        return None

composio_scraper_service = ComposioScraperService()
