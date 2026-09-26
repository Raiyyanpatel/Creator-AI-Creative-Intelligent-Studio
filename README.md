# Creator AI — Backend Engine

> High-performance multimodal creator intelligence, profiling, and automated publishing backend engineered for the **Creator AI React Native Mobile App**.

Built with **FastAPI**, **PostgreSQL 16**, **Docker & Docker Compose**, **Composio**, **yt-dlp**, **YouTube Transcript API**, **Feedparser**, and **Google Trends Realtime Feeds**.

---

## 🚀 Key Features & APIs

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| **`/profiling`** | `POST` | Ingests real creator videos, shorts, transcripts, Substack newsletters, and social posts. Deeply extracts tone, video duration distribution, video types, thumbnail strategies, and authentic spoken vocal mannerisms ("what user says often"), generating `user.md` and `hook.md`. Persists directly into PostgreSQL and disk. |
| **`/profiling/{slug}`** | `GET` | Fetches previously saved `user.md` and `hook.md` for a creator directly. |
| **`/dashboard`** | `GET`, `POST` | Cross-platform metrics (YouTube, Substack, LinkedIn, X/Twitter) + in-app Creator AI pipeline analytics (scripts, hooks, pending approvals, published) + formatted datasets for React Native charts. |
| **`/trends`** | `GET`, `POST` | Live Google Trends RSS feeds, domain/niche-specific trending topics, viral format templates, and actionable content angles. |
| **`/intelligence`** | `POST` | **🆕 Cross-platform trend intelligence.** Scans YouTube, Instagram, LinkedIn, and X/Twitter for domain, location, and global trends. Generates `platform_{name}.md` files with trending links, hashtags, content strategies, and AI-powered recommendations. |
| **`/intelligence/quick`** | `GET` | Lightweight GET version of the intelligence scan via query params. |
| **`/intelligence/platforms`** | `GET` | Lists available platforms and default goal types. |
| **`/publish`** | `POST` | Submits content for multi-platform publishing (YouTube, LinkedIn, X, Substack) with strict **Human-In-The-Loop Approval**. |
| **`/publish/jobs`** | `GET` | Lists publishing jobs and pending approval queue. |
| **`/publish/jobs/{id}/approve`** | `POST` | Authorizes content and dispatches live via **Composio**, updating PostgreSQL record status. |
| **`/publish/jobs/{id}/reject`** | `POST` | Rejects content with reviewer feedback. |

---

## 🐳 Docker & PostgreSQL Container Setup (Recommended)

The entire stack is containerized with **Docker Compose** containing the FastAPI Backend and PostgreSQL 16 database with auto-provisioned schema.

### 1. Start Containers
```bash
docker compose up -d
```

### 2. Verify Container Health
```bash
docker compose ps
```
Both `creator_ai_backend` (`http://localhost:8000`) and `creator_ai_postgres` (`localhost:5432`) will be running and healthy.

### 3. View Logs
```bash
docker compose logs -f backend
```

### 4. Direct PostgreSQL Access
```bash
docker exec -it creator_ai_postgres psql -U creator -d creator_ai_db
```

---

## 🗄️ PostgreSQL Database Schema

