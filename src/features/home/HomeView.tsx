import React, { useState } from 'react';
import { Sparkles, Plus, Play, ChevronRight, SlidersHorizontal, ArrowUpRight } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useCreatorStore } from '@/shared/state/creator.store';
import { useProjectStore } from '@/shared/state/project.store';
import { Button } from '@/shared/components/Button';
import { Chip } from '@/shared/components/Chip';

export const HomeView: React.FC = () => {
  const { creator } = useCreatorStore();
  const { projects, setActiveProjectId } = useProjectStore();
  const { openCopilot, openModal, setActiveTab } = useAppStore();
  const [quickInput, setQuickInput] = useState('');

  const handleQuickSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickInput.trim()) {
      openCopilot(quickInput);
      setQuickInput('');
    }
  };

  const handleOpenProject = (id: string) => {
    setActiveProjectId(id);
    openModal('editor');
  };

  return (
    <main className="screen-container">
      {/* Top Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            onClick={() => setActiveTab('profile')}
            style={{
              width: '42px',
              height: '42px',
              borderRadius: '50%',
              backgroundImage: `url(${creator.avatarUrl})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              border: '2px solid rgba(216, 255, 0, 0.4)',
              cursor: 'pointer',
            }}
          />
          <div>
            <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--text-muted)' }}>
              Creator AI Studio
            </div>
            <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)' }}>
              {creator.name}
            </div>
          </div>
        </div>

        <button
          onClick={() => openModal('script')}
          style={{
            width: '38px',
            height: '38px',
            borderRadius: '50%',
            backgroundColor: 'var(--bg-surface-2)',
            color: 'var(--text-secondary)',
            display: 'grid',
            placeItems: 'center',
            border: '1px solid rgba(255, 255, 255, 0.08)',
          }}
          title="Script Studio"
        >
          <SlidersHorizontal size={18} />
        </button>
      </div>

      {/* Greeting Headline */}
      <div style={{ marginBottom: '20px' }}>
        <h1
          style={{
            fontSize: '28px',
            fontWeight: 800,
            lineHeight: 1.15,
            letterSpacing: '-0.03em',
            margin: 0,
          }}
        >
          Turn what you know into <span style={{ color: 'var(--ai-accent)' }}>viral content</span>.
        </h1>
      </div>

      {/* Hero Inspiration Card */}
      <div
        onClick={() => openCopilot('Create video from on-device AI trends')}
        className="media-bg"
        style={{
          minHeight: '260px',
          borderRadius: '26px',
          overflow: 'hidden',
          backgroundImage: `url('/assets/home-hero.jpg')`,
          padding: '20px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-end',
          boxShadow: 'var(--shadow-card)',
          cursor: 'pointer',
          marginBottom: '22px',
          border: '1px solid rgba(255, 255, 255, 0.08)',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.88) 100%)',
          }}
        />
        <div style={{ position: 'relative', zIndex: 2 }}>
          <div style={{ display: 'inline-flex', marginBottom: '8px' }}>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                padding: '6px 12px',
                borderRadius: 'var(--radius-pill)',
                backgroundColor: 'rgba(216, 255, 0, 0.18)',
                color: 'var(--ai-accent)',
                fontSize: '11px',
                fontWeight: 700,
                backdropFilter: 'blur(10px)',
                border: '1px solid var(--ai-border)',
              }}
            >
              <Sparkles size={13} />
              AI INSPIRATION FOR TODAY
            </span>
          </div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff', marginBottom: '6px', lineHeight: 1.25 }}>
            “Can a phone run a useful AI agent?”
          </h2>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, maxWidth: '320px' }}>
            Rising +94% in Tech & AI niches. Aligns directly with your audience retention style.
          </p>
        </div>
      </div>

      {/* AI Prompt Quick Bar */}
      <form
        onSubmit={handleQuickSubmit}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          backgroundColor: '#12160d',
          border: '1px solid var(--ai-border)',
          borderRadius: '20px',
          padding: '8px 10px 8px 16px',
          marginBottom: '28px',
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
        }}
      >
        <Sparkles size={18} color="var(--ai-accent)" style={{ flexShrink: 0 }} />
        <input
          type="text"
          value={quickInput}
          onChange={(e) => setQuickInput(e.target.value)}
          placeholder="What do you want to create or edit?"
          style={{
            flex: 1,
            backgroundColor: 'transparent',
            border: 'none',
            outline: 'none',
            color: 'var(--text-primary)',
            fontSize: '13px',
          }}
        />
        <button
          type="submit"
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: 'var(--ai-accent)',
            color: '#080808',
            display: 'grid',
            placeItems: 'center',
            fontWeight: 800,
            flexShrink: 0,
          }}
        >
          <ArrowUpRight size={18} />
        </button>
      </form>

      {/* Projects Section */}
      <section style={{ marginBottom: '24px' }}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '14px',
          }}
        >
          <h3 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
            Recent Projects
          </h3>
          <span
            onClick={() => openModal('editor')}
            style={{ fontSize: '12px', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
          >
            Open Editor <ChevronRight size={14} />
          </span>
        </div>

        <div
          style={{
            display: 'flex',
            gap: '12px',
            overflowX: 'auto',
            paddingBottom: '8px',
            marginRight: '-18px',
            paddingRight: '18px',
          }}
        >
          {projects.map((proj) => (
            <article
              key={proj.id}
              onClick={() => handleOpenProject(proj.id)}
              className="media-bg"
              style={{
                minWidth: '185px',
                height: '210px',
                borderRadius: '20px',
                overflow: 'hidden',
                backgroundImage: `url(${proj.thumbnailUrl})`,
                flexShrink: 0,
                position: 'relative',
                cursor: 'pointer',
                border: '1px solid rgba(255, 255, 255, 0.08)',
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.92) 100%)',
                }}
              />
              <div
                style={{
                  position: 'absolute',
                  top: '12px',
                  right: '12px',
                  padding: '4px 8px',
                  borderRadius: 'var(--radius-pill)',
                  backgroundColor: 'rgba(0, 0, 0, 0.65)',
                  backdropFilter: 'blur(8px)',
                  fontSize: '10px',
                  color: '#fff',
                  fontWeight: 600,
                }}
              >
                {proj.aspectRatio}
              </div>

              <div style={{ position: 'absolute', bottom: '14px', left: '14px', right: '14px', zIndex: 2 }}>
                <div
                  style={{
                    fontSize: '14px',
                    fontWeight: 700,
                    color: '#fff',
                    marginBottom: '4px',
                    lineHeight: '1.2',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}
                >
                  {proj.title}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                  {proj.durationSeconds}s · {proj.updatedAt}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Primary New Project CTA */}
      <Button
        variant="ai"
        fullWidth
        size="lg"
        onClick={() => setActiveTab('create')}
        style={{ gap: '8px' }}
      >
        <Plus size={18} />
        New Project +
      </Button>
    </main>
  );
};
