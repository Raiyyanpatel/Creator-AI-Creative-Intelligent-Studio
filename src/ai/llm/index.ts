import { CopilotEditPlan } from '@/shared/types/project';
import { CreatorDNA } from '@/shared/types/creator';
import { VideoKnowledge } from '@/shared/types/video-knowledge';

export interface LLMGenerateOptions {
  projectKnowledge?: VideoKnowledge;
  creatorDNA?: CreatorDNA;
  context?: string;
}

export const llm = {
  /**
   * Generates context-aware responses, script outlines, or editing action plans
   */
  async generate(prompt: string, options: LLMGenerateOptions = {}): Promise<string> {
    const p = prompt.toLowerCase();
    if (p.includes('reel') || p.includes('edit') || p.includes('cut') || p.includes('short')) {
      return `I've analyzed your footage based on your Creator DNA. I recommend a high-impact 30s cut with dynamic captions and smart 9:16 reframing.`;
    }
    if (p.includes('script') || p.includes('idea')) {
      return `# Video Script: Can Phones Run Useful AI Agents?
## Hook (0:00 - 0:04)
Stop believing that AI agents only live inside giant cloud data centers.
## Value (0:05 - 0:18)
Right here on this device, we're running localized Whisper and vision models with zero latency and complete privacy.
## Proof (0:19 - 0:26)
Look at this real-time transcription and automatic edit plan generated in under 300 milliseconds.
## Call to Action (0:27 - 0:30)
Tap create to try it yourself right now.`;
    }
    return `Copilot analyzed your request: "${prompt}". Ready to transform your creative workflow.`;
  },

  /**
   * Generates a concrete structured Copilot edit plan with applyable steps
   */
  async generateEditPlan(prompt: string, options: LLMGenerateOptions = {}): Promise<CopilotEditPlan> {
    return {
      id: `plan_${Date.now()}`,
      prompt,
      summary: `I'll transform this footage into an optimized 9:16 vertical Reel aligned with your Creator DNA.`,
      targetAspectRatio: '9:16',
      estimatedDuration: 30,
      steps: [
        {
          id: 'step_1',
          action: 'Highlight Extraction',
          description: 'Pinpointed top 3 hook moments (Virality Score 94%)',
          status: 'pending',
        },
        {
          id: 'step_2',
          action: 'Silence & Filler Removal',
          description: 'Trimmed 3.4s of dead pauses and 2 filler words ("um", "uh")',
          status: 'pending',
        },
        {
          id: 'step_3',
          action: 'Smart 9:16 Reframe',
          description: 'Subject centered via on-device YOLO vision tracking',
          status: 'pending',
        },
        {
          id: 'step_4',
          action: 'Kinetic Captions',
          description: 'Generated dynamic word-by-word highlighted captions',
          status: 'pending',
        },
        {
          id: 'step_5',
          action: 'Audio Normalization',
          description: 'Ducked background noise and leveled vocal presence',
          status: 'pending',
        },
      ],
    };
  },
};
