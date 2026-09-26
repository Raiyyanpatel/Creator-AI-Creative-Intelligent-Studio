import { useState, useEffect } from 'react';

export type EditorPanel = null | 'cut' | 'audio' | 'captions' | 'reframe' | 'highlights' | 'effects';

interface EditorState {
  currentTime: number;
  isPlaying: boolean;
  activePanel: EditorPanel;
  zoomLevel: number;
  selectedClipId: string | null;
  aspectRatio: '9:16' | '16:9' | '1:1';
  hasCaptions: boolean;
  audioNoiseReduction: boolean;
}

const INITIAL_STATE: EditorState = {
  currentTime: 6,
  isPlaying: false,
  activePanel: null,
  zoomLevel: 1,
  selectedClipId: 'c1',
  aspectRatio: '9:16',
  hasCaptions: true,
  audioNoiseReduction: true,
};

let state: EditorState = { ...INITIAL_STATE };
const listeners = new Set<() => void>();

function notify() {
  listeners.forEach((l) => l());
}

export const editorStore = {
  getState: () => state,
  setCurrentTime: (timeOrUpdater: number | ((prev: number) => number)) => {
    state = {
      ...state,
      currentTime: typeof timeOrUpdater === 'function' ? timeOrUpdater(state.currentTime) : timeOrUpdater,
    };
    notify();
  },
  togglePlay: () => {
    state = { ...state, isPlaying: !state.isPlaying };
    notify();
  },
  setPlaying: (playing: boolean) => {
    state = { ...state, isPlaying: playing };
    notify();
  },
  setActivePanel: (panel: EditorPanel) => {
    state = { ...state, activePanel: state.activePanel === panel ? null : panel };
    notify();
  },
  setAspectRatio: (ar: '9:16' | '16:9' | '1:1') => {
    state = { ...state, aspectRatio: ar };
    notify();
  },
  toggleCaptions: () => {
    state = { ...state, hasCaptions: !state.hasCaptions };
    notify();
  },
  toggleNoiseReduction: () => {
    state = { ...state, audioNoiseReduction: !state.audioNoiseReduction };
    notify();
  },
};

export function useEditorStore() {
  const [, setVersion] = useState(0);
  useEffect(() => {
    const update = () => setVersion((v) => v + 1);
    listeners.add(update);
    return () => {
      listeners.delete(update);
    };
  }, []);

  return {
    ...state,
    setCurrentTime: editorStore.setCurrentTime,
    togglePlay: editorStore.togglePlay,
    setPlaying: editorStore.setPlaying,
    setActivePanel: editorStore.setActivePanel,
    setAspectRatio: editorStore.setAspectRatio,
    toggleCaptions: editorStore.toggleCaptions,
    toggleNoiseReduction: editorStore.toggleNoiseReduction,
  };
}
