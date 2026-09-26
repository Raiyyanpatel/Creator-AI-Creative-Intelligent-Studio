import logging
import re
from typing import List, Dict, Any, Optional
import feedparser
from bs4 import BeautifulSoup
from app.models.profiling import ArticleItem

logger = logging.getLogger(__name__)

class SubstackService:
    def fetch_creator_articles(
        self,
        creator_name: str,
        substack_url_or_handle: Optional[str] = None,
        max_articles: int = 5
    ) -> Dict[str, Any]:
        """
        Fetches authentic Substack newsletter articles using Substack's real RSS feed.
        """
        feed_url = self._resolve_feed_url(creator_name, substack_url_or_handle)
        articles: List[ArticleItem] = []
        metadata = {
            "publication_title": f"{creator_name}'s Substack",
            "publication_url": feed_url.replace('/feed', ''),
            "description": "",
            "total_articles": 0
        }

        try:
            feed = feedparser.parse(feed_url)
            
            if feed.entries:
                if hasattr(feed, 'feed'):
                    metadata["publication_title"] = getattr(feed.feed, 'title', metadata["publication_title"])
                    metadata["description"] = getattr(feed.feed, 'subtitle', '')
                    metadata["publication_url"] = getattr(feed.feed, 'link', metadata["publication_url"])

                for entry in feed.entries[:max_articles]:
                    title = getattr(entry, 'title', 'Untitled Post')
                    link = getattr(entry, 'link', '')
                    published = getattr(entry, 'published', getattr(entry, 'updated', None))
                    
                    # Extract body content / summary
                    raw_content = ""
                    if hasattr(entry, 'content') and entry.content:
                        raw_content = entry.content[0].value
                    elif hasattr(entry, 'summary'):
                        raw_content = entry.summary
                    
                    # Clean HTML tags to get pure text
                    soup = BeautifulSoup(raw_content, 'html.parser')
                    clean_text = soup.get_text(separator=' ', strip=True)
                    words = clean_text.split()
                    word_count = len(words)

                    summary = clean_text[:350] + "..." if len(clean_text) > 350 else clean_text

                    articles.append(
                        ArticleItem(
                            title=title,
                            url=link,
                            published_date=published,
                            word_count=word_count,
                            summary=summary
                        )
                    )
                metadata["total_articles"] = len(feed.entries)

        except Exception as e:
            logger.error(f"Error reading Substack feed {feed_url}: {e}")

        total_words = sum(a.word_count for a in articles)
        avg_word_count = total_words // len(articles) if articles else 0

        return {
            "metadata": metadata,
            "articles": articles,
            "avg_word_count": avg_word_count,
            "feed_source": feed_url
        }

    def _resolve_feed_url(self, creator_name: str, input_str: Optional[str]) -> str:
        if input_str and input_str.strip():
            url = input_str.strip()
            if not url.startswith('http'):
                url = f"https://{url}"
            if not url.endswith('/feed') and not url.endswith('/feed/'):
                url = url.rstrip('/') + '/feed'
            return url
        
        # Auto-construct likely substack feed from creator handle or slug
        slug = re.sub(r'[^a-zA-Z0-9]', '', creator_name.lower())
        return f"https://{slug}.substack.com/feed"

substack_service = SubstackService()
