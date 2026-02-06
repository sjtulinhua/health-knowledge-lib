"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

type Language = "en" | "zh";

type Translations = {
  [key in Language]: {
    [key: string]: string;
  };
};

const translations: Translations = {
  en: {
    // Navigation
    "nav.browse": "Browse",
    "nav.chat": "Chat",
    "nav.title": "HealthLib",
    "nav.collector": "Collector",
    
    // Home
    "home.badge": "v1.0 Public Beta",
    "home.title.prefix": "Reliable Health Knowledge for",
    "home.title.highlight": "Everyone",
    "home.subtitle": "Access evidence-based insights from global authorities like WHO, AHA, and ACSM. No noise, just science.",
    "home.cta.browse": "Start Browsing",
    "home.cta.chat": "Ask AI Assistant",
    "home.stats.sources": "Authoritative Sources",
    "home.stats.articles": "Verified Articles",
    "home.stats.updates": "Daily Updates",
    "home.feat.evidence.title": "Evidence First",
    "home.feat.evidence.desc": "Only guidelines from Tier 1 medical institutions are indexed. We prioritize accuracy over volume.",
    "home.feat.smart.title": "Smart Retrieval",
    "home.feat.smart.desc": "Semantic search understands medical context, not just keywords. Powered by advanced RAG.",
    "home.feat.hierarchy.title": "Clear Hierarchy",
    "home.feat.hierarchy.desc": "Knowledge is structured by authority level: Guidelines > Clinical Trials > Research.",
    "footer.rights": "© 2026 Health Knowledge Library. All rights reserved.",

    // Browse
    "browse.sidebar.title": "Knowledge Base",
    "browse.all_categories": "All Categories",
    "browse.title": "Internal Knowledge Retrieval",
    "browse.subtitle": "Search across verified guidelines and clinical studies.",
    "browse.search.placeholder": "Search for 'heart rate zones' or 'sleep hygiene'...",
    "browse.loading": "Loading...",
    "browse.empty": "Select a category or enter a search term.",
    "browse.source": "Source:",
    "browse.view_source": "View Source",
    "browse.modal.view_original": "View Original",
    "browse.modal.category": "Category:",

    // Chat
    "chat.empty.title": "Health Assistant",
    "chat.empty.subtitle": "Ask questions about heart rate, sleep, exercise, and stress. Answers are grounded in guideline documents.",
    "chat.input.placeholder": "Ask a follow-up question...",
    "chat.sources": "SOURCES",
    "chat.relevance": "Relevance:",
    "chat.read_guide": "Read Guide",
    "chat.error": "Sorry, I encountered an error. Please try again.",

    // Categories
    "cat.heart_rate": "Heart Rate",
    "cat.hrv": "HRV",
    "cat.sleep": "Sleep",
    "cat.exercise": "Exercise",
    "cat.stress": "Stress",

    // Tiers
    "tier.1": "Guideline",
    "tier.2": "Medical",
    "tier.3": "Research",
    "tier.4": "Reference",
  },
  zh: {
    // Navigation
    "nav.browse": "浏览知识库",
    "nav.chat": "智能问答",
    "nav.title": "健康知识库",
    "nav.collector": "知识捕手",

    // Home
    "home.badge": "v1.0 公测版",
    "home.title.prefix": "人人可用的",
    "home.title.highlight": "权威健康知识",
    "home.subtitle": "基于 WHO、AHA、ACSM 等国际权威机构的官方指南。拒绝噪音，只有科学。",
    "home.cta.browse": "浏览知识库",
    "home.cta.chat": "AI 助手问答",
    "home.stats.sources": "权威来源",
    "home.stats.articles": "验证文章",
    "home.stats.updates": "每日更新",
    "home.feat.evidence.title": "证据优先",
    "home.feat.evidence.desc": "仅收录一级医疗机构的指南。我们优先考虑准确性而非数量。",
    "home.feat.smart.title": "智能检索",
    "home.feat.smart.desc": "语义搜索理解医学语境，而不仅仅是关键词匹配。由高级 RAG 驱动。",
    "home.feat.hierarchy.title": "清晰层级",
    "home.feat.hierarchy.desc": "知识按权威级别组织：指南 > 临床试验 > 研究论文。",
    "footer.rights": "© 2026 Health Knowledge Library. 保留所有权利。",

    // Browse
    "browse.sidebar.title": "知识分类",
    "browse.all_categories": "全部分类",
    "browse.title": "知识检索",
    "browse.subtitle": "搜索经过验证的指南和临床研究。",
    "browse.search.placeholder": "搜索 '心率区间' 或 '睡眠卫生'...",
    "browse.loading": "加载中...",
    "browse.empty": "请选择分类或输入关键词开始。",
    "browse.source": "来源:",
    "browse.view_source": "查看来源",
    "browse.modal.view_original": "查看原文",
    "browse.modal.category": "分类:",

    // Chat
    "chat.empty.title": "健康助手",
    "chat.empty.subtitle": "咨询关于心率、睡眠、运动和压力的问题。所有回答均基于权威指南。",
    "chat.input.placeholder": "追问更多细节...",
    "chat.sources": "参考来源",
    "chat.relevance": "相关度:",
    "chat.read_guide": "阅读指南",
    "chat.error": "抱歉，遇到错误，请重试。",

    // Categories
    "cat.heart_rate": "心率",
    "cat.hrv": "HRV",
    "cat.sleep": "睡眠",
    "cat.exercise": "运动",
    "cat.stress": "压力",

    // Tiers
    "tier.1": "权威指南",
    "tier.2": "医疗机构",
    "tier.3": "研究论文",
    "tier.4": "参考资料",
  },
};

const LanguageContext = createContext<{
  lang: Language;
  setLang: (lang: Language) => void;
  t: (key: string) => string;
}>({
  lang: "zh",
  setLang: () => {},
  t: (key) => key,
});

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLang] = useState<Language>("zh"); // Default to Chinese based on user feedback

  const t = (key: string) => {
    return translations[lang][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useTranslation() {
  return useContext(LanguageContext);
}
