from app.routers.profiling import router as profiling_router
from app.routers.dashboard import router as dashboard_router
from app.routers.trends import router as trends_router
from app.routers.publish import router as publish_router
from app.routers.intelligence import router as intelligence_router

__all__ = [
    "profiling_router",
    "dashboard_router",
    "trends_router",
    "publish_router",
    "intelligence_router",
]
