import { useState, useEffect } from "react";
import {
  Region,
  DiscoveryTab,
  ContentItem,
  StoryboardItem,
  SearchResultsGrouped,
  GeneratedContent,
  GenerationInput,
  CopilotMessage,
} from "../types/creatorIntelligence";
import { searchService } from "../services/searchService";
import { bookmarkService } from "../services/bookmarkService";
import { storyboardService } from "../services/storyboardService";
import { mockGenerationService } from "../services/mockGenerationService";

interface StoreState {
  selectedRegion: Region;
  selectedDiscoveryTab: DiscoveryTab;
  searchQuery: string;
  searchResults: SearchResultsGrouped;
  isSearching: boolean;
  bookmarkedItems: ContentItem[];
  storyboardItems: StoryboardItem[];
  selectedContent: ContentItem | null;
  detailModalVisible: boolean;
  storyboardSheetVisible: boolean;
  generateModalVisible: boolean;
  generationLoading: boolean;
  generationInput: GenerationInput;
  generatedDraft: GeneratedContent | null;
  activeGenerateTab: "copilot" | "final";
  copilotMessages: CopilotMessage[];
  toastMessage: string | null;
}

const initialGenerationInput: GenerationInput = {
  topic: "On-Device AI & Autonomous Creator Workflows",
  referenceIds: ["video-1"],
  contentType: "reel",
  duration: "30_sec",
  tone: "creators_style",
};

let state: StoreState = {
  selectedRegion: "for_you",
  selectedDiscoveryTab: "videos",
  searchQuery: "",
  searchResults: {
    trends: [],
    creators: [],
    videos: [],
    reels: [],
    topics: [],
    totalMatches: 0,
  },
  isSearching: false,
  bookmarkedItems: bookmarkService.getBookmarkedItems(),
  storyboardItems: storyboardService.getItems(),
  selectedContent: null,
  detailModalVisible: false,
  storyboardSheetVisible: false,
  generateModalVisible: false,
  generationLoading: false,
  generationInput: initialGenerationInput,
  generatedDraft: null,
  activeGenerateTab: "copilot",
  copilotMessages: [
    {
      id: "init-ai-msg",
      sender: "ai",
      text: "I found three strong angles from your references. I'd suggest focusing on how on-device AI is changing mobile creation.",
      timestamp: "Just now",
    },
  ],
  toastMessage: null,
};

const listeners = new Set<() => void>();

function notify() {
  listeners.forEach((listener) => listener());
}

