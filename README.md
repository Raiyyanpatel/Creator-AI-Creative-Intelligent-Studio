# Creator AI — Backend Engine

> High-performance multimodal creator intelligence & automated publishing backend engineered for the **Creator AI React Native Mobile App**.

Built with **FastAPI**, **Composio**, **yt-dlp**, **YouTube Transcript API**, **Feedparser**, and **Google Trends Realtime Feeds**.

---

## 🚀 Key Features & APIs

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| **`/profiling`** | `POST` | Ingests real creator videos, shorts, transcripts, Substack newsletters, and social posts. Deeply extracts tone, video duration distribution, video types, thumbnail strategies, and authentic spoken vocal mannerisms ("what user says often"), generating `user.md` and `hook.md`. |
| **`/profiling/{slug}`** | `GET` | Fetches previously saved `user.md` and `hook.md` for a creator directly from disk. |
| **`/dashboard`** | `GET`, `POST` | Cross-platform metrics (YouTube, Substack, LinkedIn, X/Twitter) + in-app Creator AI pipeline analytics (scripts, hooks, pending approvals, published) + formatted datasets for React Native charts. |
| **`/trends`** | `GET`, `POST` | Live Google Trends RSS feeds, domain/niche-specific trending topics, viral format templates, and actionable content angles. |
| **`/publish`** | `POST` | Submits content for multi-platform publishing (YouTube, LinkedIn, X, Substack) with strict **Human-In-The-Loop Approval**. |
| **`/publish/jobs`** | `GET` | Lists publishing jobs and pending approval queue. |
| **`/publish/jobs/{id}/approve`** | `POST` | Authorizes content and dispatches live via **Composio**. |
| **`/publish/jobs/{id}/reject`** | `POST` | Rejects content with reviewer feedback. |

---

## 🛠️ Quick Start

### 1. Environment Setup
```bash
# Clone or open repository
cd c:\MangoDB-iqoo

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies (already pre-installed)
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)
Copy `.env.example` to `.env`:
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional: Add keys for custom LLMs and Composio
COMPOSIO_API_KEY=your_composio_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Launch Backend Server
```bash
python run.py
```
Server runs at `http://localhost:8000` with interactive Swagger UI at `http://localhost:8000/docs`.

### 4. Run Automated Test Suite
```bash
python test_endpoints.py
```

---

## 📡 API Reference for React Native

### 1. `/profiling`
**Request:**
```json
POST /profiling
{
  "creator_name": "Ali Abdaal",
  "youtube_handle_or_url": "https://www.youtube.com/@aliabdaal",
  "substack_handle_or_url": "https://aliabdaal.substack.com/feed",
  "max_videos_to_analyze": 8,
  "max_articles_to_analyze": 5
}
```
**Output:**
- Real video duration analytics & shorts vs long-form ratios.
- Spoken transcripts mined for signature vocal mannerisms (`"Hey friends, welcome back..."`, `"Here's the honest truth"`).
- Production of `user.md` and `hook.md` saved under `creators/{creator_slug}/`.

---

### 2. `/dashboard`
**Request:**
```http
GET /dashboard?creator_name=Ali%20Abdaal&timeframe=30d
```
**Output:**
- Platform-by-platform followers, views, engagement rates, top-performing formats.
- In-app metrics (scripts generated, hooks created, pending approvals, published posts).
- `charts.views_trend`: Array of `{ label, youtube_views, social_engagement, substack_reads }` ready for React Native chart libraries (`victory-native`, `react-native-gifted-charts`, etc.).

---

### 3. `/trends`
**Request:**
```http
GET /trends?domain=Tech%20%26%20AI&geo=US&limit=10
```
**Output:**
- Real-time world trends from live Google Trends RSS feed.
- Niche trends filtered by creator's domain.
- Viral format blueprints (e.g. *Why Everyone Is Wrong About X*, *30-Day Transformation*).
- Actionable opening hook angles tailored to current trends.

---

### 4. `/publish` & Human Approval Workflow
**Step 1: Submit draft content**
```json
POST /publish/request
{
  "creator_id": "ali-abdaal",
  "platform": "twitter",
  "content_format": "post",
  "title": "Systems over Goals",
  "content": "Most people think inconsistency is a character flaw. It's actually an uncalibrated feedback loop.",
  "require_human_approval": true
}
```
*Returns job with status `PENDING_APPROVAL`.*

**Step 2: Creator approves draft in mobile app**
```json
POST /publish/jobs/pub_a31807b3ca/approve
{
  "reviewer_name": "Ali Abdaal",
  "feedback": "LGTM, publish immediately."
}
```
*Authorizes dispatch and triggers **Composio** action (`Action.TWITTER_CREATION_OF_A_POST`, `Action.LINKEDIN_CREATE_A_POST`, etc.) returning the live published URL.*
