"use client";

import { useState } from "react";
import type { PalabraLexicon } from "@/lib/lexicon";
import { Card, Overline } from "@/components/simulador/ui";

const CATEGORIES = ["todos", "sust", "v_raiz", "pron", "num", "part", "adj", "interr", "topón", "título"];

// Las 9 categorías de fuente del lexicón (ver metodología en CLAUDE.md) -- no
// son las mismas 5 lenguas que el chart de deriva (lib/sim-theme.ts LANGS),
// esas son específicamente las que score_linguistico() mide en los agentes.
const LANG_COLORS: Record<string, string> = {
  "caquetío": "#C47A2B",
  "wayunaiki": "#2E7D4F",
  "lokono": "#5B4FCF",
  "taíno": "#B04040",
  "proto-arahuaco": "#6D8A9E",
  "kalinago": "#8a6c57",
  "kalinago-caribe-overlay": "#9d7f66",
  "jirajaroide-contacto": "#72584a",
  "hipotético-no-verificado": "#c5b59f",
};
const LANG_FILTERS = Object.keys(LANG_COLORS);

// Cupo de filas renderizadas por consulta -- una sola fuente de verdad para
// el slice de la tabla y los dos mensajes que lo describen.
const FILA_LIMITE = 500;

export default function LexiconFilter({ palabras }: { palabras: PalabraLexicon[] }) {
  const [search, setSearch] = useState("");
  const [catFilter, setCatFilter] = useState("todos");
  const [langFilter, setLangFilter] = useState("todos");

  const filtered = palabras.filter((e) => {
    if (search.trim()) {
      const q = search.toLowerCase();
      if (!e.word.toLowerCase().includes(q) && !e.meaning.toLowerCase().includes(q)) return false;
    }
    if (catFilter !== "todos" && e.category !== catFilter) return false;
    if (langFilter !== "todos" && e.source_language !== langFilter) return false;
    return true;
  });

  const distribution = LANG_FILTERS.map((lang) => ({
    lang,
    count: palabras.filter((e) => e.source_language === lang).length,
    color: LANG_COLORS[lang],
  })).filter((d) => d.count > 0);

  return (
    <div>
      <div className="mb-4 flex flex-wrap gap-2">
        {distribution.map(({ lang, count, color }) => {
          const active = langFilter === lang;
          return (
            <button
              key={lang}
              onClick={() => setLangFilter(active ? "todos" : lang)}
              className="rounded-full border px-3 py-1.5 font-sans text-sm transition-colors"
              style={{
                background: active ? `${color}1a` : "transparent",
                borderColor: active ? color : "#dcd2c3",
                color: active ? color : "#72584a",
              }}
            >
              <span className="mr-1.5 inline-block h-2 w-2 rounded-full align-middle" style={{ background: color }} />
              {lang} · {count}
            </button>
          );
        })}
      </div>

      <div className="mb-5 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Buscar palabra o significado…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="min-w-[12rem] flex-1 rounded-lg border border-earth-200 bg-earth-50/80 px-3.5 py-2 font-sans text-sm text-deep-900 placeholder:text-earth-400 outline-none focus:border-frequency"
        />
        {search && (
          <button
            onClick={() => setSearch("")}
            className="rounded-lg border border-earth-200 px-3 py-2 font-sans text-sm text-earth-600 transition-colors hover:text-deep-800"
            aria-label="Limpiar búsqueda"
          >
            Limpiar
          </button>
        )}
        <select
          value={catFilter}
          onChange={(e) => setCatFilter(e.target.value)}
          className="rounded-lg border border-earth-200 bg-earth-50/80 px-3 py-2 font-sans text-sm text-deep-800 outline-none focus:border-frequency"
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <p className="mb-3 font-sans text-xs text-earth-500">
        Mostrando {Math.min(filtered.length, FILA_LIMITE)} de {filtered.length} resultados
        {filtered.length !== palabras.length && ` (de ${palabras.length} palabras en total)`}
      </p>

      <Card className="overflow-hidden p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-earth-200 bg-earth-100/50">
                {["Palabra", "Significado", "Categoría", "Lengua fuente", "Atest."].map((h) => (
                  <th key={h} className="px-4 py-3 font-sans text-[0.7rem] font-medium uppercase tracking-wider text-earth-600">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.slice(0, FILA_LIMITE).map((entry) => {
                const color = LANG_COLORS[entry.source_language] ?? "#9d7f66";
                return (
                  <tr key={entry.id} className="border-b border-earth-200/50 transition-colors hover:bg-earth-100/40">
                    <td className="px-4 py-2.5 font-serif font-semibold text-frequency">{entry.word}</td>
                    <td className="px-4 py-2.5 font-sans text-sm text-deep-800">{entry.meaning}</td>
                    <td className="px-4 py-2.5">
                      <span className="rounded bg-earth-100 px-1.5 py-0.5 font-sans text-xs text-earth-600">{entry.category}</span>
                    </td>
                    <td className="px-4 py-2.5">
                      <span className="rounded px-1.5 py-0.5 font-sans text-xs" style={{ background: `${color}1a`, color }}>
                        {entry.source_language}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 font-sans text-xs text-earth-500">{entry.attested ? "✓" : "—"}</td>
                  </tr>
                );
              })}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-10 text-center font-sans text-sm text-earth-500">
                    Sin resultados para esa búsqueda.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {filtered.length > FILA_LIMITE && (
          <p className="border-t border-earth-200/70 px-4 py-3 font-sans text-xs text-earth-500">
            Mostrando las primeras {FILA_LIMITE} — afina la búsqueda o el filtro para ver más.
          </p>
        )}
      </Card>
    </div>
  );
}
