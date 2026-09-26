import { useState, useEffect } from 'react';
import { storage } from '@/utils/storage';

export interface MediaAsset {
  id: string;
  name: string;
  type: 'video' | 'audio' | 'image';
  url: string;
  duration?: number;
  size?: number;
  createdAt: string;
}

const INITIAL_ASSETS: MediaAsset[] = [
  { id: 'm1', name: 'Main A-Roll Talk', type: 'video', url: '/assets/create-edit-video.jpg', duration: 42, createdAt: 'Today' },
  { id: 'm2', name: 'Agent Interface Demo', type: 'video', url: '/assets/trend-on-device-ai.jpg', duration: 18, createdAt: 'Yesterday' },
  { id: 'm3', name: 'Lo-Fi Chill Beat', type: 'audio', url: '/assets/effects-showcase.jpg', duration: 120, createdAt: '2 days ago' },
  { id: 'm4', name: 'AI Inspiration Hero', type: 'image', url: '/assets/ai-inspiration.jpg', createdAt: '3 days ago' },
];

let assets: MediaAsset[] = storage.load('media_assets', INITIAL_ASSETS);
const listeners = new Set<() => void>();

function notify() {
  storage.save('media_assets', assets);
  listeners.forEach((l) => l());
}

export const mediaStore = {
  getAssets: () => assets,
  addAsset: (asset: Omit<MediaAsset, 'id' | 'createdAt'>) => {
    const newAsset: MediaAsset = {
      ...asset,
      id: `asset_${Date.now()}`,
      createdAt: 'Just now',
    };
    assets = [newAsset, ...assets];
    notify();
    return newAsset;
  },
  removeAsset: (id: string) => {
    assets = assets.filter((a) => a.id !== id);
    notify();
  },
};

export function useMediaStore() {
  const [, setVersion] = useState(0);
  useEffect(() => {
    const update = () => setVersion((v) => v + 1);
    listeners.add(update);
    return () => {
      listeners.delete(update);
    };
  }, []);

  return {
    assets,
    addAsset: mediaStore.addAsset,
    removeAsset: mediaStore.removeAsset,
  };
}
