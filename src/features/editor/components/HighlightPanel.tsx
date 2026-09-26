import React from 'react';
import { Sparkles, Flame, Check } from 'lucide-react';
import { useEditorStore } from '../editor.store';
import { Button } from '@/shared/components/Button';

export const HighlightPanel: React.FC = () => {
  const { setCurrentTime } = useEditorStore();

  const highlights = [
    { id: 'h1', title: 'Strong Opening Hook', time: 0, score: 94, reason: 'High vocal energy + contrarian question' },
    { id: 'h2', title: 'On-Device Benchmark Proof', time: 22, score: 91, reason: 'Live interaction and reaction face' },
    { id: 'h3', title: 'Final CTA / Conclusion', time: 36, score: 86, reason: 'Direct audience engagement' },
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
        <Flame size={16} color="var(--warning)" />
        <strong style={{ fontSize: '14px' }}>AI Viral Highlights</strong>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {highlights.map((h) => (
          <div
            key={h.id}
            onClick={() => setCurrentTime(h.time)}
            style={{
              padding: '12px 14px',
              borderRadius: '12px',
              backgroundColor: '#0c0c0c',
              border: '1px solid rgba(255, 255, 255, 0.06)',
              cursor: 'pointer',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: '#fff' }}>{h.title}</div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{h.reason}</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '11px', color: 'var(--ai-accent)', fontWeight: 700 }}>
                {h.score}% Virality
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
