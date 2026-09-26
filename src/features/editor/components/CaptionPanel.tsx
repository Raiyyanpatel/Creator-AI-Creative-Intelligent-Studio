import React, { useState } from 'react';
import { useEditorStore } from '../editor.store';
import { whisper } from '@/ai/whisper';
import { Sparkles, Check, Type } from 'lucide-react';
import { Button } from '@/shared/components/Button';

export const CaptionPanel: React.FC = () => {
  const { hasCaptions, toggleCaptions } = useEditorStore();
  const [selectedStyle, setSelectedStyle] = useState<'kinetic' | 'karaoke' | 'minimal'>('kinetic');
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [captionText, setCaptionText] = useState('Building autonomous AI agents directly on phones');

  const handleTranscribe = async () => {
    setIsTranscribing(true);
    const result = await whisper.transcribe('mock_audio');
    setCaptionText(result.fullText);
    setIsTranscribing(false);
  };

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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Type size={16} color="var(--ai-accent)" />
          <strong style={{ fontSize: '14px' }}>AI Kinetic Captions</strong>
        </div>
        <Button variant="glass" size="sm" onClick={handleTranscribe} disabled={isTranscribing} style={{ gap: '4px' }}>
          <Sparkles size={13} color="var(--ai-accent)" />
          {isTranscribing ? 'Whisper...' : 'Auto-Transcribe'}
        </Button>
      </div>

      <div
        style={{
          backgroundColor: '#0c0c0c',
          borderRadius: '12px',
          padding: '10px 14px',
          fontSize: '13px',
          color: 'var(--text-primary)',
          marginBottom: '12px',
          border: '1px solid rgba(255, 255, 255, 0.06)',
        }}
      >
        "{captionText}"
      </div>

      {/* Style Presets */}
      <div style={{ display: 'flex', gap: '8px' }}>
        {(['kinetic', 'karaoke', 'minimal'] as const).map((style) => (
          <button
            key={style}
            onClick={() => setSelectedStyle(style)}
            style={{
              flex: 1,
              padding: '8px 4px',
              borderRadius: '12px',
              backgroundColor: selectedStyle === style ? 'var(--ai-soft)' : 'var(--bg-surface-3)',
              color: selectedStyle === style ? 'var(--ai-accent)' : 'var(--text-secondary)',
              fontSize: '11px',
              fontWeight: 600,
              textTransform: 'capitalize',
              border: selectedStyle === style ? '1px solid var(--ai-border)' : '1px solid transparent',
            }}
          >
            {style}
          </button>
        ))}
      </div>
    </div>
  );
};
