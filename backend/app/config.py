"""Application configuration management."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    app_name: str = "Health Knowledge Library"
    debug: bool = True
    
    # API Keys
    gemini_api_key: str = ""
    
    # Database
    database_url: str = "sqlite:///./data/app.db"
    
    # ChromaDB
    chroma_persist_directory: str = "./data/chroma"
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent
    knowledge_base_dir: Path = base_dir / "knowledge_base"
    data_dir: Path = base_dir / "data"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"  # Allow extra environment variables like http_proxy
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Ensure data directories exist
def init_directories():
    """Create necessary directories if they don't exist."""
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.knowledge_base_dir.mkdir(parents=True, exist_ok=True)
    Path(settings.chroma_persist_directory).mkdir(parents=True, exist_ok=True)
