import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.db_models import (
    CreatorDB,
    CreatorProfileDB,
    CreatorPlatformDB,
    ContentItemDB,
    TrendsCacheDB,
    PublishJobDB
)

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self._init_tables()

    def _init_tables(self):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables initialized successfully via SQLAlchemy.")
        except Exception as e:
            logger.warning(f"Could not auto-create database tables on start: {e}")

    def save_creator_profile(
        self,
        creator_name: str,
        creator_slug: str,
        analysis_data: Dict[str, Any],
        user_md: str,
        hook_md: str,
        catalog_summary: Dict[str, Any],
        custom_instructions: Optional[str] = None
    ) -> Optional[str]:
        """
        Saves creator and detailed profile into PostgreSQL tables.
        """
        session = SessionLocal()
        try:
            # 1. Upsert Creator
            creator = session.query(CreatorDB).filter_by(slug=creator_slug).first()
            if not creator:
                creator = CreatorDB(
                    name=creator_name,
                    slug=creator_slug,
                    primary_domain=analysis_data.get("core_themes", ["Tech & AI"])[0] if analysis_data.get("core_themes") else "Tech & AI"
                )
                session.add(creator)
                session.flush()

            # 2. Add Profile Record
            profile = CreatorProfileDB(
                creator_id=creator.id,
                user_md_content=user_md,
                hook_md_content=hook_md,
                tone_blueprint=analysis_data.get("tone", {}),
                video_length_analysis=analysis_data.get("video_length", {}),
                video_taxonomy=analysis_data.get("video_types", []),
                thumbnail_strategy=analysis_data.get("thumbnail_strategy", {}),
                frequent_spoken_phrases=analysis_data.get("frequent_spoken_phrases", []),
                catalog_summary=catalog_summary,
                custom_instructions=custom_instructions
            )
            session.add(profile)
            session.commit()
            logger.info(f"Persisted profile for creator {creator_name} to database.")
            return creator.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving creator profile to DB: {e}")
            return None
        finally:
            session.close()

    def _parse_dt(self, val: Any) -> Optional[datetime]:
        if isinstance(val, datetime):
            return val
        if isinstance(val, str) and val.strip():
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                return None
        return None

    def sync_publish_job(self, job_dict: Dict[str, Any]):
        """
        Syncs a publish job record to PostgreSQL.
        """
        session = SessionLocal()
        try:
            job_id = job_dict.get("job_id")
            existing = session.query(PublishJobDB).filter_by(job_id=job_id).first()
            
            if not existing:
                job_db = PublishJobDB(
                    job_id=job_id,
                    creator_id=job_dict.get("creator_id"),
                    platform=job_dict.get("platform"),
                    content_format=job_dict.get("content_format"),
                    title=job_dict.get("title"),
                    content=job_dict.get("content"),
                    media_urls=job_dict.get("media_urls", []),
                    thumbnail_url=job_dict.get("thumbnail_url"),
                    tags=job_dict.get("tags", []),
                    status=job_dict.get("status"),
                    requires_human_approval=job_dict.get("requires_human_approval", True),
                    reviewer_name=job_dict.get("reviewer_name"),
                    reviewer_notes=job_dict.get("reviewer_notes"),
                    rejection_reason=job_dict.get("rejection_reason"),
                    composio_action=job_dict.get("composio_action"),
                    composio_execution_status=job_dict.get("composio_execution_status"),
                    composio_output=job_dict.get("composio_output"),
                    published_url=job_dict.get("published_url"),
                    created_at=self._parse_dt(job_dict.get("created_at")) or datetime.now(timezone.utc),
                    approved_at=self._parse_dt(job_dict.get("approved_at")),
                    rejected_at=self._parse_dt(job_dict.get("rejected_at")),
                    published_at=self._parse_dt(job_dict.get("published_at"))
                )
                session.add(job_db)
            else:
                for k in ["status", "reviewer_name", "reviewer_notes", "rejection_reason",
                          "composio_execution_status", "composio_output", "published_url"]:
                    if k in job_dict and job_dict[k] is not None:
                        setattr(existing, k, job_dict[k])
                for dt_k in ["approved_at", "rejected_at", "published_at"]:
                    if dt_k in job_dict and job_dict[dt_k] is not None:
                        setattr(existing, dt_k, self._parse_dt(job_dict[dt_k]))
            
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error syncing publish job {job_dict.get('job_id')} to DB: {e}")
        finally:
            session.close()

db_service = DatabaseService()
