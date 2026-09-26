import React from 'react';
import { BottomNav } from './BottomNav';
import { Toast } from './Toast';
import { useAppStore } from '@/shared/state/app.store';

interface AppShellProps {
  children: React.ReactNode;
  hideNav?: boolean;
}

export const AppShell: React.FC<AppShellProps> = ({ children, hideNav = false }) => {
  const { activeModal } = useAppStore();
  const showNav = !hideNav && !activeModal;

  return (
    <div className="app-viewport">
      <Toast />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>{children}</div>
      {showNav && <BottomNav />}
    </div>
  );
};
