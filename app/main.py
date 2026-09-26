import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers.profiling import router as profiling_router
from app.routers.dashboard import router as dashboard_router
from app.routers.trends import router as trends_router
from app.routers.publish import router as publish_router
from app.routers.intelligence import router as intelligence_router
from app.routers.clipping import router as clipping_router

# Configure clean logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("creator_ai")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Data storage directory: {settings.DATA_DIR}")
    logger.info(f"Creators profile directory: {settings.CREATORS_DIR}")
    yield
    logger.info("Shutting down Creator AI engine...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
# Creator AI — Autonomous Creator Backend API Engine

High-performance backend for the React Native Creator AI mobile application, delivering real-time multimodal creator intelligence:

- **`/profiling`**: Ingests real creator videos, shorts, transcripts, Substack newsletters, and social posts. Deeply extracts tone, video duration distribution, video types, thumbnail strategies, and authentic spoken vocal mannerisms ("what user says often"), generating `user.md` and `hook.md`.
- **`/dashboard`**: Unified cross-platform metrics across YouTube, Substack, LinkedIn, and X/Twitter + in-app Creator AI pipeline analytics and React Native chart datasets.
- **`/trends`**: Live Google Trends RSS feeds, domain/niche-specific trending topics, viral format templates, and actionable content angles.
- **`/publish`**: Human-In-The-Loop approval gate with **Composio** automation for publishing to YouTube, LinkedIn, X/Twitter, and Substack.
    """,
    lifespan=lifespan
)

# Enable CORS for React Native and Web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include core routers cleanly without duplicate prefix mounting
app.include_router(profiling_router)
app.include_router(dashboard_router)
app.include_router(trends_router)
app.include_router(publish_router)
app.include_router(intelligence_router)
app.include_router(clipping_router)

@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": [
            "/profiling",
            "/dashboard",
            "/trends",
            "/publish",
            "/intelligence",
            "/docs"
        ]
    }
