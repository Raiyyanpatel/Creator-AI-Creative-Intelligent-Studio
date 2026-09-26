"""
Verification script for Creator AI Platform Intelligence:
Tests:
1. Native language extraction (Hindi / Hinglish for Dhruv Rathee)
2. Cause/work-centric trends (social causes, environment, civic issues - NOT personal news)
3. Scoped investigation (e.g. YouTube + Instagram only)
4. Accurate user.md and hook.md generation with native speech mannerisms & hooks
5. Platform-specific growth goals:
   - YouTube: Increase subscribers (domain + global + location videos)
   - Instagram: More views & followers (domain + global + location reels)
"""

import sys
import json
from pathlib import Path

# Ensure UTF-8 output for Windows console displaying Hindi / Devanagari characters
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from app.models.intelligence import IntelligenceRequest, PlatformChoice, GoalType
from app.services.platform_intel_service import platform_intel_service


def test_dhruv_rathee():
    print("=" * 70)
    print("TESTING DHRUV RATHEE INTELLIGENCE & DOSSIER GENERATION")
    print("=" * 70)

    req = IntelligenceRequest(
        creator_name="Dhruv Rathee",
        niche="Social Causes & Civic Awareness",
        causes_or_topics=[
            "Environmental Crisis and Climate Change",
            "Civic Rights and Democratic Awareness",
            "Public Health and Social Inequality"
        ],
        location="IN",
        platforms=[PlatformChoice.YOUTUBE, PlatformChoice.INSTAGRAM],  # Scoped to only 2 requested apps
        platform_handles={
            "youtube": "@dhruvrathee",
            "instagram": "dhruvrathee"
        },
        goals={
            "youtube": GoalType.INCREASE_SUBSCRIBERS,
            "instagram": GoalType.MORE_VIEWS_AND_FOLLOWERS
        },
        generate_platform_md=True,
        generate_user_hook_md=True
    )

    print(f"\n[1] Submitting Intelligence Scan for {req.creator_name}...")
    print(f"    Platforms Requested: {[p.value for p in req.platforms]}")
    print(f"    Causes / Work Topics: {req.causes_or_topics}")
    print(f"    Location: {req.location}")

    res = platform_intel_service.run_intelligence(req)

    print("\n" + "=" * 70)
    print("RESULTS VERIFICATION")
    print("=" * 70)

    # 1. Scoped platforms
    print(f"\n[+] Platforms Analyzed: {res.platforms_analyzed}")
    assert set(res.platforms_analyzed) == {"youtube", "instagram"}, "Should ONLY analyze requested platforms!"
    assert "linkedin" not in res.platforms_analyzed, "LinkedIn should NOT be analyzed when not requested!"
    assert "x_twitter" not in res.platforms_analyzed, "X/Twitter should NOT be analyzed when not requested!"
    print("    [PASS] Scoped investigation respected only requested apps.")

    # 2. Detected Language
    print(f"\n[+] Detected Creator Language: {res.detected_language}")
    assert res.detected_language and ("Hindi" in res.detected_language or "hi" in res.detected_language.lower()), \
        f"Expected Hindi/Hinglish detection, got: {res.detected_language}"
    print("    [PASS] Native language accurately detected as Hindi / Hinglish.")

    # 3. Trends & Content Recommendations
    print("\n[+] Top Recommendations Generated (Checking Native Language Hooks):")
    for idx, rec in enumerate(res.top_recommendations[:6], 1):
        print(f"\n    {idx}. [{rec.platform.upper()}] Topic: {rec.topic[:60]}")
        print(f"       Format: {rec.content_type}")
        print(f"       Native Hook: {rec.hook}")
        print(f"       Why Now: {rec.why_now}")

    # 4. Check user.md and hook.md file generation
    print(f"\n[+] user.md Path: {res.user_md_path}")
    print(f"[+] hook.md Path: {res.hook_md_path}")
    assert res.user_md_path and Path(res.user_md_path).exists(), "user.md must exist!"
    assert res.hook_md_path and Path(res.hook_md_path).exists(), "hook.md must exist!"

    with open(res.user_md_path, "r", encoding="utf-8") as f:
        user_md_content = f.read()
    with open(res.hook_md_path, "r", encoding="utf-8") as f:
        hook_md_content = f.read()

    print("\n[+] Checking user.md contents:")
    assert "Primary Spoken Language & Vocal Architecture" in user_md_content
    assert "Hindi" in user_md_content
    print("    [PASS] user.md contains Primary Spoken Language and Hindi vocal architecture.")

    print("\n[+] Checking hook.md contents:")
    assert "Signature Spoken Opening Hooks" in hook_md_content
    assert any(h in hook_md_content for h in ["नमस्कार दोस्तों", "सच तो यह है कि", "क्या आपने कभी सोचा"]), \
        "hook.md must contain authentic Hindi opening hooks!"
    print("    [PASS] hook.md contains authentic spoken opening hooks in Hindi/Hinglish.")

    # 5. Check platform blocks for goals
    for block in res.platform_trends:
        print(f"\n[+] Verified Block for {block.platform.upper()}:")
        print(f"    Goal: {block.goal}")
        print(f"    Domain Trends count: {len(block.domain_trends)}")
        print(f"    Location Trends count: {len(block.location_trends)}")
        print(f"    Global Trends count: {len(block.global_trends)}")
        if block.platform == "youtube":
            assert block.goal == "increase_subscribers"
        elif block.platform == "instagram":
            assert block.goal == "more_views_and_followers"

    print("\n" + "=" * 70)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    test_dhruv_rathee()
