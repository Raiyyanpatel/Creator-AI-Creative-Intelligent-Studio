import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import httpx

payload = {
    'creator_name': 'Dhruv Rathee',
    'location': 'India',
    'niche': 'auto',
    'platforms': ['youtube', 'instagram', 'x_twitter', 'linkedin'],
    'platform_handles': {
        'youtube': '@dhruvrathee',
        'instagram': 'dhruvrathee',
        'x_twitter': 'dhruv_rathee',
        'linkedin': 'dhruv-rathee'
    },
    'goals': {
        'youtube': 'increase_subscribers',
        'instagram': 'more_views_and_followers',
        'x_twitter': 'spread_domain_posts',
        'linkedin': 'increase_connections'
    },
    'language': 'hi',
    'generate_platform_md': True,
    'generate_user_hook_md': True
}

print("Running Multi-Platform Intelligence Pipeline...")
with httpx.Client(timeout=120.0) as client:
    res = client.post('http://localhost:8000/intelligence', json=payload)
    print("Status code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("\n=== MULTI-PLATFORM INTELLIGENCE RESULTS ===")
        print("Identified Domain:", data.get("identified_domain"))
        print("Detected Language:", data.get("detected_language"))
        print("Platforms Analyzed:", data.get("platforms_analyzed"))
        
        print("\n=== EXTRACTED CREATOR FOOTPRINT ===")
        for p, prof in data.get("creator_profiles", {}).items():
            print(f"[{p.upper()}] Handle: {prof.get('handle')}")
            print(f"  Display Name: {prof.get('display_name')}")
            print(f"  Followers/Subs: {prof.get('follower_or_sub_count')}")
            print(f"  Total Catalog: {prof.get('total_posts_or_videos')}")
            print(f"  Verified: {prof.get('verified')}")
            recent = prof.get('recent_content', [])
            print(f"  Recent Content Extracted: {len(recent)} items")
            if recent:
                first = recent[0]
                sample_text = first.get('title') or first.get('caption', '')
                print(f"  Sample Item: {sample_text[:80]} | Engagement: {first.get('likes') or first.get('views') or first.get('engagement')}")
        
        print("\n=== TRENDS DISCOVERY (DOMAIN + LOCATION + GLOBAL) ===")
        for blk in data.get("platform_trends", []):
            p = blk.get("platform")
            d_cnt = len(blk.get("domain_trends", []))
            l_cnt = len(blk.get("location_trends", []))
            g_cnt = len(blk.get("global_trends", []))
            h_cnt = len(blk.get("hashtag_trends", []))
            print(f"[{p.upper()}] Domain Trends: {d_cnt} | Location: {l_cnt} | Global: {g_cnt} | Hashtags: {h_cnt}")
            if blk.get("domain_trends"):
                first_tr = blk["domain_trends"][0]
                print(f"  Top Domain Trend: {first_tr.get('title')} ({first_tr.get('url')})")
        
        print("\n=== GENERATED DOSSIERS ===")
        print("User MD Path:", data.get("user_md_path"))
        print("Hook MD Path:", data.get("hook_md_path"))
        print("Platform MD Files:", list(data.get("platform_md_files", {}).keys()))
    else:
        print("Failed:", res.text[:500])
