from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    - Startup: Verify database connection
    - Shutdown: Dispose of database connections
    """
    # Startup
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection verified")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

    yield

    # Shutdown
    await engine.dispose()
    print("Database connections closed")


app = FastAPI(
    title="Vibe Tweet",
    description="AI-powered tweet generator that learns your writing style",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "service": "vibe-tweet"}


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Vibe Tweet API",
        "version": "0.1.0",
        "docs": "/docs",
    }


# Routers will be included here as we build them
# from app.api.routes import users, tweets, preferences
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(tweets.router, prefix="/users/{user_id}/tweets", tags=["tweets"])
# app.include_router(preferences.router, prefix="/users/{user_id}/preferences", tags=["preferences"])
