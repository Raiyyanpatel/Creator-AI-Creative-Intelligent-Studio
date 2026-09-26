import { VideoKnowledge } from './video-knowledge';

export type AspectRatio = '9:16' | '16:9' | '1:1';

export interface TimelineClip {
  id: string;
  mediaUrl: string;
  title: string;
  start: number;
  duration: number;
  cutIn: number;
  cutOut: number;
  speed: number;
  volume: number;
}

export interface EditPlanStep {
  id: string;
  action: string;
  description: string;
  status: 'pending' | 'in_progress' | 'applied';
}

export interface CopilotEditPlan {
  id: string;
  prompt: string;
  summary: string;
  targetAspectRatio: AspectRatio;
  estimatedDuration: number;
  steps: EditPlanStep[];
}

export interface Project {
  id: string;
  title: string;
  description?: string;
  thumbnailUrl: string;
  durationSeconds: number;
  aspectRatio: AspectRatio;
  updatedAt: string;
  status: 'draft' | 'ready' | 'rendering' | 'exported';
  clips: TimelineClip[];
  knowledge?: VideoKnowledge;
}
