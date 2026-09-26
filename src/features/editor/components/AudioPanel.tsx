import React from 'react';
import { useEditorStore } from '../editor.store';
import { Volume2, Mic, Music, Sparkles } from 'lucide-react';

export const AudioPanel: React.FC = () => {
  const { audioNoiseReduction, toggleNoiseReduction } = useEditorStore();

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
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
        <Volume2 size={16} color="var(--ai-accent)" />
        <strong style={{ fontSize: '14px' }}>Audio Cleanup & Levels</strong>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div
          onClick={toggleNoiseReduction}
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            backgroundColor: '#0c0c0c',
            borderRadius: '14px',
            padding: '12px 14px',
            cursor: 'pointer',
            border: audioNoiseReduction ? '1px solid var(--ai-border)' : '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Sparkles size={16} color={audioNoiseReduction ? 'var(--ai-accent)' : 'var(--text-muted)'} />
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600 }}>AI Voice Isolation</div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Remove background room hum & aircon noise</div>
            </div>
          </div>
          <span
            style={{
              fontSize: '11px',
              fontWeight: 700,
              color: audioNoiseReduction ? 'var(--ai-accent)' : 'var(--text-muted)',
            }}
          >
            {audioNoiseReduction ? 'ACTIVE' : 'OFF'}
          </span>
        </div>

        {/* Volume Level Sliders */}
        <div style={{ backgroundColor: '#0c0c0c', borderRadius: '14px', padding: '12px 14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Vocal Boost</span>
            <span style={{ color: 'var(--ai-accent)', fontWeight: 600 }}>+3.5 dB</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            defaultValue="80"
            style={{ width: '100%', accentColor: 'var(--ai-accent)' }}
          />
        </div>
      </div>
    </div>
  );
};
