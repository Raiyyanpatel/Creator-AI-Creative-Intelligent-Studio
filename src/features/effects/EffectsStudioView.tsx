import React, { useState } from 'react';
import { ArrowLeft, Wand2, Sparkles, Check } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { Button } from '@/shared/components/Button';
import { Card } from '@/shared/components/Card';
import { Chip } from '@/shared/components/Chip';

export const EffectsStudioView: React.FC = () => {
  const { closeModal, showToast } = useAppStore();
  const [selectedEffect, setSelectedEffect] = useState('cinematic_dark');

  const effects = [
    { id: 'cinematic_dark', name: 'Cyber Cinematic Dark', type: 'Color Grade', desc: 'Crushed blacks, high micro-contrast, vibrant lime highlights.' },
    { id: 'smooth_studio', name: 'Studio Key Light', type: 'Lighting', desc: 'Softens facial shadows with simulated 3-point diffused lighting.' },
    { id: 'vintage_kodak', name: 'Kodak 250D', type: 'Film Emulation', desc: 'Analog organic 16mm grain and warm highlight rolloff.' },
    { id: 'auto_zoom', name: 'Dynamic Punch-In', type: 'Camera Motion', desc: 'Automated 1.15x zooms on key vocal emphasis words.' },
  ];

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
      {/* Top Navbar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
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
        <span style={{ fontSize: '15px', fontWeight: 700 }}>Effects Studio</span>
        <Chip label="GPU Shaders" variant="ai" />
      </div>

      {/* Showcase Visual */}
      <div
        className="media-bg"
        style={{
          height: '200px',
          borderRadius: '24px',
          backgroundImage: `url('/assets/effects-showcase.jpg')`,
          padding: '18px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-end',
          position: 'relative',
          overflow: 'hidden',
          marginBottom: '20px',
          border: '1px solid rgba(255, 255, 255, 0.08)',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.85) 100%)',
          }}
        />
        <div style={{ position: 'relative', zIndex: 2 }}>
          <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#fff', margin: '0 0 4px' }}>
            Cinematic Effects Presets
          </h2>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0 }}>
            Color grading LUTs and AI camera motions designed for high social retention.
          </p>
        </div>
      </div>

      {/* Preset List */}
      <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '10px' }}>Available Presets</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
        {effects.map((fx) => {
          const isSelected = selectedEffect === fx.id;
          return (
            <Card
              key={fx.id}
              variant={isSelected ? 'ai' : 'surface'}
              padding="16px"
              onClick={() => setSelectedEffect(fx.id)}
              style={{ cursor: 'pointer' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                <strong style={{ fontSize: '14px', color: isSelected ? 'var(--ai-accent)' : '#fff' }}>
                  {fx.name}
                </strong>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{fx.type}</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0 }}>
                {fx.desc}
              </p>
            </Card>
          );
        })}
      </div>

      {/* Action */}
      <div style={{ marginTop: 'auto' }}>
        <Button
          variant="ai"
          size="lg"
          fullWidth
          onClick={() => {
            showToast(`Preset "${effects.find((e) => e.id === selectedEffect)?.name}" applied`);
            closeModal();
          }}
          style={{ gap: '8px' }}
        >
          <Sparkles size={18} />
          Apply Effect to Active Project ✦
        </Button>
      </div>
    </div>
  );
};
