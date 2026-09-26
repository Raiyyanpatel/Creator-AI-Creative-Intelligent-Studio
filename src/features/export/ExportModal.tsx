import React, { useState } from 'react';
import { X, Share2, Download, Check, Sparkles, Film } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { exportUtil } from '@/utils/export';
import { Button } from '@/shared/components/Button';

export const ExportModal: React.FC = () => {
  const { closeModal, showToast } = useAppStore();
  const { activeProject } = useProjectStore();

  const [resolution, setResolution] = useState<'1080p' | '4K'>('1080p');
  const [aspectRatio, setAspectRatio] = useState<'9:16' | '16:9'>('9:16');
  const [isRendering, setIsRendering] = useState(false);
  const [renderProgress, setRenderProgress] = useState(0);
  const [renderedUrl, setRenderedUrl] = useState<string | null>(null);

  const handleStartRender = async () => {
    setIsRendering(true);
    setRenderProgress(0);
    const url = await exportUtil.render(
      activeProject?.id || 'p1',
      {
        resolution,
        aspectRatio,
        includeCaptions: true,
        normalizeAudio: true,
        fps: 60,
      },
      (p) => setRenderProgress(p)
    );
    setRenderedUrl(url);
    setIsRendering(false);
    showToast('Video rendered successfully');
  };

  const handleShare = async () => {
    if (renderedUrl && activeProject) {
      await exportUtil.share(activeProject.title, renderedUrl);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(10px)',
        zIndex: 100,
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'center',
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget && !isRendering) closeModal();
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '480px',
          backgroundColor: '#151515',
          borderTopLeftRadius: '28px',
          borderTopRightRadius: '28px',
          padding: '24px 20px 32px',
          boxShadow: '0 -20px 60px rgba(0, 0, 0, 0.9)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Film size={18} color="var(--ai-accent)" />
            <h3 style={{ fontSize: '17px', fontWeight: 700, margin: 0 }}>Export & Share</h3>
          </div>
          {!isRendering && (
            <button
              onClick={closeModal}
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
              <X size={16} />
            </button>
          )}
        </div>

        {renderedUrl ? (
          <div>
            <div
              style={{
                backgroundColor: 'var(--bg-surface-2)',
                borderRadius: '20px',
                padding: '20px',
                textAlign: 'center',
                border: '1px solid var(--ai-border)',
                marginBottom: '20px',
              }}
            >
              <div
                style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '50%',
                  backgroundColor: 'var(--ai-soft)',
                  color: 'var(--ai-accent)',
                  margin: '0 auto 12px',
                  display: 'grid',
                  placeItems: 'center',
                }}
              >
                <Check size={24} />
              </div>
              <h4 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', margin: '0 0 4px' }}>
                Export Complete
              </h4>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0 }}>
                {activeProject?.title} ({resolution} · {aspectRatio})
              </p>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <Button
                variant="secondary"
                style={{ flex: 1, gap: '6px' }}
                onClick={() => {
                  showToast('Downloaded to device gallery');
                  closeModal();
                }}
              >
                <Download size={16} /> Download
              </Button>
              <Button
                variant="ai"
                style={{ flex: 1, gap: '6px' }}
                onClick={handleShare}
              >
                <Share2 size={16} /> Share Video
              </Button>
            </div>
          </div>
        ) : (
          <div>
            {/* Resolution Selector */}
            <div style={{ marginBottom: '16px' }}>
              <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>
                Resolution
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
                {(['1080p', '4K'] as const).map((res) => (
                  <button
                    key={res}
                    onClick={() => setResolution(res)}
                    style={{
                      padding: '12px',
                      borderRadius: '14px',
                      backgroundColor: resolution === res ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
                      color: resolution === res ? 'var(--ai-accent)' : '#fff',
                      border: resolution === res ? '1px solid var(--ai-border)' : '1px solid rgba(255, 255, 255, 0.06)',
                      fontWeight: 600,
                      fontSize: '13px',
                    }}
                  >
                    {res} {res === '4K' ? 'Ultra HD' : 'Full HD'}
                  </button>
                ))}
              </div>
            </div>

            {/* Aspect Ratio Selector */}
            <div style={{ marginBottom: '22px' }}>
              <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>
                Format
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
                {(['9:16', '16:9'] as const).map((ar) => (
                  <button
                    key={ar}
                    onClick={() => setAspectRatio(ar)}
                    style={{
                      padding: '12px',
                      borderRadius: '14px',
                      backgroundColor: aspectRatio === ar ? 'var(--ai-soft)' : 'var(--bg-surface-2)',
                      color: aspectRatio === ar ? 'var(--ai-accent)' : '#fff',
                      border: aspectRatio === ar ? '1px solid var(--ai-border)' : '1px solid rgba(255, 255, 255, 0.06)',
                      fontWeight: 600,
                      fontSize: '13px',
                    }}
                  >
                    {ar} {ar === '9:16' ? '(Vertical Reel)' : '(Landscape)'}
                  </button>
                ))}
              </div>
            </div>

            {/* Render Progress */}
            {isRendering && (
              <div style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--ai-accent)', fontWeight: 600, marginBottom: '6px' }}>
                  <span>Rendering on-device silicon...</span>
                  <span>{renderProgress}%</span>
                </div>
                <div style={{ height: '6px', backgroundColor: '#202020', borderRadius: 'var(--radius-pill)', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${renderProgress}%`, backgroundColor: 'var(--ai-accent)', transition: 'width 0.1s ease' }} />
                </div>
              </div>
            )}

            <Button
              variant="ai"
              size="lg"
              fullWidth
              disabled={isRendering}
              onClick={handleStartRender}
              style={{ gap: '8px' }}
            >
              <Sparkles size={18} />
              {isRendering ? 'Rendering...' : 'Render & Export ✦'}
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};
