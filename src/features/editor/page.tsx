import React, { useState, useEffect } from 'react';
import { ArrowLeft, Play, Pause, Scissors, Volume2, Type, Crop, Sparkles, Check, Flame, Share2 } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { useEditorStore } from './editor.store';
import { Timeline } from './components/Timeline';
import { CaptionPanel } from './components/CaptionPanel';
import { AudioPanel } from './components/AudioPanel';
import { ReframePanel } from './components/ReframePanel';
import { HighlightPanel } from './components/HighlightPanel';
import { Button } from '@/shared/components/Button';
import { formatDuration } from '@/utils/format';

export const EditorPage: React.FC = () => {
  const { closeModal, openCopilot, openModal, showToast } = useAppStore();
  const { activeProject } = useProjectStore();
  const {
    currentTime,
    setCurrentTime,
    isPlaying,
    togglePlay,
    activePanel,
    setActivePanel,
    aspectRatio,
    hasCaptions,
  } = useEditorStore();

  const duration = activeProject?.durationSeconds || 42;

  // Playback timer simulation
  useEffect(() => {
    let interval: any;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= duration) {
            return 0;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, duration, setCurrentTime]);

  const previewMedia = activeProject?.thumbnailUrl || '/assets/create-edit-video.jpg';

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--bg-primary)',
        display: 'flex',
        flexDirection: 'column',
        padding: '14px 16px 28px',
      }}
    >
      {/* Top Navbar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '14px',
        }}
      >
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

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--text-primary)' }}>
            {activeProject?.title || 'Video Project'}
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            {aspectRatio} · {formatDuration(duration)}
          </div>
        </div>

        <button
          onClick={() => openModal('export')}
          style={{
            padding: '6px 14px',
            borderRadius: 'var(--radius-pill)',
            backgroundColor: 'var(--ai-accent)',
            color: '#080808',
            fontSize: '12px',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
          }}
        >
          Export <Share2 size={13} />
        </button>
      </div>

      {/* Video Preview Canvas */}
      <div
        className="media-bg"
        style={{
          height: aspectRatio === '9:16' ? '390px' : aspectRatio === '1:1' ? '320px' : '220px',
          borderRadius: '24px',
          overflow: 'hidden',
          backgroundImage: `url(${previewMedia})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          boxShadow: 'var(--shadow-card)',
          transition: 'height 0.25s ease',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.4) 100%)',
          }}
        />

        {/* Dynamic Caption Overlay */}
        {hasCaptions && (
          <div
            style={{
              position: 'absolute',
              bottom: '24px',
              left: '20px',
              right: '20px',
              textAlign: 'center',
              backgroundColor: 'rgba(0, 0, 0, 0.72)',
              backdropFilter: 'blur(8px)',
              padding: '8px 14px',
              borderRadius: '12px',
              fontSize: '13px',
              fontWeight: 700,
              color: 'var(--ai-accent)',
              border: '1px solid var(--ai-border)',
              zIndex: 3,
            }}
          >
            ✦ Building autonomous AI agents directly on phones
          </div>
        )}

        {/* Play/Pause Button */}
        <button
          onClick={togglePlay}
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            backgroundColor: 'rgba(255, 255, 255, 0.92)',
            color: '#080808',
            display: 'grid',
            placeItems: 'center',
            position: 'relative',
            zIndex: 4,
            boxShadow: '0 6px 20px rgba(0, 0, 0, 0.5)',
          }}
        >
          {isPlaying ? <Pause size={24} /> : <Play size={24} style={{ marginLeft: '3px' }} />}
        </button>

        {/* Time overlay indicator */}
        <div
          style={{
            position: 'absolute',
            top: '12px',
            left: '12px',
            padding: '4px 8px',
            borderRadius: 'var(--radius-pill)',
            backgroundColor: 'rgba(0, 0, 0, 0.6)',
            backdropFilter: 'blur(6px)',
            fontSize: '11px',
            color: '#fff',
            fontWeight: 600,
          }}
        >
          {formatDuration(currentTime)} / {formatDuration(duration)}
        </div>
      </div>

      {/* Timeline Component */}
      <Timeline duration={duration} />

      {/* Editing Tool Row */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: '6px',
          margin: '10px 0 16px',
        }}
      >
        <button
          onClick={() => setActivePanel(activePanel === 'cut' ? null : 'cut')}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            padding: '10px 4px',
            borderRadius: '14px',
            backgroundColor: activePanel === 'cut' ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
            color: activePanel === 'cut' ? 'var(--ai-accent)' : 'var(--text-secondary)',
            fontSize: '11px',
            border: activePanel === 'cut' ? '1px solid var(--ai-border)' : '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <Scissors size={17} />
          <span>Cut</span>
        </button>

        <button
          onClick={() => setActivePanel(activePanel === 'audio' ? null : 'audio')}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            padding: '10px 4px',
            borderRadius: '14px',
            backgroundColor: activePanel === 'audio' ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
            color: activePanel === 'audio' ? 'var(--ai-accent)' : 'var(--text-secondary)',
            fontSize: '11px',
            border: activePanel === 'audio' ? '1px solid var(--ai-border)' : '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <Volume2 size={17} />
          <span>Audio</span>
        </button>

        <button
          onClick={() => setActivePanel(activePanel === 'captions' ? null : 'captions')}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            padding: '10px 4px',
            borderRadius: '14px',
            backgroundColor: activePanel === 'captions' ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
            color: activePanel === 'captions' ? 'var(--ai-accent)' : 'var(--text-secondary)',
            fontSize: '11px',
            border: activePanel === 'captions' ? '1px solid var(--ai-border)' : '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <Type size={17} />
          <span>Text</span>
        </button>

        <button
          onClick={() => setActivePanel(activePanel === 'reframe' ? null : 'reframe')}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            padding: '10px 4px',
            borderRadius: '14px',
            backgroundColor: activePanel === 'reframe' ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
            color: activePanel === 'reframe' ? 'var(--ai-accent)' : 'var(--text-secondary)',
            fontSize: '11px',
            border: activePanel === 'reframe' ? '1px solid var(--ai-border)' : '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <Crop size={17} />
          <span>Crop</span>
        </button>

        <button
          onClick={() => setActivePanel(activePanel === 'highlights' ? null : 'highlights')}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            padding: '10px 4px',
            borderRadius: '14px',
            backgroundColor: activePanel === 'highlights' ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
            color: activePanel === 'highlights' ? 'var(--ai-accent)' : 'var(--text-secondary)',
            fontSize: '11px',
            border: activePanel === 'highlights' ? '1px solid var(--ai-border)' : '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <Flame size={17} />
          <span>Highlights</span>
        </button>
      </div>

      {/* Subpanels */}
      {activePanel === 'captions' && <CaptionPanel />}
      {activePanel === 'audio' && <AudioPanel />}
      {activePanel === 'reframe' && <ReframePanel />}
      {activePanel === 'highlights' && <HighlightPanel />}
      {activePanel === 'cut' && (
        <div style={{ backgroundColor: 'var(--bg-surface-2)', borderRadius: '18px', padding: '16px', marginTop: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '13px', fontWeight: 600 }}>Split clip at {formatDuration(currentTime)}?</span>
            <Button
              variant="ai"
              size="sm"
              onClick={() => {
                showToast(`Clip split at ${formatDuration(currentTime)}`);
                setActivePanel(null);
              }}
            >
              Split
            </Button>
          </div>
        </div>
      )}

      {/* Contextual Copilot Action Bar */}
      <div
        style={{
          marginTop: 'auto',
          backgroundColor: '#15190c',
          border: '1px solid var(--ai-border)',
          borderRadius: '22px',
          padding: '16px',
          boxShadow: 'var(--shadow-card)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--ai-accent)', fontWeight: 700, fontSize: '14px' }}>
            <Sparkles size={16} />
            Ask Copilot
          </div>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Project-aware AI</span>
        </div>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: '0 0 12px', lineHeight: 1.4 }}>
          "Make this a 30s Reel", "Remove filler words", or "Add auto-zooms to highlights".
        </p>
        <Button
          variant="ai"
          fullWidth
          onClick={() => openCopilot('Make this a 30 second Instagram reel')}
          style={{ gap: '6px' }}
        >
          <Sparkles size={15} />
          Open Copilot Assistant ✦
        </Button>
      </div>
    </div>
  );
};
