"""
Domain & Niche Intelligence Service
===================================
Automatically identifies, categorizes, and generates deep domain profiles
(core verticals, research standards, audience psychographics, competitive moats,
and domain-tailored monologues) for ANY creator across any niche and language.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

from app.models.domain import (
    CreatorDomainProfile,
    DomainMonologue,
    DomainAudienceProfile,
    DomainMoat,
    DomainCadence,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# Recognized Pre-built Domain Archetypes
# ─────────────────────────────────────────────────────────────

DOMAIN_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "tech_gadgets": {
        "domain_id": "tech_gadgets",
        "domain_name": "Consumer Technology, Hardware & AI Gadgets",
        "sub_niche": "Smartphones, Computing, EVs & Next-Gen Consumer Electronics",
        "primary_search_topics": [
            "Smartphone camera shootout review",
            "Next gen AI hardware gadget teardown",
            "Electric vehicle range and battery test",
            "Flagship laptop performance benchmark",
            "Tech company anti-consumer controversy",
            "Best tech accessories and daily driver setup",
        ],
        "core_verticals": [
            "Flagship Smartphone Reviews, Real-World Tests & Long-Term Teardowns",
            "Next-Gen AI Hardware, Spatial Computing & Smart Wearables",
            "Electric Vehicles, Autonomous Tech & Clean Mobility",
            "Custom PC Builds, Laptop Benchmarks & Silicon Architecture",
            "Tech Industry Ethics, Right to Repair & Anti-Consumer Policies",
        ],
        "content_portfolio": [
            "10 to 18-Minute Cinematic Deep-Dive Hardware Reviews ('The Truth After 30 Days')",
            "Blind Camera Tests & Direct Competitor Shootouts",
            "Snappy 60-Second First Impressions & Feature Demos (Shorts/Reels)",
            "Long-Term Hardware Retrospectives & Tech Ecosystem Award Shows",
        ],
        "investigation_methodology": (
            "Standardized real-world battery drain loops, calibrated lux and decibel meters, "
            "thermal imaging heatmaps under sustained GPU/CPU load, and side-by-side blind camera "
            "comparisons without brand badges to remove subjective bias."
        ),
        "audience_profile": {
            "demographics": "Primary 18–35 (Gen Z & Millennials), predominantly tech enthusiasts, engineers, designers, early adopters, and prospective electronics buyers across global tech hubs.",
            "psychographics": "Allergic to corporate marketing hype and spec-sheet regurgitation; values brutally honest usability verdicts, pixel-peeping aesthetic polish, and pragmatic buying advice.",
            "consumption_habits": "Consulted religiously before making hardware purchase decisions; high re-watch rate on comparison tables; video links shared heavily on Reddit, Discord, and tech Twitter.",
        },
        "domain_positioning_and_moat": {
            "mission": "Helping consumers make confident, informed buying decisions through uncompromising hardware testing and cinematic visual storytelling.",
            "positioning": "The gold-standard aesthetic arbiter and honest tech critic who tests gadgets as daily drivers rather than reading promotional press releases.",
            "competitive_moat": "Peerless cinematic 8K production quality, proprietary standardized benchmark suites, and uncompromising editorial independence that brands cannot purchase.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Warm, articulate baritone; maintains conversational cool during aesthetic appreciation; modulates into skeptical analytical inflection when pointing out cut corners or build compromises.",
            "micro_pause_timing": "Inserts a 1.2-second pause before delivering the final verdict or price evaluation to build retention tension.",
            "articulation_and_pacing": "Starts at a brisk 140 WPM during rapid b-roll sequences, slowing down to 110 WPM during spec breakdowns and macro close-ups.",
            "inclusive_pronoun_habit": "Direct second-person engagement ('If you are considering upgrading...', 'Here is what you actually need to know').",
        },
        "signature_phrases": [
            {"phrase": "So I've been using this as my daily driver for the last two weeks...", "category": "opening", "sample_context": "Establishing real-world credibility before the spec sheet."},
            {"phrase": "Here is the massive elephant in the room that nobody is talking about...", "category": "emphasis", "sample_context": "Highlighting a major flaw or price hike."},
            {"phrase": "At this price point, the competition completely destroys it.", "category": "verdict", "sample_context": "Delivering an unvarnished buying recommendation."},
            {"phrase": "Let's look at the actual camera samples side-by-side.", "category": "transition", "sample_context": "Moving from exterior design into photographic benchmarks."},
        ],
        "monologues_by_language": {
            "en": {
                "thesis": {
                    "title": "45-Second Tech Reality Check Monologue",
                    "speech": "So I've been using this device as my exclusive daily driver for the past two weeks, and there's one massive elephant in the room that every promotional review seems to be glossing over. On paper, the spec sheet sounds incredible: a revolutionary new sensor, all-day battery life, and an AI processor that promises to change how you work. But when you take it out into the real world—under direct sunlight, on cellular data, and during actual heavy workflows—the reality is very different. In this video, we're skipping the marketing buzzwords and breaking down whether this is truly a generational leap, or just an expensive incremental update that you should skip.",
                    "staging_breakdown": "0:00-0:08 High-framerate macro b-roll of device | 0:08-0:25 Fast-cut contrast between launch keynote claims and real battery drain | 0:25-0:45 Steady, direct eye-contact to camera delivering thesis.",
                },
                "evidence": {
                    "title": "60-Second Hardware Benchmark & Teardown Monologue",
                    "speech": "Now, let's talk about that camera bump. The brand claimed a 40% improvement in low-light detail. But look at these uncompressed side-by-side crops on my studio monitor. On the left is last year's model, and on the right is the new flagship. Notice anything? The aggressive noise reduction is completely smearing fine textures on fabric and skin tones. And when we ran our standardized three-hour thermal stress loop, the frame throttled down by nearly 35% after just 22 minutes to prevent overheating. That means the peak performance they advertise on the box is only sustainable in short bursts. So before you spend twelve hundred dollars, you need to understand where your money is actually going.",
                    "staging_breakdown": "0:00-0:15 Display 400% zoom crop comparison | 0:15-0:40 Thermal imaging overlay and sustained benchmark curve | 0:40-1:00 Direct address with 1.2s micro-pause before price verdict.",
                },
                "outro": {
                    "title": "45-Second Buyer's Verdict & Call-to-Action Monologue",
                    "speech": "At the end of the day, here's my bottom line. If you're coming from a device that is three or four years old, this upgrade will feel like night and day. But if you already own last year's model, save your money—the incremental gains simply don't justify the price tag. Drop a comment down below and let me know: would you buy this, or would you wait for the next generation? All full-res camera samples and battery test logs are linked in the description. Thanks for watching, hit subscribe for more honest hardware reviews, and I'll catch you in the next one.",
                    "staging_breakdown": "0:00-0:20 Clear tiered buyer recommendations | 0:20-0:35 Community prompt on pricing | 0:35-0:45 Clean outro and subscribe graphic.",
                },
            },
            "hi": {
                "thesis": {
                    "title": "45-Second Tech Reality Check Monologue (Hindi)",
                    "speech": "नमस्कार दोस्तों! पिछले दो हफ्तों से मैं इस नए फ्लैगशिप फोन को अपना प्राइमरी डेली ड्राइवर बनाकर टेस्ट कर रहा हूं। और सच कहूं तो एक ऐसी बहुत बड़ी बात है जो ब्रांड्स के बड़े-बड़े विज्ञापनों में आपसे छुपाई जा रही है। स्पेसिफिकेशन शीट देखने में तो बहुत शानदार लगती है—200 मेगापिक्सल कैमरा, नया एआई प्रोसेसर और सुपरफास्ट चार्जिंग। लेकिन जब आप इसे असली जिंदगी में धूप में, गेमिंग में और हेवी कॉलिंग पर इस्तेमाल करते हैं, तो जमीनी हकीकत कुछ और ही निकल कर आती है। आज के इस वीडियो में बिना किसी स्पॉन्सरशिप बायस के, हम इसके हर एक फीचर का असली टेस्ट करेंगे ताकि आपको पता चले कि क्या यह आपके पैसे वसूल कराएगा या नहीं।",
                    "staging_breakdown": "0:00-0:08 हाथ में फोन के साथ डायरेक्ट आई-कॉन्टैक्ट | 0:08-0:25 ऑन-स्क्रीन रियल-लाइफ ओवरहीटिंग टेस्ट फुटेज | 0:25-0:45 निष्पक्ष रिव्यू का वादा और वीडियो का एजेंडा।",
                },
                "evidence": {
                    "title": "60-Second Hardware Benchmark & Teardown Monologue (Hindi)",
                    "speech": "अब कंपनी का दावा है कि इसका नया कैमरा पिछले साल के मॉडल से 40% बेहतर है। लेकिन जरा ठहरिए—मेरे स्टूडियो के इस बड़े मॉनिटर पर इन दोनों तस्वीरों को 400% जूम करके देखिए। बाईं तरफ है पिछले साल का मॉडल और दाईं तरफ यह नया वाला। क्या आपको कोई बड़ा फर्क नजर आ रहा है? सच तो यह है कि नया फोन फोटो को इतना ज्यादा स्मूथ कर रहा है कि असली डिटेल्स ही गायब हो रही हैं। और जब हमने इसमें 30 मिनट का हेवी गेमिंग टेस्ट चलाया, तो फोन का टेम्परेचर 44 डिग्री तक पहुंच गया और परफॉर्मेंस 30% ड्रॉप हो गई। इसका मतलब जो परफॉर्मेंस बॉक्स पर लिखी है, वो सिर्फ पहले कुछ मिनटों के लिए है। तो क्या इस पर इतना ज्यादा पैसा खर्च करना समझदारी है?",
                    "staging_breakdown": "0:00-0:15 स्क्रीन पर साइड-बाय-साइड 400% जूम फोटो कम्पेरिजन | 0:15-0:40 थर्मल गन से नापा गया टेम्परेचर ग्राफ | 0:40-1:00 1.2 सेकंड का पॉज और असली सवाल।",
                },
                "outro": {
                    "title": "45-Second Buyer's Verdict Monologue (Hindi)",
                    "speech": "तो दोस्तों, फाइनल फैसला क्या है? अगर आप तीन साल पुराना फोन इस्तेमाल कर रहे हैं, तो यह अपग्रेड आपके लिए बहुत बड़ा बदलाव साबित होगा। लेकिन अगर आपके पास पिछले साल का फ्लैगशिप है, तो पैसे बचाइए—यह मामूली बदलाव इतने पैसों के लायक बिल्कुल नहीं है। आप नीचे कमेंट करके बताइए कि क्या आप इसे खरीदेंगे या फिर किसी और ब्रांड का इंतजार करेंगे? सभी ऑरिजिनल कैमरा सैंपल्स डिस्क्रिप्शन में हैं। वीडियो पसंद आया हो तो लाइक और सब्सक्राइब जरूर कीजिए, मिलते हैं अगले वीडियो में!",
                    "staging_breakdown": "0:00-0:20 स्पष्ट खरीदार सलाह | 0:20-0:35 दर्शकों से राय पूछना | 0:35-0:45 वार्म साइन-ऑफ और सब्सक्राइब अपील।",
                },
            },
        },
    },

    "personal_finance": {
        "domain_id": "personal_finance",
        "domain_name": "Personal Finance, Wealth Building & Taxation",
        "sub_niche": "Index Investing, Tax Optimization, Real Estate & Financial Freedom",
        "primary_search_topics": [
            "New tax regime vs old tax regime deduction calculator",
            "Best index funds and SIP strategies for long term",
            "Credit card rewards points loophole redemption",
            "Real estate vs stock market returns comparison",
            "Hidden bank fees and investment charges to avoid",
            "How to reach financial independence early retirement",
        ],
        "core_verticals": [
            "Direct Index Fund Investing, Asset Allocation & Systematic Investment Plans (SIPs)",
            "Legal Tax Loopholes, Deductions & Corporate Expense Restructuring",
            "Credit Card Optimization, Reward Maximization & Credit Score Engineering",
            "Real Estate Analysis: Buying vs. Renting Mathematical Models",
            "Financial Scams, High-Commission Insurance Policies & Predatory Schemes",
        ],
        "content_portfolio": [
            "12 to 20-Minute Spreadsheet-Backed Financial Teardowns",
            "Skits & Conversational Reels Translating Complex Tax Clauses (<60s)",
            "Step-by-Step Retirement Calculators & Portfolio Rebalancing Walkthroughs",
            "Exposés on Hidden Banking Charges & High-Expense Mutual Funds",
        ],
        "investigation_methodology": (
            "Auditing official tax code gazettes, regulatory circulars (SEBI/RBI/IRS), "
            "running 20-year compound interest Monte Carlo backtests on index datasets, and reading "
            "the fine print of scheme information documents (SIDs) to expose hidden distributor commissions."
        ),
        "audience_profile": {
            "demographics": "Ages 22–42, salaried professionals, young entrepreneurs, freelancers, and first-time wealth builders seeking financial autonomy and tax minimization.",
            "psychographics": "Stressed by inflation and aggressive tax deductions; seeks high-ROI actionable strategies; deeply values transparent mathematical proof over vague motivational wealth advice.",
            "consumption_habits": "Screenshots spreadsheets and tax tables; saves videos into private 'Finance' playlists; shares breakdowns with spouses, coworkers, and family chat groups during tax season.",
        },
        "domain_positioning_and_moat": {
            "mission": "Democratizing financial literacy by translating jargon-heavy banking and tax rules into simple, mathematically proven wealth blueprints.",
            "positioning": "The trusted, relatable money mentor who shares practical frameworks rather than selling high-risk speculative day-trading schemes.",
            "competitive_moat": "Mathematical rigor with verifiable spreadsheet downloads, zero sponsorship of unregulated crypto or gambling apps, and unshakeable viewer trust.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Energetic, engaging, and conversational; modulates into high curiosity when framing a tax hack, then shifts into calm mathematical certainty when walking through spreadsheet formulas.",
            "micro_pause_timing": "Inserts a 1.2-second pause after stating a shocking compounding number (e.g. 'That 1% fee costs you 35 lakhs over 20 years') to let the financial gravity sink in.",
            "articulation_and_pacing": "Starts at an energetic 145 WPM during the hook, slowing down to 115 WPM during formula explanations.",
            "inclusive_pronoun_habit": "Empathetic peer framing ('Let's calculate our savings together', 'Here is how you and I can legally save on taxes').",
        },
        "signature_phrases": [
            {"phrase": "If you are investing without knowing this one rule, you are losing lakhs of rupees...", "category": "hook", "sample_context": "Pattern-interrupt hook highlighting compounding friction."},
            {"phrase": "Here is the exact math that banks and insurance agents don't want you to see.", "category": "emphasis", "sample_context": "Transition into spreadsheet calculations."},
            {"phrase": "At the end of 20 years, that tiny 1.5% fee wipes out 30% of your total wealth.", "category": "evidence", "sample_context": "Exposing expense ratios."},
            {"phrase": "I built a free calculator for you—link is in the pinned comment.", "category": "resource", "sample_context": "Delivering high-value utility."},
        ],
        "monologues_by_language": {
            "en": {
                "thesis": {
                    "title": "45-Second Wealth Compounder Monologue",
                    "speech": "If you are currently saving money in a traditional bank account or investing into standard mutual funds through your bank advisor, there is a very high probability that you are silently losing hundreds of thousands of dollars to hidden fees and inflation. Most people believe that building wealth requires picking the next winning stock or having a massive salary. But if you actually run the compound interest math over a 20-year horizon, the real difference between retiring wealthy and struggling comes down to three specific tax and fee levers that virtually nobody teaches in school. In this video, I'm opening up the exact spreadsheets and showing you step-by-step how to optimize your portfolio for maximum net returns.",
                    "staging_breakdown": "0:00-0:08 Direct punchy statement on hidden banking fees | 0:08-0:25 Split-screen comparison of traditional savings vs index compounding | 0:25-0:45 Pull up custom spreadsheet template on screen.",
                },
                "evidence": {
                    "title": "60-Second Mathematical Wealth Teardown Monologue",
                    "speech": "Now, let's look at why your bank advisor will never tell you this. When you invest in a regular mutual fund, they charge an expense ratio of around 1.8%. That sounds harmless, right? Less than two percent. But look at this compounding simulation over 25 years with a monthly contribution of five hundred dollars. With a low-cost direct index fund charging 0.05%, your portfolio grows to over six hundred thousand dollars. But with that 1.8% regular plan, you end up with four hundred and ten thousand dollars. That tiny 1.75% difference didn't take 1.75% of your money—it took nearly thirty-five percent of your total gains! You took all the financial risk, while the institution took a guaranteed third of your profit.",
                    "staging_breakdown": "0:00-0:15 Unpack the psychological trap of 'only 1.8%' | 0:15-0:40 Highlight the $190,000 lost gap on a visual compounding chart | 0:40-1:00 Deliver the core punchline with 1.2s micro-pause.",
                },
                "outro": {
                    "title": "45-Second Action Blueprint Monologue",
                    "speech": "The good news is that switching your portfolio to a direct, low-cost index allocation takes less than fifteen minutes once you know where to look. I have put together a completely free, automated spreadsheet calculator that runs your exact numbers and compares both tax regimes side by side—you can grab it using the link in the top comment. Let me know in the comments below: what percentage of your monthly income are you currently investing? If this breakdown saved you money, make sure to share it with a colleague who needs to see it, and hit subscribe for more honest financial playbooks.",
                    "staging_breakdown": "0:00-0:20 Free spreadsheet resource walkthrough | 0:20-0:35 Community question on savings rate | 0:35-0:45 Professional sign-off and subscribe cue.",
                },
            },
            "hi": {
                "thesis": {
                    "title": "45-Second Wealth Compounder Monologue (Hindi)",
                    "speech": "नमस्कार दोस्तों! अगर आप हर महीने अपनी मेहनत की कमाई में से ₹10,000 या ₹20,000 की SIP कर रहे हैं, तो एक मिनट रुक जाइए! 90% भारतीय निवेशक एक ऐसी बहुत बड़ी गलती कर रहे हैं जिसकी वजह से रिटायरमेंट के वक्त उन्हें लाखों रुपयों का नुकसान हो जाएगा। ज्यादातर लोग सोचते हैं कि वेल्थ बनाने के लिए शेयर बाजार के उतार-चढ़ाव को समझना जरूरी है, लेकिन असल खेल छुपा है उन हिडन चार्जेस, कमिशन्स और टैक्स नियमों में जिनके बारे में बैंक और एजेंट आपको कभी नहीं बताते। आज के इस वीडियो में मैं एक्सेल शीट खोलकर, एक-एक फॉर्मूले के साथ साबित करूंगा कि कैसे आप बिना कोई बड़ा रिस्क लिए अपनी वेल्थ को 30% से 40% तक बढ़ा सकते हैं।",
                    "staging_breakdown": "0:00-0:08 सीधे कैमरे में देखकर वित्तीय चेतावनी | 0:08-0:25 एजेंट कमिशन और हिडन चार्जेस का खुलासा | 0:25-0:45 लैपटॉप पर एक्सेल शीट खोलते हुए वीडियो का एजेंडा।",
                },
                "evidence": {
                    "title": "60-Second Mathematical Wealth Teardown Monologue (Hindi)",
                    "speech": "अब बहुत से लोग कहेंगे कि '1.5% का एक्सपेंस रेशियो तो बहुत मामूली है, इससे क्या फर्क पड़ता है?' तो आइए इस एक्सेल शीट पर देखिए असली गणित। मान लीजिए आप 25 साल तक हर महीने ₹10,000 निवेश करते हैं 12% के रिटर्न पर। अगर आप 'डायरेक्ट इंडेक्स फंड' चुनते हैं जिसमें सिर्फ 0.1% फीस है, तो 25 साल बाद आपके पास होंगे लगभग ₹1.85 करोड़। लेकिन अगर वही फंड आप बैंक एजेंट के जरिए 'रेगुलर प्लान' में लेते हैं जिसमें 1.6% फीस है, तो आपके हाथ में आएंगे सिर्फ ₹1.35 करोड़। यानी पूरे ₹50 लाख रुपये का सीधा नुकसान! रिस्क आपने उठाया, मेहनत आपकी कमाई की थी, लेकिन 50 लाख रुपये बिना कुछ किए उस ब्रोकर की जेब में चले गए।",
                    "staging_breakdown": "0:00-0:15 1.5% के भ्रम को तोड़ना | 0:15-0:40 स्क्रीन पर 50 लाख के अंतर को लाल रंग में हाईलाइट करना | 0:40-1:00 1.2 सेकंड का गंभीर पॉज और दर्शकों से सवाल।",
                },
                "outro": {
                    "title": "45-Second Action Blueprint Monologue (Hindi)",
                    "speech": "तो दोस्तों, अच्छी बात यह है कि इस नुकसान से बचने के लिए आपको सिर्फ 10 मिनट का समय चाहिए और आप खुद अपने फोन से डायरेक्ट फंड्स में स्विच कर सकते हैं। मैंने आपके लिए एक बिल्कुल फ्री एक्सेल कैलकुलेटर बनाया है जिससे आप न्यू टैक्स रिजीम बनाम ओल्ड टैक्स रिजीम और अपने फंड्स के खर्चों को खुद चेक कर सकते हैं—लिंक नीचे पिन्ड कमेंट में है। मुझे कमेंट में जरूर बताइए कि आप हर महीने अपनी सैलरी का कितना प्रतिशत निवेश करते हैं? इस वीडियो को अपने दोस्तों और परिवार के साथ जरूर शेयर करें ताकि किसी के भी पैसे बर्बाद न हों। मिलते हैं अगले वीडियो में!",
                    "staging_breakdown": "0:00-0:20 फ्री टूल और सॉल्यूशन का लिंक | 0:20-0:35 दर्शकों से उनकी सेविंग हैबिट्स पूछना | 0:35-0:45 शेयर करने की अपील और साइन-ऑफ।",
                },
            },
        },
    },

    "productivity_growth": {
        "domain_id": "productivity_growth",
        "domain_name": "Productivity Systems, Deep Work & Creator Growth",
        "sub_niche": "Evidence-Based Habits, Second Brain Systems & Workflow Design",
        "primary_search_topics": [
            "Best Notion second brain setup and workflow tutorial",
            "How to stop procrastinating and enter deep work state",
            "Evidence based study techniques active recall spaced repetition",
            "Morning routine habits of high performers scientific audit",
            "Time blocking and calendar management for entrepreneurs",
            "Building a creator business side hustle step by step",
        ],
        "core_verticals": [
            "Evidence-Based Habit Formation & Behavioral Psychology Protocols",
            "Digital Knowledge Management (Second Brain, Notion, Obsidian)",
            "Deep Work, Dopamine Detoxification & Distraction Elimination",
            "Creator Business Systems, Passive Income & Skill Monetization",
            "Book Syntheses, Mental Models & Life Design Frameworks",
        ],
        "content_portfolio": [
            "12 to 22-Minute Aesthetic Desk-Setup Workflow & System Walkthroughs",
            "Book Summaries Distilled into Actionable 5-Step Mental Models",
            "60-Second Micro-Habit Frameworks (Shorts/Reels)",
            "Day-in-the-Life Time Audits & Real-Time Productive Sprints",
        ],
        "investigation_methodology": (
            "Auditing peer-reviewed behavioral psychology studies, conducting 30-day "
            "self-quantified habit experiments with biometric tracking (sleep, HRV, screen time), "
            "and testing productivity applications against strict frictionless workflow criteria."
        ),
        "audience_profile": {
            "demographics": "Ages 18–34, university students, software engineers, startup founders, knowledge workers, and aspiring online creators across global knowledge hubs.",
            "psychographics": "Suffers from digital distraction, decision fatigue, and fear of wasted potential; craves structured calm, actionable systems, and aesthetic clarity.",
            "consumption_habits": "Takes active notes in Notion or Obsidian while watching; revisits videos at the beginning of each quarter/semester for workflow resets; shares widely in student and founder circles.",
        },
        "domain_positioning_and_moat": {
            "mission": "Helping ambitious people do more of what matters through evidence-based systems, joyful productivity, and thoughtful life design.",
            "positioning": "The warm, approachable digital mentor who replaces toxic hustle culture with sustainable, joyful productivity systems.",
            "competitive_moat": "Aesthetic visual serenity, rigorous evidence-backed synthesis of classic literature, and authentic transparency regarding personal failures and experiments.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Warm, reassuring, and articulate conversational tone; speaks with gentle pedagogical optimism, avoiding aggressive motivational shouting.",
            "micro_pause_timing": "Inserts a 1.0-second thoughtful pause after sharing a counter-intuitive insight (e.g. 'Motivation is an emotional trap') to encourage reflective internalization.",
            "articulation_and_pacing": "Consistent, serene 130 WPM with clear diction and minimal filler words.",
            "inclusive_pronoun_habit": "Collaborative peer framing ('I used to struggle with this constantly until I realized...', 'Let's rethink how we organize our week').",
        },
        "signature_phrases": [
            {"phrase": "If you feel exhausted at the end of the day but made zero actual progress...", "category": "hook", "sample_context": "Highlighting friction without progress."},
            {"phrase": "The problem isn't your willpower or motivation—it's your friction loop.", "category": "thesis", "sample_context": "Reframing productivity as systemic."},
            {"phrase": "Here is the exact 3-step framework I use to organize my entire life.", "category": "transition", "sample_context": "Moving into the concrete system breakdown."},
            {"phrase": "Make it stupidly easy to start, and the momentum will take care of itself.", "category": "framework", "sample_context": "Actionable rule of thumb."},
        ],
        "monologues_by_language": {
            "en": {
                "thesis": {
                    "title": "45-Second System Over Willpower Monologue",
                    "speech": "If you constantly find yourself reaching the end of the day feeling utterly exhausted, but looking at your to-do list and realizing you made zero meaningful progress on the things that actually matter, I want you to know something important: the problem is not your willpower, and the problem is definitely not your motivation. The hustle culture narrative that you just need to 'grind harder' or wake up at 5 AM is scientifically backwards. High performers don't rely on discipline to get through their day—they design low-friction systems that make procrastination practically impossible. In this video, we're breaking down the exact evidence-based framework that took me from overwhelmed and scattered to effortlessly consistent.",
                    "staging_breakdown": "0:00-0:08 Warm gaze into camera in minimalist aesthetic studio | 0:08-0:25 Graphic showing the failure rate of raw willpower vs environmental design | 0:25-0:45 Transition to digital workspace breakdown.",
                },
                "evidence": {
                    "title": "60-Second Behavioral Psychology Workflow Monologue",
                    "speech": "Let's look at what behavioral psychology actually says about friction. In a landmark study on habit adherence, researchers found that adding just twenty seconds of friction to an undesirable habit reduced participation by over seventy percent. The reason you check your phone eighty times a day isn't that you lack character—it's because your phone is sitting three inches from your hand with notifications enabled. Conversely, when we apply that exact same twenty-second rule to deep work by setting up our document the night before, blocking our calendar in ninety-minute ultradian cycles, and using a single capture inbox, the cognitive activation energy required to start drops to near zero. You don't need motivation when the path of least resistance leads directly to focused execution.",
                    "staging_breakdown": "0:00-0:15 Scientific research citation overlay | 0:15-0:40 Screen capture of Notion second brain database and time blocks | 0:40-1:00 Direct conversational summary with 1.0s micro-pause.",
                },
                "outro": {
                    "title": "45-Second Reflection & Routine Reset Monologue",
                    "speech": "Remember, productivity isn't about packing every single minute of your calendar with relentless tasks. It's about creating enough mental clarity and leverage so that you can enjoy your life without constant background anxiety. I have made this entire Notion template and daily checklist completely free to duplicate in the description below. Leave a comment down below and tell me: what is the single biggest distraction holding you back right now? If you enjoyed this video, hit subscribe, take care of yourself, and I will see you in the next one.",
                    "staging_breakdown": "0:00-0:20 Gentle philosophy of joyful productivity | 0:20-0:35 Free template download CTA | 0:35-0:45 Warm and calm sign-off.",
                },
            },
            "hi": {
                "thesis": {
                    "title": "45-Second System Over Willpower Monologue (Hindi)",
                    "speech": "नमस्कार दोस्तों! क्या आपके साथ भी ऐसा होता है कि पूरा दिन बीत जाने के बाद आप थका हुआ महसूस करते हैं, लेकिन जब आप अपने काम को देखते हैं तो लगता है कि कोई भी जरूरी काम पूरा ही नहीं हुआ? अगर हां, तो एक बात साफ समझ लीजिए: समस्या आपकी मेहनत या आपकी नीयत में नहीं है, और समस्या यह भी नहीं है कि आपके अंदर मोटिवेशन की कमी है। इंटरनेट पर जो आपको सुबह 4 बजे उठकर बिना सोचे-समझे भागने की सलाह दी जाती है, वो पूरी तरह से गलत है। जो लोग असल में जिंदगी में बड़े रिजल्ट्स हासिल करते हैं, वो सिर्फ अपनी इच्छाशक्ति पर निर्भर नहीं रहते—वो एक ऐसा आसान सिस्टम बनाते हैं जहां काम न करना नामुमकिन हो जाता है। आज के इस वीडियो में हम उसी प्रैक्टिकल सिस्टम को समझेंगे।",
                    "staging_breakdown": "0:00-0:08 शांत स्टूडियो में कैमरे के साथ सीधा संवाद | 0:08-0:25 मोटिवेशन बनाम सिस्टम का ग्राफिक | 0:25-0:45 स्क्रीन पर वर्कफ्लो का परिचय।",
                },
                "evidence": {
                    "title": "60-Second Behavioral Psychology Workflow Monologue (Hindi)",
                    "speech": "अब आइए इसे वैज्ञानिक नजरिए से समझते हैं। बिहेवियरल साइकोलॉजी की एक प्रसिद्ध स्टडी बताती है कि अगर किसी खराब आदत में सिर्फ 20 सेकंड की रुकावट या फ्रिक्शन डाल दिया जाए, तो उस आदत के दोहराए जाने की संभावना 70% तक गिर जाती है। आप दिनभर में 50 बार इंस्टाग्राम या फोन इसलिए नहीं देखते कि आप कमजोर हैं, बल्कि इसलिए देखते हैं क्योंकि फोन आपके हाथ से सिर्फ 2 इंच की दूरी पर रखा है। और ठीक यही नियम हमारे जरूरी काम पर भी लागू होता है। अगर आप अपने काम का सेटअप रात को ही तैयार कर लें, अगले दिन के 90 मिनट के सिर्फ दो फोकस स्लॉट कैलेंडर में लॉक कर दें, तो काम शुरू करने का आलस अपने आप खत्म हो जाएगा। आपको किसी मोटिवेशनल वीडियो की जरूरत नहीं पड़ेगी, आपका वातावरण ही आपसे काम करवा लेगा।",
                    "staging_breakdown": "0:00-0:15 स्टडी और रिसर्च का हवाला | 0:15-0:40 स्क्रीन पर टाइम-ब्लॉकिंग और वर्कफ्लो का प्रदर्शन | 0:40-1:00 1.2 सेकंड का विचारशील पॉज।",
                },
                "outro": {
                    "title": "45-Second Reflection & Routine Reset Monologue (Hindi)",
                    "speech": "अंत में दोस्तों, प्रोडक्टिविटी का मतलब यह बिल्कुल नहीं है कि आप मशीन की तरह 24 घंटे काम करते रहें और अपनी सेहत खराब कर लें। असली प्रोडक्टिविटी का मतलब है कम समय में अपना सबसे बेहतरीन काम करना, ताकि आप अपने परिवार और अपनी जिंदगी को भी सुकून से जी सकें। मैंने यह पूरा सिस्टम और टेम्पलेट आपके लिए डिस्क्रिप्शन में बिल्कुल फ्री दिया है। नीचे कमेंट करके जरूर बताइए कि आपका सबसे ज्यादा समय किस चीज में बर्बाद होता है? वीडियो अच्छा लगा हो तो सब्सक्राइब करें और अपने दोस्तों के साथ शेयर करें। मिलते हैं अगले वीडियो में!",
                    "staging_breakdown": "0:00-0:20 स्वस्थ जीवनशैली और प्रोडक्टिविटी का संतुलन | 0:20-0:35 फ्री टेम्पलेट लिंक | 0:35-0:45 गर्मजोशी से साइन-ऑफ।",
                },
            },
        },
    },

    "civic_social_issues": {
        "domain_id": "civic_social_issues",
        "domain_name": "Civic Rights, Democratic Awareness & Public Policy",
        "sub_niche": "Public Policy Audits, Environmental Crises, Geopolitics & Fact-Checking",
        "primary_search_topics": [
            "Electoral reforms and democratic institution transparency",
            "Environmental crisis air pollution and water scarcity audit",
            "Geopolitical conflict root causes historical context",
            "Public healthcare infrastructure and education budget spending",
            "Fact check viral political claims official gazette audit",
            "Scientific temper critical thinking vs online misinformation",
        ],
        "core_verticals": [
            "Civic Rights, Electoral Systems & Democratic Transparency",
            "Environmental Science, Climate Crisis & Pollution Audits",
            "Geopolitics, International Diplomacy & Historical Root Causes",
            "Public Policy, Economic Disparity & Healthcare Infrastructure",
            "Scientific Thinking, Critical Rationality & Media Literacy",
        ],
        "content_portfolio": [
            "15 to 25-Minute Long-Form Deep-Dive Investigative Video Essays",
            "30 to 60-Second Fact-Check Shorts & Explanatory Reels",
            "Structured Masterclasses (Critical Thinking, Video Editing, Time Mastery)",
            "On-Site Ground-Reality Citizen Documentaries",
        ],
        "investigation_methodology": (
            "Grounds every claim in official documentation: government gazettes, parliamentary "
            "answers, Right to Information (RTI) filings, peer-reviewed scientific journals, and "
            "validated international indices (World Bank, UN, IPCC). Highlights exact PDF excerpts on screen with yellow markers."
        ),
        "audience_profile": {
            "demographics": "Primary 18–34 years (Gen Z and Millennials), secondary 35–50 years; college students, working professionals, educators, urban and Tier 1/2 citizens, and an extensive global diaspora.",
            "psychographics": "Values intellectual honesty, objectivity, and calm pedagogy; experiences severe fatigue with sensationalist TV shouting matches; seeks structured clarity, logical consistency, and empirical evidence to understand modern systems.",
            "consumption_habits": "Exceptionally high average view duration (12–18 minutes); active participant in structured comment debates; frequently shares videos on family and peer WhatsApp groups and social networks as educational reference material.",
        },
        "domain_positioning_and_moat": {
            "mission": "Democratizing objective knowledge by translating high-complexity legal, scientific, and geopolitical issues into accessible, engaging citizen mental models.",
            "positioning": "The trusted, objective digital educator who brings calm, rigorous journalism to an internet saturated with algorithmic noise and sensationalism.",
            "competitive_moat": "Deep-rooted public trust established through transparent source citation (every link provided in description), verifiable methodology, and refusal to adopt sensationalist screaming.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Begins at a calm, conversational mid-frequency (grounded and pedagogical); subtly drops 2–3 semitones when introducing grave systemic failures; elevates slightly with measured intensity during evidence presentation before returning to a steady, thoughtful baseline.",
            "micro_pause_timing": "Inserts deliberate 1.0 to 1.5-second complete audio silences directly following pivotal questions ('लेकिन सवाल यह है कि...') or surprising statistics, allowing the cognitive dissonance to register before presenting charts.",
            "articulation_and_pacing": "Starts at an energetic 135–145 words per minute during the hook; steadily decelerates to 110–115 WPM during complex data explanations to ensure total conceptual comprehension.",
            "inclusive_pronoun_habit": "Consistently employs inclusive plural pronouns ('हम सब', 'आप और मैं', 'हमारे देश में') to establish a collaborative peer dynamic rather than preaching down to the viewer.",
        },
        "signature_phrases": [
            {"phrase": "नमस्कार दोस्तों, स्वागत है आपका एक और नए वीडियो में", "category": "greeting", "sample_context": "Iconic opening greeting setting an objective, grounded tone."},
            {"phrase": "सच तो यह है कि...", "category": "emphasis", "sample_context": "Spoken right before debunking a popular misconception or presenting official statistics."},
            {"phrase": "आइए इसको गहराई से समझते हैं", "category": "transition", "sample_context": "Used to transition from the introductory hook into structured chapter breakdowns."},
            {"phrase": "अब असली सवाल यह उठता है कि...", "category": "transition", "sample_context": "Pivotal question hook challenging the viewer's preconceived notions."},
            {"phrase": "कमेंट करके जरूर बताइए कि आपकी इस पर क्या राय है", "category": "call_to_action", "sample_context": "Closing call to action encouraging civic debate and engagement."},
        ],
        "monologues_by_language": {
            "hi": {
                "thesis": {
                    "title": "45-Second Thesis Framing Monologue (Opening Speech)",
                    "speech": "नमस्कार दोस्तों! अगर आप पिछले कुछ सालों के ट्रेंड्स को देखें तो आपको एक बात साफ नजर आएगी कि हर कोई इस बारे में बात कर रहा है। लेकिन क्या कभी आपने गहराई से सोचा है कि इसके पीछे का असली खेल क्या है? सरकार और मुख्यधारा मीडिया हमें कुछ और बता रहे हैं, जबकि असल डेटा और जमीनी हकीकत कुछ बिल्कुल अलग बयां कर रही है। आज के इस वीडियो में हम बिना किसी बायस के, सिर्फ फैक्ट्स, डेटा और ऑफिशियल रिपोर्ट्स के साथ इस पूरे मुद्दे की परतें खोलेंगे। अंत तक जरूर देखिएगा ताकि आपको पूरी सच्चाई समझ आए।",
                    "staging_breakdown": "0:00-0:08 High-clarity greeting & widespread belief | 0:08-0:25 Contradiction & official data teaser | 0:25-0:45 Unbiased mission statement & invitation into deep dive.",
                },
                "evidence": {
                    "title": "60-Second Empirical Evidence & Debunking Monologue",
                    "speech": "अब आप में से बहुत से लोग कहेंगे कि यह तो सिर्फ एक इत्तेफाक है, या फिर यह समस्या सिर्फ हमारे देश में है। लेकिन जरा ठहरिए। अगर आप इस सरकारी रिपोर्ट के पेज नंबर 42 को देखें, तो साफ लिखा है कि पिछले पांच सालों में यह समस्या घटने के बजाय 40% बढ़ गई है। दूसरा बड़ा सबूत है यह इंटरनेशनल इंडेक्स, जहां हमारी रैंकिंग लगातार नीचे गिर रही है। और तीसरा सबसे बड़ा कारण है वो छुपा हुआ नियम जिसके बारे में मुख्यधारा की मीडिया में एक भी डिबेट नहीं हुई। तो असली सवाल यह नहीं है कि ऐसा क्यों हुआ, बल्कि असली सवाल यह उठता है कि इसे हम सब से छुपाया क्यों गया?",
                    "staging_breakdown": "0:00-0:12 Acknowledge counter-argument | 0:12-0:35 Display on-screen official gazette/index with highlighted yellow box | 0:35-1:00 Deliver the core investigative question with a 1.2s micro-pause.",
                },
                "outro": {
                    "title": "45-Second Climax Call to Reflection & Civic Responsibility Monologue",
                    "speech": "आखिरकार दोस्तों, बात किसी एक पार्टी या किसी एक विचारधारा की नहीं है। बात है हमारे देश के भविष्य की, हमारे समाज की और आने वाली पीढ़ी की। जब तक हम जागरूक नागरिक बनकर सही सवाल नहीं पूछेंगे, तब तक कोई भी जमीनी बदलाव मुमकिन नहीं है। नीचे कमेंट करके जरूर बताइए कि इस पूरे विश्लेषण पर आपकी अपनी क्या राय है? और इस वीडियो को अपने दोस्तों और परिवार के साथ जरूर शेयर कीजिए ताकि सच हर नागरिक तक पहुंचे। मिलते हैं अगले वीडियो में, बहुत-बहुत शुक्रिया।",
                    "staging_breakdown": "0:00-0:15 Transcending political tribalism to focus on collective civic future | 0:15-0:30 Provocative question to viewer | 0:30-0:45 Respectful outro with calm, warm sign-off.",
                },
            },
            "en": {
                "thesis": {
                    "title": "45-Second Thesis Framing Monologue",
                    "speech": "Hey friends, welcome back. Over the last couple of years, there has been an overwhelming narrative around this topic across headlines and social media. But if you actually dig beneath the surface and examine the peer-reviewed research, economic data, and corporate disclosures, a very different picture begins to emerge. In this video, we're not dealing with hype or emotional speculation—we are breaking down the exact mechanics, the hidden conflicts of interest, and what this actually means for your daily life. Let's get straight into it.",
                    "staging_breakdown": "0:00-0:08 Warm greeting & mainstream narrative | 0:08-0:25 The counter-evidence teaser | 0:25-0:45 Thesis promise & visual transition into data breakdown.",
                },
                "evidence": {
                    "title": "60-Second Empirical Evidence & Debunking Monologue",
                    "speech": "Now, the conventional explanation that we've all been told sounds reasonable at first glance. But look at what happens when you cross-reference that narrative with official audit figures. On page 78 of this federal filing, the numbers tell an entirely contradictory story: expenditure increased by 65%, while public delivery collapsed. Furthermore, independent investigative audits confirmed that key regulatory oversight was quietly deregulated two years prior. So the real question isn't whether the system broke down—the real question is who profited while everyone was looking the other way?",
                    "staging_breakdown": "0:00-0:15 Stating the conventional myth | 0:15-0:40 Highlighting document page number with on-screen graphic | 0:40-1:00 Punchline question with 1.2s micro-pause.",
                },
                "outro": {
                    "title": "45-Second Reflection & Civic Awareness Monologue",
                    "speech": "At the end of the day, systemic problems don't get solved by passive acceptance or tribal arguments. They get solved when informed citizens understand the incentives and demand transparent accountability. I'd love to hear your perspective on this in the comments below—especially if you have firsthand experience with this issue. If you found this breakdown valuable, share it with someone who cares about the facts, and make sure to subscribe for more deep-dive analyses. Thanks for watching, and see you in the next one.",
                    "staging_breakdown": "0:00-0:20 Synthesizing root systemic incentives | 0:20-0:35 Solicit authentic viewer comment dialogue | 0:35-0:45 Collaborative closing and subscribe prompt.",
                },
            },
        },
    },

    "startups_business": {
        "domain_id": "startups_business",
        "domain_name": "Startups, Business Strategy & Venture Capital",
        "sub_niche": "Unicorn Teardowns, Go-To-Market, Moats & Unit Economics",
        "primary_search_topics": [
            "Startup business model teardown and failure analysis",
            "How unicorn startup achieved product market fit GTM strategy",
            "Venture capital fundraising market trends and valuations",
            "Pricing strategy psychology and high ticket sales conversion",
            "B2B SaaS customer acquisition cost CAC and LTV economics",
            "Business moats network effects and competitive advantage",
        ],
        "core_verticals": [
            "Unicorn Case Studies, Strategic Moats & Failure Root Causes",
            "Unit Economics, Customer Acquisition Cost (CAC) & Retention Funnels",
            "Go-To-Market (GTM) Playbooks, Cold Outreach & High-Ticket Offers",
            "Venture Capital vs. Bootstrapping Tradeoffs & Capital Efficiency",
            "Pricing Psychology, Enterprise Sales & Founder Decision Frameworks",
        ],
        "content_portfolio": [
            "15 to 25-Minute Narrative Business Case Studies with Kinetic Motion Graphics",
            "Rapid 60-Second Marketing & Pricing Psychological Breakdowns",
            "Founder Pitch Deck Teardowns & Balance Sheet Audits",
            "Live Interviews with High-Scale Operators & Venture Capitalists",
        ],
        "investigation_methodology": (
            "Dissecting audited corporate balance sheets, SEC 10-K filings, MCA records, "
            "investor presentation pitch decks, and interviewing former employees to uncover "
            "the real unit economics beneath promotional PR valuation announcements."
        ),
        "audience_profile": {
            "demographics": "Ages 22–45, startup founders, tech operators, product managers, venture investors, and ambitious professionals across innovation hubs.",
            "psychographics": "Pragmatic, ambitious, and metrics-oriented; seeks battle-tested commercial frameworks rather than generic academic business theory; fascinated by competitive strategy.",
            "consumption_habits": "Rewatches key slides; shares episodes on company Slack channels, LinkedIn, and founder WhatsApp communities as required strategic reading.",
        },
        "domain_positioning_and_moat": {
            "mission": "Deconstructing how the world's most valuable companies are built, scaled, and defended through rigorous strategic analysis.",
            "positioning": "The trusted boardroom strategist for the digital generation who strips away corporate PR to reveal the underlying business mechanics.",
            "competitive_moat": "Direct access to real operational data, mastery of corporate finance, and top-tier storytelling that turns balance sheets into gripping narratives.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Confident, authoritative executive delivery; modulates with intense focus when revealing a startup's hidden burn rate or commercial vulnerability.",
            "micro_pause_timing": "Inserts a 1.2-second pause before unveiling the core strategic mistake that cost a company billions.",
            "articulation_and_pacing": "Starts at an energetic 140 WPM, modulating down to 115 WPM when dissecting balance sheet metrics.",
            "inclusive_pronoun_habit": "Direct second-person strategic challenge ('If you are building an offer in this market...', 'Here is the mistake you must avoid').",
        },
        "signature_phrases": [
            {"phrase": "Here is the dirty secret behind how this company actually makes money...", "category": "hook", "sample_context": "Exposing non-obvious revenue models."},
            {"phrase": "They raised a hundred million dollars, but their unit economics were completely broken.", "category": "emphasis", "sample_context": "Highlighting capital inefficiency."},
            {"phrase": "Without a defensible moat, your revenue is just someone else's future opportunity.", "category": "framework", "sample_context": "Core strategic takeaway."},
        ],
        "monologues_by_language": {
            "en": {
                "thesis": {
                    "title": "45-Second Business Strategy Teardown Monologue",
                    "speech": "On paper, this company looked completely unstoppable. They raised over two hundred million dollars from tier-one Silicon Valley venture capitalists, grew their customer base by four hundred percent year-over-year, and plastered their logo across every major airport terminal in the country. But if you actually dig into their private unit economics and look past the vanity metrics of gross revenue, you discover that they were losing sixty dollars on every single order they shipped. In this case study, we are breaking down the exact strategic miscalculations, the pricing traps, and the fatal operational mistakes that turned a multi-billion dollar market leader into a cautionary tale—and what you can learn from it.",
                    "staging_breakdown": "0:00-0:08 Dramatic headline montage with soaring valuation numbers | 0:08-0:25 Red highlighted balance sheet showing negative gross margins | 0:25-0:45 Founder takeaway framing.",
                },
                "evidence": {
                    "title": "60-Second Unit Economics Breakdown Monologue",
                    "speech": "Let's look at the customer acquisition cost. In their first year, acquiring a customer cost them roughly thirty dollars, and that customer generated fifty dollars of lifetime value. That is a healthy three-to-one LTV-to-CAC ratio. But when they attempted to scale from ten million to fifty million in annual recurring revenue, their marketing efficiency fell off a cliff. To sustain their artificial growth targets, they poured millions into paid social ads, driving their acquisition cost up to two hundred and ten dollars while their churn rate doubled to six percent monthly. In plain English: they were pouring water into an increasingly leaky bucket, and when the venture capital market dried up, the business had zero organic customer retention to fall back on.",
                    "staging_breakdown": "0:00-0:15 Clean animated CAC vs LTV chart | 0:15-0:40 Churn curve trajectory animation | 0:40-1:00 1.2s micro-pause followed by the strategic moral.",
                },
                "outro": {
                    "title": "45-Second Strategic Takeaway Monologue",
                    "speech": "The ultimate lesson for every entrepreneur and operator watching this is simple: growth is vanity, profit is sanity, but cash flow is king. Before you worry about scaling your marketing spend, make sure you have achieved true product-market fit and built a real competitive moat that competitors cannot easily copy. What do you think was their single biggest mistake: reckless expansion or terrible unit economics? Let me know in the comments below. If you want more deep-dive business teardowns like this, hit subscribe, and I'll see you in the next case study.",
                    "staging_breakdown": "0:00-0:20 Core operational maxim | 0:20-0:35 Comment debate prompt on business strategy | 0:35-0:45 Professional outro.",
                },
            },
            "hi": {
                "thesis": {
                    "title": "45-Second Business Strategy Teardown Monologue (Hindi)",
                    "speech": "नमस्कार दोस्तों! अखबारों और सोशल मीडिया पर इस स्टार्टअप की इतनी ज्यादा चर्चा थी कि हर किसी को लग रहा था कि यह कंपनी इतिहास रचने वाली है। 500 करोड़ रुपये की फंडिंग, हर टीवी चैनल पर विज्ञापन और लाखों यूजर्स। लेकिन अगर आप इनके पीआर और हाइप से बाहर निकलकर इनकी असली बैलेंस शीट को देखें, तो आपको समझ आएगा कि यह कंपनी हर 100 रुपये कमाने के लिए 250 रुपये जला रही थी! आज के इस बिजनेस केस स्टडी में हम बिना किसी लाग-लपेट के समझेंगे कि कैसे एक अरबों की वैल्यूएशन वाली कंपनी ने ऐसी कौन सी तीन भयानक गलतियां कीं, जिनकी वजह से यह पूरा बिजनेस ताश के पत्तों की तरह बिखर गया—और इससे हर बिजनेसमैन को क्या सीख मिलती है।",
                    "staging_breakdown": "0:00-0:08 हाई-एनर्जी केस स्टडी ओपनिंग | 0:08-0:25 बैलेंस शीट और कैश बर्न का खुलासा | 0:25-0:45 केस स्टडी का रोडमैप।",
                },
                "evidence": {
                    "title": "60-Second Unit Economics Breakdown Monologue (Hindi)",
                    "speech": "अब इनके बिजनेस मॉडल को जरा ध्यान से समझिए। शुरुआत में इनका कस्टमर एक्विजिशन कॉस्ट यानी ग्राहक लाने का खर्चा बहुत कम था क्योंकि इन्होंने भारी डिस्काउंट दिए। लेकिन जैसे ही इन्होंने डिस्काउंट देना बंद किया, 80% ग्राहक दूसरे ऐप पर चले गए! इसके बावजूद इन्होंने अपनी गलतियों को सुधारने के बजाय और ज्यादा विज्ञापन चलाए ताकि वे निवेशकों को सिर्फ यूजर ग्रोथ दिखा सकें। नतीजा यह हुआ कि इनका कैश बर्न हर महीने 20 करोड़ पहुंच गया और जब बाजार में मंदी आई तो किसी भी नए निवेशक ने पैसा देने से मना कर दिया। यानी इनके पास कोई ऐसा यूनीक कॉम्पिटिटिव मोट नहीं था जिसकी वजह से कस्टमर इनके पास टिका रहे।",
                    "staging_breakdown": "0:00-0:15 डिस्काउंट मॉडल के धोखे का विश्लेषण | 0:15-0:40 स्क्रीन पर कैश बर्न और रेवेन्यू चार्ट | 0:40-1:00 1.2 सेकंड का पॉज और बिजनेस का सबक।",
                },
                "outro": {
                    "title": "45-Second Strategic Takeaway Monologue (Hindi)",
                    "speech": "तो दोस्तों, इस पूरी कहानी से हर बिजनेस ओनर और आंत्रप्रेन्योर के लिए सबसे बड़ा सबक यह है कि सिर्फ रेवेन्यू बढ़ाना कोई समझदारी नहीं है, असली समझदारी है प्रॉफिटेबल यूनिट इकोनॉमिक्स बनाना। जब तक आपके बिजनेस की नींव मजबूत नहीं होगी, तब तक कितनी भी बड़ी फंडिंग आपको डूबने से नहीं बचा सकती। आपकी राय में इस कंपनी की सबसे बड़ी गलती क्या थी? नीचे कमेंट करके जरूर बताइए। अगर बिजनेस और केस स्टडीज में रुचि है तो चैनल को सब्सक्राइब जरूर करें। मिलते हैं अगले वीडियो में!",
                    "staging_breakdown": "0:00-0:20 बिजनेस का मुख्य फॉर्मूला | 0:20-0:35 दर्शकों से राय मांगना | 0:35-0:45 सब्सक्राइब अपील और साइन-ऑफ।",
                },
            },
        },
    },

    "health_fitness": {
        "domain_id": "health_fitness",
        "domain_name": "Health Optimization, Exercise Science & Longevity",
        "sub_niche": "Hypertrophy Science, Circadian Biology, Nutrition Protocols & Biohacking",
        "primary_search_topics": [
            "Hypertrophy science progressive overload workout split",
            "Optimal sleep protocol circadian rhythm light exposure",
            "Zone 2 cardio cardiovascular longevity protocol",
            "Protein synthesis distribution and daily diet plan",
            "Blood biomarker test panels longevity optimization",
            "Fitness fads and fake supplement debunking",
        ],
        "core_verticals": [
            "Hypertrophy Biomechanics, Progressive Overload & Injury Prevention",
            "Circadian Biology, Sleep Architecture & Energy Protocols",
            "Evidence-Based Nutrition, Protein Synthesis & Metabolic Health",
            "Cardiovascular Longevity (Zone 2, VO2 Max & Mitochondrial Health)",
            "Debunking Fitness Fads, Snake-Oil Supplements & Bro-Science Myths",
        ],
        "content_portfolio": [
            "15 to 25-Minute Science-Backed Physiology Explanations with 3D Anatomy Graphics",
            "Step-by-Step Exercise Form Teardowns & Mistake Corrections (<60s)",
            "Comprehensive Bloodwork & Biomarker Audit Walkthroughs",
            "Full-Day Eating & Training Regimens Grounded in Peer-Reviewed Data",
        ],
        "investigation_methodology": (
            "Cross-referencing randomized controlled trials (RCTs) indexed in PubMed, "
            "evaluating effect sizes and sample sizes, reviewing systematic meta-analyses, and using "
            "electromyography (EMG) studies and joint biomechanics to evaluate exercise effectiveness."
        ),
        "audience_profile": {
            "demographics": "Ages 18–45, lifters, athletes, health-conscious tech professionals, and longevity enthusiasts seeking optimal physical and cognitive performance.",
            "psychographics": "Fatigued by gimmicky workout fads and misleading influencer supplement sponsorships; craves physiological first-principles understanding and measurable progress.",
            "consumption_habits": "Saves routine checklists; references exercise cues while working out at the gym; shares scientific breakdowns on health subreddits and fitness group chats.",
        },
        "domain_positioning_and_moat": {
            "mission": "Empowering individuals to optimize their health, strength, and longevity through rigorous, peer-reviewed exercise and nutritional science.",
            "positioning": "The trusted physiological scientist who replaces bro-science and marketing myths with verified human biology.",
            "competitive_moat": "Deep academic citation rigor, transparent disclosure of supplement realities, and high-fidelity anatomical visualization.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Measured, calm, and scientific authority; modulates into emphatic clarity when correcting dangerous gym posture or debunking pseudoscientific health claims.",
            "micro_pause_timing": "Inserts a 1.2-second pause before naming the exact physiological mechanism or hormone responsible for a training adaptation.",
            "articulation_and_pacing": "Deliberate 125 WPM to ensure complex anatomical terminology is easily digested.",
            "inclusive_pronoun_habit": "Peer-educational dynamic ('When we look at the human muscle fiber data...', 'Let's examine how your body processes this').",
        },
        "signature_phrases": [
            {"phrase": "If you are doing this exercise in the gym, stop immediately...", "category": "hook", "sample_context": "Pattern-interrupt injury prevention hook."},
            {"phrase": "Let's look at what the randomized controlled trials actually demonstrate.", "category": "evidence", "sample_context": "Citing peer-reviewed PubMed literature."},
            {"phrase": "The supplement industry made billions selling you this, but the science shows zero benefit.", "category": "debunk", "sample_context": "Exposing ineffective products."},
        ],
        "monologues_by_language": {
            "en": {
                "thesis": {
                    "title": "45-Second Exercise Physiology Reality Check Monologue",
                    "speech": "If you have been training consistently in the gym for the last six months but feel like your strength and muscle growth have completely plateaued, there is a very high probability that you are falling for one of the most common training fallacies pushed by fitness influencers. The mainstream advice to 'switch up your routine every week to confuse the muscle' or train to complete muscular failure on every single set is not only inefficient—it is directly counterproductive to progressive overload. In this video, we are putting aside the bro-science and looking directly at the latest meta-analyses on hypertrophic stimulus, biomechanical leverage, and systemic fatigue to fix your programming once and for all.",
                    "staging_breakdown": "0:00-0:08 Direct gym floor address demonstrating common posture mistake | 0:08-0:25 3D muscle fiber overlay showing fatigue vs stimulus | 0:25-0:45 Academic study title screen overlay.",
                },
                "evidence": {
                    "title": "60-Second Biomechanical & Scientific Teardown Monologue",
                    "speech": "Look at what happens when we examine this recent systematic review covering over twenty-five randomized controlled trials. When training volume is equated, taking every set to absolute failure generated identical muscle hypertrophy compared to stopping one to two reps in reserve. But here is the critical difference: the systemic fatigue on your central nervous system and joint connective tissue was over forty percent higher in the failure group. That means you are accumulating massive recovery debt without triggering any additional protein synthesis. By simply leaving one clean repetition in reserve and prioritizing strict mechanical tension over momentum, you dramatically reduce your injury risk while maximizing weekly training density.",
                    "staging_breakdown": "0:00-0:15 Study effect size comparison graphic | 0:15-0:40 3D anatomical skeletal model showing joint shear forces | 0:40-1:00 Direct camera address with 1.2s micro-pause.",
                },
                "outro": {
                    "title": "45-Second Training Protocol Outro Monologue",
                    "speech": "The key takeaway is that sustainable physical progress is a science of consistency, recovery, and progressive overload—not reckless exhaustion. I have put together a complete, evidence-based training split with exact set, rep, and rest parameters that you can download for free in the description below. Drop a comment and tell me: what exercise do you struggle with the most in the gym? If this scientific breakdown helped you, hit subscribe, train smart, and I will see you in the next breakdown.",
                    "staging_breakdown": "0:00-0:20 Training blueprint summary | 0:20-0:35 Viewer engagement prompt on gym struggles | 0:35-0:45 Professional sign-off.",
                },
            },
            "hi": {
                "thesis": {
                    "title": "45-Second Exercise Physiology Reality Check Monologue (Hindi)",
                    "speech": "नमस्कार दोस्तों! अगर आप पिछले कई महीनों से जिम में पसीना बहा रहे हैं लेकिन आपकी बॉडी में कोई खास बदलाव नजर नहीं आ रहा, तो यकीन मानिए गलती आपकी मेहनत में नहीं है, बल्कि गलती उस गलत जानकारी में है जो अक्सर हमें जिम में या सोशल मीडिया पर दी जाती है। 'हर हफ्ते वर्कआउट बदलो' या 'जब तक जान न निकल जाए तब तक सेट लगाओ' जैसी बातें सुनने में तो अच्छी लगती हैं, लेकिन स्पोर्ट्स साइंस के मुताबिक ये आपकी रिकवरी को बर्बाद कर देती हैं। आज के इस वीडियो में हम बिना किसी मिथक के, असली मेडिकल रिसर्च और बायोमैकेनिक्स के आधार पर समझेंगे कि कैसे आप कम समय में ज्यादा बेहतर और सेफ रिजल्ट्स हासिल कर सकते हैं।",
                    "staging_breakdown": "0:00-0:08 जिम में आम गलतियों को दिखाते हुए ओपनिंग | 0:08-0:25 साइंस-बेस्ड रिकवरी और प्रोग्रेसिव ओवरलोड का महत्व | 0:25-0:45 वीडियो का एजेंडा।",
                },
                "evidence": {
                    "title": "60-Second Biomechanical Teardown Monologue (Hindi)",
                    "speech": "अब हाल ही में आई इस इंटरनेशनल स्पोर्ट्स साइंस स्टडी को देखिए। जब वैज्ञानिकों ने 500 से ज्यादा एथलीट्स के डेटा का विश्लेषण किया, तो पाया गया कि हर सेट को बिल्कुल फेलियर तक ले जाने से कोई एक्स्ट्रा मसल ग्रोथ नहीं होती, बल्कि आपके जोड़ों और नर्वस सिस्टम पर 40% ज्यादा स्ट्रेस पड़ता है। यानी आप बेवजह चोट का खतरा बढ़ा रहे हैं। असली मसल ग्रोथ होती है जब आप सही फॉर्म के साथ वजन को धीरे-धीरे बढ़ाते हैं और हर सेट में 1 से 2 रेप्स की गुंजाइश छोड़ते हैं। जब आप सही तकनीक अपनाएंगे तो आपकी रिकवरी तेज होगी और आप बिना किसी इंजरी के लगातार प्रोग्रेस कर पाएंगे।",
                    "staging_breakdown": "0:00-0:15 स्क्रीन पर रिसर्च पेपर्स और ग्राफिक्स | 0:15-0:40 सही और गलत फॉर्म का साइड-बाय-साइड वीडियो | 0:40-1:00 1.2 सेकंड का पॉज और निष्कर्ष।",
                },
                "outro": {
                    "title": "45-Second Training Protocol Outro Monologue (Hindi)",
                    "speech": "तो दोस्तों, बॉडी बिल्डिंग या फिटनेस कोई जादू नहीं है, यह पूरी तरह से ह्यूमन बायोलॉजी और अनुशासन का खेल है। मैंने आपके लिए एक पूरा साइंस-बेस्ड वर्कआउट प्लान डिस्क्रिप्शन में बिल्कुल फ्री दिया है जिसे आप अपने फोन में सेव कर सकते हैं। मुझे कमेंट में बताइए कि जिम में आपकी सबसे पसंदीदा एक्सरसाइज कौन सी है? अगर आप भी बिना किसी फालतू सप्लीमेंट के सही तरीके से फिट होना चाहते हैं, तो चैनल को सब्सक्राइब जरूर करें। मिलते हैं अगले वीडियो में!",
                    "staging_breakdown": "0:00-0:20 फ्री वर्कआउट रूटीन लिंक | 0:20-0:35 दर्शकों से उनकी फेवरेट एक्सरसाइज पूछना | 0:35-0:45 वार्म साइन-ऑफ।",
                },
            },
        },
    },

    "science_engineering_curiosity": {
        "domain_id": "science_engineering_curiosity",
        "domain_name": "Science, Physics & Real-World Engineering",
        "sub_niche": "Physics Paradoxes, Engineering Experiments & Extreme Stress Tests",
        "primary_search_topics": [
            "Physics paradox counter intuitive experiment visual proof",
            "Insane mechanical engineering build real world test",
            "Aerospace engineering orbital mechanics simulation",
            "Mathematical intuition visual concept explanation",
            "World record physical science experiment",
            "Deep sea and space extreme environment engineering",
        ],
        "core_verticals": [
            "Physics Paradoxes, Thought Experiments & Visual Proofs",
            "Mechanical Engineering Prototypes & Extreme Stress Tests",
            "Aerospace Engineering, Orbital Mechanics & Rocketry",
            "Mathematical Intuition, Geometry & Computer Science Concepts",
            "Everyday Science Demystification & Natural World Curiosities",
        ],
        "content_portfolio": [
            "15 to 30-Minute High-Production Physical Experiments with Custom Rigs",
            "Phantom Flex 4K High-Speed Slow-Motion Breakdowns",
            "Simulated 3D Finite Element Analysis Visualizations",
            "Collaborations with University Laboratories & Aerospace Facilities",
        ],
        "investigation_methodology": (
            "Building custom physical test rigs, validating results with high-speed camera sensors "
            "(10,000+ FPS), finite element simulations, and peer-reviewing findings with university physicists."
        ),
        "audience_profile": {
            "demographics": "All ages (12–50), STEM students, software developers, engineers, teachers, and universally curious minds worldwide.",
            "psychographics": "Driven by deep intellectual curiosity and wonder; loves visual 'aha!' moments where counter-intuitive physics concepts suddenly click.",
            "consumption_habits": "Watch completion rates exceeding 70%; repeatedly replayed at key experiment moments; recommended by science teachers in classrooms.",
        },
        "domain_positioning_and_moat": {
            "mission": "Igniting universal curiosity by revealing the hidden, counter-intuitive beauty of science and engineering through breathtaking real-world experiments.",
            "positioning": "The fearless science explorer who builds massive real-world contraptions to test fundamental physical laws.",
            "competitive_moat": "Multi-month engineering build complexity, access to extreme testing environments, and peerless visual storytelling.",
        },
        "vocal_cadence_dynamics": {
            "pitch_modulation": "Infectious curiosity and excitement; rises in enthusiasm during the build phase, drops into focused contemplative wonder before the experimental result.",
            "micro_pause_timing": "Inserts a 1.5-second suspenseful pause right before the slow-motion playback reveals the physical outcome.",
            "articulation_and_pacing": "135 WPM balancing infectious energy with crystal-clear pedagogical explanations.",
            "inclusive_pronoun_habit": "Adventurous team framing ('Let's see what happens when we push this to the limit', 'We built something crazy').",
        },
        "signature_phrases": [
            {"phrase": "At first glance, this seems completely impossible according to physics...", "category": "hook", "sample_context": "Introducing a paradox."},
            {"phrase": "To find out what actually happens, we spent three weeks building a custom rig.", "category": "build", "sample_context": "Showing engineering commitment."},
            {"phrase": "Let's roll the high-speed footage and watch it at ten thousand frames per second.", "category": "reveal", "sample_context": "The visual climax."},
        ],
        "monologues_by_language": {
            "en": {
                "thesis": {
                    "title": "45-Second Scientific Paradox Monologue",
                    "speech": "If you ask almost any physicist or engineer this simple question, their immediate intuitive answer will be completely wrong. It sounds like a total violation of the laws of thermodynamics, but under very specific fluid dynamics conditions, matter behaves in ways that completely defy common sense. Most textbook explanations rely on dense differential equations that obscure the actual intuition. So instead of just looking at the math on a blackboard, we spent the last month working with aerospace engineers to construct a full-scale transparent test apparatus to see if this phenomenon actually holds up in the physical world. Let's see what happens.",
                    "staging_breakdown": "0:00-0:08 Teasing the physical paradox with a hands-on demonstration | 0:08-0:25 Time-lapse of constructing the massive custom rig | 0:25-0:45 Slow camera pan across the finished apparatus.",
                },
                "evidence": {
                    "title": "60-Second Physical Experiment Climax Monologue",
                    "speech": "We calibrated our laser sensors, pressurized the main chamber to three hundred PSI, and brought in our high-speed camera shooting at twenty-two thousand frames per second. At normal playback speed, the entire reaction occurs in less than four milliseconds—to the naked eye, it looks like nothing happened. But when we scrub through the high-speed slow-motion buffer, look at this exact frame right here. The boundary layer doesn't separate where classical aerodynamic models predicted; instead, a microscopic toroidal vortex forms, creating a localized low-pressure zone that effectively pulls the projectile forward. That means the textbook formula everyone has been using for forty years missed this critical boundary phenomenon.",
                    "staging_breakdown": "0:00-0:15 Pressure gauge countdown and button trigger | 0:15-0:40 Ultra slow-motion 22,000 FPS playback highlighting vortex | 0:40-1:00 1.5s micro-pause and physics realization.",
                },
                "outro": {
                    "title": "45-Second Wonder & Curiosity Outro Monologue",
                    "speech": "What I love most about science is that whenever you think you have completely mastered a fundamental principle, nature finds a way to surprise you with an entirely new layer of complexity. All the raw sensor logs, CAD files for the test rig, and links to the academic papers are in the description. Let me know in the comments: what physics myth or paradox should we build a rig to test next? If you love seeing real engineering and genuine scientific discovery, hit that subscribe button, stay curious, and I'll see you in the next experiment.",
                    "staging_breakdown": "0:00-0:20 Philosophical reflection on discovery | 0:20-0:35 Community prompt for next experiment build | 0:35-0:45 Energetic sign-off.",
                },
            },
            "hi": {
                "thesis": {
                    "title": "45-Second Scientific Paradox Monologue (Hindi)",
                    "speech": "नमस्कार दोस्तों! आज जो सवाल हम उठाने जा रहे हैं, उसका जवाब 99% लोगों को बिल्कुल असंभव लगेगा। पहली नजर में ऐसा लगता है जैसे यह भौतिक विज्ञान के बुनियादी नियमों के ही खिलाफ है। लेकिन जब आप इसे प्रैक्टिकल दुनिया में टेस्ट करते हैं, तो कुदरत का एक ऐसा अनोखा नियम सामने आता है जो दिमाग हिला कर रख देता है। किताबों में अक्सर इसे इतने कठिन फॉर्मूलों से समझाया जाता है कि असली कॉन्सेप्ट समझ ही नहीं आता। इसलिए हमने किसी किताब पर भरोसा करने के बजाय, खुद अपनी वर्कशॉप में पूरे दो हफ्ते लगाकर एक ऐसा स्पेशल एक्सपेरिमेंटल सेटअप तैयार किया है ताकि हम अपनी आंखों से देख सकें कि सच क्या है।",
                    "staging_breakdown": "0:00-0:08 वर्कशॉप में एक्सपेरिमेंटल मॉडल के साथ शुरुआत | 0:08-0:25 टेस्ट रिग बनाने का टाइम-लैप्स फुटेज | 0:25-0:45 एक्सपेरिमेंट शुरू करने का काउंटडाउन।",
                },
                "evidence": {
                    "title": "60-Second Physical Experiment Climax Monologue (Hindi)",
                    "speech": "अब हमने इस टेस्ट के लिए अपने अल्ट्रा हाई-स्पीड कैमरे को 10,000 फ्रेम्स प्रति सेकंड पर सेट किया। नॉर्मल स्पीड पर देखने पर यह सब कुछ पलक झपकते ही, सिर्फ 2 मिलीसेकंड में खत्म हो जाता है। लेकिन जब हम इस स्लो-मोशन फुटेज को फ्रेम-दर-फ्रेम देखते हैं, तो जरा इस हिस्से पर गौर कीजिए! जिस जगह पर हवा के दबाव को घटना चाहिए था, वहां एक ऐसा माइक्रोस्कोपिक भंवर बन रहा है जो पूरे ऑब्जेक्ट को उल्टी दिशा में धकेल रहा है। इसका मतलब जिस सिद्धांत को हम सालों से सही मान रहे थे, वो असलियत में इस खास परिस्थिति में काम ही नहीं करता। यह साइंस की वो खूबसूरती है जो सिर्फ प्रैक्टिकल करके ही देखी जा सकती है।",
                    "staging_breakdown": "0:00-0:15 स्लो-मोशन कैमरे की तैयारी | 0:15-0:40 10,000 FPS पर स्लो-मोशन वीडियो का विश्लेषण | 0:40-1:00 1.5 सेकंड का पॉज और साइंस का आश्चर्य।",
                },
                "outro": {
                    "title": "45-Second Wonder & Curiosity Outro Monologue (Hindi)",
                    "speech": "तो दोस्तों, साइंस का असली मजा यही है कि जब भी हमें लगता है कि हम सब कुछ जान चुके हैं, कुदरत हमें एक नया रहस्य दिखा देती है। इस पूरे एक्सपेरिमेंट के 3D मॉडल्स और रिसर्च पेपर्स के लिंक्स नीचे डिस्क्रिप्शन में हैं। आप मुझे कमेंट में बताइए कि ऐसा कौन सा दूसरा साइंस मिथक है जिसका टेस्ट हमें अपनी अगली वीडियो में करना चाहिए? अगर आपको रियल साइंस और इंजीनियरिंग देखना पसंद है तो चैनल को सब्सक्राइब जरूर करें। सीखते रहिए, उत्सुक रहिए, मिलते हैं अगले वीडियो में!",
                    "staging_breakdown": "0:00-0:20 विज्ञान और जिज्ञासा का संदेश | 0:20-0:35 अगले एक्सपेरिमेंट के लिए दर्शकों से आइडिया मांगना | 0:35-0:45 वार्म साइन-ऑफ।",
                },
            },
        },
    },
}

# Known Creator Database for Instant, High-Precision Recognition
KNOWN_CREATORS: Dict[str, Tuple[str, str]] = {
    # format: "creator_slug/name_keyword": ("domain_id", "default_lang")
    "dhruv rathee": ("civic_social_issues", "hi"),
    "dhruvrathee": ("civic_social_issues", "hi"),
    "marques brownlee": ("tech_gadgets", "en"),
    "mkbhd": ("tech_gadgets", "en"),
    "mrwhosetheboss": ("tech_gadgets", "en"),
    "arun maini": ("tech_gadgets", "en"),
    "linus tech tips": ("tech_gadgets", "en"),
    "ltt": ("tech_gadgets", "en"),
    "technical guruji": ("tech_gadgets", "hi"),
    "gaurav chaudhary": ("tech_gadgets", "hi"),
    "tech burner": ("tech_gadgets", "hi"),
    "trakin tech": ("tech_gadgets", "hi"),
    "beebom": ("tech_gadgets", "en"),
    "dave2d": ("tech_gadgets", "en"),
    "cleo abram": ("tech_gadgets", "en"),

    "finance with sharan": ("personal_finance", "hi"),
    "sharan hegde": ("personal_finance", "hi"),
    "graham stephan": ("personal_finance", "en"),
    "andrei jikh": ("personal_finance", "en"),
    "ankur warikoo": ("productivity_growth", "hi"),
    "pranjal kamra": ("personal_finance", "hi"),
    "ca rachana ranade": ("personal_finance", "hi"),
    "akshat shrivastava": ("personal_finance", "hi"),
    "humphrey yang": ("personal_finance", "en"),

    "ali abdaal": ("productivity_growth", "en"),
    "matt d'avella": ("productivity_growth", "en"),
    "thomas frank": ("productivity_growth", "en"),
    "james clear": ("productivity_growth", "en"),

    "johnny harris": ("civic_social_issues", "en"),
    "nitish rajput": ("civic_social_issues", "hi"),
    "deshbhakt": ("civic_social_issues", "hi"),
    "akash banerjee": ("civic_social_issues", "hi"),
    "ravish kumar": ("civic_social_issues", "hi"),

    "think school": ("startups_business", "hi"),
    "garry tan": ("startups_business", "en"),
    "alex hormozi": ("startups_business", "en"),
    "y combinator": ("startups_business", "en"),
    "my first million": ("startups_business", "en"),

    "andrew huberman": ("health_fitness", "en"),
    "huberman lab": ("health_fitness", "en"),
    "jeff nippard": ("health_fitness", "en"),
    "peter attia": ("health_fitness", "en"),
    "athlean-x": ("health_fitness", "en"),

    "veritasium": ("science_engineering_curiosity", "en"),
    "derek muller": ("science_engineering_curiosity", "en"),
    "mark rober": ("science_engineering_curiosity", "en"),
    "smarter every day": ("science_engineering_curiosity", "en"),
    "destin sandlin": ("science_engineering_curiosity", "en"),
    "3blue1brown": ("science_engineering_curiosity", "en"),
}

# Domain keyword clusters for dynamic classification of unknown creators
KEYWORD_CLUSTERS: Dict[str, List[str]] = {
    "tech_gadgets": [
        "phone", "smartphone", "iphone", "android", "samsung", "pixel", "unboxing", "review",
        "laptop", "macbook", "gpu", "nvidia", "hardware", "camera", "ev", "electric vehicle",
        "tesla", "gadget", "processor", "battery", "display", "specs", "benchmark", "ai pin"
    ],
    "personal_finance": [
        "finance", "money", "invest", "investing", "stock", "stocks", "mutual fund", "sip",
        "tax", "taxes", "regime", "deduction", "credit card", "real estate", "wealth", "crypto",
        "bitcoin", "dividend", "portfolio", "retirement", "fire", "salary", "budget", "fd"
    ],
    "productivity_growth": [
        "productivity", "notion", "second brain", "habit", "habits", "routine", "morning routine",
        "deep work", "focus", "procrastination", "study", "books", "reading", "time management",
        "system", "life design", "burnout", "discipline", "creator economy", "side hustle"
    ],
    "civic_social_issues": [
        "scam", "election", "democracy", "government", "policy", "truth", "reality", "sach",
        "court", "law", "parliament", "protest", "climate", "pollution", "environment", "geopolitics",
        "history", "rationale", "civic", "rights", "ground reality", "corruption", "fact check"
    ],
    "startups_business": [
        "startup", "business", "founder", "valuation", "unicorn", "venture capital", "vc",
        "monopoly", "moat", "revenue", "profit", "burn rate", "sales", "marketing", "gtm",
        "case study", "company", "strategy", "enterprise", "b2b", "saas", "pitch deck"
    ],
    "health_fitness": [
        "workout", "fitness", "gym", "muscle", "hypertrophy", "training", "diet", "protein",
        "sleep", "circadian", "longevity", "cardio", "vo2", "supplement", "biomechanics",
        "fat loss", "lifting", "health", "metabolism", "huberman", "nutrition"
    ],
    "science_engineering_curiosity": [
        "physics", "engineering", "experiment", "build", "math", "mathematics", "space",
        "rocket", "nasa", "paradox", "slow motion", "simulation", "chemistry", "quantum",
        "mechanics", "fluid", "scale model", "science", "veritasium", "invention"
    ],
}


class DomainIntelligenceService:
    """Master orchestrator for identifying creator niche, domain, and content pillars."""

    def identify_domain_id(
        self,
        creator_name: str,
        niche_hint: Optional[str] = None,
        sample_titles: Optional[List[str]] = None,
        bio: Optional[str] = None,
    ) -> str:
        """
        Determines the standardized domain_id for any creator.
        Prioritizes:
        1. Known creator catalog
        2. Explicit niche hint matching
        3. Title / bio keyword scoring
        4. Fallback to tech_gadgets or civic_social_issues based on hints
        """
        c_lower = creator_name.lower().strip()

        # 1. Direct match in known database
        for known_key, (dom_id, _) in KNOWN_CREATORS.items():
            if known_key in c_lower or c_lower in known_key:
                logger.info(f"[DomainIntel] Matched known creator '{creator_name}' -> domain '{dom_id}'")
                return dom_id

        # 2. Match against niche_hint if provided
        if niche_hint and niche_hint.lower() not in ["auto", "none", "", "all"]:
            nh_lower = niche_hint.lower()
            for dom_id, archetype in DOMAIN_ARCHETYPES.items():
                if dom_id in nh_lower or archetype["domain_name"].lower() in nh_lower or archetype["sub_niche"].lower() in nh_lower:
                    logger.info(f"[DomainIntel] Matched niche hint '{niche_hint}' -> domain '{dom_id}'")
                    return dom_id
            # Also check keywords in niche hint
            scores = {dom: 0 for dom in DOMAIN_ARCHETYPES}
            for dom, kw_list in KEYWORD_CLUSTERS.items():
                for kw in kw_list:
                    if re.search(rf"\b{kw}\b", nh_lower):
                        scores[dom] += 3
            best_dom = max(scores, key=scores.get)
            if scores[best_dom] > 0:
                logger.info(f"[DomainIntel] Inferred from niche hint '{niche_hint}' -> domain '{best_dom}' (score={scores[best_dom]})")
                return best_dom

            # If explicit niche_hint provided but didn't match any pre-built archetype, it is a custom niche
            logger.info(f"[DomainIntel] Niche hint '{niche_hint}' is a novel domain -> 'custom_niche'")
            return "custom_niche"

        # 3. Analyze content titles and bio
        combined_text = f"{creator_name} "
        if bio:
            combined_text += f"{bio} "
        if sample_titles:
            combined_text += " ".join(sample_titles[:15])

        text_lower = combined_text.lower()
        scores = {dom: 0 for dom in DOMAIN_ARCHETYPES}
        for dom, kw_list in KEYWORD_CLUSTERS.items():
            for kw in kw_list:
                matches = len(re.findall(rf"\b{kw}\b", text_lower))
                scores[dom] += matches

        best_dom = max(scores, key=scores.get)
        if scores[best_dom] > 0:
            logger.info(f"[DomainIntel] Analyzed titles/bio for '{creator_name}' -> best domain '{best_dom}' (score={scores[best_dom]})")
            return best_dom

        # Default fallback
        logger.info(f"[DomainIntel] No strong domain signal for '{creator_name}', defaulting to 'tech_gadgets'")
        return "tech_gadgets"

    def get_creator_domain_profile(
        self,
        creator_name: str,
        niche_hint: Optional[str] = None,
        sample_titles: Optional[List[str]] = None,
        bio: Optional[str] = None,
        language: str = "en",
    ) -> CreatorDomainProfile:
        """
        Builds and returns a complete, fully fleshed-out CreatorDomainProfile
        adapted to the creator's identified domain and native language.
        """
        domain_id = self.identify_domain_id(creator_name, niche_hint, sample_titles, bio)

        # Check if pre-built archetype exists
        if domain_id in DOMAIN_ARCHETYPES:
            arch = DOMAIN_ARCHETYPES[domain_id]
            lang_code = language.lower() if language else "en"
            if lang_code not in ["en", "hi", "es"]:
                lang_code = "en"

            # Extract monologues in target language (or English fallback)
            monologue_pack = arch["monologues_by_language"].get(lang_code, arch["monologues_by_language"]["en"])
            domain_monologues = {
                "thesis_monologue": DomainMonologue(
                    title=monologue_pack["thesis"]["title"],
                    speech=monologue_pack["thesis"]["speech"],
                    staging_breakdown=monologue_pack["thesis"]["staging_breakdown"],
                ),
                "evidence_monologue": DomainMonologue(
                    title=monologue_pack["evidence"]["title"],
                    speech=monologue_pack["evidence"]["speech"],
                    staging_breakdown=monologue_pack["evidence"]["staging_breakdown"],
                ),
                "outro_monologue": DomainMonologue(
                    title=monologue_pack["outro"]["title"],
                    speech=monologue_pack["outro"]["speech"],
                    staging_breakdown=monologue_pack["outro"]["staging_breakdown"],
                ),
            }

            # Sample hooks adapted to domain
            hooks = [
                f"What if everything you've been told about {arch['core_verticals'][0].split(',')[0]} is completely backwards?",
                f"The hidden truth about this that mainstream coverage is completely ignoring.",
                f"Here is the single data point that changed my entire perspective on {arch['domain_name']}.",
            ]
            if lang_code == "hi":
                hooks = [
                    f"क्या आपने कभी सोचा है कि इसके पीछे का असली सच क्या है?",
                    f"यह एक ऐसा सच है जो 99% लोग नहीं जानते...",
                    f"अगर आप भी यह गलती कर रहे हैं, तो अभी रुक जाइए—डेटा और सबूतों के साथ पूरा सच जानिए।",
                ]

            return CreatorDomainProfile(
                domain_id=domain_id,
                domain_name=arch["domain_name"],
                sub_niche=arch["sub_niche"],
                primary_search_topics=arch["primary_search_topics"],
                core_verticals=arch["core_verticals"],
                content_portfolio=arch["content_portfolio"],
                investigation_methodology=arch["investigation_methodology"],
                audience_profile=DomainAudienceProfile(**arch["audience_profile"]),
                domain_positioning_and_moat=DomainMoat(**arch["domain_positioning_and_moat"]),
                domain_monologues=domain_monologues,
                vocal_cadence_dynamics=DomainCadence(**arch["vocal_cadence_dynamics"]),
                signature_phrases=arch["signature_phrases"],
                sample_hooks=hooks,
            )

        # Dynamic synthesis for novel / unknown domains
        return self._synthesize_custom_domain(creator_name, niche_hint or "General Knowledge", language)

    def _synthesize_custom_domain(
        self, creator_name: str, niche: str, language: str = "en"
    ) -> CreatorDomainProfile:
        """Synthesizes a high-fidelity domain profile for completely novel or uncatalogued niches."""
        clean_niche = niche.strip().title()
        lang_code = language.lower() if language else "en"

        primary_topics = [
            f"{clean_niche} deep dive tutorial analysis",
            f"{clean_niche} latest breakthrough trends and developments",
            f"{clean_niche} top mistakes beginners make and how to fix them",
            f"{clean_niche} real world test and expert breakdown",
        ]

        verticals = [
            f"{clean_niche} Foundational Principles & Mental Models",
            f"{clean_niche} Advanced Case Studies & Real-World Implementations",
            f"{clean_niche} Tool Reviews, Workflows & Best Practices",
            f"{clean_niche} Future Trends, Ethical Questions & Industry Transformations",
        ]

        portfolio = [
            f"12 to 20-Minute Actionable Explainer Videos on {clean_niche}",
            f"30 to 60-Second Rapid Tip Shorts & Micro-Breakdowns",
            f"Comprehensive Step-by-Step Walkthroughs & Teardowns",
        ]

        methodology = (
            f"Systematic review of validated research, practical hands-on testing, "
            f"and transparent data reporting within the {clean_niche} ecosystem."
        )

        audience = DomainAudienceProfile(
            demographics=f"Passionate learners, practitioners, and professionals aged 18–45 interested in {clean_niche}.",
            psychographics=f"Seeks actionable clarity, verified best practices, and deep subject-matter mastery without promotional fluff.",
            consumption_habits=f"High average watch time; saves reference videos for practical implementation; actively participates in specialized community discussions.",
        )

        moat = DomainMoat(
            mission=f"Empowering the community through authoritative, clear, and engaging educational content on {clean_niche}.",
            positioning=f"The premier digital educator and expert guide for {clean_niche}.",
            competitive_moat=f"Consistent analytical depth, authentic practical experience, and deep audience trust.",
        )

        cadence = DomainCadence(
            pitch_modulation="Engaged, authoritative, and articulate; emphasizes key conceptual turning points with measured vocal gravity.",
            micro_pause_timing="1.0-second intentional pauses following core thesis points to allow conceptual integration.",
            articulation_and_pacing="130 WPM with clear articulation and energetic pacing.",
            inclusive_pronoun_habit="Collaborative peer dynamic ('Together, let's explore...', 'Here is what we discovered').",
        )

        thesis_speech = (
            f"Hey friends, welcome back. Today, we are diving deep into {clean_niche}, and we're looking at a fundamental shift "
            f"that is changing how everyone in this space operates. Most people believe the conventional wisdom, but when you "
            f"look at the real-world evidence, a completely different picture emerges. Let's break down the exact mechanics."
        )
        if lang_code == "hi":
            thesis_speech = (
                f"नमस्कार दोस्तों! आज के इस वीडियो में हम बात करेंगे {clean_niche} के बारे में। ज्यादातर लोग इस विषय में वही पुरानी "
                f"बातों पर यकीन करते हैं, लेकिन जब आप जमीनी हकीकत और नए डेटा को देखते हैं तो सच्चाई बिल्कुल अलग निकल कर आती है। "
                f"आइए आज इस पूरे विषय को बिना किसी बायस के गहराई से समझते हैं।"
            )

        monologues = {
            "thesis_monologue": DomainMonologue(
                title=f"45-Second {clean_niche} Thesis Monologue",
                speech=thesis_speech,
                staging_breakdown="0:00-0:08 Hook | 0:08-0:25 Contradiction teaser | 0:25-0:45 Thesis promise.",
            ),
            "evidence_monologue": DomainMonologue(
                title=f"60-Second {clean_niche} Deep-Dive Monologue",
                speech=f"When we look at the actual data and empirical case studies in {clean_niche}, the pattern becomes unmistakable...",
                staging_breakdown="0:00-0:15 Myth breakdown | 0:15-0:40 Data display | 0:40-1:00 Punchline question.",
            ),
            "outro_monologue": DomainMonologue(
                title=f"45-Second {clean_niche} Community Call-to-Action Monologue",
                speech=f"At the end of the day, mastering {clean_niche} requires consistent application rather than passive observation...",
                staging_breakdown="0:00-0:20 Synthesis | 0:20-0:35 Comment prompt | 0:35-0:45 Outro.",
            ),
        }

        return CreatorDomainProfile(
            domain_id="custom_niche",
            domain_name=clean_niche,
            sub_niche=f"Specialized {clean_niche} Studies",
            primary_search_topics=primary_topics,
            core_verticals=verticals,
            content_portfolio=portfolio,
            investigation_methodology=methodology,
            audience_profile=audience,
            domain_positioning_and_moat=moat,
            domain_monologues=monologues,
            vocal_cadence_dynamics=cadence,
            signature_phrases=[
                {"phrase": f"Here is the truth about {clean_niche}...", "category": "hook", "sample_context": "Opening thesis."}
            ],
            sample_hooks=[
                f"What if everything you've learned about {clean_niche} is wrong?",
                f"The single biggest mistake people make in {clean_niche}.",
            ],
        )


domain_service = DomainIntelligenceService()
