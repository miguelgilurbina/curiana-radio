import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Curiana — Emergencia Lingüística Caquetía",
  description:
    "Simulación multi-agente de la lengua Caquetío-Arahuaca · Golfete de Coro · Siglo XIV-XV",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="min-h-screen">
        {/* Nav */}
        <nav
          className="border-b px-6 py-3 flex items-center gap-8 text-sm"
          style={{ borderColor: "#4A3520", background: "#2A1F14" }}
        >
          <span
            className="font-bold text-base tracking-wide"
            style={{ color: "#C47A2B" }}
          >
            ◈ CURIANA
          </span>
          <Link
            href="/"
            className="hover:text-amber-400 transition-colors"
            style={{ color: "#F5EDD6" }}
          >
            Dashboard
          </Link>
          <Link
            href="/lexicon"
            className="hover:text-amber-400 transition-colors"
            style={{ color: "#F5EDD6" }}
          >
            Léxico
          </Link>
          <Link
            href="/neologisms"
            className="hover:text-amber-400 transition-colors"
            style={{ color: "#F5EDD6" }}
          >
            Neologismos
          </Link>
          <span className="ml-auto text-xs" style={{ color: "#9C8A6E" }}>
            Golfete de Coro · s. XIV-XV
          </span>
        </nav>

        {/* Contenido */}
        <main className="p-6 max-w-7xl mx-auto">{children}</main>
      </body>
    </html>
  );
}
