"use client";

import { useState, useEffect } from "react";
import { 
  getCategories, 
  searchKnowledge, 
  browseKnowledge,
  getKnowledgeItem,
  type Category, 
  type SearchResult,
  type KnowledgeItem 
} from "@/lib/api";
import { useTranslation } from "@/lib/i18n";

const CATEGORY_ICONS: Record<string, string> = {
  heart_rate: "❤️",
  hrv: "💓",
  sleep: "😴",
  exercise: "🏃",
  stress: "🧘",
};

const TIER_LABELS: Record<number, { bg: string; text: string; border: string; key: string }> = {
  1: { key: "tier.1", bg: "bg-emerald-500/10", text: "text-emerald-500", border: "border-emerald-500/20" },
  2: { key: "tier.2", bg: "bg-sky-500/10", text: "text-sky-500", border: "border-sky-500/20" },
  3: { key: "tier.3", bg: "bg-amber-500/10", text: "text-amber-500", border: "border-amber-500/20" },
  4: { key: "tier.4", bg: "bg-slate-500/10", text: "text-slate-500", border: "border-slate-500/20" },
};

export default function BrowsePage() {
  const { t, lang } = useTranslation();
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState<KnowledgeItem | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    getCategories(lang).then(setCategories).catch(console.error);
  }, [lang]);

  useEffect(() => {
      // Always load content when lang changes or category changes
      loadCategoryContent();
  }, [selectedCategory, lang]);

  const loadCategoryContent = async () => {
    setLoading(true);
    try {
      // Pass lang to browseKnowledge
      const data = await browseKnowledge(selectedCategory || undefined, undefined, 1, 20, lang);
      setResults(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadCategoryContent();
      return;
    }
    setLoading(true);
    try {
      // Pass lang to searchKnowledge
      const data = await searchKnowledge(searchQuery, selectedCategory || undefined, lang);
      setResults(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (categoryId: string | null) => {
    setSelectedCategory(categoryId);
    setSearchQuery("");
  };

  const openDetail = async (item: SearchResult) => {
    // Force fetch with current lang to ensure complete and translated content
    try {
        const fullItem = await getKnowledgeItem(item.id, lang);
        setSelectedItem(fullItem);
    } catch (e) {
        console.error("Failed to fetch full item details:", e);
        // Fallback
        setSelectedItem({
            id: item.id,
            title: item.metadata.title,
            content: item.content,
            category: item.metadata.category,
            source: item.metadata.source,
            source_url: item.metadata.source_url,
            tier: item.metadata.tier
        });
    }
    setModalOpen(true);
  };

  return (
    <div className="container-width py-12">
      <div className="flex flex-col md:flex-row gap-12">
        {/* Sidebar */}
        <aside className="md:w-64 flex-shrink-0 space-y-8">
          <div>
            <h2 className="text-sm font-bold text-muted-foreground uppercase tracking-wider mb-4 px-2">{t("browse.sidebar.title")}</h2>
            <div className="space-y-1">
              <button
                onClick={() => handleCategoryChange(null)}
                className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex justify-between ${
                  !selectedCategory
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <span>{t("browse.all_categories")}</span>
                <span className="opacity-60">{categories.reduce((acc, c) => acc + c.count, 0)}</span>
              </button>
              {categories.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => handleCategoryChange(cat.id)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center justify-between group ${
                    selectedCategory === cat.id
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`}
                >
                  <span className="flex items-center gap-2">{t(`cat.${cat.id}`) || cat.name}</span>
                  <span className="opacity-60 bg-black/10 px-1.5 rounded text-xs">{cat.count}</span>
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 min-w-0">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">{t("browse.title")}</h1>
            <p className="text-muted-foreground">{t("browse.subtitle")}</p>
          </div>

          <div className="relative mb-10">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder={t("browse.search.placeholder")}
              className="block w-full pl-10 pr-3 py-3 border border-input rounded-lg leading-5 bg-card text-card-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm transition-shadow"
            />
          </div>

          {/* Results List */}
          <div className="space-y-6">
            {loading ? (
               <div className="text-center py-12 text-muted-foreground animate-pulse">{t("browse.loading")}</div>
            ) : results.length > 0 ? (
              results.map((item, i) => {
                const tierStyle = TIER_LABELS[item.metadata.tier] || TIER_LABELS[4];
                return (
                  <article 
                    key={i} 
                    onClick={() => openDetail(item)}
                    className="group relative bg-card border border-border rounded-lg p-6 hover:border-primary/50 transition-colors cursor-pointer hover:shadow-sm"
                  >
                    <div className="flex items-start justify-between mb-2">
                       <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                         {item.metadata.title}
                       </h3>
                       <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${tierStyle.bg} ${tierStyle.text} ${tierStyle.border}`}>
                         {t(tierStyle.key)}
                       </span>
                    </div>
                    <p className="text-muted-foreground leading-relaxed mb-4 line-clamp-3">
                      {item.content}
                    </p>
                    <div className="flex items-center text-xs text-muted-foreground gap-4">
                      <div className="flex items-center gap-1">
                        <span className="font-medium text-foreground">{t("browse.source")}</span> {item.metadata.source}
                      </div>
                    </div>
                  </article>
                );
              })
            ) : (
              <div className="text-center py-20 border border-dashed border-border rounded-lg">
                <p className="text-muted-foreground text-sm">{t("browse.empty")}</p>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Detail Modal */}
      {modalOpen && selectedItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
            onClick={() => setModalOpen(false)}
          />
          <div className="relative bg-card w-full max-w-2xl max-h-[85vh] rounded-xl shadow-2xl border border-border flex flex-col animate-in fade-in zoom-in-95 duration-200">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-border">
              <div>
                <h3 className="text-xl font-bold">{selectedItem.title}</h3>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${TIER_LABELS[selectedItem.tier]?.bg} ${TIER_LABELS[selectedItem.tier]?.text} ${TIER_LABELS[selectedItem.tier]?.border}`}>
                    {t(TIER_LABELS[selectedItem.tier]?.key)}
                  </span>
                  <span className="text-xs text-muted-foreground">{t("browse.modal.category")} {t(`cat.${selectedItem.category}`) || selectedItem.category}</span>
                </div>
              </div>
              <button 
                onClick={() => setModalOpen(false)}
                className="text-muted-foreground hover:text-foreground transition-colors p-2 hover:bg-muted rounded-full"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            {/* Content */}
            <div className="p-6 overflow-y-auto leading-relaxed text-foreground whitespace-pre-wrap">
              {selectedItem.content}
            </div>
            
            {/* Footer */}
            <div className="p-6 border-t border-border bg-muted/20 rounded-b-xl flex justify-between items-center">
              <div className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">{t("browse.source")}</span> {selectedItem.source}
              </div>
              {selectedItem.source_url && (
                <a 
                  href={selectedItem.source_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-sm font-medium text-primary hover:underline flex items-center gap-1"
                >
                  {t("browse.modal.view_original")}
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
