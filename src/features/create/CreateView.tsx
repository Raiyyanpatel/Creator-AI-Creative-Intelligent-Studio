import React from 'react';
import { ArrowRight, Film, Lightbulb, Gamepad2, Wand2, ArrowLeft } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { files } from '@/utils/files';

export const CreateView: React.FC = () => {
  const { setActiveTab, openModal } = useAppStore();
  const { addProject } = useProjectStore();

  const handleEditVideo = async () => {
    // Allows picking a file or launching editor with default footage
    const picked = await files.pick('video/*,image/*');
    if (picked) {
      addProject({
        title: picked.name.replace(/\.[^/.]+$/, ''),
        thumbnailUrl: '/assets/create-edit-video.jpg',
      });
    }
    openModal('editor');
  };

  const creationCards = [
    {
      id: 'edit',
      title: 'Edit a Video',
      description: 'Import footage and let on-device AI understand, cut, and reframe it.',
      badge: '🎬 Quick Edit',
      bg: '/assets/create-edit-video.jpg',
      action: handleEditVideo,
    },
    {
      id: 'idea',
      title: 'Create from an Idea',
      description: 'Idea → Copilot discussion → outline → teleprompter → record → edit.',
      badge: '✦ End-to-End',
      bg: '/assets/create-from-idea.jpg',
      action: () => openModal('script'),
    },
    {
      id: 'game',
      title: 'Game Studio',
      description: 'Create camera and MediaPipe-powered interactive reaction experiences.',
      badge: '🎮 Interactive AI',
      bg: '/assets/create-game-studio.jpg',
      action: () => openModal('game-studio'),
    },
    {
      id: 'effects',
      title: 'Effects Studio',
      description: 'Discover cinematic camera color grades, visual effects, and overlays.',
      badge: '✨ Visual FX',
      bg: '/assets/create-effects-studio.jpg',
      action: () => openModal('effects'),
    },
  ];

  return (
    <main className="screen-container">
      {/* Top Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '20px' }}>
        <button
          onClick={() => setActiveTab('home')}
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
        <div>
          <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--text-muted)' }}>
            Studio Hub
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: 800, margin: 0, letterSpacing: '-0.02em' }}>
            What are you making?
          </h1>
        </div>
      </div>

      <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '22px' }}>
        Start from existing footage, an unrefined idea, or a live interactive camera format.
      </p>

      {/* Creation Cards Grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {creationCards.map((card) => (
          <article
            key={card.id}
            onClick={card.action}
            className="media-bg"
            style={{
              minHeight: '135px',
              borderRadius: '24px',
              overflow: 'hidden',
              backgroundImage: `url(${card.bg})`,
              padding: '18px 20px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              position: 'relative',
              cursor: 'pointer',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              transition: 'transform 0.18s ease, border-color 0.18s ease',
            }}
          >
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.88) 100%)',
              }}
            />
            <div style={{ position: 'relative', zIndex: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span
                style={{
                  padding: '4px 10px',
                  borderRadius: 'var(--radius-pill)',
                  backgroundColor: 'rgba(0, 0, 0, 0.65)',
                  fontSize: '11px',
                  fontWeight: 600,
                  color: 'var(--text-primary)',
                  backdropFilter: 'blur(8px)',
                }}
              >
                {card.badge}
              </span>
              <div
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  backgroundColor: 'rgba(255, 255, 255, 0.12)',
                  backdropFilter: 'blur(8px)',
                  display: 'grid',
                  placeItems: 'center',
                  color: '#fff',
                }}
              >
                <ArrowRight size={16} />
              </div>
            </div>

            <div style={{ position: 'relative', zIndex: 2, marginTop: '16px' }}>
              <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#fff', margin: '0 0 4px' }}>
                {card.title}
              </h3>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, maxWidth: '280px' }}>
                {card.description}
              </p>
            </div>
          </article>
        ))}
      </div>
    </main>
  );
};
