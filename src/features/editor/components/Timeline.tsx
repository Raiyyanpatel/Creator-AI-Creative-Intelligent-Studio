import React from 'react';
import { useEditorStore } from '../editor.store';
import { formatDuration } from '@/utils/format';

interface TimelineProps {
  duration: number;
}

export const Timeline: React.FC<TimelineProps> = ({ duration }) => {
  const { currentTime, setCurrentTime } = useEditorStore();

  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    setCurrentTime(Math.round(pos * duration));
  };

  const playheadPercent = Math.min(100, Math.max(0, (currentTime / (duration || 42)) * 100));

  return (
    <div style={{ margin: '14px 0' }}>
      {/* Timecode row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-muted)', marginBottom: '6px' }}>
        <span>{formatDuration(currentTime)}</span>
        <span>{formatDuration(duration)}</span>
      </div>

      {/* Interactive Timeline Container */}
      <div
        onClick={handleSeek}
        style={{
          position: 'relative',
          padding: '4px 0',
          cursor: 'pointer',
        }}
      >
        {/* Playhead Indicator Line */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            bottom: 0,
            left: `${playheadPercent}%`,
            width: '2px',
            backgroundColor: 'var(--ai-accent)',
            boxShadow: '0 0 8px var(--ai-accent)',
            zIndex: 10,
            pointerEvents: 'none',
            transform: 'translateX(-50%)',
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: '-4px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              backgroundColor: 'var(--ai-accent)',
            }}
          />
        </div>

        {/* Video Track Strip */}
        <div
          style={{
            height: '46px',
            borderRadius: '10px',
            backgroundColor: '#191919',
            marginBottom: '6px',
            overflow: 'hidden',
            display: 'flex',
            position: 'relative',
            border: '1px solid rgba(255, 255, 255, 0.06)',
          }}
        >
          <div
            style={{
              width: '55%',
              height: '100%',
              background: 'repeating-linear-gradient(90deg, #25382e 0px, #25382e 32px, #334e40 32px, #334e40 64px)',
              borderRight: '2px solid rgba(255, 255, 255, 0.2)',
              display: 'flex',
              alignItems: 'center',
              paddingLeft: '10px',
              fontSize: '11px',
              fontWeight: 600,
              color: 'rgba(255, 255, 255, 0.8)',
            }}
          >
            Hook & Intro (A-Roll)
          </div>
          <div
            style={{
              width: '45%',
              height: '100%',
              background: 'repeating-linear-gradient(90deg, #1c2e3d 0px, #1c2e3d 32px, #264157 32px, #264157 64px)',
              display: 'flex',
              alignItems: 'center',
              paddingLeft: '10px',
              fontSize: '11px',
              fontWeight: 600,
              color: 'rgba(255, 255, 255, 0.8)',
            }}
          >
            NPU Benchmark Demo
          </div>
        </div>

        {/* Audio Track Strip */}
        <div
          style={{
            height: '34px',
            borderRadius: '10px',
            backgroundColor: '#161616',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            padding: '0 8px',
            border: '1px solid rgba(255, 255, 255, 0.04)',
          }}
        >
          <div
            style={{
              width: '100%',
              height: '18px',
              background:
                'repeating-linear-gradient(90deg, #9e7d2a 0px, #9e7d2a 4px, transparent 4px, transparent 8px)',
              borderRadius: '4px',
              opacity: 0.85,
            }}
          />
        </div>
      </div>
    </div>
  );
};
