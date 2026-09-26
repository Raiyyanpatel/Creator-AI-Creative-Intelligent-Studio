/**
 * Creator Intelligence Type Definitions
 * =====================================
 * Common data contracts for the Creator Operating System.
 * Designed to mirror future backend responses without UI coupling.
 */

export type Region = "for_you" | "global" | "india" | "hyderabad" | "my_niche";

export type ContentType = "video" | "reel" | "post" | "short";

export type Platform = "youtube" | "instagram" | "x_twitter" | "linkedin" | "tiktok";

export type DiscoveryTab = "creators" | "videos" | "reels" | "topics" | "saved";

export interface Trend {
  id: string;
  topic: string;
  growth: number; // percentage, e.g. 42
  explanation: string;
  category: string;
  region: Region;
  relatedContentIds: string[];
  volume?: string; // e.g. "145K posts"
  momentum?: "rising" | "viral" | "steady";
  score?: number; // 0-100
  relatedTopics?: string[];
}

export interface Creator {
  id: string;
  name: string;
  handle: string;
  avatar: string;
  platform: Platform;
  followers: string;
  growth: string;
  niche: string;
  bio?: string;
  verified?: boolean;
}

export interface ContentItem {
  id: string;
  type: ContentType;
  title: string;
  creatorId: string;
  creatorName: string;
  creatorHandle: string;
  creatorAvatar: string;
  platform: Platform;
  thumbnail: string;
  views: string;
  engagement: string;
  publishedAt: string;
  topics: string[];
  trendScore: number; // e.g. 34 (meaning +34%)
  whyTrending?: string;
  whyThisMatters?: string;
  region?: Region;
  url?: string;
  duration?: string;
  isBookmarked: boolean;
}

export interface TopicItem {
  id: string;
  name: string;
  category: string;
  growth: number;
  description: string;
  relatedCount: number;
  region?: Region;
}

export interface StoryboardItem {
  id: string;
  contentId: string;
  content: ContentItem;
  addedAt: string;
  note?: string;
}

export type GenerationContentType =
  | "short_video"
  | "reel"
  | "youtube_video"
  | "linkedin_post"
  | "podcast"
  | "thread";

export type GenerationDuration = "30_sec" | "60_sec" | "90_sec" | "custom";

export type GenerationTone =
  | "educational"
  | "energetic"
  | "cinematic"
  | "conversational"
  | "creators_style";

export interface GenerationInput {
  topic: string;
  referenceIds: string[];
  contentType: GenerationContentType;
  duration: GenerationDuration;
  tone: GenerationTone;
  customNotes?: string;
}

export interface Scene {
  id: string;
  sceneNumber: number;
  duration: string; // e.g. "0–4 sec"
  visual: string;
  dialogue: string;
  camera: string;
  movement: string;
  bRollTrigger?: string;
}

export interface GeneratedContent {
  id: string;
  title: string;
  hook: string;
  coreMessage: string;
  script: string;
  scenes: Scene[];
  visualDirection: {
    camera: string;
    movement: string;
    lighting: string;
    colorPalette?: string;
  };
  broll: string[];
  music: {
    genre: string;
    bpm: number;
    mood: string;
  };
  cta: string;
  targetPlatform: string;
  estimatedRetention: string;
  changesApplied?: string[];
  version: number;
}

export interface CopilotMessage {
  id: string;
  sender: "user" | "ai" | "system";
  text: string;
  timestamp: string;
  changesMade?: {
    field: string;
    before: string;
    after: string;
  }[];
  appliedSummary?: string;
}

export interface SearchResultsGrouped {
  trends: Trend[];
  creators: Creator[];
  videos: ContentItem[];
  reels: ContentItem[];
  topics: TopicItem[];
  totalMatches: number;
}
