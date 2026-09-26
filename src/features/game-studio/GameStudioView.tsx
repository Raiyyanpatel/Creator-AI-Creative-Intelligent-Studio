import React, { useState } from 'react';
import { ArrowLeft, Gamepad2, Sparkles, Trophy, Play, Check } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { Button } from '@/shared/components/Button';
import { Card } from '@/shared/components/Card';
import { Chip } from '@/shared/components/Chip';

export const GameStudioView: React.FC = () => {
  const { closeModal, showToast } = useAppStore();
  const [selectedGame, setSelectedGame] = useState<'facial_react' | 'speed_trivia' | 'head_tilt'>('facial_react');
  const [isPlaying, setIsPlaying] = useState(false);
  const [score, setScore] = useState(1420);

  const games = [
    {
      id: 'facial_react',
      title: 'AI Reaction Challenge',
      desc: 'Matches facial landmarks against viral emotion prompts in real time.',
      points: '1,420 pts',
    },
    {
      id: 'speed_trivia',
      title: 'Niche Speed Trivia',
      desc: 'Nod or shake head to answer tech and AI creator trivia under 15 seconds.',
      points: '980 pts',
    },
    {
      id: 'head_tilt',
      title: 'Tilt to Reframe',
      desc: 'Interactive motion-tracking workout for camera engagement practice.',
      points: '750 pts',
    },
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
        <span style={{ fontSize: '15px', fontWeight: 700 }}>Game Studio</span>
        <Chip label="MediaPipe AI" variant="ai" />
      </div>

      {/* Game Showcase Banner */}
      <div
        className="media-bg"
        style={{
          height: '220px',
          borderRadius: '24px',
          backgroundImage: `url('/assets/game-studio-showcase.jpg')`,
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
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--ai-accent)', fontWeight: 700, fontSize: '11px', marginBottom: '4px' }}>
            <Trophy size={14} /> HIGH SCORE: {score}
          </div>
          <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#fff', margin: '0 0 4px' }}>
            Interactive Audience Minigames
          </h2>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0 }}>
            Record high-energy reaction videos with instant on-screen score overlays.
          </p>
        </div>
      </div>

      {/* Game Modes */}
      <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '10px' }}>Select Game Mode</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
        {games.map((g) => {
          const isSelected = selectedGame === g.id;
          return (
            <Card
              key={g.id}
              variant={isSelected ? 'ai' : 'surface'}
              padding="16px"
              onClick={() => setSelectedGame(g.id as any)}
              style={{ cursor: 'pointer' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                <strong style={{ fontSize: '14px', color: isSelected ? 'var(--ai-accent)' : '#fff' }}>
                  {g.title}
                </strong>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{g.points}</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0 }}>
                {g.desc}
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
            showToast('MediaPipe game session initialized');
            setIsPlaying(true);
          }}
          style={{ gap: '8px' }}
        >
          <Play size={18} />
          Launch Live Interactive Session ✦
        </Button>
      </div>
    </div>
  );
};
