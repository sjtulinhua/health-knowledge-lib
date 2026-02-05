"""RAG (Retrieval-Augmented Generation) service using ChromaDB."""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import json

from app.config import get_settings
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor

class RAGService:
    """Service for managing knowledge base and semantic search."""
    
    def __init__(self):
        """Initialize ChromaDB client."""
        settings = get_settings()
        
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)

        persist_dir = Path(settings.chroma_persist_directory)
        persist_dir.mkdir(parents=True, exist_ok=True)
        
        self._client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name="health_knowledge",
            metadata={"description": "Health and fitness knowledge base"},
        )

    def _translate_text(self, text: str, target_lang: str, is_title: bool = False) -> str:
        """Translate text using Gemini."""
        if not text:
            return ""
        try:
            import time
            # Simple retry logic (since this is internal service method)
            for _ in range(3):
                try:
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    lang_name = 'Chinese (Simplified)' if target_lang == 'zh' else 'English'
                    request_type = "title" if is_title else "text"
                    
                    prompt = f"""Task: Translate the following {request_type} to {lang_name}.
Rules:
1. Maintain professional medical tone.
2. Output ONLY the translated {request_type}.
3. NO explanations, NO extra notes, NO markdown formatting (unless present in original).
4. If it's a title, keep it under 20 words.

Original {request_type}:
{text}"""
                    
                    response = model.generate_content(prompt)
                    return response.text.strip()
                except Exception:
                    time.sleep(1)
            
            return text
        except Exception as e:
            print(f"Translation failed: {e}")
            return text

    def ensure_translation(self, doc_id: str, content: str, metadata: Dict[str, Any], target_lang: str) -> Dict[str, Any]:
        """Ensure content and title are available in target language."""
        if not target_lang or target_lang not in ['zh', 'en']:
            return {"title": metadata.get("title", ""), "content": content}

        title_key = f"title_{target_lang}"
        content_key = f"content_{target_lang}"
        
        cached_title = metadata.get(title_key)
        cached_content = metadata.get(content_key)
        
        updates = {}
        
        if not cached_content:
            cached_content = self._translate_text(content, target_lang, is_title=False)
            updates[content_key] = cached_content
            
        if not cached_title:
             current_title = metadata.get("title", "")
             cached_title = self._translate_text(current_title, target_lang, is_title=True)
             updates[title_key] = cached_title

        if updates:
            new_metadata = metadata.copy()
            new_metadata.update(updates)
            self._collection.update(ids=[doc_id], metadatas=[new_metadata])
            
        return {"title": cached_title, "content": cached_content}

    
    @property
    def collection(self):
        """Get the knowledge collection."""
        return self._collection
    
    def _generate_id(self, content: str, source: str) -> str:
        """Generate a unique ID for a document."""
        hash_input = f"{content[:100]}_{source}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
    ) -> str:
        """Add a document to the knowledge base.
        
        Args:
            content: The document text content
            metadata: Document metadata (title, source, category, tier, url, etc.)
            
        Returns:
            The document ID
        """
        doc_id = self._generate_id(content, metadata.get("source", "unknown"))
        
        self._collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id],
        )
        
        return doc_id
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> List[str]:
        """Add multiple documents to the knowledge base.
        
        Args:
            documents: List of document contents
            metadatas: List of metadata dicts
            
        Returns:
            List of document IDs
        """
        ids = [
            self._generate_id(doc, meta.get("source", "unknown"))
            for doc, meta in zip(documents, metadatas)
        ]
        
        self._collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        
        return ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        category: Optional[str] = None,
        tier: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Search the knowledge base using semantic search.
        
        Args:
            query: Search query
            n_results: Maximum number of results
            category: Optional category filter
            tier: Optional authority tier filter
            
        Returns:
            List of search results with content, metadata, and relevance score
        """
        # Build where filter
        where_filter = None
        if category or tier:
            conditions = []
            if category:
                conditions.append({"category": category})
            if tier:
                conditions.append({"tier": tier})
            
            if len(conditions) == 1:
                where_filter = conditions[0]
            else:
                where_filter = {"$and": conditions}
        
        # Execute search
        results = self._collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                result = {
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "relevance_score": 1 - (results["distances"][0][i] if results["distances"] else 0),
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_all_by_category(
        self,
        category: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get all documents in a category."""
        results = self._collection.get(
            where={"category": category},
            limit=limit,
            include=["documents", "metadatas"],
        )
        
        items = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"]):
                items.append({
                    "id": results["ids"][i],
                    "content": doc,
                    "metadata": results["metadatas"][i] if results["metadatas"] else {},
                })
        
        return items
    
    def get_category_counts(self) -> Dict[str, int]:
        """Get count of documents per category."""
        # Get all metadata
        result = self._collection.get(include=["metadatas"])
        
        counts = {}
        if result["metadatas"]:
            for meta in result["metadatas"]:
                cat = meta.get("category", "uncategorized")
                counts[cat] = counts.get(cat, 0) + 1
                
        return counts

    def batch_ensure_translations(self, items: List[Dict[str, Any]], target_lang: str) -> List[Dict[str, Any]]:
        """Ensure translations for a list of items concurrently."""
        if not target_lang or target_lang not in ['zh', 'en']:
            return items

        # Identify items needing translation
        to_translate = []
        for i, item in enumerate(items):
            metadata = item.get("metadata", {})
            title_key = f"title_{target_lang}"
            content_key = f"content_{target_lang}"
            
            if not metadata.get(title_key) or not metadata.get(content_key):
                to_translate.append((i, item))

        if not to_translate:
            return items

        # Define translation task
        def process_item(idx_item):
            idx, item = idx_item
            doc_id = item.get("id")
            content = item.get("content", "")
            metadata = item.get("metadata", {})
            
            # This updates DB and returns translated content
            translated = self.ensure_translation(doc_id, content, metadata, target_lang)
            
            # Update item in memory
            new_item = item.copy()
            new_item["content"] = translated["content"]
            new_metadata = metadata.copy()
            new_metadata[f"title_{target_lang}"] = translated["title"]
            new_metadata[f"content_{target_lang}"] = translated["content"]
            new_metadata["title"] = translated["title"] # Update display title
            new_item["metadata"] = new_metadata
            return idx, new_item

        # Execute concurrently
        # Limit max workers to avoid rate limits
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(process_item, to_translate))

        # Merge results back
        result_items = list(items)
        for idx, new_item in results:
            result_items[idx] = new_item
            
        return result_items

    def get_document(self, doc_id: str, lang: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID, optionally translated."""
        results = self._collection.get(
            ids=[doc_id],
            include=["documents", "metadatas"],
        )
        
        if results["documents"]:
            content = results["documents"][0]
            metadata = results["metadatas"][0] if results["metadatas"] else {}
            
            # Handle translation if requested
            if lang and lang in ['zh', 'en']:
                translated = self.ensure_translation(doc_id, content, metadata, lang)
                return {
                    "id": doc_id,
                    "content": translated["content"],
                    "metadata": {**metadata, "title": translated["title"]},
                }

            return {
                "id": doc_id,
                "content": content,
                "metadata": metadata,
            }
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        count = self._collection.count()
        return {
            "total_documents": count,
            "collection_name": self._collection.name,
        }
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        try:
            self._collection.delete(ids=[doc_id])
            return True
        except Exception:
            return False


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get the RAG service singleton."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
