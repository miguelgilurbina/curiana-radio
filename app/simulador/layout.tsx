import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Curiana — Emergencia Lingüística Caquetía",
  description:
    "Simulación multi-agente de la lengua Caquetío-Arahuacana · Golfete de Coro · Siglo XIV-XV",
};

export default function SimuladorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Contenedor opaco oscuro: cubre el fondo claro del shell de la radio y da
  // al simulador su identidad visual propia (paleta caquetía).
  return (
    <div style={{ background: "#1C1510", color: "#F5EDD6", minHeight: "100vh" }}>
      <div
        className="flex items-center gap-6 px-6 py-3 text-sm flex-wrap"
        style={{ borderBottom: "1px solid #4A3520", background: "#2A1F14" }}
      >
        <span className="font-bold tracking-wide" style={{ color: "#C47A2B" }}>
          ◈ CURIANA · Simulador
        </span>
        <Link href="/simulador" style={{ color: "#F5EDD6" }} className="hover:opacity-80 transition-opacity">
          Dashboard
        </Link>
        <Link href="/simulador/lexicon" style={{ color: "#F5EDD6" }} className="hover:opacity-80 transition-opacity">
          Léxico
        </Link>
        <Link href="/simulador/neologisms" style={{ color: "#F5EDD6" }} className="hover:opacity-80 transition-opacity">
          Neologismos
        </Link>
        <Link
          href="/"
          className="ml-auto text-xs hover:opacity-80 transition-opacity"
          style={{ color: "#9C8A6E" }}
        >
          ← Volver a Curiana Radio
        </Link>
      </div>

      <main className="p-6 max-w-7xl mx-auto">{children}</main>
    </div>
  );
}
