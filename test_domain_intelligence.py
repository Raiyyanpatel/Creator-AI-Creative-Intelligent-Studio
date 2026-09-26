"""
Test Suite: Universal Domain & Niche Intelligence
===================================================
Tests dynamic domain identification, custom niche synthesis, and domain-tailored
dossier generation (user.md & hook.md) across diverse creators (Tech, Finance,
Productivity, Health, Civic, and Custom Niches).
"""

import sys
import io

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.domain_service import domain_service, DOMAIN_ARCHETYPES
from app.services.llm_service import llm_service
from app.models.domain import IdentifyDomainRequest
from app.models.intelligence import IntelligenceRequest, PlatformChoice


def test_domain_identification():
    print("=" * 70)
    print("TEST 1: TESTING CREATOR DOMAIN IDENTIFICATION")
    print("=" * 70)

    test_creators = [
        ("Dhruv Rathee", None, "civic_social_issues", "Civic Rights, Democratic Awareness & Public Policy"),
        ("Marques Brownlee", None, "tech_gadgets", "Consumer Technology, Hardware & AI Gadgets"),
        ("Finance With Sharan", None, "personal_finance", "Personal Finance, Wealth Building & Taxation"),
        ("Ali Abdaal", None, "productivity_growth", "Productivity Systems, Deep Work & Creator Growth"),
        ("Andrew Huberman", None, "health_fitness", "Health Optimization, Exercise Science & Longevity"),
        ("Think School", None, "startups_business", "Startups, Business Strategy & Venture Capital"),
        ("Veritasium", None, "science_engineering_curiosity", "Science, Physics & Real-World Engineering"),
    ]

    for creator_name, hint, expected_domain_id, expected_domain_name in test_creators:
        prof = domain_service.get_creator_domain_profile(creator_name, niche_hint=hint)
        print(f"[+] Creator: {creator_name:<20} -> Domain: '{prof.domain_name}' (id: {prof.domain_id})")
        assert prof.domain_id == expected_domain_id, f"Expected {expected_domain_id}, got {prof.domain_id}"
        assert prof.domain_name == expected_domain_name
        assert len(prof.core_verticals) >= 4
        assert len(prof.primary_search_topics) >= 4
        assert prof.investigation_methodology
        assert prof.audience_profile.psychographics

    print("\n[PASS] All recognized creators accurately identified with their specific domains!\n")


def test_custom_niche_synthesis():
    print("=" * 70)
    print("TEST 2: TESTING DYNAMIC CUSTOM NICHE SYNTHESIS")
    print("=" * 70)

    custom_creator = "AeroDrone Academy"
    custom_niche = "FPV Drone Cinematography & Racing"

    prof = domain_service.get_creator_domain_profile(
        creator_name=custom_creator,
        niche_hint=custom_niche,
        language="en"
    )

    print(f"[+] Custom Creator: {custom_creator}")
    print(f"    Domain Name: {prof.domain_name}")
    print(f"    Core Verticals: {prof.core_verticals}")
    print(f"    Search Topics: {prof.primary_search_topics[:2]}")
    print(f"    Methodology: {prof.investigation_methodology}")
    print(f"    Thesis Monologue: {prof.domain_monologues['thesis_monologue'].speech[:100]}...")

    assert prof.domain_name == "Fpv Drone Cinematography & Racing"
    assert len(prof.primary_search_topics) >= 3
    assert "FPV Drone Cinematography & Racing" in prof.core_verticals[0] or "Fpv Drone" in prof.core_verticals[0]
    print("\n[PASS] Arbitrary / custom creator niches synthesized dynamically with full profiles!\n")


