"use client";

import { useEffect, useState } from "react";
import { supabase, LANG_COLORS } from "@/lib/supabase";
import type { LexiconEntry } from "@/lib/supabase";

const CATEGORIES = ["todos", "sust", "v_raiz", "pron", "num", "part", "adj", "interr", "topón", "título"];
const LANG_FILTERS = ["todos", "caquetío", "wayunaiki", "lokono", "taíno", "proto-arahuaco"];

export default function LexiconPage() {
  const [entries, setEntries] = useState<LexiconEntry[]>([]);
  const [filtered, setFiltered] = useState<LexiconEntry[]>([]);
  const [search, setSearch] = useState("");
  const [catFilter, setCatFilter] = useState("todos");
  const [langFilter, setLangFilter] = useState("todos");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase
      .from("lexicon")
      .select("*")
      .order("word")
      .then(({ data }) => {
        setEntries((data as LexiconEntry[]) ?? []);
        setFiltered((data as LexiconEntry[]) ?? []);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    let result = entries;
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (e) =>
          e.word.toLowerCase().includes(q) ||
          e.meaning.toLowerCase().includes(q)
      );
    }
    if (catFilter !== "todos") {
      result = result.filter((e) => e.category === catFilter);
    }
    if (langFilter !== "todos") {
      result = result.filter((e) => e.source_language === langFilter);
    }
    setFiltered(result);
  }, [search, catFilter, langFilter, entries]);

  // Distribución por lengua
  const distribution = LANG_FILTERS.slice(1).map((lang) => ({
    lang,
    count: entries.filter((e) => e.source_language === lang).length,
    color: LANG_COLORS[lang] ?? "#9C8A6E",
  }));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold" style={{ color: "#C47A2B" }}>
          Léxico Caquetío-Arahuacano
        </h1>
        <p className="text-sm mt-1" style={{ color: "#9C8A6E" }}>
          {entries.length} palabras · vocabulario base del simulador
        </p>
      </div>

      {/* Distribución */}
      <div className="flex gap-3 flex-wrap">
        {distribution.map(({ lang, count, color }) => (
          <div
            key={lang}
            className="rounded px-3 py-2 text-sm cursor-pointer"
            style={{
              background: langFilter === lang ? color + "33" : "#2A1F14",
              border: `1px solid ${langFilter === lang ? color : "#4A3520"}`,
              color: langFilter === lang ? color : "#9C8A6E",
            }}
            onClick={() => setLangFilter(langFilter === lang ? "todos" : lang)}
          >
            {lang} · {count}
          </div>
        ))}
      </div>

      {/* Filtros */}
      <div className="flex gap-3 flex-wrap">
        <input
          type="text"
          placeholder="Buscar palabra o significado..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="rounded px-3 py-2 text-sm flex-1 min-w-48"
          style={{
            background: "#2A1F14",
            border: "1px solid #4A3520",
            color: "#F5EDD6",
            outline: "none",
          }}
        />
        <select
          value={catFilter}
          onChange={(e) => setCatFilter(e.target.value)}
          className="rounded px-3 py-2 text-sm"
          style={{
            background: "#2A1F14",
            border: "1px solid #4A3520",
            color: "#F5EDD6",
          }}
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {/* Tabla */}
      {loading ? (
        <div className="text-center py-16" style={{ color: "#9C8A6E" }}>
          Cargando léxico...
        </div>
      ) : (
        <div
          className="rounded-lg overflow-hidden"
          style={{ border: "1px solid #4A3520" }}
        >
          <table className="w-full text-sm">
            <thead>
              <tr style={{ background: "#2A1F14", borderBottom: "1px solid #4A3520" }}>
                <th className="text-left px-4 py-3" style={{ color: "#9C8A6E" }}>
                  Palabra
                </th>
                <th className="text-left px-4 py-3" style={{ color: "#9C8A6E" }}>
                  Significado
                </th>
                <th className="text-left px-4 py-3" style={{ color: "#9C8A6E" }}>
                  Categoría
                </th>
                <th className="text-left px-4 py-3" style={{ color: "#9C8A6E" }}>
                  Lengua fuente
                </th>
                <th className="text-left px-4 py-3" style={{ color: "#9C8A6E" }}>
                  Atestiguado
                </th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((entry, i) => {
                const color = LANG_COLORS[entry.source_language] ?? "#9C8A6E";
                return (
                  <tr
                    key={entry.id}
                    style={{
                      background: i % 2 === 0 ? "#1C1510" : "#2A1F14",
                      borderBottom: "1px solid #4A352033",
                    }}
                  >
                    <td className="px-4 py-2.5 font-bold" style={{ color: "#C47A2B" }}>
                      {entry.word}
                    </td>
                    <td className="px-4 py-2.5" style={{ color: "#F5EDD6" }}>
                      {entry.meaning}
                    </td>
                    <td className="px-4 py-2.5">
                      <span
                        className="text-xs px-1.5 py-0.5 rounded"
                        style={{ background: "#4A352055", color: "#9C8A6E" }}
                      >
                        {entry.category}
                      </span>
                    </td>
                    <td className="px-4 py-2.5">
                      <span
                        className="text-xs px-1.5 py-0.5 rounded"
                        style={{ background: color + "22", color }}
                      >
                        {entry.source_language}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 text-xs" style={{ color: "#9C8A6E" }}>
                      {entry.attested ? "✓" : "—"}
                    </td>
                  </tr>
                );
              })}
              {filtered.length === 0 && (
                <tr>
                  <td
                    colSpan={5}
                    className="px-4 py-8 text-center"
                    style={{ color: "#9C8A6E" }}
                  >
                    Sin resultados para esa búsqueda.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
