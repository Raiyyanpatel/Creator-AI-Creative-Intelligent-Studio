import React from 'react';
import { Home, Compass, Plus, User } from 'lucide-react';
import { MainTab, useAppStore } from '@/shared/state/app.store';

export const BottomNav: React.FC = () => {
  const { activeTab, setActiveTab } = useAppStore();

  const navItems: { tab: MainTab; label: string; icon: React.ReactNode; isAI?: boolean }[] = [
    { tab: 'home', label: 'Home', icon: <Home size={20} /> },
    { tab: 'insights', label: 'Insights', icon: <Compass size={20} /> },
    { tab: 'create', label: 'Create', icon: <Plus size={22} />, isAI: true },
    { tab: 'profile', label: 'Profile', icon: <User size={20} /> },
  ];

  return (
    <nav
      style={{
        position: 'fixed',
        bottom: '16px',
        left: '50%',
        transform: 'translateX(-50%)',
        width: 'min(calc(100% - 28px), 440px)',
        padding: '6px 8px',
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '6px',
        borderRadius: 'var(--radius-xl)',
        backgroundColor: 'rgba(20, 20, 20, 0.88)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        border: '1px solid rgba(255, 255, 255, 0.09)',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.7)',
        zIndex: 50,
      }}
    >
      {navItems.map((item) => {
        const isActive = activeTab === item.tab;
        return (
          <button
            key={item.tab}
            onClick={() => setActiveTab(item.tab)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '4px',
              padding: '8px 4px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: isActive ? '#242424' : 'transparent',
              color: item.isAI
                ? 'var(--ai-accent)'
                : isActive
                ? 'var(--text-primary)'
                : 'var(--text-muted)',
              fontSize: '11px',
              fontWeight: isActive ? 600 : 500,
              transition: 'all 0.18s ease',
            }}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
};
