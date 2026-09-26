import { ContentItem } from "../types/creatorIntelligence";
import { MOCK_CONTENT } from "../data/mockContent";

/**
 * In-memory bookmark store with session persistence.
 */
class BookmarkService {
  private bookmarkedIds: Set<string> = new Set<string>();

  constructor() {
    // Default preset with 1 initial bookmark for a smooth demo experience
    this.bookmarkedIds.add("video-1");
  }

  isBookmarked(contentId: string): boolean {
    return this.bookmarkedIds.has(contentId);
  }

  toggle(contentId: string): boolean {
    if (this.bookmarkedIds.has(contentId)) {
      this.bookmarkedIds.delete(contentId);
      return false;
    } else {
      this.bookmarkedIds.add(contentId);
      return true;
    }
  }

  getBookmarkedItems(): ContentItem[] {
    return MOCK_CONTENT.filter((item) => this.bookmarkedIds.has(item.id)).map(
      (item) => ({
        ...item,
        isBookmarked: true,
      })
    );
  }

  getCount(): number {
    return this.bookmarkedIds.size;
  }
}

export const bookmarkService = new BookmarkService();
