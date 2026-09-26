/**
 * VideoKnowledge defines the unified multimodal intelligence representation
 * specified in INIT.md.
 * Used across Editor, Copilot, Captions, Highlights, and Smart Reframing.
 */

export interface WordTimestamp {
  id: string;
  word: string;
  start: number; // in seconds
  end: number;
  confidence: number;
  speaker?: string;
  isFiller?: boolean;
}

export interface Transcript {
  id: string;
  language: string;
  fullText: string;
  words: WordTimestamp[];
}

export interface DetectedPerson {
  id: string;
  name?: string;
  box: [number, number, number, number]; // [x, y, width, height] normalized 0..1
  faceVisible: boolean;
  gazeAngle?: number;
  timestamp: number;
}

export interface DetectedObject {
  id: string;
  label: string;
  confidence: number;
  box: [number, number, number, number];
  timestamp: number;
}

export interface SceneCut {
  id: string;
  start: number;
  end: number;
  visualSummary: string;
  keyframeUrl?: string;
  motionIntensity: 'low' | 'medium' | 'high';
}

export interface AudioEvent {
  id: string;
  type: 'speech' | 'applause' | 'music' | 'silence' | 'laughter' | 'noise';
  start: number;
  end: number;
  confidence: number;
}

export interface VideoHighlight {
  id: string;
  title: string;
  reason: string;
  start: number;
  end: number;
  viralityScore: number; // 0..100
  suggestedAspectRatio: '9:16' | '16:9' | '1:1';
}

export interface QualityIssue {
  id: string;
  type: 'filler_word' | 'dead_air' | 'poor_lighting' | 'audio_clipping' | 'unstable_framing';
  start: number;
  end: number;
  description: string;
  suggestedFix: string;
}

export interface VideoTrackItem {
  id: string;
  type: 'video' | 'audio' | 'caption' | 'effect';
  start: number;
  duration: number;
  title: string;
  data?: any;
}

export interface VideoKnowledge {
  projectId: string;
  mediaId: string;
  duration: number;
  resolution: { width: number; height: number };
  aspectRatio: string;
  transcript: Transcript;
  words: WordTimestamp[];
  scenes: SceneCut[];
  people: DetectedPerson[];
  objects: DetectedObject[];
  tracks: VideoTrackItem[];
  audioEvents: AudioEvent[];
  highlights: VideoHighlight[];
  qualityIssues: QualityIssue[];
}
