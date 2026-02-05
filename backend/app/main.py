"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings, init_directories
from app.routers import knowledge, chat

# Initialize directories
init_directories()

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="权威医疗健康与运动科学资料检索系统",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
        "message": "Welcome to Health Knowledge Library API"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
