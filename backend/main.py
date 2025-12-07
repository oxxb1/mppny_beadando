from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
import logging
import threading

from .background import start_periodic_import

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Weather API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stop_event = threading.Event()

try:
    from .api import router
    app.include_router(router)
    logger.info("API router registered")
except ImportError as e:
    logger.error(f"Failed to import API router: {e}")
    raise

@app.on_event("startup")
async def startup_event():
    """Startup esemény - adatbázis és háttérfolyamat indítása"""
    logger.info("🚀 Starting Weather API...")
    
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    try:
        background_thread = start_periodic_import(stop_event)
        logger.info(f"Background importer started (thread: {background_thread.name})")
    except Exception as e:
        logger.error(f"Failed to start background importer: {e}")
    
    logger.info("Startup completed")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    stop_event.set()
    logger.info("Background importer stopped")

@app.get("/")
def read_root():
    return {
        "message": "Weather Analytics API",
        "version": "1.0.0",
        "city": "Eger, Hungary",
        "endpoints": {
            "weather_list": "/api/weather",
            "weather_detail": "/api/weather/{id}",
            "stats": "/api/stats",
            "refresh": "/api/refresh",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-15T12:00:00Z"}