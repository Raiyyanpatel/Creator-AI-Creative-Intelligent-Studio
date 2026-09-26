export interface MediaMetadata {
  duration: number;
  width: number;
  height: number;
  aspectRatio: string;
}

export const media = {
  async getMetadata(videoUrl: string): Promise<MediaMetadata> {
    return new Promise((resolve) => {
      const vid = document.createElement('video');
      vid.preload = 'metadata';
      vid.src = videoUrl;
      vid.onloadedmetadata = () => {
        const width = vid.videoWidth || 1080;
        const height = vid.videoHeight || 1920;
        const duration = vid.duration || 42;
        const aspectRatio = width > height ? '16:9' : width === height ? '1:1' : '9:16';
        resolve({ duration, width, height, aspectRatio });
      };
      vid.onerror = () => {
        // Fallback for mocked assets
        resolve({ duration: 42, width: 1080, height: 1920, aspectRatio: '9:16' });
      };
    });
  },

  async getThumbnail(videoUrl: string, atTime = 1): Promise<string> {
    return new Promise((resolve) => {
      const vid = document.createElement('video');
      vid.crossOrigin = 'anonymous';
      vid.src = videoUrl;
      vid.currentTime = atTime;
      vid.onseeked = () => {
        try {
          const canvas = document.createElement('canvas');
          canvas.width = vid.videoWidth || 320;
          canvas.height = vid.videoHeight || 568;
          const ctx = canvas.getContext('2d');
          ctx?.drawImage(vid, 0, 0, canvas.width, canvas.height);
          resolve(canvas.toDataURL('image/jpeg', 0.8));
        } catch {
          resolve(videoUrl);
        }
      };
      vid.onerror = () => resolve(videoUrl);
    });
  },

  getDuration(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  }
};
