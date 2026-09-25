import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

logger = logging.getLogger(__name__)

# Fetch database URL from environment or settings
DATABASE_URL = os.environ.get("DATABASE_URL") or getattr(settings, "DATABASE_URL", None)

if not DATABASE_URL:
    # Default to local postgres or fallback sqlite for offline development
    DATABASE_URL = "postgresql+psycopg2://creator:creator_password@localhost:5432/creator_ai_db"

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Handle fallback if postgres driver or connection fails initially
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        connect_args=connect_args
    )
    # Test connection
    with engine.connect() as conn:
        logger.info(f"Database connected successfully to: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'local'}")
except Exception as e:
    logger.warning(f"PostgreSQL connection to {DATABASE_URL} failed ({e}). Falling back to local SQLite engine.")
    DATABASE_URL = "sqlite:///./data/creator_ai.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
