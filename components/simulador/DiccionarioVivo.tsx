"use client";

import Link from "next/link";
import { useMemo, useState, useSyncExternalStore } from "react";
import type { Capa, CapaInfo, FichaIndice } from "@/types/fichas";
import { CAPAS_EPISTEMICAS } from "@/lib/sim-theme";
import { EmptyState } from "@/components/simulador/ui";
import Etiqueta, { GRADO_DE_CAPA, glifoDe } from "@/components/kaketiana/Etiqueta";
import FormaCaquetia from "@/components/kaketiana/Forma";

// El índice del diccionario: las voces caquetías, cada una con su capa, en
// orden alfabético y agrupadas por letra. La leyenda de capas ES el filtro.
// El filtro vive en la URL (?capa=reconstruido) para que se pueda compartir;
// se lee con useSyncExternalStore y se escribe con replaceState, sin efectos.
//
// Desde el 2026-10-03 con el manual de Kaketiana (Vistas §03, Sistema §06): el
// filtro es la fila «TODO ▮ ◆ ◇ ~» de controles de 44px, la descripción de la
// capa aparece al elegirla, y cada voz va como forma del comparatista con su
// etiqueta cerrando la fila.

// El orden de la escala del manual: ▮ ◆ ◇ ~.
const ESCALA = ["atestiguado", "reconstruido", "hipotetico", "retroabstraido"] as const;

const DIACRITICOS = /[̀-ͯ]/g;

function inicial(forma: string): string {
  const ch = forma.normalize("NFD").replace(DIACRITICOS, "").match(/\p{L}/u);
  return ch ? ch[0].toUpperCase() : "·";
}

function sinAcentos(t: string): string {
  return t.normalize("NFD").replace(DIACRITICOS, "").toLowerCase();
}

const CLAVES = new Set<string>(CAPAS_EPISTEMICAS.map((c) => c.key));
const CAPA_PLURAL = Object.fromEntries(CAPAS_EPISTEMICAS.map((c) => [c.key, c.plural])) as Record<Capa, string>;

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

  const elegirTodo = () => {
    if (capa !== null) elegir(capa);
  };

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
      {/* El filtro: cómo sabemos cada palabra. La fila es la leyenda. */}
      <ul className="flex flex-wrap gap-2" aria-label="Filtrar por cómo la sabemos">
        <li>
          <button
            type="button"
            onClick={() => elegirTodo()}
            aria-pressed={capa === null}
            className={`sim-mono inline-flex min-h-11 cursor-pointer items-center rounded-[2px] border px-3.5 text-[0.62rem] uppercase tracking-[0.14em] transition-colors ${
              capa === null
                ? "border-(--sim-ink) bg-(--sim-ink) text-(--sim-paper)"
                : "border-(--sim-rule) text-(--sim-ink-soft) hover:border-(--sim-rubrica)"
            }`}
          >
            Todo · {fichas.length}
          </button>
        </li>
        {ESCALA.filter((c) => (conteo[c] ?? 0) > 0).map((c) => {
          const activa = capa === c;
          const grado = GRADO_DE_CAPA[c];
          return (
            <li key={c}>
              <button
                type="button"
                onClick={() => elegir(c)}
                aria-pressed={activa}
                className={`sim-mono inline-flex min-h-11 cursor-pointer items-center gap-2 rounded-[2px] border px-3.5 text-[0.62rem] uppercase tracking-[0.14em] transition-colors ${
                  activa
                    ? "border-(--sim-ink) bg-(--sim-ink) text-(--sim-paper)"
                    : "border-(--sim-rule) text-(--sim-ink-soft) hover:border-(--sim-rubrica)"
                }`}
              >
                <span aria-hidden="true">{glifoDe(grado)}</span>
                {CAPA_PLURAL[c]} · {conteo[c]}
              </button>
            </li>
          );
        })}
      </ul>
      {capa && capas[capa] && (
        <p className="mt-3 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
          <Etiqueta grado={GRADO_DE_CAPA[capa]} corta className="mr-2 align-[0.1em]" />
          {capas[capa]?.que_es}
        </p>
      )}

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
                    className="group flex min-h-11 items-baseline gap-3 py-2.5"
                  >
                    <FormaCaquetia
                      forma={f.forma}
                      capa={f.capa}
                      className="shrink-0 text-[1.1rem] underline decoration-transparent underline-offset-2 transition-colors group-hover:decoration-(--sim-fuego)"
                    />
                    <span className="min-w-0 flex-1 font-sans text-sm leading-snug text-(--sim-ink-soft)">
                      {f.glosa}
                    </span>
                    <Etiqueta grado={GRADO_DE_CAPA[f.capa]} corta className="shrink-0 self-center" />
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
