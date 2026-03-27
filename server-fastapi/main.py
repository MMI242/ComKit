from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables FIRST before any imports that use them
load_dotenv()

# Initialize logging configuration
import logging_config  # noqa: F401

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from database import Base, engine
from routes_auth import router as auth_router
from routes_items import router as items_router
from routes_user_items import router as user_items_router
from routes_user_requests import router as user_requests_router
from routes_ai import router as ai_router
from routes_dev import router as dev_router
from routes_websocket import router as websocket_router
from config import config_manager
from exceptions import http_exception_handler, validation_exception_handler


def get_cors_allowed_origins() -> list[str]:
    configured_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
    origins = [
        origin.strip().rstrip("/")
        for origin in configured_origins.split(",")
        if origin.strip()
    ]

    if origins:
        return origins

    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ]


IS_DEVELOPMENT = (
    config_manager.get("ENVIRONMENT", "production").lower() == "development"
)
CORS_ALLOWED_ORIGINS = get_cors_allowed_origins()
CORS_ALLOW_ORIGIN_REGEX = (
    r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$" if IS_DEVELOPMENT else None
)
ENABLE_NOTIFICATIONS = config_manager.get_bool("ENABLE_NOTIFICATIONS", True)

# Create media directory
os.makedirs("media/items", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Kitchen Sharing API",
    description="API for community kitchen item sharing application",
    version="1.0.0",
    lifespan=lifespan,
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_origin_regex=CORS_ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for media
media_dir = Path(__file__).parent / "media"
media_dir.mkdir(exist_ok=True)
app.mount("/media", StaticFiles(directory=str(media_dir)), name="media")

# Include routers
app.include_router(auth_router)
app.include_router(items_router)
app.include_router(user_items_router)
app.include_router(user_requests_router)
app.include_router(ai_router)
app.include_router(dev_router)

# Include WebSocket router only if notifications are enabled
if ENABLE_NOTIFICATIONS:
    app.include_router(websocket_router)


@app.get("/")
def root():
    return {"message": "Kitchen Sharing API", "version": "1.0.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    import sys

    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", "8000"))

    # Check if port argument is passed
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
