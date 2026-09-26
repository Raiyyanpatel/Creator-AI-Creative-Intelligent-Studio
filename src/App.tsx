import React from 'react';
import { useAppStore } from '@/shared/state/app.store';
import { AppShell } from '@/shared/components/AppShell';
import { HomeView } from '@/features/home/HomeView';
import { InsightsView } from '@/features/insights/InsightsView';
import { CreateView } from '@/features/create/CreateView';
import { ProfileView } from '@/features/profile/ProfileView';
import { OnboardingFlow } from '@/features/onboarding/OnboardingFlow';
import { EditorPage } from '@/features/editor/page';
import { RecordingView } from '@/features/recording/RecordingView';
import { TeleprompterView } from '@/features/teleprompter/TeleprompterView';
import { ScriptView } from '@/features/script/ScriptView';
import { GameStudioView } from '@/features/game-studio/GameStudioView';
import { EffectsStudioView } from '@/features/effects/EffectsStudioView';
import { AssetsView } from '@/features/assets/AssetsView';
import { ExportModal } from '@/features/export/ExportModal';
import { CopilotSheet } from '@/features/copilot/CopilotSheet';

export const App: React.FC = () => {
  const { activeTab, activeModal } = useAppStore();

  // Render modal views if open
  if (activeModal === 'onboarding') {
    return <OnboardingFlow />;
  }
  if (activeModal === 'editor') {
    return (
      <>
        <EditorPage />
        <CopilotSheet />
      </>
    );
  }
  if (activeModal === 'recording') {
    return <RecordingView />;
  }
  if (activeModal === 'teleprompter') {
    return <TeleprompterView />;
  }
  if (activeModal === 'script') {
    return <ScriptView />;
  }
  if (activeModal === 'game-studio') {
    return <GameStudioView />;
  }
  if (activeModal === 'effects') {
    return <EffectsStudioView />;
  }
  if (activeModal === 'assets') {
    return <AssetsView />;
  }

  return (
    <AppShell>
      {activeTab === 'home' && <HomeView />}
      {activeTab === 'insights' && <InsightsView />}
      {activeTab === 'create' && <CreateView />}
      {activeTab === 'profile' && <ProfileView />}

      {/* Overlays */}
      {activeModal === 'export' && <ExportModal />}
      <CopilotSheet />
    </AppShell>
  );
};

export default App;
