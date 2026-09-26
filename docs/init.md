You are initializing a mobile-first AI Creative Studio project for an iQOO/Snapdragon hackathon.

IMPORTANT:
Keep the architecture SIMPLE. Do not over-engineer.
Do not create unnecessary abstractions, services, repositories, adapters, dependency-injection layers, or enterprise architecture.

PRODUCT:
A phone-first AI Creative Studio that helps creators go from:

Idea → Script → Record → Analyze → Edit → Review → Export

It also supports:
- Creator profiling / Creator DNA
- Dashboard and creator insights
- Trends and content opportunities
- AI video analysis
- AI video editing
- Captions
- Audio cleanup
- Smart reframing
- Highlights
- AI Copilot
- Script Studio
- Teleprompter
- Recording
- Effects Studio
- Game Studio
- Assets
- Export

TECHNICAL DIRECTION:
- Mobile-first
- React / React Native as appropriate for the existing project
- TypeScript
- Dark cinematic UI
- Premium, minimal interface
- AI features should be designed around on-device/local inference where possible
- Backend should NOT become the center of the application
- Build the frontend architecture so mocked data can later be replaced by real APIs

KEEP THE PROJECT STRUCTURE TO ONLY FOUR MAIN DIRECTORIES:

src/
├── features/
├── shared/
├── ai/
└── utils/

FEATURES:

src/features/
├── onboarding/
├── home/
├── insights/
├── projects/
├── editor/
├── copilot/
├── script/
├── recording/
├── teleprompter/
├── effects/
├── game-studio/
├── assets/
└── export/

Each feature should be self-contained.

Example:

features/editor/
├── page.tsx
├── components/
└── editor.store.ts

Do NOT create separate top-level features for tiny editor operations such as:
- clipping
- captions
- audio
- reframing
- highlights

These belong inside the editor feature.

Example:

features/editor/
├── page.tsx
├── components/
│   ├── Timeline.tsx
│   ├── CaptionPanel.tsx
│   ├── AudioPanel.tsx
│   ├── ReframePanel.tsx
│   └── HighlightPanel.tsx
└── editor.store.ts

SHARED:

src/shared/
├── components/
├── state/
└── types/

Shared state should contain only state genuinely used across multiple features.

Initially create:

shared/state/
├── creator.store.ts
├── project.store.ts
├── media.store.ts
└── app.store.ts

AI:

src/ai/
├── whisper/
├── yolo/
├── mediapipe/
└── llm/

Keep AI integrations simple.

Provide clean functions such as:

whisper.transcribe()
yolo.detect()
mediapipe.track()
llm.generate()

Do not build unnecessary AI abstraction layers.

UTILITIES:

src/utils/
├── files.ts
├── media.ts
├── storage.ts
├── permissions.ts
├── export.ts
└── format.ts

Utilities should handle generic operations such as:

files.pick()
files.copy()
files.delete()
files.rename()

media.getMetadata()
media.getThumbnail()
media.getDuration()

storage.save()
storage.load()

export.render()
export.share()

Do not directly scatter filesystem, media, or storage logic throughout features.

DESIGN:

Use this visual direction:

Background: #080808
Surface: #111111
Surface 2: #171717
Surface 3: #202020

Primary text: #F7F7F2
Secondary text: #A6A6A0
Muted text: #70706B

AI accent: #D8FF00
AI soft: rgba(216,255,0,0.14)

Success: #A7F36B
Warning: #FFCC66
Danger: #FF5C6C
Info: #8AB4FF

Border radius:
10px / 14px / 20px / 28px / pill

Use Inter/system typography.

The UI should feel:
- cinematic
- premium
- minimal
- dark
- mobile-first
- media-focused
- AI-native

Avoid:
- generic SaaS dashboards
- excessive gradients
- excessive cards
- desktop video-editor layouts
- unnecessary sidebars
- excessive borders
- clutter

NAVIGATION:

Primary mobile navigation:

Home | Insights | Create | Profile

Projects should be prominent on Home rather than being a fifth bottom-navigation item.

Copilot should be a contextual bottom sheet / action surface rather than another navigation tab.

HOME:

Include:
- greeting
- creator avatar
- hero/inspiration area
- recent projects
- New Project
- Ask Copilot

INSIGHTS:

Include:
- creator metrics
- engagement
- views
- watch time
- follower growth
- niche trends
- world trends
- creator-specific opportunities

CREATE:

Include:
- Edit a Video
- Create from an Idea
- Game Studio
- Effects Studio

EDITOR:

Structure:

Preview
↓
Timeline
↓
Editing tools
↓
Ask Copilot

Editing tools:
- Cut
- Audio
- Text
- Effects
- Crop/Reframe
- Highlights

COPILOT:

Copilot is context-aware.

It should conceptually understand:
- current project
- current media
- timeline
- VideoKnowledge
- Creator DNA
- trends

Example:

User:
"Make this a 30 second Instagram reel."

Copilot should conceptually produce an edit plan:

1. Find strongest highlights
2. Remove silence
3. Remove fillers
4. Reframe to 9:16
5. Generate captions
6. Add appropriate zooms
7. Adjust audio
8. Preview
9. Ask user to Apply

Never directly mutate the project from an AI response without an explicit Apply action.

VIDEO KNOWLEDGE:

Use a shared conceptual structure:

VideoKnowledge
├── Project
├── Media
├── Transcript
├── Words
├── Scenes
├── People
├── Objects
├── Tracks
├── AudioEvents
├── Highlights
└── QualityIssues

This becomes the common information layer used by:
- editor
- copilot
- captions
- highlights
- reframing

IMPLEMENTATION STRATEGY:

First build a polished frontend/demo experience with mocked data.

Do NOT start by building:
- authentication
- complex backend
- cloud rendering
- distributed workers
- social publishing infrastructure
- elaborate database architecture

Prioritize:

1. App shell/navigation
2. Home
3. Create
4. Editor
5. Copilot UI
6. Insights
7. Profile/Creator DNA
8. Onboarding
9. Recording
10. Script/Teleprompter
11. Effects/Game Studio

Create realistic mock data so the application feels functional.

Every screen should look intentional and production-quality even if the underlying AI is mocked.

CODE QUALITY:

- TypeScript
- Strong typing
- Small components
- Avoid giant components
- Keep feature-specific code inside its feature
- Reuse shared components
- Avoid premature abstraction
- Avoid duplicate UI logic
- Keep naming obvious
- Prefer simple code over clever code

BEFORE WRITING CODE:

1. Inspect the existing repository.
2. Identify the existing framework and package manager.
3. Preserve useful existing configuration.
4. Do not unnecessarily rewrite the project.
5. Create the simple architecture above.
6. Then implement the application incrementally.

DO NOT:
- invent a complicated architecture
- create unnecessary folders
- install libraries without a reason
- replace working configuration
- create fake backend infrastructure just for appearance
- implement every AI model immediately

The goal is to create a clean, extensible foundation that can quickly become a polished hackathon demo.

Start by inspecting the repository and then implement the app shell + navigation + Home screen first.