"""Knowledge base browsing and search API."""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel

from app.services.rag import get_rag_service

router = APIRouter()


class KnowledgeItem(BaseModel):
    """Knowledge item response model."""
    id: str
    title: str
    content: str
    category: str
    source: str
    source_url: Optional[str] = None
    tier: int  # 1-4, higher tier = more authoritative


class KnowledgeListResponse(BaseModel):
    """Response for knowledge list endpoint."""
    items: List[KnowledgeItem]
    total: int
    page: int
    page_size: int


class CategoryInfo(BaseModel):
    """Category information."""
    id: str
    name: str
    name_en: str
    count: int


@router.get("/categories", response_model=List[CategoryInfo])
async def get_categories(lang: str = Query("zh", description="Language code (en/zh)")):
    """Get all knowledge categories."""
    rag = get_rag_service()
    counts = rag.get_category_counts()
    
    # Localize names based on lang
    is_en = lang == "en"
    
    categories = [
        CategoryInfo(id="heart_rate", name="Heart Rate" if is_en else "心率", name_en="Heart Rate", count=counts.get("heart_rate", 0)),
        CategoryInfo(id="hrv", name="HRV", name_en="HRV", count=counts.get("hrv", 0)),
        CategoryInfo(id="sleep", name="Sleep" if is_en else "睡眠", name_en="Sleep", count=counts.get("sleep", 0)),
        CategoryInfo(id="exercise", name="Exercise" if is_en else "运动", name_en="Exercise", count=counts.get("exercise", 0)),
        CategoryInfo(id="stress", name="Stress" if is_en else "压力", name_en="Stress", count=counts.get("stress", 0)),
    ]
    return categories


@router.get("/browse", response_model=KnowledgeListResponse)
async def browse_knowledge(
    category: Optional[str] = Query(None, description="Filter by category"),
    tier: Optional[int] = Query(None, ge=1, le=4, description="Filter by authority tier"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    lang: str = Query("zh", description="Language code"),
):
    """Browse knowledge base with optional filters."""
    rag = get_rag_service()
    
    # Get items by category
    if category:
        items = rag.get_all_by_category(category, limit=page_size * page)
    else:
        # Get all items - use a large query to get everything
        items = rag.collection.get(limit=page_size * page, include=["documents", "metadatas"])
        # Convert to expected format
        formatted_items = []
        if items["documents"]:
            for i, doc in enumerate(items["documents"]):
                formatted_items.append({
                    "id": items["ids"][i],
                    "content": doc,
                    "metadata": items["metadatas"][i] if items["metadatas"] else {},
                })
        items = formatted_items
    
    # Filter by tier if specified
    if tier:
        items = [item for item in items if item.get("metadata", {}).get("tier") == tier]
    
    # Pagination
    total = len(items)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = items[start_idx:end_idx]
    
    # Batch translate items if needed
    if lang in ['zh', 'en']:
        paginated_items = rag.batch_ensure_translations(paginated_items, lang)

    # Convert to response format
    knowledge_items = []
    for item in paginated_items:
        metadata = item.get("metadata", {})
        
        # Determine title and content based on available metadata (batch translation handles updates)
        content = item.get("content", "")
        title = metadata.get("title", "Untitled")
        
        # Try to use translated fields if available (batch_ensure_translations updates metadata)
        if lang in ['zh', 'en']:
             cached_title = metadata.get(f"title_{lang}")
             cached_content = metadata.get(f"content_{lang}")
             if cached_title: title = cached_title
             if cached_content: content = cached_content

        knowledge_items.append(
            KnowledgeItem(
                id=item.get("id", ""),
                title=title,
                content=content,
                category=metadata.get("category", ""),
                source=metadata.get("source", "Unknown"),
                source_url=metadata.get("source_url"),
                tier=metadata.get("tier", 4),
            )
        )
    
    return KnowledgeListResponse(
        items=knowledge_items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/search")
async def search_knowledge(
    q: str = Query(..., min_length=1, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    lang: str = Query("zh", description="Language code"),
):
    """Search knowledge base using semantic search."""
    rag = get_rag_service()
    results = rag.search(q, n_results=limit, category=category)
    
    # Attempt to use cached translation if available
    for res in results:
        meta = res.get("metadata", {})
        if lang in ['zh', 'en']:
             cached_content = meta.get(f"content_{lang}")
             if cached_content:
                 res["content"] = cached_content
                 
    return {
        "query": q,
        "results": results,
        "total": len(results),
    }


@router.get("/{item_id}", response_model=KnowledgeItem)
async def get_knowledge_item(item_id: str, lang: str = Query("zh")):
    """Get a specific knowledge item by ID."""
    rag = get_rag_service()
    item = rag.get_document(item_id, lang=lang)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    metadata = item.get("metadata", {})
    return KnowledgeItem(
        id=item.get("id", ""),
        title=metadata.get("title", "Untitled"),
        content=item.get("content", ""),
        category=metadata.get("category", ""),
        source=metadata.get("source", "Unknown"),
        source_url=metadata.get("source_url"),
        tier=metadata.get("tier", 4),
    )