export const creatorIntelligenceActions = {
  setRegion(region: Region) {
    state = { ...state, selectedRegion: region };
    notify();
  },

  setDiscoveryTab(tab: DiscoveryTab) {
    state = { ...state, selectedDiscoveryTab: tab };
    notify();
  },

  setSearchQuery(query: string) {
    const isSearching = query.trim().length > 0;
    const results = isSearching ? searchService.search(query, state.selectedRegion) : {
      trends: [],
      creators: [],
      videos: [],
      reels: [],
      topics: [],
      totalMatches: 0,
    };
    state = {
      ...state,
      searchQuery: query,
      isSearching,
      searchResults: results,
    };
    notify();
  },

  clearSearch() {
    state = {
      ...state,
      searchQuery: "",
      isSearching: false,
      searchResults: {
        trends: [],
        creators: [],
        videos: [],
        reels: [],
        topics: [],
        totalMatches: 0,
      },
    };
    notify();
  },

  toggleBookmark(content: ContentItem) {
    const isSaved = bookmarkService.toggle(content.id);
    state = {
      ...state,
      bookmarkedItems: bookmarkService.getBookmarkedItems(),
      toastMessage: isSaved ? "Saved to bookmarks" : "Removed from bookmarks",
    };
    notify();
    setTimeout(() => {
      state = { ...state, toastMessage: null };
      notify();
    }, 2500);
  },

  addToStoryboard(content: ContentItem) {
    storyboardService.add(content);
    state = {
      ...state,
      storyboardItems: storyboardService.getItems(),
      toastMessage: "Added to storyboard",
    };
    notify();
    setTimeout(() => {
      state = { ...state, toastMessage: null };
      notify();
    }, 2500);
  },

  removeFromStoryboard(storyboardItemId: string) {
    storyboardService.remove(storyboardItemId);
    state = {
      ...state,
      storyboardItems: storyboardService.getItems(),
      toastMessage: "Removed from storyboard",
    };
    notify();
    setTimeout(() => {
      state = { ...state, toastMessage: null };
      notify();
    }, 2500);
  },

  openContentDetail(content: ContentItem) {
    state = {
      ...state,
      selectedContent: content,
      detailModalVisible: true,
    };
    notify();
  },

  closeContentDetail() {
    state = {
      ...state,
      selectedContent: null,
      detailModalVisible: false,
    };
    notify();
  },

  setStoryboardSheetVisible(visible: boolean) {
    state = {
      ...state,
      storyboardSheetVisible: visible,
    };
    notify();
  },

  openGenerateModal() {
    const refIds = state.storyboardItems.map((i) => i.contentId);
    state = {
      ...state,
      storyboardSheetVisible: false,
      generateModalVisible: true,
      generationInput: {
        ...state.generationInput,
        referenceIds: refIds,
        topic: state.storyboardItems[0]?.content.title || "On-Device AI & Autonomous Workflows",
      },
      activeGenerateTab: "copilot",
    };
    notify();
  },

  closeGenerateModal() {
    state = {
      ...state,
      generateModalVisible: false,
    };
    notify();
  },

  setGenerationInput(partial: Partial<GenerationInput>) {
    state = {
      ...state,
      generationInput: {
        ...state.generationInput,
        ...partial,
      },
    };
    notify();
  },

  setActiveGenerateTab(tab: "copilot" | "final") {
    state = {
      ...state,
      activeGenerateTab: tab,
    };
    notify();
  },

  triggerGeneration() {
    state = { ...state, generationLoading: true };
    notify();

    setTimeout(() => {
      const generated = mockGenerationService.generateInitialContent(state.generationInput);
      state = {
        ...state,
        generationLoading: false,
        generatedDraft: generated,
        activeGenerateTab: "copilot",
        toastMessage: "Draft generated successfully!",
      };
      notify();

      setTimeout(() => {
        state = { ...state, toastMessage: null };
        notify();
      }, 2500);
    }, 1200);
  },

  sendCopilotMessage(userMessageText: string) {
    if (!userMessageText.trim() || !state.generatedDraft) return;

    const userMsg: CopilotMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: userMessageText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    const updatedMessages = [...state.copilotMessages, userMsg];
    state = {
      ...state,
      copilotMessages: updatedMessages,
    };
    notify();

    // Trigger AI revision
    setTimeout(() => {
      if (!state.generatedDraft) return;
      const { responseMessage, updatedDraft } = mockGenerationService.processCopilotCommand(
        userMessageText,
        state.generatedDraft
      );

      state = {
        ...state,
        generatedDraft: updatedDraft,
        copilotMessages: [...state.copilotMessages, responseMessage],
        toastMessage: responseMessage.appliedSummary || "Changes applied to draft",
      };
      notify();

      setTimeout(() => {
        state = { ...state, toastMessage: null };
        notify();
      }, 3000);
    }, 600);
  },

  saveDraftToProject() {
    state = {
      ...state,
      toastMessage: "Saved to your project drafts!",
    };
    notify();
    setTimeout(() => {
      state = { ...state, toastMessage: null };
      notify();
    }, 3000);
  },
};

export function useCreatorIntelligenceStore(): StoreState & typeof creatorIntelligenceActions {
  const [snapshot, setSnapshot] = useState<StoreState>(state);

  useEffect(() => {
    const onChange = () => setSnapshot(state);
    listeners.add(onChange);
    return () => {
      listeners.delete(onChange);
    };
  }, []);

  return {
    ...snapshot,
    ...creatorIntelligenceActions,
  };
}