def test_tech_creator_dossier_generation():
    print("=" * 70)
    print("TEST 3: GENERATING DOSSIER FOR TECH CREATOR (MARQUES BROWNLEE)")
    print("=" * 70)

    # Mock video data for Marques Brownlee
    mkbhd_videos = {
        "videos": [
            {
                "title": "Smartphone Camera Shootout 2024!",
                "duration_seconds": 960,
                "is_short": False,
                "key_opening_words": "So I've been using this phone as my daily driver...",
                "transcript_snippet": "The camera on this new flagship has an incredible sensor, but the thermal throttling is a big problem."
            },
            {
                "title": "The Truth About Electric Vehicles in Cold Weather",
                "duration_seconds": 840,
                "is_short": False,
                "key_opening_words": "Here is the honest truth about EV range...",
                "transcript_snippet": "We ran our standardized battery drain loop in freezing temperatures to see the real drop."
            },
            {
                "title": "Apple Vision Pro: 6 Months Later!",
                "duration_seconds": 1100,
                "is_short": False,
                "key_opening_words": "Welcome back to the studio...",
                "transcript_snippet": "Spatial computing is fascinating, but at thirty-five hundred dollars, who is this actually for?"
            }
        ],
        "shorts_count": 5
    }

    res = llm_service.profile_creator(
        creator_name="Marques Brownlee",
        youtube_data=mkbhd_videos,
        niche="Consumer Tech & Gadgets",
        language="en"
    )

    user_md = res["user_md"]
    hook_md = res["hook_md"]
    identified_domain = res["identified_domain"]

    print(f"[+] Identified Domain: {identified_domain}")
    print(f"[+] Detected Language: {res['detected_language']}")
    print(f"[+] user.md written to: {res['file_paths']['user_md']}")
    print(f"[+] hook.md written to: {res['file_paths']['hook_md']}")

    # Verification: user.md MUST contain Tech domain elements, NOT Civic elements!
    assert "Consumer Technology" in user_md, "user.md must contain Tech domain title"
    assert "daily driver" in user_md.lower() or "hardware" in user_md.lower() or "spec" in user_md.lower()
    assert "battery drain" in user_md.lower() or "benchmark" in user_md.lower()
    assert "Electoral Systems" not in user_md, "user.md must NOT contain Dhruv Rathee's civic verticals for a tech creator!"

    # Verification: hook.md MUST contain Tech monologues
    assert "Consumer Technology" in hook_md or "daily driver" in hook_md.lower() or "hardware" in hook_md.lower()
    assert "Civic Responsibility" not in hook_md, "hook.md must NOT contain civic monologues for a tech creator!"

    print("\n[PASS] Marques Brownlee dossier generated with 100% domain-accurate Tech monologues and verticals!\n")


def test_finance_creator_dossier_generation():
    print("=" * 70)
    print("TEST 4: GENERATING DOSSIER FOR FINANCE CREATOR (SHARAN HEGDE)")
    print("=" * 70)

    sharan_videos = {
        "videos": [
            {
                "title": "New Tax Regime vs Old Tax Regime: Which is Better?",
                "duration_seconds": 720,
                "is_short": False,
                "key_opening_words": "Stop investing in mutual funds before knowing this...",
                "transcript_snippet": "Here is the exact excel sheet that shows how much tax you will pay under section 80C."
            },
            {
                "title": "How Index Funds Make You Rich",
                "duration_seconds": 650,
                "is_short": False,
                "key_opening_words": "If you invest ₹10,000 every month...",
                "transcript_snippet": "A 1.5% expense ratio in a regular plan wipes out 30% of your total retirement wealth."
            }
        ],
        "shorts_count": 8
    }

    res = llm_service.profile_creator(
        creator_name="Finance With Sharan",
        youtube_data=sharan_videos,
        niche="Personal Finance & Investing",
        language="hi"
    )

    user_md = res["user_md"]
    hook_md = res["hook_md"]
    identified_domain = res["identified_domain"]

    print(f"[+] Identified Domain: {identified_domain}")
    print(f"[+] Detected Language: {res['detected_language']}")
    print(f"[+] user.md written to: {res['file_paths']['user_md']}")
    print(f"[+] hook.md written to: {res['file_paths']['hook_md']}")

    # Verification: user.md MUST contain Personal Finance domain elements in Hindi/Hinglish
    assert "Personal Finance" in user_md
    assert "SIP" in user_md or "इंडेक्स" in user_md or "टैक्स" in user_md or "wealth" in user_md.lower()
    assert "Electoral Systems" not in user_md, "Finance creator must not have civic electoral verticals!"

    print("\n[PASS] Finance With Sharan dossier generated with 100% domain-accurate Finance monologues in Hindi!\n")


if __name__ == "__main__":
    test_domain_identification()
    test_custom_niche_synthesis()
    test_tech_creator_dossier_generation()
    test_finance_creator_dossier_generation()
    print("=" * 70)
    print("ALL UNIVERSAL DOMAIN INTELLIGENCE TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)
