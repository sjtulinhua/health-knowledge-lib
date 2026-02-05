const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface Category {
  id: string;
  name: string;
  name_en: string;
  count: number;
}

export interface KnowledgeItem {
  id: string;
  title: string;
  content: string;
  category: string;
  source: string;
  source_url?: string;
  tier: number;
}

export interface SearchResult {
  id: string;
  content: string;
  metadata: {
    title: string;
    source: string;
    source_url?: string;
    category: string;
    tier: number;
  };
  relevance_score: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  sources?: {
      title: string;
      url?: string;
      relevance_score: number;
  }[];
}

export interface ChatResponse {
  conversation_id: string;
  message: ChatMessage;
  sources: {
      title: string;
      url?: string;
      relevance_score: number;
  }[];
  confidence: 'high' | 'medium' | 'low';
}

export interface Suggestion {
  question: string;
  category: string;
}

// Knowledge API
export async function getCategories(lang: string = "zh"): Promise<Category[]> {
  const params = new URLSearchParams({ lang });
  const res = await fetch(`${API_BASE}/api/knowledge/categories?${params}`);
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function searchKnowledge(query: string, category?: string, lang: string = "zh"): Promise<SearchResult[]> {
  const params = new URLSearchParams({ q: query, lang });
  if (category) params.append('category', category);
  
  const res = await fetch(`${API_BASE}/api/knowledge/search?${params}`);
  if (!res.ok) throw new Error('Failed to search');
  const data = await res.json();
  return data.results;
}

export async function getKnowledgeItem(id: string, lang: string = "zh"): Promise<KnowledgeItem> {
  const params = new URLSearchParams({ lang });
  const res = await fetch(`${API_BASE}/api/knowledge/${id}?${params}`);
  if (!res.ok) throw new Error('Failed to fetch item');
  return res.json();
}

export interface BrowseResponse {
  items: KnowledgeItem[];
  total: number;
  page: number;
  page_size: number;
}

export async function browseKnowledge(
  category?: string,
  tier?: number,
  page: number = 1,
  pageSize: number = 20,
  lang: string = "zh"
): Promise<SearchResult[]> {
  const params = new URLSearchParams({ 
    page: page.toString(), 
    page_size: pageSize.toString(),
    lang
  });
  if (category) params.append('category', category);
  if (tier) params.append('tier', tier.toString());
  
  const res = await fetch(`${API_BASE}/api/knowledge/browse?${params}`);
  if (!res.ok) throw new Error('Failed to browse');
  const data: BrowseResponse = await res.json();
  
  // Convert KnowledgeItem to SearchResult format for frontend compatibility
  // Note: We need to ensure ID is included for detail view fetching
  return data.items.map(item => ({
    id: item.id,
    content: item.content,
    metadata: {
      title: item.title,
      source: item.source,
      source_url: item.source_url,
      category: item.category,
      tier: item.tier,
    },
    relevance_score: 1, // No relevance score for browse
  }));
}

// Chat API
export async function sendChatMessage(
  message: string,
  conversationId?: string,
  history?: ChatMessage[]
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat/send`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      history,
    }),
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}

export async function getSuggestedQuestions(): Promise<Suggestion[]> {
  const res = await fetch(`${API_BASE}/api/chat/suggestions`);
  if (!res.ok) throw new Error('Failed to fetch suggestions');
  return res.json();
}
