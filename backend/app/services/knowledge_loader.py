"""Knowledge base data loader service."""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.services.rag import get_rag_service
from app.config import get_settings


class KnowledgeLoader:
    """Service for loading knowledge data into ChromaDB."""
    
    def __init__(self):
        """Initialize loader."""
        self.rag_service = get_rag_service()
        settings = get_settings()
        self.knowledge_dir = settings.knowledge_base_dir
    
    def load_from_json(self, json_path: Path) -> int:
        """Load knowledge items from a JSON file.
        
        Expected JSON format:
        {
            "category": "heart_rate",
            "items": [
                {
                    "title": "...",
                    "content": "...",
                    "source": "AHA",
                    "source_url": "https://...",
                    "tier": 1
                }
            ]
        }
        
        Returns:
            Number of items loaded
        """
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        category = data.get("category", "general")
        items = data.get("items", [])
        
        documents = []
        metadatas = []
        
        for item in items:
            content = item.get("content", "")
            if not content:
                continue
                
            documents.append(content)
            metadatas.append({
                "title": item.get("title", "Untitled"),
                "category": category,
                "source": item.get("source", "Unknown"),
                "source_url": item.get("source_url", ""),
                "tier": item.get("tier", 4),
            })
        
        if documents:
            self.rag_service.add_documents(documents, metadatas)
        
        return len(documents)
    
    def load_all_json_files(self) -> Dict[str, int]:
        """Load all JSON files from the knowledge base directory.
        
        Returns:
            Dict mapping filename to number of items loaded
        """
        results = {}
        
        if not self.knowledge_dir.exists():
            return results
        
        for json_file in self.knowledge_dir.glob("*.json"):
            try:
                count = self.load_from_json(json_file)
                results[json_file.name] = count
            except Exception as e:
                results[json_file.name] = f"Error: {e}"
        
        return results
    
    def add_single_item(
        self,
        title: str,
        content: str,
        category: str,
        source: str,
        source_url: str = "",
        tier: int = 4,
    ) -> str:
        """Add a single knowledge item.
        
        Returns:
            The document ID
        """
        metadata = {
            "title": title,
            "category": category,
            "source": source,
            "source_url": source_url,
            "tier": tier,
        }
        
        return self.rag_service.add_document(content, metadata)


def get_knowledge_loader() -> KnowledgeLoader:
    """Get knowledge loader instance."""
    return KnowledgeLoader()
