"use client";

import Link from "next/link";
import { useTranslation } from "@/lib/i18n";

export default function Home() {
  const { t } = useTranslation();

  return (
    <div className="container-width pt-12">
      {/* Hero Section */}
      <section className="text-center py-24 space-y-8 animate-fade-in-up">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
          </span>
          {t("home.badge")}
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white max-w-4xl mx-auto leading-[1.1]">
          {t("home.title.prefix")} <span className="text-primary">{t("home.title.highlight")}</span>
        </h1>
        
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          {t("home.subtitle")}
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link
            href="/browse"
            className="h-12 px-8 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-medium text-base inline-flex items-center justify-center transition-colors shadow-lg shadow-primary/20"
          >
            {t("home.cta.browse")}
          </Link>
          <Link
            href="/chat"
            className="h-12 px-8 rounded-lg border border-border bg-background hover:bg-muted text-foreground font-medium text-base inline-flex items-center justify-center transition-colors"
          >
            {t("home.cta.chat")}
          </Link>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 py-12 border-y border-border/50">
        {[
          { icon: "📚", label: t("home.stats.sources"), value: "100+" },
          { icon: "🔍", label: t("home.stats.articles"), value: "5,000+" },
          { icon: "⚡", label: t("home.stats.updates"), value: "Yes" },
        ].map((stat, i) => (
          <div key={i} className="flex flex-col items-center text-center p-4">
             <span className="text-3xl font-bold text-foreground mb-1">{stat.value}</span>
             <span className="text-sm text-muted-foreground">{stat.label}</span>
          </div>
        ))}
      </section>

      {/* Feature Cards */}
      <section className="grid md:grid-cols-3 gap-8 py-24">
        {[
          {
            title: t("home.feat.evidence.title"),
            desc: t("home.feat.evidence.desc"),
            icon: "⚖️"
          },
          {
            title: t("home.feat.smart.title"),
            desc: t("home.feat.smart.desc"),
            icon: "🧠"
          },
          {
            title: t("home.feat.hierarchy.title"),
            desc: t("home.feat.hierarchy.desc"),
            icon: "📊"
          }
        ].map((feature, i) => (
          <div key={i} className="p-8 rounded-2xl bg-card border border-border hover:border-primary/50 transition-colors group">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              {feature.icon}
            </div>
            <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
            <p className="text-muted-foreground leading-relaxed">
              {feature.desc}
            </p>
          </div>
        ))}
      </section>
    </div>
  );
}
