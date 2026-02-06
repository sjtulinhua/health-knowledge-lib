"""FastAPI application entry point."""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings, init_directories
from app.routers import knowledge, chat, collector

# Initialize directories
init_directories()

# Get settings
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Check and initialize knowledge base
    try:
        from app.services.rag import get_rag_service
        from app.services.knowledge_loader import get_knowledge_loader
        
        rag = get_rag_service()
        stats = rag.get_stats()
        
        if stats["total_documents"] == 0:
            print("Knowledge base is empty. Initializing from JSON files...")
            loader = get_knowledge_loader()
            results = loader.load_all_json_files()
            for filename, count in results.items():
                print(f"Loaded {count} items from {filename}")
        else:
            print(f"Knowledge base already contains {stats['total_documents']} documents.")
            
    except Exception as e:
        print(f"Warning: Failed to initialize knowledge base: {e}")
        
    yield
    # Shutdown events if any

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="权威医疗健康与运动科学资料检索系统",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
app.include_router(collector.router, prefix="/api/collector", tags=["Collector"])


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