The database schema is defined in [`schema.sql`](file:///c:/MangoDB-iqoo/schema.sql) and implemented via SQLAlchemy models in [`app/models/db_models.py`](file:///c:/MangoDB-iqoo/app/models/db_models.py):

```
┌─────────────────────────┐         ┌─────────────────────────────────┐
│        creators         │1       *│        creator_profiles         │
├─────────────────────────┼─────────┼─────────────────────────────────┤
│ id (UUID, PK)           │         │ id (UUID, PK)                   │
│ name (VARCHAR)          │         │ creator_id (UUID, FK)           │
│ slug (VARCHAR, UNIQUE)  │         │ user_md_content (TEXT)          │
│ bio (TEXT)              │         │ hook_md_content (TEXT)          │
│ primary_domain (VARCHAR)│         │ tone_blueprint (JSONB)          │
│ avatar_url (TEXT)       │         │ video_length_analysis (JSONB)   │
│ created_at (TIMESTAMPTZ)│         │ video_taxonomy (JSONB)          │
│ updated_at (TIMESTAMPTZ)│         │ thumbnail_strategy (JSONB)      │
└───────────┬─────────────┘         │ frequent_spoken_phrases (JSONB) │
            │1                      │ catalog_summary (JSONB)         │
            │                       └─────────────────────────────────┘
            │*
┌───────────┴─────────────┐         ┌─────────────────────────────────┐
│    creator_platforms    │         │          publish_jobs           │
├─────────────────────────┤         ├─────────────────────────────────┤
│ id (UUID, PK)           │         │ job_id (VARCHAR, PK)            │
│ creator_id (UUID, FK)   │         │ creator_id (VARCHAR)            │
│ platform (VARCHAR)      │         │ platform (VARCHAR)              │
│ handle_or_url (VARCHAR) │         │ content_format (VARCHAR)        │
│ is_connected (BOOLEAN)  │         │ title (TEXT)                    │
│ followers_or_sub (BIGINT│         │ content (TEXT)                  │
│ total_views (BIGINT)    │         │ media_urls (JSONB)              │
│ avg_engagement (NUMERIC)│         │ status (VARCHAR)                │
│ growth_rate_30d(NUMERIC)│         │ requires_human_approval (BOOL)  │
│ last_synced_at (TZ)     │         │ reviewer_name (VARCHAR)         │
└─────────────────────────┘         │ reviewer_notes (TEXT)           │
                                    │ composio_action (VARCHAR)       │
┌─────────────────────────┐         │ composio_execution_status (STR) │
│      content_items      │         │ composio_output (JSONB)         │
├─────────────────────────┤         │ published_url (TEXT)            │
│ id (UUID, PK)           │         │ created_at (TIMESTAMPTZ)        │
│ creator_id (UUID, FK)   │         │ approved_at (TIMESTAMPTZ)       │
│ platform (VARCHAR)      │         │ published_at (TIMESTAMPTZ)      │
│ title (TEXT)            │         └─────────────────────────────────┘
│ url (TEXT)              │
│ duration_seconds (INT)  │         ┌─────────────────────────────────┐
│ view_count (BIGINT)     │         │          trends_cache           │
│ transcript_snippet(TEXT)│         ├─────────────────────────────────┤
│ key_opening_words (TEXT)│         │ id (UUID, PK)                   │
└─────────────────────────┘         │ domain (VARCHAR)                │
                                    │ geo (VARCHAR)                   │
                                    │ world_trends (JSONB)            │
                                    │ niche_trends (JSONB)            │
                                    │ viral_formats (JSONB)           │
                                    │ fetched_at (TIMESTAMPTZ)        │
                                    └─────────────────────────────────┘
```

---

## 🛠️ Local Development (without Docker)

```bash
# 1. Activate Python virtual environment
.\.venv\Scripts\activate

# 2. Run backend locally
python run.py

# 3. Run automated verification suite
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
- Production of `user.md` and `hook.md` saved under `creators/{creator_slug}/` and stored in PostgreSQL `creator_profiles` table.

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
*Authorizes dispatch, triggers **Composio** action (`Action.TWITTER_CREATION_OF_A_POST`, `Action.LINKEDIN_CREATE_A_POST`, etc.), updates PostgreSQL `publish_jobs` table, and returns the live published URL.*

---

### 5. `/intelligence` — Cross-Platform Trend Intelligence 🆕

**Full Scan (POST):**
```json
POST /intelligence
{
  "creator_name": "Ali Abdaal",
  "niche": "Tech & AI",
  "location": "US",
  "platforms": ["youtube", "instagram", "linkedin", "x_twitter"],
  "platform_handles": {
    "youtube": "@aliabdaal",
    "instagram": "aliabdaal",
    "linkedin": "ali-abdaal",
    "x_twitter": "AliAbdaal"
  },
  "goals": {
    "instagram": "increase_reach",
    "youtube": "increase_followers",
    "linkedin": "increase_connections",
    "x_twitter": "increase_engagement"
  },
  "generate_platform_md": true
}
```

**Quick Scan (GET):**
```http
GET /intelligence/quick?creator_name=Ali%20Abdaal&niche=Tech%20%26%20AI&location=US&platforms=youtube,instagram,linkedin,x_twitter
```

**Output:**
- Per-platform **domain trends** (niche-specific), **location trends**, and **global trends** with direct links
- Trending **hashtags** per platform
- **Content strategies** optimized per platform and goal
- **AI-powered content recommendations** with hooks, posting times, and hashtags
- Auto-generated `platform_{name}.md` files under `creators/{slug}/` containing all trend intelligence

