import { useState, useEffect } from 'react';
import { storage } from '@/utils/storage';

export type MainTab = 'home' | 'insights' | 'create' | 'profile';
export type ScreenModal =
  | null
  | 'onboarding'
  | 'editor'
  | 'recording'
  | 'teleprompter'
  | 'script'
  | 'effects'
  | 'game-studio'
  | 'export'
  | 'assets';

interface AppState {
  activeTab: MainTab;
  activeModal: ScreenModal;
  isCopilotOpen: boolean;
  copilotInitialPrompt: string;
  hasCompletedOnboarding: boolean;
  toastMessage: string | null;
}

const INITIAL_APP_STATE: AppState = {
  activeTab: 'home',
  activeModal: storage.load('has_onboarded', false) ? null : 'onboarding',
  isCopilotOpen: false,
  copilotInitialPrompt: '',
  hasCompletedOnboarding: storage.load('has_onboarded', false),
  toastMessage: null,
};

let appState: AppState = { ...INITIAL_APP_STATE };
const listeners = new Set<() => void>();

function notify() {
  listeners.forEach((l) => l());
}

export const appStore = {
  getState: () => appState,
  setActiveTab: (tab: MainTab) => {
    appState = { ...appState, activeTab: tab, activeModal: null };
    notify();
  },
  openModal: (modal: ScreenModal) => {
    appState = { ...appState, activeModal: modal };
    notify();
  },
  closeModal: () => {
    appState = { ...appState, activeModal: null };
    notify();
  },
  openCopilot: (initialPrompt = '') => {
    appState = { ...appState, isCopilotOpen: true, copilotInitialPrompt: initialPrompt };
    notify();
  },
  closeCopilot: () => {
    appState = { ...appState, isCopilotOpen: false, copilotInitialPrompt: '' };
    notify();
  },
  completeOnboarding: () => {
    storage.save('has_onboarded', true);
    appState = { ...appState, hasCompletedOnboarding: true, activeModal: null, activeTab: 'home' };
    notify();
  },
  showToast: (msg: string) => {
    appState = { ...appState, toastMessage: msg };
    notify();
    setTimeout(() => {
      if (appState.toastMessage === msg) {
        appState = { ...appState, toastMessage: null };
        notify();
      }
    }, 2800);
  },
};

export function useAppStore() {
  const [, setVersion] = useState(0);
  useEffect(() => {
    const update = () => setVersion((v) => v + 1);
    listeners.add(update);
    return () => {
      listeners.delete(update);
    };
  }, []);

  return {
    ...appState,
    setActiveTab: appStore.setActiveTab,
    openModal: appStore.openModal,
    closeModal: appStore.closeModal,
    openCopilot: appStore.openCopilot,
    closeCopilot: appStore.closeCopilot,
    completeOnboarding: appStore.completeOnboarding,
    showToast: appStore.showToast,
  };
}
