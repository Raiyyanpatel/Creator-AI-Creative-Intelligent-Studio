import React from 'react';
import { useEditorStore } from '../editor.store';
import { Crop, Smartphone, Monitor, Square, Sparkles } from 'lucide-react';

export const ReframePanel: React.FC = () => {
  const { aspectRatio, setAspectRatio } = useEditorStore();

  const ratios: { id: '9:16' | '16:9' | '1:1'; label: string; icon: React.ReactNode }[] = [
    { id: '9:16', label: 'Reels / Shorts (9:16)', icon: <Smartphone size={16} /> },
    { id: '16:9', label: 'YouTube (16:9)', icon: <Monitor size={16} /> },
    { id: '1:1', label: 'Square (1:1)', icon: <Square size={16} /> },
  ];

  return (
    <div
      style={{
        backgroundColor: 'var(--bg-surface-2)',
        borderRadius: '18px',
        padding: '16px',
        marginTop: '12px',
        border: '1px solid rgba(255, 255, 255, 0.08)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
        <Crop size={16} color="var(--ai-accent)" />
        <strong style={{ fontSize: '14px' }}>Smart Reframe (YOLO Subject Tracking)</strong>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {ratios.map((r) => {
          const isSelected = aspectRatio === r.id;
          return (
            <div
              key={r.id}
              onClick={() => setAspectRatio(r.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 14px',
                borderRadius: '12px',
                backgroundColor: isSelected ? 'var(--ai-soft)' : '#0c0c0c',
                border: isSelected ? '1px solid var(--ai-border)' : '1px solid rgba(255, 255, 255, 0.06)',
                cursor: 'pointer',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ color: isSelected ? 'var(--ai-accent)' : 'var(--text-secondary)' }}>
                  {r.icon}
                </span>
                <span style={{ fontSize: '13px', fontWeight: isSelected ? 600 : 400, color: isSelected ? 'var(--ai-accent)' : '#fff' }}>
                  {r.label}
                </span>
              </div>
              {isSelected && <span style={{ fontSize: '11px', color: 'var(--ai-accent)', fontWeight: 700 }}>ACTIVE</span>}
            </div>
          );
        })}
      </div>
    </div>
  );
};
