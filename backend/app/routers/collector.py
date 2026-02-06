from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.services.collector import get_collector_service
from app.services.rag import get_rag_service

router = APIRouter()

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str

class PreviewRequest(BaseModel):
    url: str

class ContentPreview(BaseModel):
    title: str
    category: str
    summary: str
    content: str
    tier: int
    source_name: str
    url: str

class ImportRequest(ContentPreview):
    pass # Same structure as preview, plus maybe user edits

@router.get("/search", response_model=List[SearchResult])
async def search_web(q: str = Query(..., min_length=2)):
    """Search the web for health resources."""
    service = get_collector_service()
    return service.search_web(q)

@router.post("/preview", response_model=ContentPreview)
async def preview_content(request: PreviewRequest):
    """Fetch and clean content from URL."""
    service = get_collector_service()
    try:
        data = await service.fetch_and_clean(request.url)
        return ContentPreview(
            **data,
            url=request.url
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/import")
async def import_content(request: ImportRequest):
    """Save content to knowledge base."""
    rag = get_rag_service()
    
    # Construct metadata
    metadata = {
        "title": request.title,
        "source": request.source_name,
        "source_url": request.url,
        "category": request.category,
        "tier": request.tier,
        # Auto-create translated titles since we forced Chinese output
        "title_zh": request.title, 
        "content_zh": request.content
    }
    
    # Save to RAG
    doc_id = rag.add_document(request.content, metadata)
    
    return {"id": doc_id, "status": "success"}
