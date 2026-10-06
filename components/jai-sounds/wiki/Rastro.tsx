"use client";

import Link from "next/link";
import { useEffect, useLayoutEffect, useRef, useState, useSyncExternalStore, type CSSProperties } from "react";
import {
  guardarRastro,
  hrefDe,
  leerRastro,
  suscribirRastro,
  visitar,
  type PuntoRastro,
} from "@/lib/jai-rastro";

const TIPO = { estacion: "est", cancion: "can", album: "alb", artista: "art" } as const;

// leerRastro devuelve un array nuevo cada vez: se cachea por su texto para
// que useSyncExternalStore no vea un cambio en cada render.
let ultimoTexto = "";
let ultimo: PuntoRastro[] = [];
function instantanea(): PuntoRastro[] {
  const r = leerRastro();
  const t = JSON.stringify(r);
  if (t !== ultimoTexto) {
    ultimoTexto = t;
    ultimo = r;
  }
  return ultimo;
}
const vacio: PuntoRastro[] = [];

/**
 * El rastro: el camino de la sesión, fijo bajo la consola. Visitar la
 * página la suma al camino (o vuelve a ella si ya estaba). Más de seis
 * migas se pliegan: la primera, «··· +n» y las tres últimas.
 */
export default function Rastro({ punto }: { punto: PuntoRastro }) {
  const r = useSyncExternalStore(suscribirRastro, instantanea, () => vacio);
  const [abierto, setAbierto] = useState(false);
  const lista = useRef<HTMLOListElement>(null);

  // Llegar aquí es un paso del camino (en sessionStorage, no en el estado).
  const { tipo, slug, n, e } = punto;
  useEffect(() => {
    visitar({ tipo, slug, n, ...(e !== undefined ? { e } : {}) });
  }, [tipo, slug, n, e]);

  // Siempre anclado al final: la miga actual a la vista.
  useLayoutEffect(() => {
    const el = lista.current;
    if (el) el.scrollLeft = el.scrollWidth;
  }, [r, abierto]);

  const migas: ({ p: PuntoRastro; k: number } | { pliegue: number })[] =
    r.length > 6 && !abierto
      ? [{ p: r[0], k: 0 }, { pliegue: r.length - 4 }, ...r.slice(-3).map((p, j) => ({ p, k: r.length - 3 + j }))]
      : r.map((p, k) => ({ p, k }));
  const saltos = r.length > 1 ? `${r.length - 1} ${r.length === 2 ? "salto" : "saltos"}` : "empieza aquí";

  return (
    <nav aria-label="Rastro" className="sticky top-0 z-20 border-b border-(--jai-rule) bg-(--jai-noche)">
      <div className="mx-auto flex min-h-12 max-w-[1120px] items-stretch gap-4 px-[clamp(16px,4vw,32px)]">
        <span className="jai-dato flex shrink-0 items-center text-[10px] text-(--jai-luz-faint)">rastro</span>
        <ol ref={lista} className="m-0 flex min-w-0 flex-1 list-none items-stretch overflow-x-auto p-0 [scrollbar-width:none]">
          {migas.map((m, j) => (
            <li key={"pliegue" in m ? "pliegue" : `${m.p.tipo}:${m.p.slug}`} className="flex shrink-0 items-center">
              {j > 0 ? (
                <span aria-hidden className="px-2.5 font-(family-name:--jai-mono) text-[11px] text-(--jai-rule)">
                  →
                </span>
              ) : null}
              {"pliegue" in m ? (
                <button
                  onClick={() => setAbierto(true)}
                  className="border border-(--jai-rule) px-2 py-1 font-(family-name:--jai-mono) text-[10px] tracking-[0.2em] text-(--jai-luz-faint) transition-colors duration-300 hover:border-(--jai-luz-faint) hover:text-(--jai-luz)"
                >
                  ··· +{m.pliegue}
                </button>
              ) : (
                <Miga p={m.p} actual={m.k === r.length - 1} />
              )}
            </li>
          ))}
        </ol>
        <div className="jai-dato flex shrink-0 items-center gap-3.5 text-[10px] text-(--jai-luz-faint)">
          <span className="hidden sm:inline">{saltos}</span>
          <button
            onClick={() => guardarRastro([punto])}
            title="Empezar el rastro de nuevo desde aquí"
            className="py-1.5 transition-colors duration-300 hover:text-(--jai-luz)"
          >
            ↺ de nuevo
          </button>
        </div>
      </div>
    </nav>
  );
}

function Miga({ p, actual }: { p: PuntoRastro; actual: boolean }) {
  const estacion = p.tipo === "estacion";
  return (
    <Link
      href={hrefDe(p)}
      aria-current={actual ? "page" : undefined}
      className={`flex items-baseline gap-[7px] border-b py-1 transition-colors duration-300 hover:text-(--jai-luz) ${estacion ? "jai-estacion border-l-3 border-l-(--jai-senal) pl-2" : ""} ${actual ? "border-b-(--jai-senal) text-(--jai-luz)" : "border-b-transparent text-(--jai-luz-soft)"}`}
      style={estacion ? ({ "--jai-i": p.e ?? 0 } as CSSProperties) : undefined}
    >
      <span className="font-(family-name:--jai-mono) text-[9px] tracking-[0.2em] text-(--jai-luz-faint)">{TIPO[p.tipo]}</span>
      <span className="max-w-[24ch] truncate text-[13px]">{p.n}</span>
    </Link>
  );
}
