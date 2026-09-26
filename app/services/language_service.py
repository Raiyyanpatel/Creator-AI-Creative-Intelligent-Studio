"""
Language Intelligence Service
=============================
Detects creator's native spoken language and provides authentic cultural and
linguistic spoken mannerisms, catchphrases, and hook templates across languages
(Hindi / Hinglish, English, Spanish, German, French, etc.).
"""

import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# Linguistic dictionaries for authentic spoken habits and signature speech patterns
LANGUAGE_PATTERNS: Dict[str, Dict[str, Any]] = {
    "hi": {
        "name": "Hindi / Hinglish (हिंदी / English mix)",
        "script": "Devanagari & Romanized Hindi",
        "primary_tone": "Authoritative yet deeply approachable Hindi educator & civic communicator",
        "pacing_note": "Clear, articulated conversational Hindi with deliberate pauses before core thesis points",
        "mannerisms": [
            {
                "phrase": "नमस्कार दोस्तों, स्वागत है आपका एक और नए वीडियो में",
                "romanized": "Namaskar dosto, swagat hai aapka ek aur naye video mein",
                "category": "greeting",
                "sample_context": "Iconic opening greeting setting an objective, calm, and grounded tone."
            },
            {
                "phrase": "सच तो यह है कि...",
                "romanized": "Sach to yeh hai ki...",
                "category": "emphasis",
                "sample_context": "Spoken right before debunking a popular misconception or presenting official statistics."
            },
            {
                "phrase": "आइए इसको गहराई से समझते हैं",
                "romanized": "Aaiye isko gehrai se samajhte hain",
                "category": "transition",
                "sample_context": "Used to transition from the introductory hook into structured chapter breakdowns."
            },
            {
                "phrase": "अब असली सवाल यह उठता है कि...",
                "romanized": "Ab asli sawal yeh uthta hai ki...",
                "category": "transition",
                "sample_context": "Pivotal question hook challenging the viewer's preconceived notions."
            },
            {
                "phrase": "कमेंट करके जरूर बताइए कि आपकी इस पर क्या राय है",
                "romanized": "Comment karke zaroor bataiye ki aapki is par kya raye hai",
                "category": "call_to_action",
                "sample_context": "Closing call to action encouraging civic debate and engagement."
            },
            {
                "phrase": "यह बात 99% लोग नहीं जानते",
                "romanized": "Yeh baat 99% log nahi jaante",
                "category": "emphasis",
                "sample_context": "Pattern-interrupt phrase used to highlight hidden systemic facts."
            }
        ],
        "hooks": [
            "क्या आपने कभी सोचा है कि {topic} के पीछे की असली सच्चाई क्या है?",
            "सरकार और मुख्यधारा मीडिया आपको {topic} के बारे में यह क्यों नहीं बता रहे?",
            "यह एक बहुत बड़ा झूठ है जो सालों से हम सबको बताया जा रहा है...",
            "आज के इस वीडियो में हम {topic} का पूरा सच डेटा और सबूतों के साथ सामने लाएंगे।",
            "अगर आप भी सोचते हैं कि {topic} सिर्फ एक छोटी सी बात है, तो यह वीडियो अंत तक जरूर देखें।"
        ],
        "long_speech_monologues": {
            "thesis_monologue": {
                "title": "45-Second Thesis Framing Monologue (Opening Speech)",
                "speech": "नमस्कार दोस्तों! अगर आप पिछले कुछ सालों के ट्रेंड्स को देखें तो आपको एक बात साफ नजर आएगी कि हर कोई इस बारे में बात कर रहा है। लेकिन क्या कभी आपने गहराई से सोचा है कि इसके पीछे का असली खेल क्या है? सरकार और मुख्यधारा मीडिया हमें कुछ और बता रहे हैं, जबकि असल डेटा और जमीनी हकीकत कुछ बिल्कुल अलग बयां कर रही है। आज के इस वीडियो में हम बिना किसी बायस के, सिर्फ फैक्ट्स, डेटा और ऑफिशियल रिपोर्ट्स के साथ इस पूरे मुद्दे की परतें खोलेंगे। अंत तक जरूर देखिएगा ताकि आपको पूरी सच्चाई समझ आए।",
                "staging_breakdown": "0:00-0:08 High-clarity greeting & widespread belief | 0:08-0:25 Contradiction & official data teaser | 0:25-0:45 Unbiased mission statement & invitation into deep dive."
            },
            "evidence_monologue": {
                "title": "60-Second Empirical Evidence & Debunking Monologue",
                "speech": "अब आप में से बहुत से लोग कहेंगे कि यह तो सिर्फ एक इत्तेफाक है, या फिर यह समस्या सिर्फ हमारे देश में है। लेकिन जरा ठहरिए। अगर आप इस सरकारी रिपोर्ट के पेज नंबर 42 को देखें, तो साफ लिखा है कि पिछले पांच सालों में यह समस्या घटने के बजाय 40% बढ़ गई है। दूसरा बड़ा सबूत है यह इंटरनेशनल इंडेक्स, जहां हमारी रैंकिंग लगातार नीचे गिर रही है। और तीसरा सबसे बड़ा कारण है वो छुपा हुआ नियम जिसके बारे में मुख्यधारा की मीडिया में एक भी डिबेट नहीं हुई। तो असली सवाल यह नहीं है कि ऐसा क्यों हुआ, बल्कि असली सवाल यह उठता है कि इसे हम सब से छुपाया क्यों गया?",
                "staging_breakdown": "0:00-0:12 Acknowledge counter-argument | 0:12-0:35 Display on-screen official gazette/index with highlighted yellow box | 0:35-1:00 Deliver the core investigative question with a 1.2s micro-pause."
            },
            "outro_monologue": {
                "title": "45-Second Climax Call to Reflection & Civic Responsibility Monologue",
                "speech": "आखिरकार दोस्तों, बात किसी एक पार्टी या किसी एक विचारधारा की नहीं है। बात है हमारे देश के भविष्य की, हमारे समाज की और आने वाली पीढ़ी की। जब तक हम जागरूक नागरिक बनकर सही सवाल नहीं पूछेंगे, तब तक कोई भी जमीनी बदलाव मुमकिन नहीं है। नीचे कमेंट करके जरूर बताइए कि इस पूरे विश्लेषण पर आपकी अपनी क्या राय है? और इस वीडियो को अपने दोस्तों और परिवार के साथ जरूर शेयर कीजिए ताकि सच हर नागरिक तक पहुंचे। मिलते हैं अगले वीडियो में, बहुत-बहुत शुक्रिया।",
                "staging_breakdown": "0:00-0:15 Transcending political tribalism to focus on collective civic future | 0:15-0:30 Provocative question to viewer | 0:30-0:45 Respectful outro with calm, warm sign-off."
            }
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Begins at a calm, conversational mid-frequency (grounded and pedagogical); subtly drops 2-3 semitones when introducing grave systemic failures; elevates slightly with measured intensity during evidence presentation before returning to a steady, thoughtful baseline.",
            "micro_pause_timing": "Inserts deliberate 1.0 to 1.5-second complete audio silences directly following pivotal questions ('लेकिन सवाल यह है कि...') or surprising statistics, allowing the cognitive dissonance to register before presenting charts.",
            "articulation_and_pacing": "Starts at an energetic 135-145 words per minute during the hook; steadily decelerates to 110-115 WPM during complex data explanations to ensure total conceptual comprehension.",
            "inclusive_pronoun_habit": "Consistently employs inclusive plural pronouns ('हम सब', 'आप और मैं', 'हमारे देश में') to establish a collaborative peer dynamic rather than preaching down to the viewer."
        },
        "domain_and_work_profile": {
            "core_verticals": [
                "Civic Rights, Electoral Systems & Democratic Awareness",
                "Environmental Science, Climate Crisis & Pollution Audits",
                "Geopolitics, International Diplomacy & Historical Root Causes",
                "Public Policy, Economic Disparity & Healthcare Infrastructure",
                "Scientific Thinking, Critical Rationality & Media Literacy"
            ],
            "content_portfolio": [
                "15 to 25-Minute Long-Form Deep-Dive Investigative Video Essays",
                "30 to 60-Second Fact-Check Shorts & Explanatory Reels",
                "Structured Academy Masterclasses (Critical Thinking, Video Editing, Time Mastery)",
                "On-Site Travel Vlogs & Ground-Reality Citizen Documentaries"
            ],
            "investigation_methodology": "Grounds every claim in official documentation: government gazettes, parliamentary answers, Right to Information (RTI) filings, peer-reviewed scientific journals, and validated international indices (World Bank, UN, IPCC). Highlights exact PDF excerpts on screen with yellow markers."
        },
        "audience_profile": {
            "demographics": "Primary 18-34 years (Gen Z and Millennials), secondary 35-50 years; college students, working professionals, educators, urban and Tier 1/2 citizens, and an extensive global Indian diaspora (GCC, North America, Europe).",
            "psychographics": "Values intellectual honesty, objectivity, and calm pedagogy; experiences severe fatigue with sensationalist TV shouting matches; seeks structured clarity, logical consistency, and empirical evidence to understand modern systems.",
            "consumption_habits": "Exceptionally high average view duration (12-18 minutes); active participant in structured comment debates; frequently shares videos on family and peer WhatsApp groups and social networks as educational reference material."
        },
        "domain_positioning_and_moat": {
            "mission": "Democratizing objective knowledge by translating high-complexity legal, scientific, and geopolitical issues into accessible, engaging citizen mental models.",
            "positioning": "The trusted, objective digital educator who brings calm, rigorous journalism to an internet saturated with algorithmic noise and sensationalism.",
            "competitive_moat": "Deep-rooted public trust established through transparent source citation (every link provided in description), verifiable methodology, and refusal to adopt sensationalist screaming."
        },
        "sample_topics_format": "हिंदी / Hinglish mein facts aur ground reality analysis"
    },
    "es": {
        "name": "Spanish (Español)",
        "script": "Latin",
        "primary_tone": "Enérgico, empático y estructurado",
        "pacing_note": "Ritmo dinámico y vocalización clara",
        "mannerisms": [
            {
                "phrase": "Hola a todos y bienvenidos de nuevo al canal",
                "category": "greeting",
                "sample_context": "Apertura cálida y directa a la comunidad."
            },
            {
                "phrase": "La verdad es que nadie te está contando esto...",
                "category": "emphasis",
                "sample_context": "Punto de giro antes de revelar datos críticos."
            },
            {
                "phrase": "Vamos a analizar esto paso a paso",
                "category": "transition",
                "sample_context": "Transición estructurada a la explicación central."
            },
            {
                "phrase": "Déjame saber en los comentarios qué opinas tú",
                "category": "call_to_action",
                "sample_context": "Llamada a la interacción al final del video."
            }
        ],
        "hooks": [
            "¿Alguna vez te has preguntado cuál es la verdadera razón detrás de {topic}?",
            "El 99% de las personas están equivocadas sobre {topic}...",
            "La verdad oculta sobre {topic} que nadie se atreve a decir en voz alta."
        ],
        "long_speech_monologues": {
            "thesis_monologue": {
                "title": "45-Second Thesis Framing Monologue",
                "speech": "Hola a todos y bienvenidos de nuevo. En los últimos años, se ha creado una narrativa masiva sobre este tema en todos los medios. Pero cuando dejamos de lado el sensacionalismo y examinamos los datos oficiales y los estudios independientes, la realidad sobre el terreno es completamente distinta. En este video, vamos a analizar paso a paso, con documentos y auditorías en mano, qué es lo que realmente está ocurriendo y qué consecuencias directas tiene para todos nosotros. Quédate hasta el final para entender la historia completa.",
                "staging_breakdown": "0:00-0:08 Apertura empática | 0:08-0:25 Contraste de datos oficiales vs narrativa popular | 0:25-0:45 Promesa de análisis riguroso y objetivo."
            },
            "evidence_monologue": {
                "title": "60-Second Empirical Evidence Monologue",
                "speech": "Muchos afirman que esto es simplemente un problema inevitable o un error administrativo. Pero los datos demuestran lo contrario. En la página 35 del informe oficial de auditoría, se revela que los fondos fueron desviados sistemáticamente sin supervisión pública. Además, los índices internacionales confirman un deterioro acelerado en los últimos tres años. La verdadera pregunta que debemos hacernos no es si el sistema falló, sino quién se benefició mientras la opinión pública miraba hacia otro lado.",
                "staging_breakdown": "0:00-0:15 Desarticulación del mito | 0:15-0:40 Presentación de informes con gráficos destacados | 0:40-1:00 Pregunta retórica de alto impacto."
            },
            "outro_monologue": {
                "title": "45-Second Reflection & Engagement Monologue",
                "speech": "Al final del día, los cambios reales solo ocurren cuando una sociedad informada comprende los mecanismos detrás del poder y exige transparencia. Déjame saber en los comentarios qué opinas sobre estos datos y cómo ves esta situación. Comparte este análisis con tus amigos y familiares para que más personas conozcan la realidad verificada. Nos vemos en el próximo video, muchas gracias por estar aquí.",
                "staging_breakdown": "0:00-0:20 Conclusión reflexiva ciudadana | 0:20-0:45 Llamado a compartir y debate constructivo."
            }
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Tono empático, ritmo articulado y seguro; modulación descendente en revelaciones críticas para añadir peso testimonial.",
            "micro_pause_timing": "Pausas de 1 segundo tras plantear contradicciones evidentes para generar expectación reflexiva.",
            "articulation_and_pacing": "Cadencia fluida de 140 palabras por minuto reducida a 115 WPM durante explicaciones técnicas.",
            "inclusive_pronoun_habit": "Uso recurrente de la primera persona del plural ('nosotros', 'nuestra comunidad', 'veamos juntos')."
        },
        "domain_and_work_profile": {
            "core_verticals": [
                "Investigación Social y Gobernanza Pública",
                "Crisis Climática y Transición Ecológica",
                "Geopolítica y Conflictos Internacionales",
                "Pensamiento Crítico y Verificación de Datos"
            ],
            "content_portfolio": [
                "Videos de Análisis Profundo de 15 a 20 minutos",
                "Reels y Shorts Educativos de Alto Impacto (<60s)",
                "Reportajes de Campo y Entrevistas a Expertos"
            ],
            "investigation_methodology": "Uso de informes oficiales, auditorías estatales y publicaciones académicas verificadas con citas en pantalla."
        },
        "audience_profile": {
            "demographics": "Jóvenes y adultos de 18 a 35 años, estudiantes universitarios y profesionales en Iberoamérica y diaspora.",
            "psychographics": "Búsqueda de análisis neutral y riguroso alejado del sensacionalismo televisivo; alto interés en la verdad fáctica.",
            "consumption_habits": "Alta retención en contenidos explicativos y alta tasa de compartidos en mensajería privada y redes sociales."
        },
        "domain_positioning_and_moat": {
            "mission": "Hacer accesible el conocimiento complejo para construir una ciudadanía consciente y crítica.",
            "positioning": "El canal de referencia para entender la realidad con datos verificados y perspectiva humana.",
            "competitive_moat": "Rigor investigativo transparente y confianza forjada a través de fuentes abiertas."
        },
        "sample_topics_format": "Análisis claro con datos verificados"
    },
    "en": {
        "name": "English",
        "script": "Latin",
        "primary_tone": "Authoritative yet deeply approachable mentor",
        "pacing_note": "Measured, pedagogical cadence with dramatic micro-pauses before key thesis points",
        "mannerisms": [
            {
                "phrase": "Hey friends, welcome back to the channel",
                "category": "greeting",
                "sample_context": "Warm, authentic opening establishing peer-level collaboration."
            },
            {
                "phrase": "Here's the honest truth that nobody talks about",
                "category": "emphasis",
                "sample_context": "Spoken right before presenting a counter-intuitive finding or data point."
            },
            {
                "phrase": "Let's dive right in and break this down",
                "category": "transition",
                "sample_context": "Spoken immediately following the 5-second teaser hook."
            },
            {
                "phrase": "Links and sources are in the description below",
                "category": "call_to_action",
                "sample_context": "Standard transparency reference validating the research presented."
            },
            {
                "phrase": "At the end of the day, it all comes down to this",
                "category": "emphasis",
                "sample_context": "Synthesizing the core mental model or takeaway."
            }
        ],
        "hooks": [
            "What if everything you've been told about {topic} is completely backwards?",
            "The hidden truth about {topic} that mainstream coverage is completely ignoring.",
            "Here is the single data point that changed my entire perspective on {topic}."
        ],
        "long_speech_monologues": {
            "thesis_monologue": {
                "title": "45-Second Thesis Framing Monologue",
                "speech": "Hey friends, welcome back. Over the last couple of years, there has been an overwhelming narrative around this topic across headlines and social media. But if you actually dig beneath the surface and examine the peer-reviewed research, economic data, and corporate disclosures, a very different picture begins to emerge. In this video, we're not dealing with hype or emotional speculation—we are breaking down the exact mechanics, the hidden conflicts of interest, and what this actually means for your daily life. Let's get straight into it.",
                "staging_breakdown": "0:00-0:08 Warm greeting & mainstream narrative | 0:08-0:25 The counter-evidence teaser | 0:25-0:45 Thesis promise & visual transition into data breakdown."
            },
            "evidence_monologue": {
                "title": "60-Second Empirical Evidence & Debunking Monologue",
                "speech": "Now, the conventional explanation that we've all been told sounds reasonable at first glance. But look at what happens when you cross-reference that narrative with official audit figures. On page 78 of this federal filing, the numbers tell an entirely contradictory story: expenditure increased by 65%, while public delivery collapsed. Furthermore, independent investigative audits confirmed that key regulatory oversight was quietly deregulated two years prior. So the real question isn't whether the system broke down—the real question is who profited while everyone was looking the other way?",
                "staging_breakdown": "0:00-0:15 Stating the conventional myth | 0:15-0:40 Highlighting document page number with on-screen graphic | 0:40-1:00 Punchline question with 1.2s micro-pause."
            },
            "outro_monologue": {
                "title": "45-Second Reflection & Civic Awareness Monologue",
                "speech": "At the end of the day, systemic problems don't get solved by passive acceptance or tribal arguments. They get solved when informed citizens understand the incentives and demand transparent accountability. I'd love to hear your perspective on this in the comments below—especially if you have firsthand experience with this issue. If you found this breakdown valuable, share it with someone who cares about the facts, and make sure to subscribe for more deep-dive analyses. Thanks for watching, and see you in the next one.",
                "staging_breakdown": "0:00-0:20 Synthesizing root systemic incentives | 0:20-0:35 Solicit authentic viewer comment dialogue | 0:35-0:45 Collaborative closing and subscribe prompt."
            }
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Measured baritone authority with dynamic shifts; drops pitch to underline solemn facts, modulates upward when introducing counter-intuitive paradoxes.",
            "micro_pause_timing": "Precise 1.2-second pauses before revealing critical numbers to create maximum retention tension.",
            "articulation_and_pacing": "140 WPM intro tapering to 115 WPM on key thesis statements, avoiding filler syllables.",
            "inclusive_pronoun_habit": "Inclusive framing ('we', 'let's explore', 'together') ensuring a cooperative peer-to-peer educational dynamic."
        },
        "domain_and_work_profile": {
            "core_verticals": [
                "Investigative Policy & Systemic Economic Analyses",
                "Environmental Science, Clean Energy & Climate Realities",
                "Geopolitical Dynamics & International Statecraft",
                "Critical Thinking, Media Disinformation & Digital Literacy"
            ],
            "content_portfolio": [
                "15-25m Deep-Dive Explainer Video Essays",
                "Fast-Paced 60s Shorts & High-Retention Reels",
                "Structured Masterclasses & Long-form Audio Discussions"
            ],
            "investigation_methodology": "Peer-reviewed papers, primary government filings, economic census data, and verified investigative reporting with on-screen document highlighting."
        },
        "audience_profile": {
            "demographics": "Ages 18-35 (students, tech professionals, policy enthusiasts, knowledge workers) across global urban hubs.",
            "psychographics": "Intellectually curious, skeptical of legacy media spin, driven by systematic mental models and objective truth.",
            "consumption_habits": "High binge-watching completion rates; uses videos as learning reference material; frequently quotes findings in peer debates."
        },
        "domain_positioning_and_moat": {
            "mission": "Demystifying complex socio-economic, technological, and scientific systems through rigorous, calm, and objective visual storytelling.",
            "positioning": "The trusted intellectual anchor who cuts through hype to deliver grounded reality.",
            "competitive_moat": "Meticulous documentation, high visual production value, and an unshakeable reputation for intellectual honesty."
        },
        "sample_topics_format": "Data-backed investigative breakdowns"
    }
}


