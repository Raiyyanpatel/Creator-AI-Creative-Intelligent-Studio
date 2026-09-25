-- ====================================================================
-- CREATOR AI - POSTGRESQL PRODUCTION DATABASE SCHEMA
-- Multi-Platform Creator Intelligence, Profiling, Trends & Composio Publishing
-- ====================================================================

-- Enable pgcrypto extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. CREATORS TABLE
CREATE TABLE IF NOT EXISTS creators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    bio TEXT,
    primary_domain VARCHAR(100) DEFAULT 'Tech & AI',
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_creators_slug ON creators(slug);

-- 2. CREATOR PROFILES TABLE (Stores user.md and hook.md and deep multidimensional analyses)
CREATE TABLE IF NOT EXISTS creator_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_id UUID NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    user_md_content TEXT NOT NULL,
    hook_md_content TEXT NOT NULL,
    tone_blueprint JSONB NOT NULL DEFAULT '{}'::jsonb,
    video_length_analysis JSONB NOT NULL DEFAULT '{}'::jsonb,
    video_taxonomy JSONB NOT NULL DEFAULT '[]'::jsonb,
    thumbnail_strategy JSONB NOT NULL DEFAULT '{}'::jsonb,
    frequent_spoken_phrases JSONB NOT NULL DEFAULT '[]'::jsonb,
    catalog_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
    custom_instructions TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_creator_profiles_creator_id ON creator_profiles(creator_id);

-- 3. CREATOR PLATFORMS TABLE (YouTube, Substack, LinkedIn, X/Twitter metrics)
CREATE TABLE IF NOT EXISTS creator_platforms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_id UUID NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'youtube', 'substack', 'linkedin', 'twitter'
    handle_or_url VARCHAR(255) NOT NULL,
    is_connected BOOLEAN NOT NULL DEFAULT TRUE,
    followers_or_subscribers BIGINT NOT NULL DEFAULT 0,
    total_views_or_impressions BIGINT NOT NULL DEFAULT 0,
    total_content_pieces INTEGER NOT NULL DEFAULT 0,
    avg_engagement_rate NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    growth_rate_30d NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    platform_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_synced_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_creator_platform UNIQUE (creator_id, platform)
);

CREATE INDEX IF NOT EXISTS idx_creator_platforms_creator ON creator_platforms(creator_id);

-- 4. CONTENT ITEMS TABLE (Mined videos, shorts, Substack articles, tweets)
CREATE TABLE IF NOT EXISTS content_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_id UUID NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    external_id VARCHAR(255),
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    content_format VARCHAR(50) NOT NULL, -- 'video', 'short', 'article', 'post'
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    view_count BIGINT DEFAULT 0,
    upload_date VARCHAR(50),
    thumbnail_url TEXT,
    transcript_snippet TEXT,
    key_opening_words TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_content_items_creator_platform ON content_items(creator_id, platform);

-- 5. TRENDS CACHE TABLE (Live Google Trends RSS & Domain Niche Trends)
CREATE TABLE IF NOT EXISTS trends_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain VARCHAR(100) NOT NULL,
    geo VARCHAR(10) NOT NULL DEFAULT 'US',
    world_trends JSONB NOT NULL DEFAULT '[]'::jsonb,
    niche_trends JSONB NOT NULL DEFAULT '[]'::jsonb,
    viral_formats JSONB NOT NULL DEFAULT '[]'::jsonb,
    opportunity_matrix JSONB NOT NULL DEFAULT '[]'::jsonb,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_trends_domain_geo ON trends_cache(domain, geo, fetched_at DESC);

-- 6. PUBLISH JOBS TABLE (Human-In-The-Loop Approval & Composio Dispatch Queue)
CREATE TABLE IF NOT EXISTS publish_jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    creator_id VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL, -- 'youtube', 'linkedin', 'twitter', 'substack'
    content_format VARCHAR(50) NOT NULL, -- 'video', 'short', 'post', 'thread', 'article'
    title TEXT,
    content TEXT NOT NULL,
    media_urls JSONB NOT NULL DEFAULT '[]'::jsonb,
    thumbnail_url TEXT,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING_APPROVAL', -- 'PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'PUBLISHING', 'PUBLISHED', 'FAILED'
    requires_human_approval BOOLEAN NOT NULL DEFAULT TRUE,
    scheduled_for TIMESTAMPTZ,
    reviewer_name VARCHAR(255),
    reviewer_notes TEXT,
    rejection_reason TEXT,
    composio_action VARCHAR(100),
    composio_execution_status VARCHAR(50) DEFAULT 'WAITING_FOR_HUMAN_APPROVAL',
    composio_output JSONB,
    published_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMPTZ,
    rejected_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_publish_jobs_creator_status ON publish_jobs(creator_id, status);
CREATE INDEX IF NOT EXISTS idx_publish_jobs_created_at ON publish_jobs(created_at DESC);

-- Trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_creators_updated_at ON creators;
CREATE TRIGGER trg_creators_updated_at
BEFORE UPDATE ON creators
FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();

DROP TRIGGER IF EXISTS trg_creator_profiles_updated_at ON creator_profiles;
CREATE TRIGGER trg_creator_profiles_updated_at
BEFORE UPDATE ON creator_profiles
FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();

DROP TRIGGER IF EXISTS trg_publish_jobs_updated_at ON publish_jobs;
CREATE TRIGGER trg_publish_jobs_updated_at
BEFORE UPDATE ON publish_jobs
FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
