"""Service for collecting knowledge from the web."""
from typing import List, Dict, Any, Optional
import asyncio
from duckduckgo_search import DDGS
import trafilatura
from concurrent.futures import ThreadPoolExecutor

from app.config import get_settings
import google.generativeai as genai

class CollectorService:
    """Service for finding and processing online health content."""
    
    def __init__(self):
        settings = get_settings()
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)

    def search_web(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search the web for health guidelines."""
        import os
        # Simplify query - DuckDuckGo doesn't handle complex OR site filters well
        # We'll stick to simple keywords and maybe one broad filter
        search_query = f"{query} health guidelines"
        
        # Get proxy from ENV
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
        
        results = []
        try:
            # Use proxy explicitly if found
            with DDGS(proxy=proxy) as ddgs:
                # Use text search with a timeout/headers if possible
                ddg_results = list(ddgs.text(search_query, max_results=max_results))
                
                if not ddg_results:
                     # Try even simpler query if empty
                     print(f"No results for '{search_query}', trying simpler...")
                     ddg_results = list(ddgs.text(query, max_results=max_results))

                for r in ddg_results:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                        "source": self._extract_domain(r.get("href", ""))
                    })
        except Exception as e:
            print(f"Search error: {type(e).__name__}: {e}")
            
        return results

    def _extract_domain(self, url: str) -> str:
        """Simple domain extractor."""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return "Unknown"

    async def fetch_and_clean(self, url: str) -> Dict[str, Any]:
        """Fetch URL content and clean it using AI."""
        
        # 1. Fetch raw content
        raw_text = await self._fetch_url(url)
        if not raw_text or len(raw_text) < 200:
            raise Exception("Failed to fetch content or content too short")

        # 2. Clean with Gemini
        cleaned_data = await self._clean_with_ai(raw_text, url)
        
        return cleaned_data

    async def _fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL content using Trafilatura (runs in thread pool)."""
        loop = asyncio.get_running_loop()
        
        def fetch():
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            return None

        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, fetch)

    async def _clean_with_ai(self, raw_text: str, url: str) -> Dict[str, Any]:
        """Use Gemini to clean text and extract metadata."""
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
You are a professional medical editor. Your task is to process the following raw web content into a structured knowledge base entry.

SOURCE URL: {url}

RAW CONTENT:
{raw_text[:10000]}  # Limit to first 10k chars to fit context

INSTRUCTIONS:
1. **Analyze**: Identify the main health guidelines, facts, or research findings. Ignore navigation menus, ads, footers, and "read more" links.
2. **Translate & Format**: Convert the content into clear, professional Chinese (Simplified). Use Markdown with headers, bullet points, and bold text for key insights.
3. **Structure**:
   - Title: Create a concise, descriptive title (in Chinese).
   - Category: Choose ONE best fit: "heart_rate", "hrv", "sleep", "exercise", "stress", or "general".
   - Summary: A 1-2 sentence summary of the content.
   - Content: The full cleaned content in Markdown.
   - Tier: Estimate authority tier (1=Official Guideline/WHO/AHA, 2=Medical/Hospital, 3=Research Paper, 4=General Health Blog).

OUTPUT FORMAT (JSON ONLY):
{{
  "title": "...",
  "category": "...",
  "summary": "...",
  "content": "...",
  "tier": 1,
  "source_name": "..."  // Extracted organization name from text
}}
"""
        
        try:
            # Add simple retry
            response = await model.generate_content_async(
                 prompt,
                 generation_config={"response_mime_type": "application/json"}
            )
            import json
            return json.loads(response.text)
        except Exception as e:
            print(f"AI cleaning failed: {e}")
            # Fallback
            return {
                "title": "Error processing content",
                "category": "general",
                "summary": "Failed to clean content.",
                "content": raw_text[:2000],
                "tier": 4,
                "source_name": "Unknown"
            }

# Singleton
_collector_service = None

def get_collector_service():
    global _collector_service
    if not _collector_service:
        _collector_service = CollectorService()
    return _collector_service
