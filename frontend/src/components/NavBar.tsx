"use client";

import Link from "next/link";
import { useTranslation } from "@/lib/i18n";

export default function NavBar() {
  const { lang, setLang, t } = useTranslation();

  const toggleLang = () => {
    setLang(lang === "zh" ? "en" : "zh");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border h-16">
      <div className="container-width h-full flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all duration-300">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 6v12m-6-6h12" />
            </svg>
          </div>
          <span className="font-bold text-lg tracking-tight text-white group-hover:text-primary transition-colors">
            {t("nav.title")}
          </span>
        </Link>
        
        <div className="flex items-center gap-1">
          <div className="hidden md:flex gap-1">
            {[
              { name: t("nav.browse"), href: "/browse" },
              { name: t("nav.chat"), href: "/chat" }
            ].map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-md transition-all duration-200"
              >
                {item.name}
              </Link>
            ))}
          </div>
          
          <div className="ml-4 pl-4 border-l border-border flex items-center gap-3">
             <button
               onClick={toggleLang}
               className="text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/50 px-3 py-1.5 rounded-md transition-colors"
             >
               {lang === "zh" ? "EN" : "中"}
             </button>
          </div>

        </div>
      </div>
    </nav>
  );
}
