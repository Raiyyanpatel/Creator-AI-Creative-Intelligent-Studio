import time
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REAL_VIDEO_URL = "https://www.youtube.com/watch?v=va4GOYAAu2A"

print("=" * 75)
print("🎬 SLIDING WINDOW MULTI-FRAME VIDEO VLM BENCHMARK")
print(f"📱 Target Hardware: iQOO 15 (Snapdragon 8 Elite Hexagon NPU)")
print(f"🎥 Video URL: {REAL_VIDEO_URL}")
print("=" * 75)

t0 = time.perf_counter()
payload = {
    'video_url': REAL_VIDEO_URL,
    'creator_name': 'Dhruv Rathee',
    'target_duration_seconds': 50,
    'min_virality_score': 70,
    'max_clips': 3,
    'use_on_device_smolvlm': True,
    'on_device_endpoint': 'http://host.docker.internal:8080/v1',
    'enable_sliding_window': True,
    'window_size_seconds': 120,      # 2-minute sliding windows (30s overlap)
    'frame_interval_seconds': 3       # 1 frame every 3 seconds (40 frames/window)
}

r = requests.post('http://localhost:8000/clipping/analyze', json=payload, timeout=30)
t_elapsed = time.perf_counter() - t0

data = r.json()
print(f"\n⚡ TOTAL EXECUTION TIME: {t_elapsed:.2f} seconds ({t_elapsed * 1000:.1f} ms)")
print(f"STATUS CODE: {r.status_code}")
print(f"VIDEO TITLE: {data.get('video_title')}")
print(f"VIDEO DURATION: {data.get('video_duration')}")
print(f"SLIDING WINDOWS PROCESSED: {data.get('sliding_windows_analyzed')} Windows")
print(f"TOTAL FRAMES EVALUATED: {data.get('total_frames_processed')} Frames (at 1 frame every 3s)")
print(f"SIGNALS USED: {data.get('signals_used')}")
print(f"ON-DEVICE VLM: {data.get('on_device_model')}")

print("\n" + "=" * 75)
print("🔥 TOP VIRAL CLIPS IDENTIFIED BY SLIDING WINDOW VLM")
print("=" * 75)

for clip in data.get('top_viral_clips', []):
    rank = clip['rank']
    title = clip['suggested_title']
    score = clip['virality_score']
    start_t = clip['start_time']
    end_t = clip['end_time']
    dur = clip['duration_seconds']
    hook = clip['hook_line']
    vis = clip.get('visual_assessment') or {}

    print(f"\n🎬 [RANK #{rank}] {title}")
    print(f"   ⏱️ Timestamps: {start_t} ➔ {end_t} ({dur}s)")
    print(f"   🔥 Virality Score: {score}/100")
    print(f"   🎣 Opening Hook: \"{hook}\"")
    print(f"   📱 iQOO 15 SmolVLM Score: {vis.get('visual_hook_score')}/10")
    print(f"   📐 9:16 Crop Center X: {vis.get('face_crop_center_x')}%")
    print(f"   👁️ Observed Dynamic: {vis.get('facial_expression')}")
    print(f"   💡 Why Viral: {clip.get('why_viral')[:100]}...")

print("\n" + "=" * 75)
print("🎉 SLIDING WINDOW MULTI-FRAME VLM TEST COMPLETE!")
print("=" * 75)
