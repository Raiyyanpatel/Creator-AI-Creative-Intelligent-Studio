import React from 'react';
import { useAppStore } from '@/shared/state/app.store';

export const Toast: React.FC = () => {
  const { toastMessage } = useAppStore();
  if (!toastMessage) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: '24px',
        left: '50%',
        transform: 'translateX(-50%)',
        backgroundColor: '#1b220d',
        color: 'var(--ai-accent)',
        border: '1px solid var(--ai-border)',
        padding: '10px 18px',
        borderRadius: 'var(--radius-pill)',
        fontSize: '13px',
        fontWeight: 600,
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.6)',
        zIndex: 100,
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        animation: 'fadeIn 0.2s ease',
      }}
    >
      <span>✦</span>
      <span>{toastMessage}</span>
    </div>
  );
};
