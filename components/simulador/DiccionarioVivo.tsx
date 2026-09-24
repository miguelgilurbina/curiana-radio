"use client";

import Link from "next/link";
import { useMemo, useState, useSyncExternalStore } from "react";
import type { Capa, CapaInfo, FichaIndice } from "@/types/fichas";
import { CAPAS_EPISTEMICAS } from "@/lib/sim-theme";
import { CapaGlifo } from "@/components/simulador/capa";
import { EmptyState } from "@/components/simulador/ui";

// El índice del diccionario: las voces caquetías, cada una con su capa, en
// orden alfabético y agrupadas por letra. La leyenda de capas ES el filtro.
// El filtro vive en la URL (?capa=reconstruido) para que se pueda compartir;
// se lee con useSyncExternalStore y se escribe con replaceState, sin efectos.

const DIACRITICOS = /[̀-ͯ]/g;

function inicial(forma: string): string {
  const ch = forma.normalize("NFD").replace(DIACRITICOS, "").match(/\p{L}/u);
  return ch ? ch[0].toUpperCase() : "·";
}

function sinAcentos(t: string): string {
  return t.normalize("NFD").replace(DIACRITICOS, "").toLowerCase();
}

const CLAVES = new Set<string>(CAPAS_EPISTEMICAS.map((c) => c.key));

function capaDeLaUrl(): Capa | null {
  try {
    const c = new URLSearchParams(window.location.search).get("capa");
    return c && CLAVES.has(c) ? (c as Capa) : null;
  } catch {
    return null;
  }
}

function suscribir(cb: () => void) {
  window.addEventListener("popstate", cb);
  return () => window.removeEventListener("popstate", cb);
}

export default function DiccionarioVivo({
  fichas,
  capas,
}: {
  fichas: FichaIndice[];
  capas: Partial<Record<Capa, CapaInfo>>;
}) {
  const capaUrl = useSyncExternalStore(suscribir, capaDeLaUrl, () => null);
  // undefined = el lector aún no eligió: manda la URL.
  const [capaElegida, setCapaElegida] = useState<Capa | null | undefined>(undefined);
  const capa = capaElegida === undefined ? capaUrl : capaElegida;
  const [busqueda, setBusqueda] = useState("");

  const conteo = useMemo(() => {
    const n: Record<string, number> = {};
    for (const f of fichas) n[f.capa] = (n[f.capa] ?? 0) + 1;
    return n;
  }, [fichas]);

  const filtradas = useMemo(() => {
    const q = sinAcentos(busqueda.trim());
    return fichas.filter((f) => {
      if (capa && f.capa !== capa) return false;
      if (q && !sinAcentos(f.forma).includes(q) && !sinAcentos(f.glosa).includes(q)) return false;
      return true;
    });
  }, [fichas, capa, busqueda]);

  const grupos: { letra: string; fichas: FichaIndice[] }[] = [];
  for (const f of filtradas) {
    const letra = inicial(f.forma);
    const ultimo = grupos[grupos.length - 1];
    if (ultimo && ultimo.letra === letra) ultimo.fichas.push(f);
    else grupos.push({ letra, fichas: [f] });
  }

  const elegir = (c: Capa) => {
    const nueva = capa === c ? null : c;
    setCapaElegida(nueva);
    try {
      const url = new URL(window.location.href);
      if (nueva) url.searchParams.set("capa", nueva);
      else url.searchParams.delete("capa");
      window.history.replaceState(null, "", url);
    } catch {
      /* sin URL no hay estado compartible, pero el filtro funciona igual */
    }
  };

  return (
    <div>
      {/* La leyenda: cómo sabemos cada palabra. Pinchar una capa filtra. */}
      <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        {CAPAS_EPISTEMICAS.map((c) => {
          const activa = capa === c.key;
          const info = capas[c.key];
          return (
            <li key={c.key}>
              <button
                type="button"
                onClick={() => elegir(c.key)}
                aria-pressed={activa}
                className="group h-full w-full rounded-md border px-3.5 py-3 text-left transition-colors"
                style={{
                  borderColor: activa ? c.color : "var(--sim-rule)",
                  background: activa ? "var(--sim-paper-deep)" : "transparent",
                }}
              >
                <span className="flex items-baseline justify-between gap-3">
                  <span className="inline-flex items-center gap-2 font-sans text-sm font-semibold" style={{ color: c.color }}>
                    <CapaGlifo capa={c.key} size={12} />
                    {c.plural}
                  </span>
                  <span className="sim-mono text-xs tabular-nums text-(--sim-ink-faint)">
                    {conteo[c.key] ?? 0}
                  </span>
                </span>
                {info && (
                  <span className="mt-1 block font-sans text-xs leading-relaxed text-(--sim-ink-soft)">
                    {info.que_es}
                  </span>
                )}
              </button>
            </li>
          );
        })}
      </ul>

      <div className="mt-5 flex flex-wrap items-center gap-3">
        <label className="sr-only" htmlFor="buscar-voz">
          Buscar una voz o su significado
        </label>
        <input
          id="buscar-voz"
          type="search"
          placeholder="Buscar una voz o lo que significa…"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          className="min-w-[12rem] flex-1 rounded-md border border-(--sim-rule) bg-(--sim-paper-deep) px-3.5 py-2 font-sans text-sm text-(--sim-ink) placeholder:text-(--sim-ink-faint) outline-none focus:border-(--sim-fuego)"
        />
        <p className="font-sans text-xs tabular-nums text-(--sim-ink-faint)" aria-live="polite">
          {filtradas.length === fichas.length
            ? `${fichas.length} voces`
            : `${filtradas.length} de ${fichas.length} voces`}
        </p>
      </div>

      {filtradas.length === 0 ? (
        <div className="mt-6">
          <EmptyState title="Ninguna voz con esa búsqueda" />
        </div>
      ) : (
        grupos.map(({ letra, fichas: delGrupo }) => (
          <section key={letra} className="mt-7">
            <h3 className="border-b border-(--sim-rule) pb-1 sim-display text-2xl font-semibold text-(--sim-ink-faint)">
              {letra}
            </h3>
            <ul>
              {delGrupo.map((f) => (
                <li key={f.slug} className="border-t border-(--sim-rule) first:border-t-0">
                  <Link
                    href={`/kaketiana/lexicon/${f.slug}`}
                    className="group flex items-baseline gap-2.5 py-2"
                  >
                    <span className="self-center">
                      <CapaGlifo capa={f.capa} size={10} />
                    </span>
                    <span className="sim-display shrink-0 text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                      {f.forma}
                    </span>
                    <span className="min-w-0 font-sans text-sm leading-snug text-(--sim-ink-soft)">
                      {f.glosa}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        ))
      )}
    </div>
  );
}
