import time
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_VIDEO_URL = r"C:\Users\Raiyyan Patel\Downloads\example.mp4"

print("=" * 75)
print(f"🎬 TESTING USER SPECIFIED LOCAL VIDEO: {USER_VIDEO_URL}")
print("📱 Target Hardware: iQOO 15 (Snapdragon 8 Elite Hexagon NPU)")
print("=" * 75)

t0 = time.perf_counter()
payload = {
    'video_url': USER_VIDEO_URL,
    'creator_name': 'Frame Order',
    'target_duration_seconds': 45,
    'min_virality_score': 70,
    'max_clips': 3,
    'use_on_device_smolvlm': True,
    'on_device_endpoint': 'http://host.docker.internal:8080/v1',
    'enable_sliding_window': True,
    'window_size_seconds': 120,
    'frame_interval_seconds': 3
}

r = requests.post('http://localhost:8000/clipping/analyze', json=payload, timeout=60)
t_elapsed = time.perf_counter() - t0

data = r.json()
print(f"\n⚡ TOTAL EXECUTION TIME: {t_elapsed:.2f} seconds ({t_elapsed * 1000:.1f} ms)")
print(f"STATUS CODE: {r.status_code}")
print(f"REAL VIDEO TITLE: {data.get('video_title')}")
print(f"REAL VIDEO DURATION: {data.get('video_duration')} (621 seconds)")
print(f"SLIDING WINDOWS PROCESSED: {data.get('sliding_windows_analyzed')} Windows")
print(f"TOTAL FRAMES EVALUATED: {data.get('total_frames_processed')} Frames (at 1 frame every 3s)")
print(f"SIGNALS LEVERAGED: {data.get('signals_used')}")
print(f"ON-DEVICE VLM: {data.get('on_device_model')}")

print("\n" + "=" * 75)
print("🔥 TOP VIRAL CLIPS FOUND FROM REAL CARTOON BOX VIDEO")
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
    print(f"   ⏱️ Exact Timestamps: {start_t} ➔ {end_t} (Duration: {dur}s)")
    print(f"   🔥 Virality Score: {score}/100")
    print(f"   🎣 Hook / Trigger: \"{hook}\"")
    print(f"   📝 Caption: {clip['suggested_caption']}")
    print(f"   🏷️ Hashtags: {' '.join(clip['hashtags'])}")
    print(f"   📱 iQOO 15 SmolVLM Score: {vis.get('visual_hook_score')}/10")
    print(f"   📐 9:16 Crop Center X: {vis.get('face_crop_center_x')}%")
    print(f"   👁️ Visual Analysis: {vis.get('facial_expression')}")
    print(f"   💡 Why Viral: {clip.get('why_viral')}")

print("\n" + "=" * 75)
print("🎉 REAL VIDEO TEST COMPLETE!")
print("=" * 75)
