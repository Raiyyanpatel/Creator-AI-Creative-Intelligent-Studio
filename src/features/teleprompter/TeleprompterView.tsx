import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Play, Pause, RotateCcw, Video, Sliders } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { Button } from '@/shared/components/Button';

export const TeleprompterView: React.FC = () => {
  const { closeModal, openModal } = useAppStore();
  const { activeProject } = useProjectStore();

  const [isScrolling, setIsScrolling] = useState(false);
  const [scrollSpeed, setScrollSpeed] = useState(2);
  const [fontSize, setFontSize] = useState(22);
  const scrollRef = useRef<HTMLDivElement>(null);

  const scriptText =
    activeProject?.description ||
    `Stop believing that AI agents only live inside giant cloud data centers.

Right here on this device, we're running localized Whisper and vision models with zero latency and complete privacy.

Look at this real-time transcription and automatic edit plan generated in under 300 milliseconds.

Tap create to try it yourself right now.`;

  useEffect(() => {
    let animId: number;
    const scrollStep = () => {
      if (isScrolling && scrollRef.current) {
        scrollRef.current.scrollTop += scrollSpeed * 0.7;
      }
      animId = requestAnimationFrame(scrollStep);
    };
    animId = requestAnimationFrame(scrollStep);
    return () => cancelAnimationFrame(animId);
  }, [isScrolling, scrollSpeed]);

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#050505',
        display: 'flex',
        flexDirection: 'column',
        padding: '16px 18px 24px',
      }}
    >
      {/* Top Navbar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <button
          onClick={closeModal}
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: 'var(--bg-surface-2)',
            color: 'var(--text-secondary)',
            display: 'grid',
            placeItems: 'center',
          }}
        >
          <ArrowLeft size={18} />
        </button>

        <span style={{ fontSize: '15px', fontWeight: 700 }}>AI Teleprompter</span>

        <button
          onClick={() => openModal('recording')}
          style={{
            padding: '6px 12px',
            borderRadius: 'var(--radius-pill)',
            backgroundColor: 'var(--danger)',
            color: '#fff',
            fontSize: '11px',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
          }}
        >
          <Video size={13} />
          Record
        </button>
      </div>

      {/* Speed & Controls Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          backgroundColor: 'var(--bg-surface-2)',
          padding: '10px 16px',
          borderRadius: '16px',
          marginBottom: '14px',
          border: '1px solid rgba(255, 255, 255, 0.08)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Speed:</span>
          {[1, 2, 3, 4].map((s) => (
            <button
              key={s}
              onClick={() => setScrollSpeed(s)}
              style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                backgroundColor: scrollSpeed === s ? 'var(--ai-accent)' : 'var(--bg-surface-3)',
                color: scrollSpeed === s ? '#080808' : '#fff',
                fontSize: '11px',
                fontWeight: 700,
              }}
            >
              {s}x
            </button>
          ))}
        </div>

        <button
          onClick={() => {
            if (scrollRef.current) scrollRef.current.scrollTop = 0;
          }}
          style={{
            color: 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            fontSize: '11px',
          }}
        >
          <RotateCcw size={13} /> Reset
        </button>
      </div>

      {/* Teleprompter Scroll View */}
      <div
        ref={scrollRef}
        style={{
          flex: 1,
          backgroundColor: '#0a0a0a',
          borderRadius: '24px',
          padding: '40px 24px',
          overflowY: 'auto',
          border: '1px solid rgba(255, 255, 255, 0.06)',
          position: 'relative',
        }}
      >
        {/* Eye-level Focus Marker */}
        <div
          style={{
            position: 'sticky',
            top: '40px',
            left: 0,
            right: 0,
            height: '2px',
            backgroundColor: 'rgba(216, 255, 0, 0.35)',
            boxShadow: '0 0 10px rgba(216, 255, 0, 0.5)',
            pointerEvents: 'none',
            marginBottom: '10px',
          }}
        />

        <div
          style={{
            fontSize: `${fontSize}px`,
            lineHeight: 1.7,
            color: '#F7F7F2',
            fontWeight: 600,
            textAlign: 'center',
            whiteSpace: 'pre-line',
            paddingBottom: '200px',
          }}
        >
          {scriptText}
        </div>
      </div>

      {/* Floating Play/Pause Controls */}
      <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'center' }}>
        <Button
          variant="ai"
          size="lg"
          onClick={() => setIsScrolling(!isScrolling)}
          style={{ width: '220px', gap: '8px' }}
        >
          {isScrolling ? <Pause size={20} /> : <Play size={20} />}
          {isScrolling ? 'Pause Scroll' : 'Start Scroll'}
        </Button>
      </div>
    </div>
  );
};
