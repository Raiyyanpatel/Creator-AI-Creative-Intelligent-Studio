import React, { useState } from 'react';
import { ArrowLeft, Sparkles, Send, Play, Copy, Check } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { llm } from '@/ai/llm';
import { Button } from '@/shared/components/Button';

export const ScriptView: React.FC = () => {
  const { closeModal, openModal, showToast } = useAppStore();
  const { addProject } = useProjectStore();

  const [topic, setTopic] = useState('Can phones run useful AI agents?');
  const [isGenerating, setIsGenerating] = useState(false);
  const [scriptContent, setScriptContent] = useState(
    `# Video Script: Can Phones Run Useful AI Agents?

## Hook (0:00 - 0:04)
Stop believing that AI agents only live inside giant cloud data centers.

## Value (0:05 - 0:18)
Right here on this device, we're running localized Whisper and vision models with zero latency and complete privacy.

## Proof (0:19 - 0:26)
Look at this real-time transcription and automatic edit plan generated in under 300 milliseconds.

## Call to Action (0:27 - 0:30)
Tap create to try it yourself right now.`
  );

  const handleGenerate = async () => {
    setIsGenerating(true);
    const generated = await llm.generate(`Create high retention script for: ${topic}`);
    setScriptContent(generated);
    setIsGenerating(false);
  };

  const handleSendToTeleprompter = () => {
    addProject({
      title: topic,
      description: scriptContent,
    });
    openModal('teleprompter');
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--bg-primary)',
        padding: '16px 18px 24px',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
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
        <span style={{ fontSize: '15px', fontWeight: 700 }}>Script Studio</span>
        <button
          onClick={() => {
            navigator.clipboard.writeText(scriptContent);
            showToast('Script copied to clipboard');
          }}
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: 'var(--bg-surface-2)',
            color: 'var(--text-secondary)',
            display: 'grid',
            placeItems: 'center',
          }}
          title="Copy"
        >
          <Copy size={16} />
        </button>
      </div>

      {/* Idea Prompt Input */}
      <div style={{ marginBottom: '16px' }}>
        <label style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>
          Topic / Core Idea
        </label>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            style={{
              flex: 1,
              backgroundColor: '#111',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '14px',
              padding: '10px 14px',
              color: '#fff',
              fontSize: '13px',
              outline: 'none',
            }}
          />
          <Button
            variant="ai"
            size="sm"
            onClick={handleGenerate}
            disabled={isGenerating}
            style={{ gap: '6px' }}
          >
            <Sparkles size={14} />
            {isGenerating ? 'Writing...' : 'Generate ✦'}
          </Button>
        </div>
      </div>

      {/* Script Editor Canvas */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', marginBottom: '20px' }}>
        <textarea
          value={scriptContent}
          onChange={(e) => setScriptContent(e.target.value)}
          style={{
            flex: 1,
            minHeight: '340px',
            backgroundColor: '#111',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '18px',
            padding: '16px',
            color: '#fff',
            fontSize: '14px',
            lineHeight: 1.6,
            outline: 'none',
            resize: 'none',
            fontFamily: 'monospace',
          }}
        />
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: '10px' }}>
        <Button
          variant="secondary"
          style={{ flex: 1 }}
          onClick={() => openModal('recording')}
        >
          Direct Record
        </Button>
        <Button
          variant="ai"
          style={{ flex: 1, gap: '6px' }}
          onClick={handleSendToTeleprompter}
        >
          <Play size={16} />
          Open Teleprompter
        </Button>
      </div>
    </div>
  );
};
