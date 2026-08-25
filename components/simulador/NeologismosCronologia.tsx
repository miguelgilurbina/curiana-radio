"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import type { Neologismo } from "@/lib/neologismos";
import { Avatar, LangPill, EmptyState } from "@/components/simulador/ui";
import { NEO_STATUS } from "@/lib/sim-theme";

// Diccionario cronológico de neologismos: la fecha de acuñación ordena la
// lectura (no el score). Entradas fusionadas por forma — una misma palabra
// puede haberse glosado de dos maneras (ej. kali-bana-chaa) y ambas son
// acepciones de la misma entrada, como en un diccionario de verdad.

interface Entrada {
  form: string;
  dia: number; // primera acuñación
  status: Neologismo["status"];
  proposedBy: string;
  acepciones: Neologismo[];
  adoptadoPor: string[];
  quotes: { quote: string; traduccion: string; agente: string; agente_slug: string }[];
}

function agrupar(neologismos: Neologismo[]): Entrada[] {
  const porForma = new Map<string, Neologismo[]>();
  for (const n of neologismos) {
    porForma.set(n.form, [...(porForma.get(n.form) ?? []), n]);
  }
  return [...porForma.entries()]
    .map(([form, acepciones]) => {
      // Estado "mayor" de la entrada: adoptado gana sobre propuesto.
      const status =
        acepciones.find((a) => a.status === "adoptado")?.status ?? acepciones[0].status;
      const vistos = new Set<string>();
      const quotes = acepciones
        .filter((a) => a.destacado)
        .map((a) => a.destacado!)
        .filter((d) => {
          if (vistos.has(d.quote)) return false;
          vistos.add(d.quote);
          return true;
        });
      return {
        form,
        dia: Math.min(...acepciones.map((a) => a.proposed_day)),
        status,
        proposedBy: acepciones[0].proposed_by,
        acepciones,
        adoptadoPor: [...new Set(acepciones.flatMap((a) => a.adopted_by ?? []))],
        quotes,
      };
    })
    .sort((a, b) => a.dia - b.dia || a.form.localeCompare(b.form));
}

export default function NeologismosCronologia({
  neologismos,
  slugPorNombre,
}: {
  neologismos: Neologismo[];
  slugPorNombre: Record<string, string>;
}) {
  const [statusFilter, setStatusFilter] = useState<"todos" | Neologismo["status"]>("todos");

  const entradas = useMemo(() => agrupar(neologismos), [neologismos]);
  const statusPresentes = [...new Set(entradas.map((e) => e.status))].sort();
  const filtradas =
    statusFilter === "todos" ? entradas : entradas.filter((e) => e.status === statusFilter);

  // Secciones por día de acuñación — la cronología manda.
  const dias = [...new Set(filtradas.map((e) => e.dia))].sort((a, b) => a - b);

  return (
    <div>
      <div className="mb-6 flex flex-wrap gap-2">
        {(["todos", ...statusPresentes] as const).map((s) => {
          const count = s === "todos" ? entradas.length : entradas.filter((e) => e.status === s).length;
          const color = s === "todos" ? "#C47A2B" : NEO_STATUS[s].color;
          const active = statusFilter === s;
          return (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className="rounded-full border px-3 py-1.5 font-sans text-sm transition-colors"
              style={{
                background: active ? `${color}1a` : "transparent",
                borderColor: active ? color : "var(--sim-rule)",
                color: active ? color : "var(--sim-ink-soft)",
              }}
            >
              {s} · {count}
            </button>
          );
        })}
      </div>

      {filtradas.length === 0 ? (
        <EmptyState title="Sin neologismos con ese filtro" />
      ) : (
        dias.map((dia) => (
          <section key={dia} className="mt-8 first:mt-0">
            <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-(--sim-rubrica)">
              Día {dia}
            </span>
            <div className="mt-1 border-l border-(--sim-rule)">
              {filtradas
                .filter((e) => e.dia === dia)
                .map((e) => {
                  const st = NEO_STATUS[e.status] ?? NEO_STATUS.propuesto;
                  const slug = slugPorNombre[e.proposedBy];
                  return (
                    <article key={e.form} className="relative py-5 pl-5 md:pl-7">
                      <span
                        aria-hidden="true"
                        className="absolute -left-[4.5px] top-7 h-2 w-2 rounded-full"
                        style={{ background: st.color }}
                      />
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                        <h3 className="sim-display text-2xl font-semibold text-(--sim-fuego)">{e.form}</h3>
                        <LangPill color={st.color}>{st.label}</LangPill>
                      </div>

                      <div className="mt-1.5 flex items-center gap-1.5 font-sans text-xs text-(--sim-ink-faint)">
                        <span>acuñó</span>
                        {slug ? (
                          <Link
                            href={`/kaketiana/personajes/${slug}`}
                            className="inline-flex items-center gap-1 text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
                          >
                            <Avatar name={e.proposedBy} size={18} />
                            {e.proposedBy}
                          </Link>
                        ) : (
                          <span className="inline-flex items-center gap-1">
                            <Avatar name={e.proposedBy} size={18} />
                            {e.proposedBy}
                          </span>
                        )}
                      </div>

                      <ol className="mt-3 flex flex-col gap-2">
                        {e.acepciones.map((a, i) => (
                          <li key={a.id} className="max-w-reading">
                            <p className="font-sans text-[0.95rem] leading-relaxed text-(--sim-ink)">
                              {e.acepciones.length > 1 && (
                                <span className="mr-1.5 font-serif font-semibold text-(--sim-ink-faint)">{i + 1}.</span>
                              )}
                              {a.meaning}
                            </p>
                            {a.components && (
                              <p className="mt-0.5 font-sans text-xs text-(--sim-ink-faint)">
                                {a.components}
                                {a.morphological_rule && a.morphological_rule !== "desconocida" && (
                                  <span> · regla {a.morphological_rule}</span>
                                )}
                              </p>
                            )}
                          </li>
                        ))}
                      </ol>

                      {e.adoptadoPor.length > 0 && (
                        <p className="mt-2 font-sans text-xs text-(--sim-ink-faint)">
                          la adoptaron: {e.adoptadoPor.join(", ")}
                        </p>
                      )}

                      {e.quotes.map((q) => (
                        <blockquote key={q.quote} className="mt-3 border-l-[3px] border-(--sim-fuego)/60 pl-3">
                          <p className="font-serif text-base italic leading-snug text-(--sim-ink)">{q.quote}</p>
                          {q.traduccion && (
                            <p className="mt-1 font-sans text-xs leading-relaxed text-(--sim-ink-soft)">{q.traduccion}</p>
                          )}
                          <Link
                            href={`/kaketiana/personajes/${q.agente_slug}`}
                            className="mt-1 inline-block font-sans text-xs text-(--sim-ink-faint) transition-colors hover:text-(--sim-fuego)"
                          >
                            — {q.agente}
                          </Link>
                        </blockquote>
                      ))}
                    </article>
                  );
                })}
            </div>
          </section>
        ))
      )}
    </div>
  );
}
