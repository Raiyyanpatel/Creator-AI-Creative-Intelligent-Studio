import React from 'react';
import { ArrowLeft, Plus, Music, Video, Image as ImageIcon } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useMediaStore } from '@/shared/state/media.store';
import { files } from '@/utils/files';
import { Button } from '@/shared/components/Button';
import { Card } from '@/shared/components/Card';

export const AssetsView: React.FC = () => {
  const { closeModal, showToast } = useAppStore();
  const { assets, addAsset } = useMediaStore();

  const handleImport = async () => {
    const picked = await files.pick();
    if (picked) {
      addAsset({
        name: picked.name,
        type: picked.type.includes('audio') ? 'audio' : picked.type.includes('video') ? 'video' : 'image',
        url: picked.url,
      });
      showToast(`Imported ${picked.name}`);
    }
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
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
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
        <span style={{ fontSize: '15px', fontWeight: 700 }}>Media & B-Roll Library</span>
        <button
          onClick={handleImport}
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: 'var(--ai-accent)',
            color: '#080808',
            display: 'grid',
            placeItems: 'center',
          }}
        >
          <Plus size={18} />
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
        {assets.map((asset) => (
          <Card key={asset.id} variant="surface" padding="10px">
            <div
              className="media-bg"
              style={{
                height: '110px',
                borderRadius: '12px',
                backgroundImage: `url(${asset.url})`,
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'flex-start',
                justifyContent: 'flex-end',
                padding: '6px',
              }}
            >
              <span
                style={{
                  padding: '3px 8px',
                  borderRadius: 'var(--radius-pill)',
                  backgroundColor: 'rgba(0,0,0,0.6)',
                  fontSize: '10px',
                  color: '#fff',
                }}
              >
                {asset.type}
              </span>
            </div>
            <div style={{ fontSize: '12px', fontWeight: 600, color: '#fff', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {asset.name}
            </div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>{asset.createdAt}</div>
          </Card>
        ))}
      </div>
    </div>
  );
};
