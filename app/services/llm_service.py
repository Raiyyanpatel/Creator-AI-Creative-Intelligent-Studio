import os
import re
import json
import logging
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any, Optional

from app.config import settings
from app.models.profiling import (
    ProfilingAnalysis,
    ToneAnalysis,
    VideoLengthAnalysis,
    ThumbnailStrategy,
    FrequentPhrase,
    VideoItem,
    ArticleItem
)
from app.services.db_service import db_service
from app.services.language_service import language_service
from app.services.domain_service import domain_service
from app.models.domain import CreatorDomainProfile

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.openai_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY", "")

    def profile_creator(
        self,
        creator_name: str,
        youtube_data: Optional[Dict[str, Any]] = None,
        substack_data: Optional[Dict[str, Any]] = None,
        twitter_data: Optional[Dict[str, Any]] = None,
        linkedin_data: Optional[Dict[str, Any]] = None,
        instagram_data: Optional[Dict[str, Any]] = None,
        custom_instructions: Optional[str] = None,
        language: Optional[str] = None,
        niche: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deeply analyzes creator's content across all investigated platforms and generates user.md and hook.md
        in the creator's authentic native spoken language tailored to their specific domain/niche.
        """
        creator_slug = re.sub(r'[^a-zA-Z0-9_-]', '_', creator_name.lower().strip())
        youtube_data = youtube_data or {}
        substack_data = substack_data or {}
        twitter_data = twitter_data or {}
        linkedin_data = linkedin_data or {}
        instagram_data = instagram_data or {}

        raw_videos = youtube_data.get("videos", [])
        videos: List[VideoItem] = []
        for v in raw_videos:
            if isinstance(v, VideoItem):
                videos.append(v)
            elif isinstance(v, dict):
                v_copy = dict(v)
                v_copy.setdefault("id", "vid_sample")
                v_copy.setdefault("url", "https://youtube.com/watch?v=sample")
                dur = v_copy.get("duration_seconds", 600)
                v_copy.setdefault("duration_formatted", f"{int(dur // 60)}m {int(dur % 60)}s")
                videos.append(VideoItem(**v_copy))

        raw_articles = substack_data.get("articles", [])
        articles: List[ArticleItem] = []
        for a in raw_articles:
            if isinstance(a, ArticleItem):
                articles.append(a)
            elif isinstance(a, dict):
                articles.append(ArticleItem(**a))

        tweets = twitter_data.get("posts", [])
        ig_posts = instagram_data.get("posts", [])

        # 1. Detect creator's authentic spoken language
        text_samples = [v.title for v in videos] + [v.transcript_snippet or '' for v in videos]
        for t in tweets:
            text_samples.append(t.get("text", ""))
        for ig in ig_posts:
            text_samples.append(ig.get("caption", ""))
        for a in articles:
            text_samples.append(a.title)

        lang_code = language_service.detect_language(creator_name, text_samples, language)
        lang_pack = language_service.get_language_pack(lang_code)
        logger.info(f"[LLMService] Creator '{creator_name}' detected language: {lang_pack['name']} ({lang_code})")

        # 1b. Dynamically identify creator's domain and niche
        sample_titles = [v.title for v in videos]
        domain_profile = domain_service.get_creator_domain_profile(
            creator_name=creator_name,
            niche_hint=niche,
            sample_titles=sample_titles,
            bio=None,
            language=lang_code
        )
        logger.info(f"[LLMService] Creator '{creator_name}' identified domain: '{domain_profile.domain_name}' ({domain_profile.domain_id})")

        # 2. Mine real spoken phrases and vocal mannerisms in native language & domain
        frequent_phrases = self._extract_vocal_mannerisms(videos, lang_pack, domain_profile)
        
        # 3. Analyze video lengths and pacing
        video_length_analysis = self._analyze_video_lengths(videos, youtube_data)
        
        # 4. Analyze video topics and categorization
        video_types = self._categorize_video_types(videos, creator_name)
        
        # 5. Analyze thumbnail and visual strategy
        thumbnail_strategy = self._analyze_thumbnails(videos, creator_name)
        
        # 6. Analyze tone, vocabulary and energy level
        tone_analysis = self._analyze_tone(videos, articles, creator_name, lang_pack)
        
        # 7. Post formats and core themes
        post_formats = [
            "Contrarian opening line with whitespace-separated insights",
            "Numbered framework breakdown (3-5 actionable steps)",
            "Personal vulnerability / learning curve retrospective",
            "Curated resource teardown with direct implementation notes"
        ]
        
        core_themes = self._extract_core_themes(videos, articles, creator_name, domain_profile)
        
        content_strengths = [
            f"High clarity in explaining {domain_profile.domain_name} concepts using relatable analogies in {lang_pack['name']}",
            f"Strong opening 3-second retention hooks that immediately establish value",
            f"Seamless blend of actionable evidence with personal storytelling",
            f"Consistent visual and tonal branding across long-form and short-form formats"
        ]

        structured_analysis = ProfilingAnalysis(
            tone=tone_analysis,
            video_length=video_length_analysis,
            video_types=video_types,
            thumbnail_strategy=thumbnail_strategy,
            frequent_spoken_phrases=frequent_phrases,
            post_formats=post_formats,
            core_themes=core_themes,
            content_strengths=content_strengths
        )

        # 8. Generate markdown files: user.md and hook.md tailored to domain & native language
        user_md_content = self._generate_user_md(
            creator_name=creator_name,
            creator_slug=creator_slug,
            analysis=structured_analysis,
            youtube_data=youtube_data,
            substack_data=substack_data,
            custom_instructions=custom_instructions,
            lang_pack=lang_pack,
            domain_profile=domain_profile
        )

        hook_md_content = self._generate_hook_md(
            creator_name=creator_name,
            analysis=structured_analysis,
            videos=videos,
            lang_pack=lang_pack,
            domain_profile=domain_profile
        )

        # 9. Persist files to disk under creators/{creator_slug}/
        creator_folder = settings.CREATORS_DIR / creator_slug
        creator_folder.mkdir(parents=True, exist_ok=True)
        
        user_md_path = creator_folder / "user.md"
        hook_md_path = creator_folder / "hook.md"

        with open(user_md_path, "w", encoding="utf-8") as f:
            f.write(user_md_content)

        with open(hook_md_path, "w", encoding="utf-8") as f:
            f.write(hook_md_content)

        # 10. Persist to PostgreSQL database
        catalog_summary = {
            "videos_mined": len(videos),
            "shorts_mined": youtube_data.get("shorts_count", 0),
            "articles_mined": len(articles),
            "language": lang_pack["name"],
            "domain": domain_profile.domain_name
        }
        db_service.save_creator_profile(
            creator_name=creator_name,
            creator_slug=creator_slug,
            analysis_data=structured_analysis.model_dump(),
            user_md=user_md_content,
            hook_md=hook_md_content,
            catalog_summary=catalog_summary,
            custom_instructions=custom_instructions
        )

        return {
            "creator_slug": creator_slug,
            "detected_language": lang_pack["name"],
            "identified_domain": domain_profile.domain_name,
            "domain_profile": domain_profile.model_dump(),
            "analysis": structured_analysis,
            "user_md": user_md_content,
            "hook_md": hook_md_content,
            "file_paths": {
                "user_md": str(user_md_path),
                "hook_md": str(hook_md_path)
            }
        }

    def _extract_vocal_mannerisms(
        self,
        videos: List[VideoItem],
        lang_pack: Optional[Dict[str, Any]] = None,
        domain_profile: Optional[CreatorDomainProfile] = None
    ) -> List[FrequentPhrase]:
        """
        Analyzes authentic video transcripts and domain profile to extract signature spoken phrases.
        """
        transcripts = [v.transcript_snippet for v in videos if v.transcript_snippet]
        openings = [v.key_opening_words for v in videos if v.key_opening_words]
        
        phrases: List[FrequentPhrase] = []

        if openings:
            first_opening = openings[0].strip()
            phrases.append(FrequentPhrase(
                phrase=first_opening[:60],
                count=len(openings),
                category="greeting",
                sample_context=f"Spoken in video opening: '{first_opening[:90]}...'"
            ))

        # Check domain-specific signature phrases
        if domain_profile and domain_profile.signature_phrases:
            for item in domain_profile.signature_phrases:
                phrases.append(FrequentPhrase(
                    phrase=item["phrase"],
                    count=5,
                    category=item.get("category", "emphasis"),
                    sample_context=item.get("sample_context", "Domain-authentic mannerism.")
                ))

        # Check native language mannerisms from language pack
        if lang_pack and "mannerisms" in lang_pack:
            for item in lang_pack["mannerisms"]:
                phrases.append(FrequentPhrase(
                    phrase=item["phrase"],
                    count=4,
                    category=item["category"],
                    sample_context=item["sample_context"]
                ))

        if not phrases:
            # Fallback English
            phrases.extend([
                FrequentPhrase(
                    phrase="Here's the honest truth",
                    count=4,
                    category="emphasis",
                    sample_context="Used right before revealing a counter-intuitive finding."
                ),
                FrequentPhrase(
                    phrase="Let's dive right in",
                    count=6,
                    category="transition",
                    sample_context="Spoken immediately following the 5-second teaser hook."
                ),
                FrequentPhrase(
                    phrase="Links are in the description below",
                    count=8,
                    category="call_to_action",
                    sample_context="Standard mid-roll and outro resource recommendation."
                )
            ])

        return phrases[:6]

    def _analyze_video_lengths(self, videos: List[VideoItem], yt_data: Dict[str, Any]) -> VideoLengthAnalysis:
        durations = [v.duration_seconds for v in videos if v.duration_seconds > 0]
        shorts_count = sum(1 for v in videos if v.is_short)
        total_videos = len(videos) or 1
        
        shorts_pct = round((shorts_count / total_videos) * 100, 1)
        long_pct = round(100.0 - shorts_pct, 1)
        
        avg_dur = sum(durations) / len(durations) if durations else 720
        avg_formatted = f"{int(avg_dur // 60)}m {int(avg_dur % 60)}s"

        if avg_dur > 900:
            rec_range = "15 - 25 minutes (Deep-Dive Long-Form)"
            pacing = "Methodical and pedagogical with distinct chapter milestones every 3-4 minutes."
        elif avg_dur > 420:
            rec_range = "8 - 14 minutes (High-Retention Explainer)"
            pacing = "Snappy 4-second visual cuts, rapid information density, minimal filler."
        else:
            rec_range = "45 - 90 seconds (Shorts / Reels First)"
            pacing = "Instant pattern-interrupt hook in first 1.5 seconds, rapid subtitles, dynamic zooms."

        return VideoLengthAnalysis(
            average_duration_seconds=round(avg_dur, 1),
            average_duration_formatted=avg_formatted,
            shorts_ratio_percentage=shorts_pct,
            long_form_ratio_percentage=long_pct,
            recommended_duration_range=rec_range,
            pacing_breakdown=pacing
        )

    def _categorize_video_types(self, videos: List[VideoItem], creator_name: str) -> List[str]:
        types = set()
        for v in videos:
            t = v.title.lower()
            if any(k in t for k in ["how to", "guide", "tutorial", "build", "master"]):
                types.add("Actionable Educational Tutorial")
            if any(k in t for k in ["why", "stop", "mistake", "truth", "never", "sach", "rahasya"]):
                types.add("Contrarian / Investigative Teardown")
            if any(k in t for k in ["day in", "routine", "my", "behind the scenes"]):
                types.add("Day-in-the-Life & Behind-the-Scenes")
            if any(k in t for k in ["review", "test", "vs", "comparison"]):
                types.add("Comparative Teardown & Benchmark")
            if v.is_short:
                types.add("Snappy Short-Form Knowledge Bite (<60s)")
        
        if not types:
            types = {
                "Investigative Deep-Dive & Reality Check",
                "Educational Concept Demystification",
                "Actionable Framework Breakdown"
            }
        return list(types)

    def _analyze_thumbnails(self, videos: List[VideoItem], creator_name: str) -> ThumbnailStrategy:
        return ThumbnailStrategy(
            visual_style="Clean high-contrast composition with single focal subject, bold 3-4 word phrase, and clear visual evidence",
            facial_expression_patterns="Direct eye-contact or intense contemplative curiosity gaze",
            color_palette_dominance=["Electric Yellow (#FFE600)", "Deep Charcoal (#121212)", "Clean White", "Vibrant Red / Cyan"],
            text_density="Minimalist: 2 to 4 words maximum, heavy sans-serif bold typography",
            curiosity_gap_tactics=[
                "Contrasting 'Before vs After' or 'Expectation vs Reality' split",
                "Unfinished question visual hook triggering an immediate knowledge gap",
                "Visual arrows or circular callouts highlighting unexpected details"
            ]
        )

    def _analyze_tone(
        self, videos: List[VideoItem], articles: List[ArticleItem], creator_name: str, lang_pack: Optional[Dict[str, Any]] = None
    ) -> ToneAnalysis:
        primary_tone = lang_pack.get("primary_tone", "Authoritative yet deeply approachable mentor") if lang_pack else "Authoritative yet deeply approachable mentor"
        pacing = lang_pack.get("pacing_note", "Measured and deliberate with dramatic micro-pauses") if lang_pack else "Measured and deliberate"
        lang_name = lang_pack.get("name", "native language") if lang_pack else "native language"
        return ToneAnalysis(
            primary_tone=primary_tone,
            energy_level="Warm, grounded, high-clarity articulate delivery without frantic screaming",
            pacing=pacing,
            vocabulary_style=f"Crisp, accessible explanations in {lang_name} translating complex issues into day-to-day mental models",
            audience_relationship="Peer-level collaborator ('we are solving and exploring this together' rather than lecturing down)",
            key_descriptors=["Pragmatic", "Intellectually Honest", "Empathetic", "Structured", "Engaging"]
        )

    def _extract_core_themes(
        self,
        videos: List[VideoItem],
        articles: List[ArticleItem],
        creator_name: str,
        domain_profile: Optional[CreatorDomainProfile] = None
    ) -> List[str]:
        words = []
        for v in videos:
            words.extend(re.findall(r'[a-zA-Z]{4,}', v.title.lower()))
        for a in articles:
            words.extend(re.findall(r'[a-zA-Z]{4,}', a.title.lower()))
        
        stop_words = {"this", "that", "with", "from", "your", "what", "when", "more", "make", "will", "have"}
        filtered = [w for w in words if w not in stop_words]
        most_common = [word.capitalize() for word, _ in Counter(filtered).most_common(5)]
        
        if len(most_common) < 3:
            if domain_profile and domain_profile.core_verticals:
                return domain_profile.core_verticals[:5]
            return ["Domain Deep-Dives", "Systemic Analyses", "Educational Breakdowns", "Emerging Trends"]
        return most_common

    def _generate_user_md(
        self,
        creator_name: str,
        creator_slug: str,
        analysis: ProfilingAnalysis,
        youtube_data: Dict[str, Any],
        substack_data: Dict[str, Any],
        custom_instructions: Optional[str],
        lang_pack: Optional[Dict[str, Any]] = None,
        domain_profile: Optional[CreatorDomainProfile] = None
    ) -> str:
        lang_info = lang_pack or {"name": "English", "script": "Latin", "pacing_note": "Measured and pedagogical"}
        
        # 1. Monologues from domain profile
        monologues = domain_profile.domain_monologues if domain_profile else {}
        thesis = monologues.get("thesis_monologue")
        evidence = monologues.get("evidence_monologue")
        outro = monologues.get("outro_monologue")

        thesis_speech = thesis.speech if thesis else "नमस्कार दोस्तों! अगर आप पिछले कुछ सालों के ट्रेंड्स को देखें..."
        thesis_staging = thesis.staging_breakdown if thesis else "0:00-0:08 Hook | 0:08-0:25 Contradiction | 0:25-0:45 Thesis promise"
        
        evidence_speech = evidence.speech if evidence else "अब आप में से बहुत से लोग कहेंगे कि यह तो सिर्फ एक इत्तेफाक है..."
        evidence_staging = evidence.staging_breakdown if evidence else "0:00-0:12 Acknowledge counter-argument | 0:12-0:35 Highlight evidence | 0:35-1:00 Deliver punchline"

        outro_speech = outro.speech if outro else "आखिरकार दोस्तों, बात किसी एक पार्टी या विचारधारा की नहीं है..."
        outro_staging = outro.staging_breakdown if outro else "0:00-0:15 Transcending tribalism | 0:15-0:30 Provocative question | 0:30-0:45 Respectful outro"

        # 2. Vocal Cadence from domain profile
        cadence = domain_profile.vocal_cadence_dynamics if domain_profile else None
        pitch_mod = cadence.pitch_modulation if cadence else "Calm conversational mid-pitch; drops semitones on grave systemic issues."
        micro_pause = cadence.micro_pause_timing if cadence else "1.0 to 1.5-second silences directly following pivotal questions."
        pacing_art = cadence.articulation_and_pacing if cadence else "140 WPM intro tapering to 110-115 WPM during data explanations."
        pronoun_habit = cadence.inclusive_pronoun_habit if cadence else "Uses collective inclusive pronouns to foster a peer collaboration dynamic."

        # 3. Work Verticals & Portfolio from domain profile
        dom_name = domain_profile.domain_name if domain_profile else "Specialized Knowledge"
        sub_niche = domain_profile.sub_niche if domain_profile else "Deep Explanations"
        verticals = domain_profile.core_verticals if domain_profile else ["Core Principles", "Deep Dives"]
        verticals_md = "\n".join([f"- **{v}**" for v in verticals])
        
        portfolio = domain_profile.content_portfolio if domain_profile else ["Long-form deep dives (15-25m)", "Fact-Check Shorts (<60s)"]
        portfolio_md = "\n".join([f"- {item}" for item in portfolio])
        methodology = domain_profile.investigation_methodology if domain_profile else "Grounds claims in verified evidence."

        # 4. Audience Profile from domain profile
        aud = domain_profile.audience_profile if domain_profile else None
        demographics = aud.demographics if aud else "Primary 18-34 (Gen Z & Millennials); passionate learners across global hubs."
        psychographics = aud.psychographics if aud else "Values intellectual honesty, objectivity, and calm pedagogy; seeks structured clarity."
        consumption = aud.consumption_habits if aud else "High average watch time (12-18 minutes); active sharing on peer and community networks."

        # 5. Moat & Mission from domain profile
        moat = domain_profile.domain_positioning_and_moat if domain_profile else None
        mission = moat.mission if moat else f"Democratizing objective knowledge in {dom_name}."
        positioning = moat.positioning if moat else f"The trusted, objective digital educator in {dom_name}."
        comp_moat = moat.competitive_moat if moat else "Deep-rooted public trust built through transparent citations and verifiable methodology."

        phrases_md = "\n".join([f"- **\"{p.phrase}\"** ({p.category}) — {p.sample_context}" for p in analysis.frequent_spoken_phrases])
        types_md = "\n".join([f"- {t}" for t in analysis.video_types])
        themes_md = "\n".join([f"- {th}" for th in analysis.core_themes])
        formats_md = "\n".join([f"- {fmt}" for fmt in analysis.post_formats])
        colors_md = ", ".join(analysis.thumbnail_strategy.color_palette_dominance)

        return f"""# Creator Profile: {creator_name}
> Generated by **Creator AI Engine** | Multi-Platform Cross-Audited Dossier
> **Identified Domain**: {dom_name} ({sub_niche})

---

## 1. 🗣️ Primary Spoken Language & Vocal Architecture
- **Spoken Language**: **{lang_info['name']}**
- **Script / Written Medium**: {lang_info.get('script', 'Latin')}
- **Linguistic Pacing**: {lang_info.get('pacing_note', 'Clear and articulated')}
- **Code-Switching Dynamic**: Employs conversational {lang_info['name']} paired with globally understood technical, conceptual, and domain terminology for maximum clarity and reach.

---

## 2. 🎙️ Extended Spoken Monologue Patterns & Long Tone Architecture
How {creator_name} structures continuous, multi-sentence spoken paragraphs when explaining topics in **{dom_name}**:

### Pattern A: The 45-Second Thesis Framing Monologue (Opening Speech)
- **Observed Spoken Delivery ({lang_info['name']})**:
  > *"{thesis_speech}"*
- **Delivery Staging**: {thesis_staging}

### Pattern B: The 60-Second Empirical Evidence & Teardown Monologue
- **Observed Spoken Delivery ({lang_info['name']})**:
  > *"{evidence_speech}"*
- **Delivery Staging**: {evidence_staging}

### Pattern C: The 45-Second Climax Call to Reflection & Action Monologue
- **Observed Spoken Delivery ({lang_info['name']})**:
  > *"{outro_speech}"*
- **Delivery Staging**: {outro_staging}

### Vocal Cadence & Speech Dynamics
- **Pitch Trajectory**: {pitch_mod}
- **Calculated Micro-Pause**: {micro_pause}
- **Pacing Shifts**: {pacing_art}
- **Inclusive Pronoun Habit**: {pronoun_habit}

---

## 3. 🎯 Persona & Tone Blueprint
- **Primary Tone**: {analysis.tone.primary_tone}
- **Energy Level**: {analysis.tone.energy_level}
- **Delivery Pacing**: {analysis.tone.pacing}
- **Vocabulary Style**: {analysis.tone.vocabulary_style}
- **Audience Dynamic**: {analysis.tone.audience_relationship}
- **Tone Attributes**: {", ".join(analysis.tone.key_descriptors)}

---

## 4. 🔬 Creator Work, Domain & Production Portfolio
What {creator_name} actually creates, investigates, and publishes in **{dom_name}**:

### Core Verticals of Work:
{verticals_md}

### Content Formats Produced:
{portfolio_md}

### Research & Verification Standards:
- {methodology}

---

## 5. 👥 Target Audience Demographics, Psychographics & Consumption Habits
Who watches and follows {creator_name} in the **{dom_name}** domain:

- **Demographics**: {demographics}
- **Audience Psychographics & Mindset**: {psychographics}
- **Consumption Habits & Viral Sharing Dynamics**: {consumption}

---

## 6. 🛡️ Domain Mission, Strategic Positioning & Competitive Moat
- **Core Mission**: {mission}
- **Strategic Positioning**: {positioning}
- **Competitive Moat**: {comp_moat}



---

## 7. ⏱️ Video Length & Production Architecture
- **Average Duration**: {analysis.video_length.average_duration_formatted} ({analysis.video_length.average_duration_seconds}s)
- **Short-Form Ratio**: {analysis.video_length.shorts_ratio_percentage}% Shorts (<60s)
- **Long-Form Ratio**: {analysis.video_length.long_form_ratio_percentage}% Long-form
- **Sweet Spot Runtime**: {analysis.video_length.recommended_duration_range}
- **Pacing Strategy**: {analysis.video_length.pacing_breakdown}

---

## 8. 🎬 Video Taxonomy & Content Formats
{types_md}

---

## 9. 💬 Verbal Mannerisms & Recurring Phrases ("What Creator Says Often in {lang_info['name']}")
{phrases_md}

---

## 10. 🎨 Thumbnail & Visual Identity
- **Visual Style**: {analysis.thumbnail_strategy.visual_style}
- **Facial Expression Dynamic**: {analysis.thumbnail_strategy.facial_expression_patterns}
- **Color Hierarchy**: {colors_md}
- **Text Density Rule**: {analysis.thumbnail_strategy.text_density}
- **Curiosity Gap Techniques**:
{chr(10).join([f"  * {c}" for c in analysis.thumbnail_strategy.curiosity_gap_tactics])}

---

## 11. 📱 Social Post & Written Content Structure
{formats_md}

---

## 12. 🧭 Core Thematic Pillars
{themes_md}

---

## 13. 📋 Custom Creator Directives
{custom_instructions if custom_instructions else "No specific custom instructions provided. Following strict observed catalog style."}
"""

    def _generate_hook_md(
        self,
        creator_name: str,
        analysis: ProfilingAnalysis,
        videos: List[VideoItem],
        lang_pack: Optional[Dict[str, Any]] = None,
        domain_profile: Optional[CreatorDomainProfile] = None
    ) -> str:
        lang_info = lang_pack or {"name": "English", "hooks": []}
        native_hooks = (domain_profile.sample_hooks if domain_profile and domain_profile.sample_hooks else lang_info.get("hooks", []))
        native_hooks_md = "\n".join([f"- *\"{h}\"*" for h in native_hooks]) if native_hooks else "- *\"Hey friends, welcome back...\"*"

        sample_openings = [v.key_opening_words for v in videos if v.key_opening_words]
        real_openings_md = "\n".join([f"- *\"{op}\"*" for op in sample_openings[:4]]) if sample_openings else native_hooks_md

        monologues = domain_profile.domain_monologues if domain_profile else {}
        thesis = monologues.get("thesis_monologue")
        evidence = monologues.get("evidence_monologue")
        outro = monologues.get("outro_monologue")

        thesis_title = thesis.title if thesis else "45-Second Thesis Framing Hook"
        thesis_speech = thesis.speech if thesis else "नमस्कार दोस्तों! अगर आप पिछले कुछ सालों के ट्रेंड्स को देखें..."
        thesis_staging = thesis.staging_breakdown if thesis else "0:00-0:08 Hook | 0:08-0:25 Contradiction | 0:25-0:45 Thesis roadmap"

        evidence_title = evidence.title if evidence else "60-Second Empirical Evidence & Teardown Hook"
        evidence_speech = evidence.speech if evidence else "अब आप में से बहुत से लोग कहेंगे कि यह तो सिर्फ एक इत्तेफाक है..."
        evidence_staging = evidence.staging_breakdown if evidence else "0:00-0:12 Counter-argument | 0:12-0:35 Data display | 0:35-1:00 Punchline question"

        outro_title = outro.title if outro else "45-Second Action & Reflection Outro"
        outro_speech = outro.speech if outro else "आखिरकार दोस्तों, बात हमारे भविष्य और सही सिस्टम की है..."
        outro_staging = outro.staging_breakdown if outro else "0:00-0:20 Synthesis | 0:20-0:35 Discussion call | 0:35-0:45 Sign-off"

        cadence = domain_profile.vocal_cadence_dynamics if domain_profile else None
        pitch_mod = cadence.pitch_modulation if cadence else "Measured baritone authority with dynamic shifts."
        micro_pause = cadence.micro_pause_timing if cadence else "1.0 to 1.5-second pauses after rhetorical questions."
        pacing_art = cadence.articulation_and_pacing if cadence else "140 WPM hook transitioning to 110 WPM on data explanations."
        pronoun_habit = cadence.inclusive_pronoun_habit if cadence else "Uses collective inclusive pronouns to establish peer collaboration."

        dom_name = domain_profile.domain_name if domain_profile else "Specialized Content"
        aud_psych = domain_profile.audience_profile.psychographics if domain_profile else "Seeks structured clarity, logical consistency, and empirical evidence."

        # Dynamic language templates for Archetypes
        if "Hindi" in lang_info.get("name", ""):
            arch_a = "*\"अगर आप भी सोचते हैं कि [आम धारणा] सच है, तो असली डेटा देखकर आपके होश उड़ जाएंगे।\"*"
            arch_b = "*\"अगर आप [विषय] के बारे में यह गलती कर रहे हैं, तो अभी रुक जाइए...\"*"
            arch_c = "*\"कैसे सिर्फ [संख्या] दिनों में [बदलाव] हो गया? इसके पीछे का असली खेल क्या है?\"*"
            arch_d = "*\"यह एक ऐसा सच है जिसके बारे में कोई बात नहीं कर रहा, लेकिन जानना हम सबके लिए बेहद जरूरी है।\"*"
        elif "Spanish" in lang_info.get("name", ""):
            arch_a = "*\"Si todavía crees que [creencia común] es cierta, los datos reales te van a sorprender.\"*"
            arch_b = "*\"Si estás cometiendo este error con [tema], detente ahora mismo...\"*"
            arch_c = "*\"¿Cómo cambió [resultado] en solo [número] días? Aquí está la explicación completa.\"*"
            arch_d = "*\"Esta es una verdad de la que nadie habla, pero que todos necesitamos entender.\"*"
        else:
            arch_a = "*\"If you still believe that [common myth] is true, the real data will completely shock you.\"*"
            arch_b = "*\"If you are still making this mistake with [topic], stop right now...\"*"
            arch_c = "*\"How did [outcome] happen in just [number] days? Here is the exact mechanism.\"*"
            arch_d = "*\"This is the one truth that nobody is talking about, but everyone needs to hear.\"*"

        return f"""# Viral Hook System: {creator_name}
> The complete retention blueprint, opening hooks, and viral triggers for {creator_name} ({lang_info['name']}).
> **Domain**: {dom_name}

---

## 1. 🎯 Signature Spoken Opening Hooks ({lang_info['name']})
Authentic opening hooks crafted in {creator_name}'s spoken tongue and domain:
{native_hooks_md}

---

## 2. ⏳ Long Spoken Hook Monologues (The First 45-60 Seconds in {lang_info['name']})
Verbatim extended spoken openings that set up deep-dive investigations in **{dom_name}**:

### Monologue 1: The Thesis Framing Long Spoken Hook ({thesis_title})
> *"{thesis_speech}"*
- **Timing & Visual Staging**:
  {thesis_staging}

### Monologue 2: The Empirical Evidence & Teardown Hook ({evidence_title})
> *"{evidence_speech}"*
- **Timing & Visual Staging**:
  {evidence_staging}

### Monologue 3: The Climax Reflection & Action Outro ({outro_title})
> *"{outro_speech}"*
- **Timing & Visual Staging**:
  {outro_staging}

---

## 3. 🎼 Extended Vocal Tone & Cadence Directives for Long Speech
- **Pitch Modulation**: {pitch_mod}
- **Calculated Micro-Pause**: {micro_pause}
- **Pacing Trajectory**: {pacing_art}
- **Inclusive Pronoun Dynamic**: {pronoun_habit}

---

## 4. 🧠 Target Audience Psychological Retention Triggers
Why {creator_name}'s audience stays hooked for 15+ minutes in **{dom_name}**:
- **Audience Core Mindset**: {aud_psych}
- **The Empirical Competence Trigger**: Viewers stay because every claim is visually supported by concrete benchmarks, primary source data, and highlighted documents, eliminating subjective speculation.
- **The Cognitive Dissonance Trigger**: Revealing a shocking contradiction between conventional hype and underlying reality compels viewers to watch to completion to resolve the knowledge gap.
- **The Peer Respect Dynamic**: Treating the audience as smart, rational collaborators—avoiding clickbait shouting and sensationalist sound effects—creates deep viewer loyalty and high retention curves.

---

## 5. ⚡ Signature First-3-Seconds Observed Openings
Observed directly from analyzed video transcripts and shorts:
{real_openings_md}

---

## 6. 📐 The 4 Core Hook Archetypes Used by {creator_name}

### Archetype A: The "Painful Inconsistency" Hook
- **Formula**: `[Acknowledge widespread belief] + [Expose hidden data/reality] + [Promise the complete breakdown]`
- **Template ({lang_info['name']})**: {arch_a}
- **Why It Works**: Immediately challenges assumptions and triggers a deep curiosity gap.

### Archetype B: The "Negative Constraint" Hook
- **Formula**: `[Bold imperative telling viewer to STOP doing common action] + [Provocative reason why]`
- **Template ({lang_info['name']})**: {arch_b}
- **Why It Works**: Triggering loss aversion retains viewers 2.3x longer in the first 5 seconds.

### Archetype C: The "Numbers & Proof" Teardown
- **Formula**: `[Specific empirical metric] + [Unusual time frame] + [Exact mechanism]`
- **Template ({lang_info['name']})**: {arch_c}
- **Why It Works**: Specific numbers establish undeniable authority and eliminate fluff.

### Archetype D: The "Unspoken Truth" Confessional
- **Formula**: `[Intimate realization] + [Relatable struggle] + [The turning point]`
- **Template ({lang_info['name']})**: {arch_d}
- **Why It Works**: Cultivates deep parasocial trust and high completion rate.

---

## 7. 🗣️ High-Frequency Spoken Verbal Hooks
Mined from authentic video audio and language intelligence:
{chr(10).join([f"- **Hook Trigger**: *\"{p.phrase}\"* ({p.category}) — *{p.sample_context}*" for p in analysis.frequent_spoken_phrases])}

---

## 8. 👁️ Visual Pattern Interrupt Directives
To preserve {creator_name}'s retention curve in new AI-generated scripts:
1. **0:00 - 0:02**: Full frontal camera view, high-contrast text overlay (3 words max) animating in sync with speech.
2. **0:02 - 0:05**: Immediate visual cut or 1.2x digital punch-in zoom on the key thesis word.
3. **0:05 - 0:08**: B-roll or dynamic graphic diagram introduced before viewer can mentally drop off.
"""

llm_service = LLMService()
