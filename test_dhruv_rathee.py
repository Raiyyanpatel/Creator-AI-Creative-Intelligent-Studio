"""
Comprehensive Live API Verification for Creator: Dhruv Rathee
Targets http://localhost:8000 (Docker Backend Container)
"""
import sys
import json
import httpx

# Ensure UTF-8 output encoding for Windows terminals
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "http://localhost:8000"

def log_section(title):
    print("\n" + "=" * 70)
    print(f">> {title}")
    print("=" * 70)

def run():
    client = httpx.Client(base_url=BASE_URL, timeout=60.0)

    # 1. Health
    log_section("1. Testing Health Endpoint: GET /health")
    r = client.get("/health")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    assert r.status_code == 200

    # 2. Profiling
    log_section("2. Testing Profiling Engine: POST /profiling")
    prof_payload = {
        "creator_name": "Dhruv Rathee",
        "youtube_handle_or_url": "@dhruvrathee",
        "twitter_handle_or_url": "@dhruv_rathee",
        "max_videos_to_analyze": 3,
        "max_articles_to_analyze": 1
    }
    print(f"Sending payload: {json.dumps(prof_payload, indent=2)}")
    r = client.post("/profiling", json=prof_payload)
    print(f"Status: {r.status_code}")
    assert r.status_code == 200, f"Profiling failed: {r.text}"
    prof_data = r.json()
    slug = prof_data.get("creator_slug", "dhruv_rathee")
    print(f"Creator Slug: {slug}")
    print(f"Tone: {prof_data['analysis']['tone']['primary_tone']} (Energy: {prof_data['analysis']['tone']['energy_level']})")
    print(f"Generated user.md chars: {len(prof_data['user_md'])}, hook.md chars: {len(prof_data['hook_md'])}")
    print(f"Spoken phrases extracted: {len(prof_data['analysis']['frequent_spoken_phrases'])}")
    for p in prof_data['analysis']['frequent_spoken_phrases'][:3]:
        print(f"   * \"{p['phrase']}\" ({p['category']})")

    # 3. GET Profiling Artifacts
    log_section(f"3. Testing Fetch Dossier: GET /profiling/{slug}")
    r = client.get(f"/profiling/{slug}")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        get_prof = r.json()
        print(f"Successfully retrieved files from DB/disk: user.md={len(get_prof.get('user_md', ''))} chars, hook.md={len(get_prof.get('hook_md', ''))} chars")
    else:
        print(f"Response: {r.text}")

    # 4. Dashboard
    log_section("4. Testing Studio Dashboard: GET /dashboard")
    r = client.get("/dashboard", params={"creator_name": "Dhruv Rathee", "timeframe": "30d"})
    print(f"Status: {r.status_code}")
    assert r.status_code == 200, f"Dashboard failed: {r.text}"
    dash_data = r.json()
    print(f"Estimated Overall Reach: {dash_data['overall_reach']:,}")
    print(f"Connected Platforms: {list(dash_data['platforms'].keys())}")
    print(f"App Metrics: {dash_data['app_platform_metrics']}")
    print(f"Views trend points: {len(dash_data['charts']['views_trend'])}")

    # 5. Trends
    log_section("5. Testing Realtime Trends: GET /trends")
    r = client.get("/trends", params={"domain": "Geopolitics & Current Affairs", "geo": "IN", "limit": 4})
    print(f"Status: {r.status_code}")
    assert r.status_code == 200, f"Trends failed: {r.text}"
    trends_data = r.json()
    print(f"Live India World Trends ({len(trends_data['world_trends'])}):")
    for wt in trends_data['world_trends'][:3]:
        print(f"   * {wt['title']} ({wt['traffic_volume']})")
    print(f"Niche Trends ({len(trends_data['niche_trends'])}):")
    for nt in trends_data['niche_trends'][:3]:
        print(f"   * {nt['title']} [{nt.get('category', 'Niche')}]")

    # 6. Intelligence Scan
    log_section("6. Testing 4-Platform Intelligence Engine: POST /intelligence")
    intel_payload = {
        "creator_name": "Dhruv Rathee",
        "niche": "Geopolitics, Current Affairs & Science",
        "location": "IN",
        "platforms": ["youtube", "instagram", "linkedin", "x_twitter"],
        "goals": {
            "youtube": "increase_followers",
            "instagram": "increase_reach",
            "linkedin": "increase_connections",
            "x_twitter": "increase_engagement"
        },
        "handles": {
            "youtube": "dhruvrathee",
            "instagram": "dhruvrathee",
            "linkedin": "dhruvrathee",
            "x_twitter": "dhruv_rathee"
        },
        "generate_platform_md": True
    }
    print(f"Sending payload: {json.dumps(intel_payload, indent=2)}")
    r = client.post("/intelligence", json=intel_payload)
    print(f"Status: {r.status_code}")
    assert r.status_code == 200, f"Intelligence failed: {r.text}"
    intel_data = r.json()
    print(f"Platforms analyzed: {intel_data['platforms_analyzed']}")
    print("Creator Footprint Audited:")
    for p, prof in intel_data["creator_profiles"].items():
        print(f"   * [{p}] Handle: {prof.get('handle')}, Subscribers/Followers: {prof.get('follower_or_sub_count') or 'Audited'}")
        print(f"     Diagnostic: {prof.get('growth_gap_analysis')[:90]}...")
    print(f"Generated platform.md files: {list(intel_data['platform_md_files'].keys())}")
    print(f"Ready-to-Post Recommendations: {len(intel_data['top_recommendations'])}")
    for idx, rec in enumerate(intel_data['top_recommendations'][:3], 1):
        print(f"   [{idx}] {rec['topic']} ({rec['content_type'].upper()})")
        print(f"       Hook: \"{rec['hook']}\"")

    # 7. Quick Intelligence Scan
    log_section("7. Testing Quick Intelligence: GET /intelligence/quick")
    r = client.get("/intelligence/quick", params={
        "creator_name": "Dhruv Rathee",
        "niche": "Education & Facts",
        "location": "IN",
        "platforms": "youtube,x_twitter"
    })
    print(f"Status: {r.status_code}")
    assert r.status_code == 200
    print(f"Quick Scan Analyzed: {r.json()['platforms_analyzed']}")

    # 8. Intelligence Platforms Directory
    log_section("8. Testing Intelligence Platforms: GET /intelligence/platforms")
    r = client.get("/intelligence/platforms")
    print(f"Status: {r.status_code}")
    assert r.status_code == 200
    print(f"Supported platforms: {r.json()['platforms']}")

    # 9. Multi-Platform Publishing Workflow
    log_section("9. Testing Human-in-the-Loop Publishing: POST /publish/request -> GET /publish/jobs -> POST /publish/jobs/{id}/approve")
    pub_payload = {
        "creator_id": slug,
        "platform": "twitter",
        "content_format": "thread",
        "title": "The Hidden Truth Behind Renewable Energy Transitions",
        "content": "Most people think solar energy adoption is just about panel efficiency. But here is the real bottleneck nobody is discussing: grid transmission infrastructure.",
        "media_urls": [],
        "require_human_approval": True
    }
    r = client.post("/publish/request", json=pub_payload)
    print(f"Create Job Status: {r.status_code}")
    assert r.status_code == 200
    job = r.json()["job"]
    job_id = job["job_id"]
    print(f"Job Created: ID={job_id}, Status={job['status']}")

    # Fetch jobs
    r = client.get(f"/publish/jobs?creator_id={slug}&status=PENDING_APPROVAL")
    print(f"Fetch Jobs Status: {r.status_code}")
    assert any(j["job_id"] == job_id for j in r.json()), "Job not in pending approval queue"
    print(f"Job {job_id} confirmed in pending approval queue.")

    # Approve
    r = client.post(f"/publish/jobs/{job_id}/approve", json={
        "reviewer_name": "Dhruv Rathee (Editorial Lead)",
        "feedback": "Factual accuracy verified, ready for publication."
    })
    print(f"Approve Status: {r.status_code}")
    assert r.status_code == 200
    approved_job = r.json()["job"]
    print(f"Job Status after approval: {approved_job['status']}")
    print(f"Composio Dispatch Status: {approved_job['composio_execution_status']}")
    print(f"Published URL: {approved_job.get('published_url')}")

    log_section("=== ALL ENDPOINTS SUCCESSFULLY VERIFIED FOR DHRUV RATHEE! ===")

if __name__ == "__main__":
    run()
