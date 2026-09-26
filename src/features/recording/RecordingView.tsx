import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Video, Square, RefreshCw, Sparkles, Mic, Eye } from 'lucide-react';
import { useAppStore } from '@/shared/state/app.store';
import { useProjectStore } from '@/shared/state/project.store';
import { formatDuration } from '@/utils/format';

export const RecordingView: React.FC = () => {
  const { closeModal, openModal, showToast } = useAppStore();
  const { addProject } = useProjectStore();

  const [isRecording, setIsRecording] = useState(false);
  const [recordSeconds, setRecordSeconds] = useState(0);
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('user');
  const [cameraActive, setCameraActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    let stream: MediaStream | null = null;
    const startCamera = async () => {
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode },
            audio: true,
          });
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            setCameraActive(true);
          }
        }
      } catch (err) {
        console.warn('Live camera access fallback:', err);
        setCameraActive(false);
      }
    };

    startCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [facingMode]);

  useEffect(() => {
    let interval: any;
    if (isRecording) {
      interval = setInterval(() => {
        setRecordSeconds((s) => s + 1);
      }, 1000);
    } else {
      setRecordSeconds(0);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  const toggleRecording = () => {
    if (isRecording) {
      setIsRecording(false);
      showToast('Recording saved to project clips');
      addProject({
        title: `Recording Take ${Date.now().toString().slice(-4)}`,
        thumbnailUrl: '/assets/create-edit-video.jpg',
        durationSeconds: recordSeconds || 12,
      });
      openModal('editor');
    } else {
      setIsRecording(true);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#000',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Live Video Feed or Mock Fallback */}
      {cameraActive ? (
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: facingMode === 'user' ? 'scaleX(-1)' : 'none',
          }}
        />
      ) : (
        <div
          className="media-bg"
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage: `url('/assets/creator-setup.jpg')`,
            backgroundSize: 'cover',
          }}
        />
      )}

      {/* Camera UI Overlay */}
      <div
        style={{
          position: 'relative',
          zIndex: 10,
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '20px 18px 36px',
          background: 'linear-gradient(180deg, rgba(0,0,0,0.6) 0%, transparent 25%, transparent 75%, rgba(0,0,0,0.8) 100%)',
        }}
      >
        {/* Top Controls */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <button
            onClick={closeModal}
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              backdropFilter: 'blur(8px)',
              color: '#fff',
              display: 'grid',
              placeItems: 'center',
            }}
          >
            <ArrowLeft size={18} />
          </button>

          {/* Recording Timer Badge */}
          {isRecording ? (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 14px',
                borderRadius: 'var(--radius-pill)',
                backgroundColor: 'rgba(255, 92, 108, 0.85)',
                color: '#fff',
                fontSize: '13px',
                fontWeight: 700,
                backdropFilter: 'blur(8px)',
              }}
            >
              <span
                style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  backgroundColor: '#fff',
                  animation: 'pulse 1s infinite',
                }}
              />
              {formatDuration(recordSeconds)}
            </div>
          ) : (
            <div
              style={{
                padding: '6px 14px',
                borderRadius: 'var(--radius-pill)',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                color: 'var(--ai-accent)',
                fontSize: '12px',
                fontWeight: 600,
                backdropFilter: 'blur(8px)',
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
              }}
            >
              <Sparkles size={13} /> 4K 60fps · NPU Active
            </div>
          )}

          <button
            onClick={() => setFacingMode((prev) => (prev === 'user' ? 'environment' : 'user'))}
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              backdropFilter: 'blur(8px)',
              color: '#fff',
              display: 'grid',
              placeItems: 'center',
            }}
          >
            <RefreshCw size={18} />
          </button>
        </div>

        {/* Center Prompt Banner */}
        <div
          style={{
            alignSelf: 'center',
            maxWidth: '320px',
            backgroundColor: 'rgba(0, 0, 0, 0.65)',
            backdropFilter: 'blur(12px)',
            borderRadius: '16px',
            padding: '12px 16px',
            textAlign: 'center',
            border: '1px solid rgba(255, 255, 255, 0.1)',
          }}
        >
          <div style={{ fontSize: '11px', color: 'var(--ai-accent)', fontWeight: 700, marginBottom: '2px' }}>
            ✦ PROMPTER CUE
          </div>
          <p style={{ fontSize: '13px', color: '#fff', margin: 0, fontWeight: 500 }}>
            "Stop believing that AI agents only live inside giant cloud data centers..."
          </p>
        </div>

        {/* Bottom Shutter Controls */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-around' }}>
          <button
            onClick={() => openModal('teleprompter')}
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              backgroundColor: 'rgba(255, 255, 255, 0.15)',
              backdropFilter: 'blur(8px)',
              color: '#fff',
              display: 'grid',
              placeItems: 'center',
            }}
            title="Teleprompter"
          >
            <Eye size={20} />
          </button>

          {/* Record Shutter Button */}
          <button
            onClick={toggleRecording}
            style={{
              width: '74px',
              height: '74px',
              borderRadius: '50%',
              border: '4px solid #fff',
              padding: '4px',
              backgroundColor: 'transparent',
              display: 'grid',
              placeItems: 'center',
            }}
          >
            <div
              style={{
                width: isRecording ? '32px' : '56px',
                height: isRecording ? '32px' : '56px',
                borderRadius: isRecording ? '8px' : '50%',
                backgroundColor: 'var(--danger)',
                transition: 'all 0.2s ease',
              }}
            />
          </button>

          <button
            onClick={() => openModal('effects')}
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              backgroundColor: 'rgba(255, 255, 255, 0.15)',
              backdropFilter: 'blur(8px)',
              color: 'var(--ai-accent)',
              display: 'grid',
              placeItems: 'center',
            }}
            title="Effects"
          >
            <Sparkles size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};
