import sys
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("RUNNING CREATOR AI BACKEND API VERIFICATION SUITE")
    print("=" * 60)

    # 1. Test Health
    print("\n[1/5] Testing Health Check (/health)...")
    res = client.get("/health")
    assert res.status_code == 200, f"Health failed: {res.text}"
    print("  -> Passed. Server healthy.")

    # 2. Test /trends
    print("\n[2/5] Testing /trends Endpoint (Live Google Trends RSS & Niche Trends)...")
    res = client.get("/trends?domain=Tech%20%26%20AI&geo=US&limit=5")
    assert res.status_code == 200, f"Trends failed: {res.text}"
    trends_data = res.json()
    assert len(trends_data["world_trends"]) > 0, "No world trends returned from Google Trends RSS"
    assert len(trends_data["niche_trends"]) > 0, "No niche trends returned"
    assert len(trends_data["viral_formats"]) > 0, "No viral formats returned"
    print(f"  -> Passed. Fetched {len(trends_data['world_trends'])} real-time world trends and {len(trends_data['niche_trends'])} niche trends.")
    print(f"  -> Sample Live World Trend: '{trends_data['world_trends'][0]['title']}' ({trends_data['world_trends'][0]['traffic_volume']})")

    # 3. Test /dashboard
    print("\n[3/5] Testing /dashboard Endpoint...")
    res = client.get("/dashboard?creator_name=Ali%20Abdaal&timeframe=7d")
    assert res.status_code == 200, f"Dashboard failed: {res.text}"
    dash_data = res.json()
    assert "youtube" in dash_data["platforms"], "YouTube platform data missing in dashboard"
    assert "app_platform_metrics" in dash_data, "App metrics missing"
    assert "charts" in dash_data, "Charts data missing"
    print(f"  -> Passed. Total estimated reach: {dash_data['overall_reach']:,}")
    print(f"  -> Ready-to-render chart data points: {len(dash_data['charts']['views_trend'])}")

    # 4. Test /publish with Human Approval and Composio
    print("\n[4/5] Testing /publish Workflow (Creation -> Pending Approval -> Human Approval -> Composio)...")
    pub_payload = {
        "creator_id": "ali-abdaal",
        "platform": "twitter",
        "content_format": "post",
        "title": "3 Lessons on Inconsistency",
        "content": "Most people think inconsistency is a character flaw. It's actually an uncalibrated feedback loop.",
        "media_urls": [],
        "require_human_approval": True
    }
    create_res = client.post("/publish/request", json=pub_payload)
    assert create_res.status_code == 200, f"Publish create failed: {create_res.text}"
    create_data = create_res.json()
    job_id = create_data["job"]["job_id"]
    assert create_data["job"]["status"] == "PENDING_APPROVAL", "Job should start as PENDING_APPROVAL"
    print(f"  -> Created job: {job_id} with status '{create_data['job']['status']}'")

    # List jobs
    list_res = client.get(f"/publish/jobs?creator_id=ali-abdaal&status=PENDING_APPROVAL")
    assert list_res.status_code == 200
    assert any(j["job_id"] == job_id for j in list_res.json()), "Created job not found in approval queue"
    print(f"  -> Verified job {job_id} in approval queue.")

    # Approve job (Human in the loop)
    approve_res = client.post(
        f"/publish/jobs/{job_id}/approve",
        json={
            "reviewer_name": "Ali Abdaal (Lead Creator)",
            "feedback": "Hook is punchy, approved for direct broadcast."
        }
    )
    assert approve_res.status_code == 200, f"Approve failed: {approve_res.text}"
    approved_data = approve_res.json()
    assert approved_data["job"]["status"] == "PUBLISHED", "Job should transition to PUBLISHED after approval"
    print(f"  -> Human Approval executed. Composio action status: {approved_data['job']['composio_execution_status']}")
    print(f"  -> Published link generated: {approved_data['job']['published_url']}")

    # 5. Test /profiling
    print("\n[5/5] Testing /profiling Endpoint (Ingesting real YouTube videos, Substack & generating user.md / hook.md)...")
    prof_payload = {
        "creator_name": "Ali Abdaal",
        "substack_handle_or_url": "https://aliabdaal.substack.com/feed",
        "max_videos_to_analyze": 3,
        "max_articles_to_analyze": 2
    }
    prof_res = client.post("/profiling", json=prof_payload)
    assert prof_res.status_code == 200, f"Profiling failed: {prof_res.text}"
    prof_data = prof_res.json()
    assert prof_data["user_md"], "user_md not generated"
    assert prof_data["hook_md"], "hook_md not generated"
    assert len(prof_data["analysis"]["frequent_spoken_phrases"]) > 0, "No spoken phrases extracted from transcripts"
    
    print(f"  -> Successfully generated user.md ({len(prof_data['user_md'])} chars) and hook.md ({len(prof_data['hook_md'])} chars)")
    print(f"  -> Spoken vocal mannerisms extracted from audio:")
    for phrase_item in prof_data["analysis"]["frequent_spoken_phrases"][:3]:
        print(f"     * \"{phrase_item['phrase']}\" ({phrase_item['category']})")
    print(f"  -> Persisted files at: {prof_data['file_paths']}")

    print("\n" + "=" * 60)
    print("ALL 4 BACKEND APIS VERIFIED AND PASSING SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
