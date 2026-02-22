from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import os

from database import Base, engine
from routes_auth import router as auth_router
from routes_items import router as items_router
from routes_user_items import router as user_items_router
from routes_user_requests import router as user_requests_router
from routes_ai import router as ai_router
from routes_dev import router as dev_router
from exceptions import http_exception_handler, validation_exception_handler

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
    lifespan=lifespan
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for media
app.mount("/media", StaticFiles(directory="media"), name="media")

# Include routers
app.include_router(auth_router)
app.include_router(items_router)
app.include_router(user_items_router)
app.include_router(user_requests_router)
app.include_router(ai_router)
app.include_router(dev_router)

@app.get("/")
def root():
    return {
        "message": "Kitchen Sharing API",
        "version": "1.0.0",
        "docs": "/docs"
    }

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
    
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
