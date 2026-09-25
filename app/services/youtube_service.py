import re
import logging
from typing import List, Dict, Any, Optional
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from app.models.profiling import VideoItem

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'skip_download': True,
        }

    def fetch_creator_videos(
        self,
        creator_name: str,
        channel_url_or_handle: Optional[str] = None,
        max_videos: int = 10
    ) -> Dict[str, Any]:
        """
        Fetches real videos and shorts from YouTube for a creator.
        Uses yt-dlp to extract authentic channel information without fake data.
        """
        query_target = channel_url_or_handle
        if not query_target or not query_target.strip():
            clean_name = creator_name.replace('@', '').strip()
            # Search both standard videos and shorts
            query_target = f"ytsearch{max_videos}:{clean_name}"

        videos: List[VideoItem] = []
        channel_metadata = {
            "channel_title": creator_name,
            "channel_url": "",
            "subscriber_count": None,
            "description": ""
        }

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                extract_result = ydl.extract_info(query_target, download=False)
                
                if not extract_result:
                    return {"videos": [], "metadata": channel_metadata}

                entries = extract_result.get('entries', [])
                if not entries and 'title' in extract_result:
                    # Single entry returned
                    entries = [extract_result]

                if 'uploader' in extract_result and extract_result.get('uploader'):
                    channel_metadata["channel_title"] = extract_result.get('uploader')
                if 'channel_url' in extract_result:
                    channel_metadata["channel_url"] = extract_result.get('channel_url')

                for entry in entries[:max_videos]:
                    if not entry:
                        continue
                    
                    vid_id = entry.get('id', '')
                    title = entry.get('title', 'Untitled Video')
                    duration = int(entry.get('duration') or 0)
                    url = entry.get('url') or f"https://www.youtube.com/watch?v={vid_id}"
                    if not url.startswith('http'):
                        url = f"https://www.youtube.com/watch?v={vid_id}"
                    
                    is_short = (duration > 0 and duration <= 65) or ('/shorts/' in url) or ('#shorts' in title.lower())
                    view_count = entry.get('view_count')
                    upload_date = entry.get('upload_date')
                    thumbnail_url = entry.get('thumbnail') or (f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg" if vid_id else None)

                    duration_formatted = f"{duration // 60}:{duration % 60:02d}"

                    # Attempt real transcript extraction
                    transcript_text, opening_words = self.fetch_transcript_and_opening(vid_id)

                    videos.append(
                        VideoItem(
                            id=vid_id,
                            title=title,
                            url=url,
                            duration_seconds=duration,
                            duration_formatted=duration_formatted,
                            is_short=is_short,
                            view_count=view_count,
                            upload_date=upload_date,
                            thumbnail_url=thumbnail_url,
                            transcript_available=bool(transcript_text),
                            transcript_snippet=transcript_text[:400] if transcript_text else None,
                            key_opening_words=opening_words
                        )
                    )

        except Exception as e:
            logger.error(f"Error fetching YouTube videos for {creator_name}: {e}")

        # Compute aggregate video metrics
        durations = [v.duration_seconds for v in videos if v.duration_seconds > 0]
        shorts_count = sum(1 for v in videos if v.is_short)
        long_count = len(videos) - shorts_count

        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "metadata": channel_metadata,
            "videos": videos,
            "total_found": len(videos),
            "shorts_count": shorts_count,
            "long_count": long_count,
            "avg_duration_seconds": avg_duration,
            "avg_duration_formatted": f"{int(avg_duration // 60)}:{int(avg_duration % 60):02d}"
        }

    def fetch_transcript_and_opening(self, video_id: str) -> tuple[Optional[str], Optional[str]]:
        """
        Fetches real spoken subtitles and the exact opening hook spoken in the video.
        """
        if not video_id:
            return None, None
        
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id)
            if not transcript_list:
                return None, None
            
            snippets = [item.text for item in transcript_list if hasattr(item, 'text')]
            full_text = " ".join(snippets)
            
            # Opening words: first 2-3 spoken snippets (typically 0-5 seconds)
            opening_snippets = [s for s in snippets[:3] if s.strip()]
            opening = " ".join(opening_snippets) if opening_snippets else None
            
            return full_text, opening
        except Exception:
            return None, None

youtube_service = YouTubeService()
