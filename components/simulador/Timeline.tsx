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
        className="sticky top-0 z-10 -mx-4 mb-8 flex items-center gap-1 overflow-x-auto border-b border-earth-200/70 bg-earth-50/90 px-4 py-2 backdrop-blur-sm sm:-mx-6 sm:px-6"
      >
        {epocas.map((e) => (
          <Link
            key={e.id}
            href={`/simulador#epoca-${e.id}`}
            className={`shrink-0 rounded-full px-3 py-1 font-sans text-xs transition-colors ${
              enPortada && activa === e.id
                ? "bg-deep-800 text-earth-50"
                : "text-earth-600 hover:text-deep-800"
            }`}
          >
            <span className="tabular-nums">
              D{e.dias[0]}–{e.dias[1]}
            </span>{" "}
            {e.titulo}
          </Link>
        ))}
        <span className="mx-1 shrink-0 text-earth-300">·</span>
        {ANEXOS.map((a) => (
          <Link
            key={a.href}
            href={a.href}
            className={`shrink-0 rounded-full px-3 py-1 font-sans text-xs transition-colors ${
              pathname?.startsWith(a.href) ? "bg-earth-200/80 text-deep-800" : "text-earth-600 hover:text-deep-800"
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
      <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-earth-600">
        Cronología
      </span>
      <p className="mt-1 font-serif text-sm italic text-earth-700">{runTitulo}</p>

      <ol className="mt-4 border-l border-earth-200">
        {epocas.map((e) => {
          const esActiva = enPortada && activa === e.id;
          return (
            <li key={e.id} className="relative pl-4 pb-5 last:pb-0">
              <span
                aria-hidden="true"
                className={`absolute -left-[4.5px] top-1.5 h-2 w-2 rounded-full transition-colors ${
                  esActiva ? "bg-frequency" : "bg-earth-300"
                }`}
              />
              <Link href={`/simulador#epoca-${e.id}`} className="group block">
                <span className="font-sans text-[0.7rem] tabular-nums uppercase tracking-wide text-earth-500">
                  Días {e.dias[0]}–{e.dias[1]}
                </span>
                <span
                  className={`block font-serif text-sm leading-snug transition-colors ${
                    esActiva ? "text-deep-900 font-semibold" : "text-earth-700 group-hover:text-deep-800"
                  }`}
                >
                  {e.titulo}
                </span>
                {e.hito && (
                  <span className="mt-0.5 block font-sans text-xs leading-snug text-earth-500">{e.hito}</span>
                )}
              </Link>
            </li>
          );
        })}
      </ol>

      <div className="mt-8 border-t border-earth-200/70 pt-4">
        <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-earth-600">
          Anexos
        </span>
        <ul className="mt-2 flex flex-col gap-1.5">
          {ANEXOS.map((a) => (
            <li key={a.href}>
              <Link
                href={a.href}
                className={`font-sans text-sm transition-colors ${
                  pathname?.startsWith(a.href)
                    ? "text-deep-900 font-medium"
                    : "text-earth-600 hover:text-deep-800"
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