class LanguageService:
    """Detects and supplies native language intelligence for creators."""

    def detect_language(
        self,
        creator_name: str,
        text_samples: List[str],
        requested_language: Optional[str] = None
    ) -> str:
        """
        Detects primary spoken language code ('hi', 'en', 'es', etc.).
        Inspects Unicode script (e.g. Devanagari), Hindi transliteration keywords,
        or respects explicit user request.
        """
        if requested_language and requested_language.lower() in LANGUAGE_PATTERNS:
            return requested_language.lower()

        combined_text = f"{creator_name} " + " ".join(text_samples[:15])

        # 1. Check for Devanagari script (Hindi, Marathi, etc.)
        devanagari_chars = len(re.findall(r'[\u0900-\u097F]', combined_text))
        if devanagari_chars > 5:
            logger.info(f"[Lang] Detected Devanagari script ({devanagari_chars} chars) -> Hindi")
            return "hi"

        # 2. Check for Hindi phonetics / Hinglish markers
        hinglish_keywords = [
            r"\bkya\b", r"\bkyu\b", r"\bkyon\b", r"\bkaise\b", r"\bkarein\b",
            r"\bhai\b", r"\bhain\b", r"\bke\s+baare\b", r"\bsach\b", r"\basli\b",
            r"\byeh\b", r"\bwoh\b", r"\baap\b", r"\baapka\b", r"\bnamaskar\b",
            r"\bdosto\b", r"\bvideo\s+mein\b", r"\bbharat\b", r"\bindian\b",
            r"\bdesh\b", r"\bmudda\b", r"\byojana\b", r"\brahasya\b"
        ]
        text_lower = combined_text.lower()
        hinglish_hits = sum(1 for kw in hinglish_keywords if re.search(kw, text_lower))

        # Known Indian creators with prominent Hindi channels
        known_hindi_creators = ["dhruv rathee", "sandeep maheshwari", "khan sir", "nitish rajput", "carryminati", "technical guruji"]
        if any(c in creator_name.lower() for c in known_hindi_creators) or hinglish_hits >= 2:
            logger.info(f"[Lang] Identified creator or Hinglish phonetic markers -> Hindi")
            return "hi"

        # 3. Check for Spanish markers
        spanish_keywords = [r"\bcomo\b", r"\bque\b", r"\bpor\s+que\b", r"\bverdades\b", r"\bespañol\b", r"\bgracias\b"]
        if sum(1 for kw in spanish_keywords if re.search(kw, text_lower)) >= 2:
            return "es"

        return "en"

    def get_language_pack(self, lang_code: str) -> Dict[str, Any]:
        """Returns language pack including mannerisms, hooks, and tone descriptors."""
        return LANGUAGE_PATTERNS.get(lang_code, LANGUAGE_PATTERNS["en"])

    def format_hook(self, template: str, topic: str) -> str:
        """Fills a topic into a native language hook template."""
        return template.replace("{topic}", topic)


language_service = LanguageService()
