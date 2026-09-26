import { StoryboardItem, ContentItem } from "../types/creatorIntelligence";
import { MOCK_CONTENT } from "../data/mockContent";

class StoryboardService {
  private items: StoryboardItem[] = [];

  constructor() {
    // Initial demo reference
    const initialContent = MOCK_CONTENT.find((c) => c.id === "video-1");
    if (initialContent) {
      this.items.push({
        id: `sb-${Date.now()}-1`,
        contentId: initialContent.id,
        content: initialContent,
        addedAt: "Just now",
        note: "Key benchmark on agent velocity vs chat prompts",
      });
    }
  }

  getItems(): StoryboardItem[] {
    return [...this.items];
  }

  getCount(): number {
    return this.items.length;
  }

  hasItem(contentId: string): boolean {
    return this.items.some((i) => i.contentId === contentId);
  }

  add(content: ContentItem, note?: string): StoryboardItem {
    const existing = this.items.find((i) => i.contentId === content.id);
    if (existing) {
      return existing;
    }

    const newItem: StoryboardItem = {
      id: `sb-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      contentId: content.id,
      content,
      addedAt: "Just now",
      note: note || `Added from ${content.platform} discovery`,
    };

    this.items.unshift(newItem);
    return newItem;
  }

  remove(storyboardItemId: string): boolean {
    const lenBefore = this.items.length;
    this.items = this.items.filter((i) => i.id !== storyboardItemId);
    return this.items.length < lenBefore;
  }

  removeByContentId(contentId: string): boolean {
    const lenBefore = this.items.length;
    this.items = this.items.filter((i) => i.contentId !== contentId);
    return this.items.length < lenBefore;
  }

  reorder(fromIndex: number, toIndex: number): void {
    if (
      fromIndex < 0 ||
      fromIndex >= this.items.length ||
      toIndex < 0 ||
      toIndex >= this.items.length
    ) {
      return;
    }
    const [moved] = this.items.splice(fromIndex, 1);
    this.items.splice(toIndex, 0, moved);
  }

  clear(): void {
    this.items = [];
  }
}

export const storyboardService = new StoryboardService();
