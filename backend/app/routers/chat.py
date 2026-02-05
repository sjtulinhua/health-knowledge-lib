"""Chat and Q&A API using RAG."""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""
    model_config = {"extra": "ignore"}  # Allow extra fields from frontend
    
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class SourceReference(BaseModel):
    """Source reference for citations."""
    title: str
    source: str
    url: Optional[str] = None
    tier: int
    relevance_score: float


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: str
    message: ChatMessage
    sources: List[SourceReference]
    confidence: str  # "high", "medium", "low"


class SuggestedQuestion(BaseModel):
    """Suggested question model."""
    question: str
    category: str


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message and get AI response based on knowledge base."""
    import uuid
    import google.generativeai as genai
    from app.services.rag import get_rag_service
    from app.config import get_settings
    
    settings = get_settings()
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    # Check if Gemini API is configured
    if not settings.gemini_api_key:
        return ChatResponse(
            conversation_id=conversation_id,
            message=ChatMessage(
                role="assistant",
                content="抱歉，AI 服务尚未配置。请联系管理员设置 GEMINI_API_KEY。",
                timestamp=datetime.now(),
            ),
            sources=[],
            confidence="low",
        )
    
    # Configure Gemini
    genai.configure(api_key=settings.gemini_api_key)
    
    # Get RAG service and search for relevant documents
    rag = get_rag_service()
    search_results = rag.search(request.message, n_results=5)
    
    # Build context from search results
    context_parts = []
    sources = []
    for i, result in enumerate(search_results):
        metadata = result.get("metadata", {})
        content = result.get("content", "")
        title = metadata.get("title", "Unknown")
        source = metadata.get("source", "Unknown")
        tier = metadata.get("tier", 4)
        url = metadata.get("source_url")
        relevance = result.get("relevance_score", 0)
        
        context_parts.append(f"[Document {i+1}] {title}\nSource: {source}\n{content}\n")
        
        sources.append(SourceReference(
            title=title,
            source=source,
            url=url,
            tier=tier,
            relevance_score=relevance,
        ))
    
    context_text = "\n---\n".join(context_parts) if context_parts else "No relevant documents found."
    
    # Build conversation history for context
    history_text = ""
    if request.history:
        for msg in request.history[-6:]:  # Last 6 messages for context
            role_label = "User" if msg.role == "user" else "Assistant"
            history_text += f"{role_label}: {msg.content}\n"
    
    # Construct the prompt
    system_prompt = """你是一个专业的健康顾问 AI，基于权威医疗健康和运动科学资料来回答用户问题。

规则：
1. 只基于提供的参考资料回答问题
2. 如果资料不足以回答问题，诚实说明
3. 使用清晰、易懂的语言
4. 适当引用来源（如"根据 WHO 指南..."）
5. 对于医疗建议，始终建议咨询专业医生

参考资料：
{context}

{history}用户问题：{question}

请根据以上资料回答用户的问题："""

    prompt = system_prompt.format(
        context=context_text,
        history=f"对话历史：\n{history_text}\n" if history_text else "",
        question=request.message,
    )
    
    async def generate_content_with_retry(prompt: str, retries: int = 3, initial_delay: float = 1.0):
        import asyncio
        import random
        from google.api_core import exceptions
        
        # List of models to try in order
        models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
        
        for model_name in models:
            current_try = 0
            model = genai.GenerativeModel(model_name)
            
            while current_try < retries:
                try:
                    # Use async generation if available, otherwise wrap sync call
                    response = await model.generate_content_async(prompt)
                    return response.text if response.text else "无法生成回答。"
                except exceptions.ResourceExhausted:
                    wait_time = (initial_delay * (2 ** current_try)) + random.uniform(0, 1)
                    print(f"Rate limited on {model_name}. Retrying in {wait_time:.2f}s...")
                    await asyncio.sleep(wait_time)
                    current_try += 1
                except Exception as e:
                    # If it's not a rate limit error, try the next model or fail
                    print(f"Error with {model_name}: {str(e)}")
                    break # Break inner loop to try next model
            
            # If we exhausted retries for this model, continue to next model
            continue
            
        raise Exception("所有可用模型均忙碌，请稍后重试。")

    try:
        # Call Gemini API with retry logic
        answer = await generate_content_with_retry(prompt)
        
        # Determine confidence based on search results
        if len(search_results) >= 3 and sources[0].relevance_score > 0.7:
            confidence = "high"
        elif len(search_results) >= 1 and sources[0].relevance_score > 0.5:
            confidence = "medium"
        else:
            confidence = "low"
        
        return ChatResponse(
            conversation_id=conversation_id,
            message=ChatMessage(
                role="assistant",
                content=answer,
                timestamp=datetime.now(),
            ),
            sources=sources[:3],  # Return top 3 sources
            confidence=confidence,
        )
        
    except Exception as e:
        return ChatResponse(
            conversation_id=conversation_id,
            message=ChatMessage(
                role="assistant",
                content=f"抱歉，处理请求时出错：{str(e)}",
                timestamp=datetime.now(),
            ),
            sources=[],
            confidence="low",
        )


@router.get("/suggestions", response_model=List[SuggestedQuestion])
async def get_suggested_questions():
    """Get suggested questions for the chat interface."""
    suggestions = [
        SuggestedQuestion(question="什么是正常的心率范围？", category="heart_rate"),
        SuggestedQuestion(question="如何提高心率变异性(HRV)？", category="hrv"),
        SuggestedQuestion(question="成年人每天需要多少睡眠？", category="sleep"),
        SuggestedQuestion(question="每天应该走多少步？", category="exercise"),
        SuggestedQuestion(question="如何通过运动缓解压力？", category="stress"),
    ]
    return suggestions


@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get conversation history by ID."""
    # TODO: Implement conversation storage
    return {
        "conversation_id": conversation_id,
        "messages": [],
    }


@router.delete("/history/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    # TODO: Implement conversation deletion
    return {"status": "deleted", "conversation_id": conversation_id}
