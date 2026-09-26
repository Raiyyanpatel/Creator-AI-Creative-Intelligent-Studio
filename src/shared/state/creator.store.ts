import { useState, useEffect } from 'react';
import { CreatorProfile } from '@/shared/types/creator';
import { storage } from '@/utils/storage';

const INITIAL_CREATOR: CreatorProfile = {
  id: 'c_default',
  name: 'Harsh Jain',
  avatarUrl: '/assets/creator-avatar.jpg',
  coverUrl: '/assets/creator-setup.jpg',
  niche: 'Technology & AI Agents',
  platforms: ['YouTube', 'X / Twitter', 'LinkedIn', 'Substack'],
  goals: ['Scale Short-form', 'Grow Audience', 'Monetize Workflows'],
  dna: {
    voice: 'Technical, conversational, concrete, fast-paced.',
    tone: ['High-energy', 'Analytical', 'Pragmatic', 'Contrarian'],
    frequentPhrases: ['Here is the unlock', 'Look at this benchmark', 'Zero latency', 'Let me show you'],
    avgVideoLength: '45s Shorts / 14m Deep Dives',
    hookStyle: 'Start with the unexpected result first, then reveal the mechanism.',
    coreThemes: ['On-Device AI', 'Autonomous Coding Agents', 'Hardware Benchmarks'],
    thumbnailStyle: 'High-contrast typography, close-up reaction, lime accents.',
  },
  hookPatterns: [
    {
      id: 'h1',
      title: 'The "Why Everyone Is Wrong" Teardown',
      example: 'Stop believing AI agents only run in giant cloud datacenters...',
      virality: 94,
    },
    {
      id: 'h2',
      title: '30-Day Rapid Transformation Case Study',
      example: 'Day 1 vs Day 30: what actually happened when I ran local LLMs...',
      virality: 91,
    },
    {
      id: 'h3',
      title: 'The Pattern Interrupt',
      example: 'If you are still writing video scripts manually, stop doing this right now...',
      virality: 88,
    },
  ],
  connectedSources: ['YouTube (@HarshTech)', 'X (@harsh_ai)', 'LinkedIn', 'Substack'],
  customInstructions: 'Keep technical jargon accessible. Prioritize rapid proofs and interactive demos.',
  metrics: {
    views: '24.3K',
    viewsChange: '+18%',
    engagement: '8.4%',
    engagementChange: '+2.1%',
    watchTime: '41m',
    growth: '+12%',
  },
};

let currentCreator: CreatorProfile = storage.load('creator_profile', INITIAL_CREATOR);
const listeners = new Set<(creator: CreatorProfile) => void>();

function notify() {
  storage.save('creator_profile', currentCreator);
  listeners.forEach((l) => l(currentCreator));
}

export const creatorStore = {
  get: () => currentCreator,
  set: (updater: (prev: CreatorProfile) => CreatorProfile) => {
    currentCreator = updater(currentCreator);
    notify();
  },
  updateProfile: (partial: Partial<CreatorProfile>) => {
    currentCreator = { ...currentCreator, ...partial };
    notify();
  },
};

export function useCreatorStore() {
  const [state, setState] = useState<CreatorProfile>(currentCreator);
  useEffect(() => {
    listeners.add(setState);
    return () => {
      listeners.delete(setState);
    };
  }, []);
  return {
    creator: state,
    updateProfile: creatorStore.updateProfile,
  };
}
