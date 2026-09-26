import { Transcript, WordTimestamp } from '@/shared/types/video-knowledge';

export interface WhisperTranscriptionOptions {
  language?: string;
  detectFillers?: boolean;
}

export const whisper = {
  /**
   * Transcribes audio into timestamps and words (supports on-device / local simulation)
   */
  async transcribe(
    audioSource: Blob | string,
    options: WhisperTranscriptionOptions = {}
  ): Promise<Transcript> {
    // Realistic mocked transcription for fast on-device demo experience
    const mockWords: WordTimestamp[] = [
      { id: 'w1', word: 'Building', start: 0.1, end: 0.6, confidence: 0.98 },
      { id: 'w2', word: 'autonomous', start: 0.65, end: 1.2, confidence: 0.96 },
      { id: 'w3', word: 'AI', start: 1.25, end: 1.5, confidence: 0.99 },
      { id: 'w4', word: 'agents', start: 1.55, end: 2.0, confidence: 0.97 },
      { id: 'w5', word: 'directly', start: 2.1, end: 2.5, confidence: 0.94 },
      { id: 'w6', word: 'on', start: 2.55, end: 2.7, confidence: 0.99 },
      { id: 'w7', word: 'phones', start: 2.75, end: 3.2, confidence: 0.98 },
      { id: 'w8', word: 'um', start: 3.3, end: 3.6, confidence: 0.88, isFiller: true },
      { id: 'w9', word: 'is', start: 3.7, end: 3.9, confidence: 0.99 },
      { id: 'w10', word: 'the', start: 3.95, end: 4.1, confidence: 0.99 },
      { id: 'w11', word: 'single', start: 4.15, end: 4.5, confidence: 0.97 },
      { id: 'w12', word: 'biggest', start: 4.55, end: 5.0, confidence: 0.98 },
      { id: 'w13', word: 'unlock', start: 5.05, end: 5.5, confidence: 0.96 },
      { id: 'w14', word: 'for', start: 5.55, end: 5.75, confidence: 0.99 },
      { id: 'w15', word: 'creators', start: 5.8, end: 6.4, confidence: 0.97 },
    ];

    const fullText = mockWords.map((w) => w.word).join(' ');

    return {
      id: `tr_${Date.now()}`,
      language: options.language || 'en',
      fullText,
      words: mockWords,
    };
  },
};
