"use client";

import { useState } from "react";
import { 
  searchWeb, 
  previewContent, 
  importContent, 
  type WebSearchResult, 
  type ContentPreview 
} from "@/lib/api";
import { useTranslation } from "@/lib/i18n";

export default function CollectorPage() {
  const { t } = useTranslation();
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState<WebSearchResult[]>([]);
  const [previewItem, setPreviewItem] = useState<ContentPreview | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) return;
    setSearching(true);
    setError("");
    try {
      const data = await searchWeb(query);
      setResults(data);
    } catch (e) {
      setError("Search failed. Please try again.");
      console.error(e);
    } finally {
      setSearching(false);
    }
  };

  const handlePreview = async (url: string) => {
    setAnalyzing(true);
    setError("");
    try {
      // In a real app we might want to show a modal immediately with loading state
      const data = await previewContent(url);
      setPreviewItem(data);
    } catch (e) {
      setError("Failed to analyze content. The URL might be inaccessible.");
      console.error(e);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleImport = async () => {
    if (!previewItem) return;
    setImporting(true);
    try {
      await importContent(previewItem);
      setPreviewItem(null); // Close modal
      alert("Successfully added to knowledge base!");
    } catch (e) {
      alert("Import failed.");
      console.error(e);
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="container-width py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Smart Knowledge Collector</h1>
        <p className="text-muted-foreground">
          Search the web for guidelines, let AI clean them, and add to your library.
        </p>
      </div>

      {/* Search Input */}
      <div className="relative mb-10 max-w-2xl">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg className="h-5 w-5 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="e.g. 'WHO hypertension guidelines 2024' or 'AHA sleep recommendations'"
          className="block w-full pl-10 pr-3 py-3 border border-input rounded-lg leading-5 bg-card text-card-foreground shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm"
        />
        <button
            onClick={handleSearch}
            disabled={searching}
            className="absolute right-2 top-2 bottom-2 px-4 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 disabled:opacity-50"
        >
            {searching ? "Searching..." : "Search"}
        </button>
      </div>

      {error && (
          <div className="mb-6 p-4 rounded-md bg-destructive/10 text-destructive text-sm">
              {error}
          </div>
      )}

      {/* Analyzing Indicator (Global overlay if needed, or just inline) */}
      {analyzing && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
             <div className="bg-card p-6 rounded-lg shadow-xl text-center space-y-4 max-w-sm mx-4">
                 <div className="animate-spin text-primary mx-auto h-8 w-8 border-4 border-current border-t-transparent rounded-full"></div>
                 <div>
                     <h3 className="font-semibold text-lg">Analyzing Content...</h3>
                     <p className="text-sm text-muted-foreground">AI is reading, cleaning, and formatting the page.</p>
                 </div>
             </div>
        </div>
      )}

      {/* Results List */}
      <div className="space-y-4 max-w-4xl">
        {results.map((result, i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-5 hover:border-primary/50 transition-colors">
            <div className="flex justify-between items-start gap-4">
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-foreground mb-1 hover:text-primary cursor-pointer" onClick={() => handlePreview(result.url)}>
                        {result.title}
                    </h3>
                    <div className="flex items-center text-xs text-muted-foreground mb-2">
                        <span className="font-medium text-foreground">{result.source}</span>
                        <span className="mx-2">•</span>
                        <a href={result.url} target="_blank" rel="noopener" className="hover:underline truncate max-w-[300px]">
                            {result.url}
                        </a>
                    </div>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                        {result.snippet}
                    </p>
                </div>
                <button
                    onClick={() => handlePreview(result.url)}
                    className="shrink-0 px-4 py-2 border border-input bg-background hover:bg-accent hover:text-accent-foreground rounded-md text-sm font-medium transition-colors"
                >
                    Extract
                </button>
            </div>
          </div>
        ))}
        
        {results.length === 0 && !searching && query && (
             <div className="text-center py-12 text-muted-foreground">
                 No results found. Try broader keywords.
             </div>
        )}
      </div>

      {/* Preview Modal */}
      {previewItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm" 
            onClick={() => setPreviewItem(null)}
          />
          <div className="relative bg-card w-full max-w-3xl max-h-[90vh] rounded-xl shadow-2xl border border-border flex flex-col my-auto">
            <div className="flex items-center justify-between p-6 border-b border-border">
              <div>
                <h3 className="text-xl font-bold">Review Content</h3>
                <p className="text-sm text-muted-foreground">Verify AI-cleaned data before importing</p>
              </div>
              <button 
                onClick={() => setPreviewItem(null)}
                className="text-muted-foreground hover:text-foreground p-2"
              >
                ✕
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto space-y-6">
                {/* Metadata Form / Preview */}
                <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Title</label>
                        <input 
                            type="text" 
                            className="w-full mt-1 p-2 bg-muted/50 rounded border border-input"
                            value={previewItem.title} 
                            onChange={(e) => setPreviewItem({...previewItem, title: e.target.value})}
                        />
                    </div>
                    <div>
                        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Category</label>
                        <select 
                            className="w-full mt-1 p-2 bg-muted/50 rounded border border-input"
                            value={previewItem.category}
                            onChange={(e) => setPreviewItem({...previewItem, category: e.target.value})}
                        >
                            <option value="general">General</option>
                            <option value="heart_rate">Heart Rate</option>
                            <option value="sleep">Sleep</option>
                            <option value="exercise">Exercise</option>
                            <option value="stress">Stress</option>
                            <option value="hrv">HRV</option>
                        </select>
                    </div>
                    <div>
                        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Authority Tier</label>
                        <select 
                            className="w-full mt-1 p-2 bg-muted/50 rounded border border-input"
                            value={previewItem.tier}
                            onChange={(e) => setPreviewItem({...previewItem, tier: parseInt(e.target.value)})}
                        >
                            <option value={1}>Tier 1 (Official)</option>
                            <option value={2}>Tier 2 (Medical)</option>
                            <option value={3}>Tier 3 (Research)</option>
                            <option value={4}>Tier 4 (Blog/News)</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Summary</label>
                    <p className="mt-1 text-sm bg-muted/30 p-3 rounded">{previewItem.summary}</p>
                </div>

                <div>
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Cleaned Content</label>
                    <div className="mt-2 p-4 bg-muted/20 rounded-lg whitespace-pre-wrap text-sm leading-relaxed max-h-[400px] overflow-y-auto border border-border">
                        {previewItem.content}
                    </div>
                </div>
            </div>

            <div className="p-6 border-t border-border bg-muted/10 rounded-b-xl flex justify-end gap-3">
              <button 
                onClick={() => setPreviewItem(null)}
                className="px-4 py-2 text-sm font-medium hover:bg-muted rounded-md transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={handleImport}
                disabled={importing}
                className="px-6 py-2 bg-emerald-600 text-white rounded-md text-sm font-medium hover:bg-emerald-700 transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                {importing ? "Importing..." : "Approve & Import"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
