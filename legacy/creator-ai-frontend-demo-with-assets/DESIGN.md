# Creator AI — Frontend Design Specification

## 1. Product direction

Creator AI is a premium, mobile-first AI Creative Studio.

The product should feel like:
- cinematic
- minimal
- creator-focused
- dark
- image/media-first
- AI-native
- polished enough for a hackathon demo

It should NOT feel like:
- a desktop video editor squeezed onto a phone
- a dashboard full of tables
- a generic SaaS admin panel
- a traditional CapCut/Premiere clone

Primary visual references: the supplied mobile creative/editor references.

---

## 2. Core product model

The application has four major surfaces:

1. Home
2. Insights
3. Create
4. Profile

Supporting flows:
- Onboarding
- Project Editor
- Copilot
- Create from Idea
- Effects Studio
- Game Studio

Bottom navigation:

Home | Insights | Create | Profile

Projects should be prominent on Home rather than becoming a fifth bottom-nav item.

---

## 3. Creator intelligence

Onboarding creates a lightweight Creator Profile.

Inputs:
- niche
- platforms
- content interests
- creator goals
- preferred tone
- existing content sources
- custom instructions

Existing content can conceptually come from:
- YouTube
- LinkedIn
- X
- Substack
- uploaded files

The demo does not need real integrations. Use realistic dummy data.

The frontend should communicate this pipeline:

Existing Content
→ Style Analysis
→ Creator DNA
→ Trends + Analytics
→ Copilot
→ Creation

---

## 4. Home

Purpose: make the user want to create something immediately.

Structure:

Top:
- greeting
- profile avatar
- small menu/settings control

Hero:
- large cinematic inspiration card
- one short headline
- subtle category/trending badge

Projects:
- horizontal media cards
- thumbnail
- project title
- duration
- last edited
- overflow menu

Primary CTA:
- bright lime "New Project +"

Copilot entry:
- floating / prominent "Ask Copilot" input
- supports text and microphone affordances

Do not overcrowd the screen.

---

## 5. Insights

Purpose: turn analytics and trends into creation opportunities.

Sections:

### Creator Snapshot
- niche
- audience
- content style
- recent performance

### Performance
Show:
- views
- engagement
- watch time
- follower growth

Use simple cards/charts, not spreadsheet tables.

### Niche Trends
Each trend card contains:
- topic
- momentum
- platforms
- relevance to creator
- short explanation

### Creation Opportunities
Example:

"AI coding agents are rising in your niche."

Then:

"Your previous developer-tool videos performed above your average."

CTA:
- "Create video ✦"

### World Trends
Show broad trends separately from niche trends.

The UI should distinguish:
World trend → Niche relevance → Personal opportunity.

---

## 6. Create

Four primary creation modes:

### Edit Video
Import existing footage → analyze → edit.

### Create from Idea
Idea → Copilot discussion → outline → script → teleprompter → record → edit.

### Game Studio
Camera/MediaPipe-powered interactive experiences.

### Effects Studio
Discover/create camera and video effects.

Use large visual cards.

---

## 7. Project Editor

The editor should be mobile-first.

Layout:

Top:
- back
- project name
- Done

Center:
- large video preview
- play button
- time indicator

Timeline:
- video strip
- audio/music strip
- playhead

Tool row:
- Cut
- Audio
- Text
- FX
- Crop
- More

Bottom:
- prominent "Ask Copilot" bar

The AI action should visually stand apart from normal editing tools.

---

## 8. Copilot

Copilot is not a separate generic chatbot.

It is context-aware and understands the current project.

Example prompt:

"Make this a 30 second Instagram reel."

Dummy response:

I'll turn this into a social-ready Reel.

✓ Find the strongest moments
✓ Remove silence
✓ Remove filler words
✓ Reframe to 9:16
✓ Add dynamic captions

Buttons:
- Preview
- Apply
- Edit

For the demo, actions can be simulated. No backend is required.

---

## 9. Onboarding

Screens:

1. Welcome
2. Choose niche
3. Choose platforms
4. Connect/sample content
5. Creator style
6. Custom instructions
7. Finish

The demo can use fake analysis progress:

"Analyzing your content..."
"Finding recurring hooks..."
"Learning your visual style..."
"Building Creator DNA..."

Finish with:

"Your creative profile is ready."

---

## 10. Profile

Show:
- avatar
- creator name
- niche
- platforms
- Creator DNA
- style
- hooks
- custom instructions
- connected sources

Use cards and chips.

---

## 11. Visual system

### Background

Primary:
#080808

Secondary:
#111111

Elevated:
#171717

Glass:
rgba(255,255,255,0.08)

### Text

Primary:
#F7F7F2

Secondary:
#A6A6A0

Muted:
#70706B

### Accent

Primary AI accent:
#D8FF00

Use lime only for:
- primary CTA
- active AI state
- important highlights
- progress
- AI-generated actions

Do not make the entire interface neon.

### Supporting colors

Success:
#A7F36B

Warning:
#FFCC66

Danger:
#FF5C6C

Information:
#8AB4FF

---

## 12. Typography

Use:
- Inter for interface text
- optional display font with a slightly editorial feel for hero headings

Weights:
- 400 body
- 500 labels
- 600 buttons
- 700 headings

Large typography should be used sparingly.

---

## 13. Shape language

Cards:
- 20–28px radius

Buttons:
- 14–18px radius

Input:
- 18px radius

Chips:
- 999px radius

Avoid excessive borders.

Use depth through:
- tonal contrast
- blur
- subtle shadows
- media
- spacing

---

## 14. Motion

Motion should be short and purposeful.

Recommended:
- 180–240ms UI transitions
- 300–500ms page transitions
- subtle card scale on press
- bottom-sheet spring
- shimmer for AI processing

Avoid:
- excessive bouncing
- long animations
- distracting particle effects

---

## 15. AI visual language

Every AI action should have a recognizable identity:

✦ Ask Copilot
✦ Generate
✦ Auto Edit
✦ Analyze
✦ Create

Use the lime accent + sparkle glyph.

AI-generated content should be visually distinguishable from manually configured content.

---

## 16. Responsive behavior

Primary target:
- mobile portrait
- 390–430px width

Also support:
- tablet
- desktop preview for the hackathon demo

Desktop should not simply stretch mobile cards.

---

## 17. Demo principles

No backend required.

All data may be mocked.

The demo should still feel real:
- believable project names
- believable metrics
- realistic trends
- fake processing states
- interactive buttons
- simulated Copilot responses
- simulated onboarding completion

The evaluator should be able to navigate:

Onboarding
→ Home
→ Insights
→ Trend
→ Create
→ Project
→ Copilot
→ Apply
→ Home

in under two minutes.

---

## 18. Primary demo story

Recommended demo:

1. Open Creator AI.
2. Show Creator Profile.
3. Open Insights.
4. Show a niche trend.
5. Tap "Create Video".
6. Enter Project Editor.
7. Tap "Ask Copilot".
8. Ask:
   "Make this a 30 second Instagram reel."
9. Show AI proposal.
10. Tap Preview.
11. Show changed timeline/preview state.
12. Apply.
13. Return to project/home.

This demonstrates the relationship between:

Creator Profile
+ Trends
+ AI Copilot
+ Video Editor
= Creator AI.
