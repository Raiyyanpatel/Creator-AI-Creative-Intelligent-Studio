export interface CreatorDNA {
  voice: string;
  tone: string[];
  frequentPhrases: string[];
  avgVideoLength: string;
  hookStyle: string;
  coreThemes: string[];
  thumbnailStyle: string;
}

export interface HookPattern {
  id: string;
  title: string;
  example: string;
  virality: number;
}

export interface CreatorProfile {
  id: string;
  name: string;
  avatarUrl: string;
  coverUrl: string;
  niche: string;
  platforms: string[];
  goals: string[];
  dna: CreatorDNA;
  hookPatterns: HookPattern[];
  connectedSources: string[];
  customInstructions: string;
  metrics: {
    views: string;
    viewsChange: string;
    engagement: string;
    engagementChange: string;
    watchTime: string;
    growth: string;
  };
}
