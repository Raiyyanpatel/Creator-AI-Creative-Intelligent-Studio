import React, { useState } from 'react';
import { Sparkles, ArrowRight, Check, CheckCircle2 } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useCreatorStore } from '@/shared/state/creator.store';
import { Button } from '@/shared/components/Button';
import { Chip } from '@/shared/components/Chip';

export const OnboardingFlow: React.FC = () => {
  const { completeOnboarding } = useAppStore();
  const { creator, updateProfile } = useCreatorStore();

  const [step, setStep] = useState(1);
  const [selectedNiche, setSelectedNiche] = useState('Technology & AI');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['YouTube', 'X / Twitter']);
  const [isBuildingDNA, setIsBuildingDNA] = useState(false);
  const [dnaProgress, setDnaProgress] = useState(0);

  const niches = [
    'Technology & AI',
    'Coding & Engineering',
    'Startups & Indie Hacking',
    'Hardware & Gadgets',
    'Design & Creative',
    'Gaming & Media',
  ];

  const platforms = ['YouTube', 'YouTube Shorts', 'Instagram Reels', 'TikTok', 'X / Twitter', 'LinkedIn'];

  const togglePlatform = (p: string) => {
    setSelectedPlatforms((prev) =>
      prev.includes(p) ? prev.filter((item) => item !== p) : [...prev, p]
    );
  };

  const handleFinish = async () => {
    setIsBuildingDNA(true);
    for (let i = 0; i <= 100; i += 20) {
      setDnaProgress(i);
      await new Promise((r) => setTimeout(r, 120));
    }
    updateProfile({
      niche: selectedNiche,
      platforms: selectedPlatforms,
    });
    setIsBuildingDNA(false);
    completeOnboarding();
  };

  return (
    <div
      className="media-bg"
      style={{
        minHeight: '100vh',
        backgroundImage: `url('/assets/creator-setup.jpg')`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '24px 20px',
        position: 'relative',
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(180deg, rgba(8,8,8,0.7) 0%, rgba(8,8,8,0.95) 100%)',
        }}
      />

      {/* Top Header */}
      <div style={{ position: 'relative', zIndex: 2 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--ai-accent)', fontWeight: 800, fontSize: '13px' }}>
            <Sparkles size={16} />
            CREATOR AI
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 600 }}>
            {step} / 3
          </span>
        </div>

        {step === 1 && (
          <div>
            <h1 style={{ fontSize: '32px', fontWeight: 800, lineHeight: 1.15, marginBottom: '12px' }}>
              Let’s calibrate <br />your Creator DNA.
            </h1>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Select your primary creation niche so Copilot generates ideas and scripts that sound authentic to you.
            </p>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '32px' }}>
              {niches.map((n) => {
                const isSelected = selectedNiche === n;
                return (
                  <button
                    key={n}
                    onClick={() => setSelectedNiche(n)}
                    style={{
                      padding: '10px 16px',
                      borderRadius: 'var(--radius-pill)',
                      backgroundColor: isSelected ? 'var(--ai-accent)' : 'var(--bg-surface-2)',
                      color: isSelected ? '#080808' : '#fff',
                      fontSize: '13px',
                      fontWeight: 600,
                      border: isSelected ? 'none' : '1px solid rgba(255, 255, 255, 0.08)',
                    }}
                  >
                    {n}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <h1 style={{ fontSize: '32px', fontWeight: 800, lineHeight: 1.15, marginBottom: '12px' }}>
              Where do you <br />publish content?
            </h1>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Copilot tailors pacing, retention hooks, and reframing algorithms for your chosen formats.
            </p>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '32px' }}>
              {platforms.map((p) => {
                const isSelected = selectedPlatforms.includes(p);
                return (
                  <button
                    key={p}
                    onClick={() => togglePlatform(p)}
                    style={{
                      padding: '10px 16px',
                      borderRadius: 'var(--radius-pill)',
                      backgroundColor: isSelected ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
                      color: isSelected ? 'var(--ai-accent)' : 'var(--text-secondary)',
                      fontSize: '13px',
                      fontWeight: 600,
                      border: isSelected ? '1px solid var(--ai-border)' : '1px solid rgba(255, 255, 255, 0.08)',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                    }}
                  >
                    {isSelected && <Check size={14} />}
                    {p}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <h1 style={{ fontSize: '30px', fontWeight: 800, lineHeight: 1.15, marginBottom: '12px' }}>
              Building your <br />Creator DNA.
            </h1>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Analyzing video transcripts, vocal mannerisms, and high-retention hook structures...
            </p>

            {isBuildingDNA ? (
              <div
                style={{
                  backgroundColor: 'var(--bg-surface-2)',
                  borderRadius: '20px',
                  padding: '24px 18px',
                  border: '1px solid var(--ai-border)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 700, marginBottom: '10px' }}>
                  <span style={{ color: 'var(--ai-accent)' }}>Synthesizing Profile...</span>
                  <span>{dnaProgress}%</span>
                </div>
                <div style={{ height: '6px', backgroundColor: '#202020', borderRadius: 'var(--radius-pill)', overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${dnaProgress}%`,
                      backgroundColor: 'var(--ai-accent)',
                      transition: 'width 0.15s ease',
                    }}
                  />
                </div>
              </div>
            ) : (
              <div
                style={{
                  backgroundColor: 'var(--bg-surface-2)',
                  borderRadius: '20px',
                  padding: '20px',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--success)', fontWeight: 700, marginBottom: '8px' }}>
                  <CheckCircle2 size={18} /> Ready to Create
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
                  Niche: <strong>{selectedNiche}</strong> · Platforms: <strong>{selectedPlatforms.join(', ')}</strong>
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Bottom Button */}
      <div style={{ position: 'relative', zIndex: 2 }}>
        {step < 3 ? (
          <Button
            variant="ai"
            size="lg"
            fullWidth
            onClick={() => setStep(step + 1)}
            style={{ gap: '8px' }}
          >
            Continue <ArrowRight size={18} />
          </Button>
        ) : (
          <Button
            variant="ai"
            size="lg"
            fullWidth
            disabled={isBuildingDNA}
            onClick={handleFinish}
            style={{ gap: '8px' }}
          >
            Launch Creative Studio ✦
          </Button>
        )}
      </div>
    </div>
  );
};
