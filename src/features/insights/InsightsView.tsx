import React from 'react';
import { TrendingUp, Sparkles, ArrowUpRight, Globe, Flame, Eye, Clock, Users, BarChart3 } from 'lucide-react';
import { useCreatorStore } from '@/shared/state/creator.store';
import { useAppStore } from '@/shared/state/app.store';
import { Card } from '@/shared/components/Card';
import { Chip } from '@/shared/components/Chip';
import { Button } from '@/shared/components/Button';

export const InsightsView: React.FC = () => {
  const { creator } = useCreatorStore();
  const { openCopilot, openModal } = useAppStore();

  const nicheTrends = [
    {
      id: 't1',
      title: 'AI coding agents',
      momentum: '+142%',
      platforms: ['YouTube', 'X / Twitter'],
      relevance: 'Very High (9.6/10)',
      bg: '/assets/trend-ai-agents.jpg',
      description: 'Massive surge across developer and founder communities. Direct alignment with your code teardown format.',
    },
    {
      id: 't2',
      title: 'On-device AI & private models',
      momentum: '+98%',
      platforms: ['YouTube Shorts', 'LinkedIn'],
      relevance: 'High (8.9/10)',
      bg: '/assets/trend-on-device-ai.jpg',
      description: 'Audience interest shifting from cloud API costs to hardware benchmarks and local mobile inference.',
    },
  ];

  const worldTrends = ['VLMs & Vision', 'Local Whisper', 'Snapdragon NPU', 'Robotics', 'Creator Economy', 'AI Phones'];

  return (
    <main className="screen-container">
      {/* Top Header */}
      <div style={{ marginBottom: '22px' }}>
        <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--text-muted)' }}>
          Creator Intelligence
        </div>
        <h1 style={{ fontSize: '28px', fontWeight: 800, letterSpacing: '-0.03em', margin: '4px 0 0' }}>
          Know what to <br />create next.
        </h1>
      </div>

      {/* 2x2 Metric Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '12px',
          marginBottom: '26px',
        }}
      >
        <Card variant="surface" padding="16px">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Total Views</span>
            <Eye size={14} color="var(--text-muted)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#fff' }}>{creator.metrics.views}</div>
          <div style={{ marginTop: '4px' }}>
            <Chip label={creator.metrics.viewsChange} variant="ai" />
          </div>
        </Card>

        <Card variant="surface" padding="16px">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Engagement</span>
            <BarChart3 size={14} color="var(--text-muted)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#fff' }}>{creator.metrics.engagement}</div>
          <div style={{ marginTop: '4px' }}>
            <Chip label={creator.metrics.engagementChange} variant="ai" />
          </div>
        </Card>

        <Card variant="surface" padding="16px">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Watch Time</span>
            <Clock size={14} color="var(--text-muted)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#fff' }}>{creator.metrics.watchTime}</div>
          <div style={{ marginTop: '4px' }}>
            <Chip label="Top 5% Niche" />
          </div>
        </Card>

        <Card variant="surface" padding="16px">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Growth Rate</span>
            <Users size={14} color="var(--text-muted)" />
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#fff' }}>{creator.metrics.growth}</div>
          <div style={{ marginTop: '4px' }}>
            <Chip label="Healthy" variant="success" />
          </div>
        </Card>
      </div>

      {/* Creation Opportunity Section */}
      <section style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <Sparkles size={16} color="var(--ai-accent)" />
          <h3 style={{ fontSize: '16px', fontWeight: 700, margin: 0 }}>High-Potential Opportunity</h3>
        </div>

        <Card variant="ai" padding="20px">
          <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--ai-accent)', fontWeight: 700 }}>
            DNA Match: 96%
          </div>
          <h4 style={{ fontSize: '18px', fontWeight: 700, margin: '8px 0', color: '#fff' }}>
            “Can a phone run a useful AI agent?”
          </h4>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.45, marginBottom: '16px' }}>
            Your technology and on-device AI topics are strongly aligned. Previous developer tool videos outperformed channel baseline by +28%.
          </p>
          <Button
            variant="primary"
            fullWidth
            onClick={() => {
              openCopilot('Generate full script and edit plan for: Can a phone run a useful AI agent?');
            }}
            style={{ gap: '6px' }}
          >
            <Sparkles size={15} />
            Create Video From Opportunity ✦
          </Button>
        </Card>
      </section>

      {/* Niche Trends */}
      <section style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
          <h3 style={{ fontSize: '17px', fontWeight: 700, margin: 0 }}>Trending In Your Niche</h3>
          <span style={{ fontSize: '11px', color: 'var(--ai-accent)', fontWeight: 600 }}>● Live Feed</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {nicheTrends.map((trend) => (
            <article
              key={trend.id}
              className="media-bg"
              style={{
                borderRadius: '20px',
                overflow: 'hidden',
                backgroundImage: `url(${trend.bg})`,
                minHeight: '160px',
                padding: '18px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                border: '1px solid rgba(255, 255, 255, 0.08)',
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'linear-gradient(90deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.45) 100%)',
                }}
              />
              <div style={{ position: 'relative', zIndex: 2 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <h4 style={{ fontSize: '17px', fontWeight: 700, color: '#fff', margin: 0 }}>{trend.title}</h4>
                    <span style={{ fontSize: '12px', color: 'var(--ai-accent)', fontWeight: 600 }}>{trend.momentum} momentum</span>
                  </div>
                  <Chip label={trend.relevance} variant="ai" />
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: '8px 0 10px', maxWidth: '300px' }}>
                  {trend.description}
                </p>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {trend.platforms.map((p) => (
                    <Chip key={p} label={p} />
                  ))}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* World Trends */}
      <section style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
          <Globe size={16} color="var(--text-muted)" />
          <h3 style={{ fontSize: '16px', fontWeight: 700, margin: 0 }}>World Trends</h3>
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {worldTrends.map((wt) => (
            <Chip
              key={wt}
              label={wt}
              onClick={() => openCopilot(`Explore content ideas for: ${wt}`)}
            />
          ))}
        </div>
      </section>
    </main>
  );
};
