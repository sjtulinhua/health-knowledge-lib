"use client";

import { useState, useRef, useEffect } from "react";
import { sendChatMessage, getSuggestedQuestions, type ChatMessage, type Suggestion } from "@/lib/api";
import { useTranslation } from "@/lib/i18n"; // Import i18n hook

export default function ChatPage() {
  const { t } = useTranslation();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Load suggestions on mount
  useEffect(() => {
    getSuggestedQuestions()
      .then(setSuggestions)
      .catch(console.error);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput("");
    
    // Optimistic update
    const newMessages: ChatMessage[] = [
      ...messages,
      { role: "user", content: userMessage }
    ];
    setMessages(newMessages);
    setLoading(true);

    try {
      const response = await sendChatMessage(userMessage, undefined, newMessages);
      
      setMessages([
        ...newMessages,
        { 
          role: "assistant", 
          content: response.message.content,
          sources: response.sources 
        }
      ]);
    } catch (error) {
      console.error(error);
      setMessages([
        ...newMessages,
        { role: "assistant", content: t("chat.error") }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (question: string) => {
    setInput(question);
  };

  return (
    <div className="container-width max-w-5xl h-[calc(100vh-64px)] py-8 flex flex-col">
      <div className="flex-1 overflow-y-auto space-y-8 pr-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-8">
            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center text-primary mb-4">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
            </div>
            <h1 className="text-2xl font-bold">{t("chat.empty.title")}</h1>
            <p className="text-muted-foreground max-w-md">
              {t("chat.empty.subtitle")}
            </p>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => handleSuggestionClick(s.question)}
                  className="p-4 text-left text-sm bg-card hover:bg-muted/50 border border-border rounded-xl transition-colors"
                >
                  {s.question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  msg.role === "user" ? "bg-primary text-white" : "bg-emerald-600 text-white"
                }`}
              >
                {msg.role === "user" ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                ) : (
                   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                )}
              </div>

              <div className={`flex flex-col max-w-[80%] ${msg.role === "user" ? "items-end" : "items-start"}`}>
                <div
                  className={`px-5 py-3.5 rounded-2xl text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-card border border-border text-foreground"
                  }`}
                >
                  {msg.content}
                </div>
                
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 space-y-2 w-full">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider ml-1">{t("chat.sources")}</p>
                    <div className="grid gap-2">
                       {msg.sources.map((src, i) => (
                         <div key={i} className="bg-muted/30 border border-border/50 rounded-lg p-3 text-sm">
                            <div className="font-medium text-foreground mb-1">{src.title}</div>
                            <div className="flex items-center justify-between text-xs text-muted-foreground">
                               <span>{t("chat.relevance")} {Math.round(src.relevance_score * 100)}%</span>
                               {src.url && (
                                 <a href={src.url} target="_blank" rel="noopener" className="text-primary hover:underline">{t("chat.read_guide")} →</a>
                               )}
                            </div>
                         </div>
                       ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="pt-4 mt-auto">
        <form onSubmit={handleSubmit} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            placeholder={t("chat.input.placeholder")}
            className="w-full pl-5 pr-12 py-4 bg-card border border-input rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all shadow-sm disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2 top-2 bottom-2 aspect-square bg-primary text-primary-foreground rounded-lg flex items-center justify-center hover:bg-primary/90 disabled:opacity-50 disabled:hover:bg-primary transition-colors"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" /></svg>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
