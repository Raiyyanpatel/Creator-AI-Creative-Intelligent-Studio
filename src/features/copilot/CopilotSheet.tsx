import React, { useState, useEffect } from 'react';
import { X, Sparkles, Check, ArrowRight, Play, CheckCircle } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { useCreatorStore } from '@/shared/state/creator.store';
import { llm } from '@/ai/llm';
import { CopilotEditPlan } from '@/shared/types/project';
import { Button } from '@/shared/components/Button';

export const CopilotSheet: React.FC = () => {
  const { isCopilotOpen, closeCopilot, copilotInitialPrompt, showToast, openModal } = useAppStore();
  const { activeProject, updateActiveProject } = useProjectStore();
  const { creator } = useCreatorStore();

  const [prompt, setPrompt] = useState(copilotInitialPrompt || '');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [plan, setPlan] = useState<CopilotEditPlan | null>(null);
  const [previewActive, setPreviewActive] = useState(false);

  useEffect(() => {
    if (copilotInitialPrompt) {
      setPrompt(copilotInitialPrompt);
    }
  }, [copilotInitialPrompt]);

  if (!isCopilotOpen) return null;

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setIsAnalyzing(true);
    setPlan(null);
    setPreviewActive(false);

    try {
      const generatedPlan = await llm.generateEditPlan(prompt, {
        creatorDNA: creator.dna,
        context: activeProject?.title,
      });
      setPlan(generatedPlan);
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleApply = () => {
    if (!plan) return;
    updateActiveProject({
      aspectRatio: plan.targetAspectRatio,
      durationSeconds: plan.estimatedDuration,
      status: 'ready',
    });
    showToast('AI Edit Plan applied to timeline');
    closeCopilot();
    openModal('editor');
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.72)',
        backdropFilter: 'blur(10px)',
        WebkitBackdropFilter: 'blur(10px)',
        zIndex: 100,
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'center',
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) closeCopilot();
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '480px',
          maxHeight: '85vh',
          overflowY: 'auto',
          backgroundColor: '#141414',
          borderTopLeftRadius: '28px',
          borderTopRightRadius: '28px',
          padding: '24px 20px 32px',
          boxShadow: '0 -20px 60px rgba(0, 0, 0, 0.9)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderBottom: 'none',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: 'var(--ai-soft)',
                color: 'var(--ai-accent)',
                display: 'grid',
                placeItems: 'center',
              }}
            >
              <Sparkles size={18} />
            </div>
            <div>
              <h3 style={{ fontSize: '17px', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                Creator AI Copilot
              </h3>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', margin: 0 }}>
                Context: {activeProject?.title || 'Active Project'} · DNA Tuned
              </p>
            </div>
          </div>
          <button
            onClick={closeCopilot}
            style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              backgroundColor: 'var(--bg-surface-3)',
              color: 'var(--text-secondary)',
              display: 'grid',
              placeItems: 'center',
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Quick Suggestion Chips */}
        <div style={{ display: 'flex', gap: '6px', overflowX: 'auto', paddingBottom: '12px', marginBottom: '8px' }}>
          {[
            'Make this a 30s Reel',
            'Remove silence & fillers',
            'Smart 9:16 reframe',
            'Extract top 3 hooks',
          ].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => {
                setPrompt(suggestion);
              }}
              style={{
                whiteSpace: 'nowrap',
                padding: '6px 12px',
                borderRadius: 'var(--radius-pill)',
                backgroundColor: 'var(--bg-surface-2)',
                color: 'var(--text-secondary)',
                fontSize: '11px',
                border: '1px solid rgba(255, 255, 255, 0.06)',
              }}
            >
              ✦ {suggestion}
            </button>
          ))}
        </div>

        {/* Input Area */}
        <div style={{ position: 'relative', marginBottom: '14px' }}>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Tell Copilot what to cut, reframe, or generate..."
            rows={3}
            style={{
              width: '100%',
              backgroundColor: '#0c0c0c',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              borderRadius: '16px',
              padding: '12px 14px',
              color: '#fff',
              fontSize: '14px',
              outline: 'none',
              resize: 'none',
              boxSizing: 'border-box',
            }}
          />
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '8px' }}>
            <Button
              variant="ai"
              size="sm"
              onClick={handleGenerate}
              disabled={isAnalyzing || !prompt.trim()}
              style={{ gap: '6px' }}
            >
              <Sparkles size={14} />
              {isAnalyzing ? 'Analyzing Footage...' : 'Generate Plan ✦'}
            </Button>
          </div>
        </div>

        {/* Analysis Progress */}
        {isAnalyzing && (
          <div
            style={{
              backgroundColor: 'var(--bg-surface-2)',
              borderRadius: '16px',
              padding: '16px',
              border: '1px solid var(--ai-border)',
              margin: '16px 0',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <span style={{ color: 'var(--ai-accent)', fontSize: '13px', fontWeight: 600 }}>
                Running local Whisper + YOLO inference...
              </span>
            </div>
            <div
              style={{
                height: '5px',
                width: '100%',
                backgroundColor: '#252525',
                borderRadius: 'var(--radius-pill)',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  height: '100%',
                  width: '68%',
                  backgroundColor: 'var(--ai-accent)',
                  borderRadius: 'var(--radius-pill)',
                  animation: 'pulse 1.2s infinite',
                }}
              />
            </div>
          </div>
        )}

        {/* Resulting Proposal */}
        {plan && (
          <div
            style={{
              backgroundColor: '#1b1d14',
              border: '1px solid var(--ai-border)',
              borderRadius: '20px',
              padding: '18px',
              marginTop: '12px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <CheckCircle size={18} color="var(--ai-accent)" />
              <strong style={{ fontSize: '14px', color: 'var(--text-primary)' }}>
                Proposed Social Reel Edit Plan
              </strong>
            </div>

            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
              {plan.summary}
            </p>

            {/* Steps checklist */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '18px' }}>
              {plan.steps.map((step) => (
                <div
                  key={step.id}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '10px',
                    fontSize: '12px',
                    color: '#e0e0e0',
                  }}
                >
                  <span
                    style={{
                      width: '18px',
                      height: '18px',
                      borderRadius: '50%',
                      backgroundColor: 'rgba(216, 255, 0, 0.2)',
                      color: 'var(--ai-accent)',
                      display: 'grid',
                      placeItems: 'center',
                      fontSize: '10px',
                      marginTop: '2px',
                      flexShrink: 0,
                    }}
                  >
                    ✓
                  </span>
                  <div>
                    <strong style={{ color: '#fff' }}>{step.action}: </strong>
                    <span style={{ color: 'var(--text-secondary)' }}>{step.description}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Target Specs */}
            <div
              style={{
                display: 'flex',
                gap: '10px',
                padding: '10px 14px',
                backgroundColor: 'rgba(0, 0, 0, 0.4)',
                borderRadius: '12px',
                fontSize: '12px',
                color: 'var(--text-muted)',
                marginBottom: '16px',
              }}
            >
              <span>Target: <strong>{plan.targetAspectRatio}</strong></span>
              <span>•</span>
              <span>Estimated: <strong>{plan.estimatedDuration}s</strong></span>
              <span>•</span>
              <span>DNA Match: <strong>98%</strong></span>
            </div>

            {/* Actions: Preview & Apply */}
            <div style={{ display: 'flex', gap: '10px' }}>
              <Button
                variant={previewActive ? 'secondary' : 'glass'}
                style={{ flex: 1, gap: '6px' }}
                onClick={() => setPreviewActive(!previewActive)}
              >
                <Play size={15} />
                {previewActive ? 'Playing Preview' : 'Preview Edit'}
              </Button>
              <Button
                variant="ai"
                style={{ flex: 1, gap: '6px' }}
                onClick={handleApply}
              >
                <Check size={16} />
                Apply to Timeline
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
