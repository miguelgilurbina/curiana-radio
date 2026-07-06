"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

// Cronología del run activo: la navegación primaria de la wiki narrativa.
// El lector avanza en el tiempo de la simulación, no en una taxonomía.
// Desktop: sidebar vertical sticky. Mobile: barra horizontal sticky.
// Los anexos (antes SubNav) quedan como navegación secundaria al pie.

export interface TimelineEpoca {
  id: string;
  titulo: string;
  dias: [number, number];
  hito?: string;
}

const ANEXOS = [
  { href: "/simulador/personajes", label: "Personajes" },
  { href: "/simulador/lexicon", label: "Léxico" },
  { href: "/simulador/neologisms", label: "Neologismos" },
];

function useEpocaActiva(epocas: TimelineEpoca[], enabled: boolean): string | null {
  const [activa, setActiva] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) setActiva(entry.target.id.replace("epoca-", ""));
        }
      },
      // banda de lectura: una época se activa cuando su sección cruza el
      // tercio superior del viewport
      { rootMargin: "-20% 0px -65% 0px" }
    );
    for (const e of epocas) {
      const el = document.getElementById(`epoca-${e.id}`);
      if (el) observer.observe(el);
    }
    return () => observer.disconnect();
  }, [epocas, enabled]);

  return activa;
}

export default function Timeline({
  runTitulo,
  epocas,
  variant,
}: {
  runTitulo: string;
  epocas: TimelineEpoca[];
  variant: "sidebar" | "bar";
}) {
  const pathname = usePathname();
  const enPortada = pathname === "/simulador";
  const activa = useEpocaActiva(epocas, enPortada);

  if (variant === "bar") {
    return (
      <nav
        aria-label="Cronología del run"
        className="sticky top-0 z-10 -mx-4 mb-8 flex items-center gap-1 overflow-x-auto border-b border-(--sim-rule) bg-(--sim-paper-deep) px-4 py-2 backdrop-blur-sm sm:-mx-6 sm:px-6"
      >
        {epocas.map((e) => (
          <Link
            key={e.id}
            href={`/simulador#epoca-${e.id}`}
            className={`shrink-0 rounded-full px-3 py-1 font-sans text-xs transition-colors ${
              enPortada && activa === e.id
                ? "bg-(--sim-ink) text-(--sim-paper)"
                : "text-(--sim-ink-soft) hover:text-(--sim-ink)"
            }`}
          >
            <span className="tabular-nums">
              D{e.dias[0]}–{e.dias[1]}
            </span>{" "}
            {e.titulo}
          </Link>
        ))}
        <span className="mx-1 shrink-0 text-(--sim-rule)">·</span>
        {ANEXOS.map((a) => (
          <Link
            key={a.href}
            href={a.href}
            className={`shrink-0 rounded-full px-3 py-1 font-sans text-xs transition-colors ${
              pathname?.startsWith(a.href) ? "bg-(--sim-rule) text-(--sim-ink)" : "text-(--sim-ink-soft) hover:text-(--sim-ink)"
            }`}
          >
            {a.label}
          </Link>
        ))}
      </nav>
    );
  }

  return (
    <nav aria-label="Cronología del run" className="sticky top-8">
      <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-(--sim-rubrica)">
        Cronología
      </span>
      <p className="mt-1 font-serif text-sm italic text-(--sim-ink-soft)">{runTitulo}</p>

      <ol className="mt-4 border-l border-(--sim-rule)">
        {epocas.map((e) => {
          const esActiva = enPortada && activa === e.id;
          return (
            <li key={e.id} className="relative pl-4 pb-5 last:pb-0">
              <span
                aria-hidden="true"
                className={`absolute -left-[4.5px] top-1.5 h-2 w-2 rounded-full transition-colors ${
                  esActiva ? "bg-(--sim-rubrica)" : "bg-(--sim-rule)"
                }`}
              />
              <Link href={`/simulador#epoca-${e.id}`} className="group block">
                <span className="font-sans text-[0.7rem] tabular-nums uppercase tracking-wide text-(--sim-ink-faint)">
                  Días {e.dias[0]}–{e.dias[1]}
                </span>
                <span
                  className={`block font-serif text-sm leading-snug transition-colors ${
                    esActiva ? "text-(--sim-ink) font-semibold" : "text-(--sim-ink-soft) group-hover:text-(--sim-ink)"
                  }`}
                >
                  {e.titulo}
                </span>
                {e.hito && (
                  <span className="mt-0.5 block font-sans text-xs leading-snug text-(--sim-ink-faint)">{e.hito}</span>
                )}
              </Link>
            </li>
          );
        })}
      </ol>

      <div className="mt-8 border-t border-(--sim-rule) pt-4">
        <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-(--sim-rubrica)">
          Anexos
        </span>
        <ul className="mt-2 flex flex-col gap-1.5">
          {ANEXOS.map((a) => (
            <li key={a.href}>
              <Link
                href={a.href}
                className={`font-sans text-sm transition-colors ${
                  pathname?.startsWith(a.href)
                    ? "text-(--sim-ink) font-medium"
                    : "text-(--sim-ink-soft) hover:text-(--sim-ink)"
                }`}
              >
                {a.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
