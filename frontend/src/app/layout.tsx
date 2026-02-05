import type { Metadata } from "next";
import { LanguageProvider } from "@/lib/i18n";
import NavBar from "@/components/NavBar";
import "./globals.css";

export const metadata: Metadata = {
  title: "Health Knowledge Library",
  description: "Evidence-based health and fitness knowledge base derived from WHO, AHA, and ACSM guidelines.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className="dark">
      <body className="min-h-screen antialiased bg-background text-foreground selection:bg-primary/20 selection:text-primary-foreground">
        <LanguageProvider>
          <NavBar />
          <main className="pt-16 min-h-screen pb-12">{children}</main>
          
          <footer className="border-t border-border py-8 bg-background">
             <div className="container-width text-center text-sm text-muted-foreground">
               <p>© 2026 Health Knowledge Library. All rights reserved.</p>
             </div>
          </footer>
        </LanguageProvider>
      </body>
    </html>
  );
}
