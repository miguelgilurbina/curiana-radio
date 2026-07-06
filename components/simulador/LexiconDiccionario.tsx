"use client";

import { useMemo, useState } from "react";
import type { PalabraLexicon } from "@/lib/lexicon";
import { EmptyState } from "@/components/simulador/ui";

// Diccionario literario del léxico base: entradas agrupadas por letra
// inicial, paginadas en el DOM (el seed completo viaja una sola vez como
// payload estático; lo que se limita es cuánto se renderiza por página).
// El id no se envía al cliente — no se usa para nada visible.
export type EntradaDiccionario = Omit<PalabraLexicon, "id">;

// Las 9 categorías de fuente del lexicón (ver metodología en CLAUDE.md) — no
// son las mismas 5 lenguas del chart de deriva (lib/sim-theme.ts LANGS),
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

const CATEGORIES = ["todos", "sust", "v_raiz", "pron", "num", "part", "adj", "interr", "topón", "título"];

const PAGE_SIZE = 120;

function inicial(word: string): string {
  const ch = word
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .match(/\p{L}/u);
  return ch ? ch[0].toUpperCase() : "·";
}

export default function LexiconDiccionario({ palabras }: { palabras: EntradaDiccionario[] }) {
  const [search, setSearch] = useState("");
  const [langFilter, setLangFilter] = useState("todos");
  const [catFilter, setCatFilter] = useState("todos");
  const [soloAtestiguadas, setSoloAtestiguadas] = useState(false);
  const [pagina, setPagina] = useState(0);

  const ordenadas = useMemo(
    () => [...palabras].sort((a, b) => a.word.localeCompare(b.word, "es")),
    [palabras]
  );

  const filtradas = useMemo(() => {
    const q = search.trim().toLowerCase();
    return ordenadas.filter((e) => {
      if (q && !e.word.toLowerCase().includes(q) && !e.meaning.toLowerCase().includes(q)) return false;
      if (langFilter !== "todos" && e.source_language !== langFilter) return false;
      if (catFilter !== "todos" && e.category !== catFilter) return false;
      if (soloAtestiguadas && !e.attested) return false;
      return true;
    });
  }, [ordenadas, search, langFilter, catFilter, soloAtestiguadas]);

  const totalPaginas = Math.max(1, Math.ceil(filtradas.length / PAGE_SIZE));
  const paginaActual = Math.min(pagina, totalPaginas - 1);
  const desde = paginaActual * PAGE_SIZE;
  const visibles = filtradas.slice(desde, desde + PAGE_SIZE);

  // Grupos por letra inicial dentro de la página visible.
  const grupos: { letra: string; entradas: EntradaDiccionario[] }[] = [];
  for (const e of visibles) {
    const letra = inicial(e.word);
    const ultimo = grupos[grupos.length - 1];
    if (ultimo && ultimo.letra === letra) ultimo.entradas.push(e);
    else grupos.push({ letra, entradas: [e] });
  }

  const distribution = Object.entries(LANG_COLORS)
    .map(([lang, color]) => ({ lang, color, count: palabras.filter((e) => e.source_language === lang).length }))
    .filter((d) => d.count > 0);
  const atestiguadas = palabras.filter((e) => e.attested).length;

  const resetear = (fn: () => void) => {
    fn();
    setPagina(0);
  };

  const Paginacion = () =>
    totalPaginas > 1 ? (
      <div className="flex items-center justify-between border-t border-(--sim-rule) py-3 font-sans text-sm">
        <button
          onClick={() => setPagina(Math.max(0, paginaActual - 1))}
          disabled={paginaActual === 0}
          className="text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego) disabled:cursor-default disabled:text-(--sim-rule)"
        >
          ← anterior
        </button>
        <span className="font-sans text-xs tabular-nums text-(--sim-ink-faint)">
          página {paginaActual + 1} de {totalPaginas}
        </span>
        <button
          onClick={() => setPagina(Math.min(totalPaginas - 1, paginaActual + 1))}
          disabled={paginaActual >= totalPaginas - 1}
          className="text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego) disabled:cursor-default disabled:text-(--sim-rule)"
        >
          siguiente →
        </button>
      </div>
    ) : null;

  return (
    <div>
      <div className="mb-4 flex flex-wrap gap-2">
        {distribution.map(({ lang, count, color }) => {
          const active = langFilter === lang;
          return (
            <button
              key={lang}
              onClick={() => resetear(() => setLangFilter(active ? "todos" : lang))}
              className="rounded-full border px-3 py-1.5 font-sans text-sm transition-colors"
              style={{
                background: active ? `${color}1a` : "transparent",
                borderColor: active ? color : "var(--sim-rule)",
                color: active ? color : "var(--sim-ink-soft)",
              }}
            >
              <span className="mr-1.5 inline-block h-2 w-2 rounded-full align-middle" style={{ background: color }} />
              {lang} · {count}
            </button>
          );
        })}
        <button
          onClick={() => resetear(() => setSoloAtestiguadas(!soloAtestiguadas))}
          className="rounded-full border px-3 py-1.5 font-sans text-sm transition-colors"
          style={{
            background: soloAtestiguadas ? "#C47A2B1a" : "transparent",
            borderColor: soloAtestiguadas ? "#C47A2B" : "var(--sim-rule)",
            color: soloAtestiguadas ? "#C47A2B" : "var(--sim-ink-soft)",
          }}
        >
          ✓ solo atestiguadas · {atestiguadas}
        </button>
      </div>

      <div className="mb-5 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Buscar palabra o significado…"
          value={search}
          onChange={(e) => resetear(() => setSearch(e.target.value))}
          className="min-w-[12rem] flex-1 rounded-lg border border-(--sim-rule) bg-(--sim-paper-deep) px-3.5 py-2 font-sans text-sm text-(--sim-ink) placeholder:text-(--sim-ink-faint) outline-none focus:border-(--sim-fuego)"
        />
        {search && (
          <button
            onClick={() => resetear(() => setSearch(""))}
            className="rounded-lg border border-(--sim-rule) px-3 py-2 font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-ink)"
            aria-label="Limpiar búsqueda"
          >
            Limpiar
          </button>
        )}
        <select
          value={catFilter}
          onChange={(e) => resetear(() => setCatFilter(e.target.value))}
          className="rounded-lg border border-(--sim-rule) bg-(--sim-paper-deep) px-3 py-2 font-sans text-sm text-(--sim-ink) outline-none focus:border-(--sim-fuego)"
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <p className="mb-2 font-sans text-xs text-(--sim-ink-faint)">
        {filtradas.length === palabras.length
          ? `${palabras.length} palabras`
          : `${filtradas.length} de ${palabras.length} palabras`}
        {totalPaginas > 1 && ` · mostrando ${desde + 1}–${Math.min(desde + PAGE_SIZE, filtradas.length)}`}
      </p>

      {filtradas.length === 0 ? (
        <EmptyState title="Sin resultados para esa búsqueda" />
      ) : (
        <>
          {grupos.map(({ letra, entradas }) => (
            <section key={`${letra}-${desde}`} className="mt-6 first:mt-2">
              <h3 className="border-b border-(--sim-rule) pb-1 font-serif text-2xl font-semibold text-(--sim-ink-faint)">
                {letra}
              </h3>
              <dl>
                {entradas.map((e, i) => {
                  const color = LANG_COLORS[e.source_language] ?? "#9d7f66";
                  return (
                    <div key={`${e.word}-${i}`} className="border-t border-(--sim-rule) py-2.5 first:border-t-0">
                      <dt className="flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
                        <span className="font-serif text-lg font-semibold text-(--sim-fuego)">{e.word}</span>
                        {e.category && (
                          <span className="font-sans text-xs italic text-(--sim-ink-faint)">{e.category}</span>
                        )}
                        <span
                          className="rounded px-1.5 py-0.5 font-sans text-[0.7rem]"
                          style={{ background: `${color}1a`, color }}
                        >
                          {e.source_language}
                        </span>
                        {e.attested && (
                          <span className="font-sans text-[0.7rem] font-medium text-(--sim-ink-soft)">✓ atestiguada</span>
                        )}
                      </dt>
                      <dd className="mt-0.5 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink)">
                        {e.meaning}
                        {e.attested && e.source_ref && e.source_ref !== e.source_language && (
                          <span className="ml-2 font-sans text-xs italic text-(--sim-ink-faint)">({e.source_ref})</span>
                        )}
                      </dd>
                    </div>
                  );
                })}
              </dl>
            </section>
          ))}
          <Paginacion />
        </>
      )}
    </div>
  );
}
