"""LLM service using Google Gemini API."""
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.config import get_settings


class LLMService:
    """Service for interacting with Gemini LLM."""
    
    def __init__(self):
        """Initialize Gemini client."""
        settings = get_settings()
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self._model = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self._model = None
    
    @property
    def is_available(self) -> bool:
        """Check if LLM is available."""
        return self._model is not None
    
    def _build_rag_prompt(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        language: str = "zh",
    ) -> str:
        """Build a RAG prompt with retrieved context.
        
        Args:
            query: User's question
            context_docs: Retrieved documents with content and metadata
            language: Response language (zh or en)
            
        Returns:
            Formatted prompt string
        """
        # Build context section
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            source = doc.get("metadata", {}).get("source", "Unknown")
            tier = doc.get("metadata", {}).get("tier", 4)
            tier_label = {1: "权威指南", 2: "医疗机构", 3: "研究论文", 4: "参考资料"}.get(tier, "参考")
            content = doc.get("content", "")
            
            context_parts.append(
                f"[来源 {i}] ({tier_label} - {source})\n{content}"
            )
        
        context_text = "\n\n".join(context_parts) if context_parts else "暂无相关资料"
        
        # Build prompt
        if language == "zh":
            prompt = f"""你是一个专业的健康知识助手。请基于以下权威资料回答用户的问题。

## 重要规则
1. 只使用提供的资料回答问题，不要编造信息
2. 如果资料不足以回答问题，请明确说明
3. 在回答中引用来源（如"根据[来源1]..."）
4. 使用通俗易懂的语言解释专业概念
5. 如涉及健康建议，请添加免责声明

## 参考资料
{context_text}

## 用户问题
{query}

## 回答要求
- 基于资料准确回答
- 引用来源编号
- 如有必要添加健康免责声明
"""
        else:
            prompt = f"""You are a professional health knowledge assistant. Please answer the user's question based on the following authoritative sources.

## Important Rules
1. Only use the provided sources to answer - do not make up information
2. If sources are insufficient, clearly state this
3. Cite sources in your answer (e.g., "According to [Source 1]...")
4. Explain technical concepts in plain language
5. Add disclaimers for health advice

## Reference Sources
{context_text}

## User Question
{query}

## Response Requirements
- Answer accurately based on sources
- Cite source numbers
- Add health disclaimers if necessary
"""
        
        return prompt
    
    async def generate_rag_response(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        language: str = "zh",
    ) -> Dict[str, Any]:
        """Generate a response using RAG.
        
        Args:
            query: User's question
            context_docs: Retrieved documents from knowledge base
            language: Response language
            
        Returns:
            Response with content and confidence level
        """
        if not self.is_available:
            return {
                "content": "LLM服务未配置。请设置 GEMINI_API_KEY 环境变量。" if language == "zh" 
                          else "LLM service not configured. Please set GEMINI_API_KEY.",
                "confidence": "low",
                "error": True,
            }
        
        if not context_docs:
            return {
                "content": "知识库中暂无相关资料。" if language == "zh"
                          else "No relevant information found in the knowledge base.",
                "confidence": "low",
                "error": False,
            }
        
        # Build and execute prompt
        prompt = self._build_rag_prompt(query, context_docs, language)
        
        try:
            response = self._model.generate_content(prompt)
            
            # Determine confidence based on source quality
            max_tier = min(doc.get("metadata", {}).get("tier", 4) for doc in context_docs)
            avg_relevance = sum(doc.get("relevance_score", 0) for doc in context_docs) / len(context_docs)
            
            if max_tier <= 2 and avg_relevance > 0.7:
                confidence = "high"
            elif max_tier <= 3 and avg_relevance > 0.5:
                confidence = "medium"
            else:
                confidence = "low"
            
            return {
                "content": response.text,
                "confidence": confidence,
                "error": False,
            }
            
        except Exception as e:
            return {
                "content": f"生成回答时出错: {str(e)}" if language == "zh"
                          else f"Error generating response: {str(e)}",
                "confidence": "low",
                "error": True,
            }
    
    async def generate_simple_response(
        self,
        prompt: str,
    ) -> str:
        """Generate a simple response without RAG.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            Generated text response
        """
        if not self.is_available:
            return "LLM service not configured."
        
        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
