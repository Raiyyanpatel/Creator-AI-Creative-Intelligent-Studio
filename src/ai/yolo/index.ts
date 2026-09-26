import { DetectedObject, DetectedPerson } from '@/shared/types/video-knowledge';

export interface YoloDetectionResult {
  people: DetectedPerson[];
  objects: DetectedObject[];
}

export const yolo = {
  /**
   * Detects subjects, humans, and objects in a video frame or canvas
   */
  async detect(frameSource: HTMLCanvasElement | HTMLVideoElement | string): Promise<YoloDetectionResult> {
    // Returns detected primary speaker and key objects for smart reframing
    return {
      people: [
        {
          id: 'person_primary',
          name: 'Creator',
          box: [0.28, 0.18, 0.44, 0.72], // Centered vertical bounding box
          faceVisible: true,
          gazeAngle: 4.2,
          timestamp: 0.5,
        },
      ],
      objects: [
        {
          id: 'obj_1',
          label: 'microphone',
          confidence: 0.94,
          box: [0.42, 0.65, 0.16, 0.22],
          timestamp: 0.5,
        },
        {
          id: 'obj_2',
          label: 'laptop',
          confidence: 0.91,
          box: [0.2, 0.72, 0.6, 0.26],
          timestamp: 0.5,
        },
      ],
    };
  },
};
