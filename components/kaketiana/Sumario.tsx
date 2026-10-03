"use client";

import { useEffect, useId, useState, type ReactNode } from "react";
import type { SeccionDelArticulo } from "@/lib/articulo";

// El sumario del ensayo, del manual de Kaketiana (Vistas §02 y Sistema §06).
// En escritorio es la columna de 230px: «EN ESTE ARTÍCULO · N», la lista con
// filete a la izquierda y la sección donde está el lector en rúbrica, con la
// Rúbrica (subrayado almagre). Muestra las primeras ocho y «… N secciones
// más», que el lector abre si quiere. En móvil se pliega a una barra sobre el
// texto, «EN ESTE ARTÍCULO · N ▾», con un botón de 44px. Debajo, en
// escritorio, lo que el artículo mide de sí mismo (los children).
//
// `plegado`: la obra de consulta (la lengua, Vistas §03) va a ancho completo
// y sin columna lateral, así que el sumario es la barra plegada en todos los
// tamaños; abierta, en dos columnas desde 640px.

const VISIBLES = 8;

export default function Sumario({
  secciones,
  plegado = false,
  children,
}: {
  secciones: SeccionDelArticulo[];
  plegado?: boolean;
  children?: ReactNode;
}) {
  const [actual, setActual] = useState<string | null>(null);
  const [todas, setTodas] = useState(false);
  const [abierto, setAbierto] = useState(false);
  const idLista = useId();
  const idMovil = useId();

  // La sección actual: el último título que ya pasó el primer tercio de la
  // pantalla. Se mide por cuadro de animación, no por cada evento de scroll.
  useEffect(() => {
    const titulos = secciones
      .map((s) => document.getElementById(s.id))
      .filter((t): t is HTMLElement => t !== null);
    if (titulos.length === 0) return;
    let cuadro = 0;
    const medir = () => {
      cuadro = 0;
      const linea = window.innerHeight * 0.3;
      let ultima: string | null = null;
      for (const t of titulos) {
        if (t.getBoundingClientRect().top > linea) break;
        ultima = t.id;
      }
      setActual(ultima);
    };
    const alMover = () => {
      if (!cuadro) cuadro = requestAnimationFrame(medir);
    };
    medir();
    window.addEventListener("scroll", alMover, { passive: true });
    window.addEventListener("resize", alMover);
    return () => {
      window.removeEventListener("scroll", alMover);
      window.removeEventListener("resize", alMover);
      cancelAnimationFrame(cuadro);
    };
  }, [secciones]);

  if (secciones.length === 0) return children ? <div className="hidden lg:block">{children}</div> : null;

  const indiceActual = secciones.findIndex((s) => s.id === actual);
  // Si el lector ya bajó más allá de las ocho, la lista se abre sola: la
  // sección en que está no puede quedar escondida.
  const verTodas = todas || indiceActual >= VISIBLES;
  const resto = secciones.length - VISIBLES;

  // En móvil cada entrada es un control de 44px y la actual va sólo en
  // rúbrica: la Rúbrica (el subrayado) cruzaría la fila entera.
  const entrada = (s: SeccionDelArticulo, alElegir?: () => void) => {
    const esActual = s.id === actual;
    const movil = Boolean(alElegir);
    return (
      <li key={s.id}>
        <a
          href={`#${s.id}`}
          onClick={alElegir}
          aria-current={esActual ? "location" : undefined}
          data-actual={esActual ? "" : undefined}
          className={`${movil ? "flex min-h-11 items-center" : "kk-sumario-enlace"} transition-colors duration-300 hover:text-(--sim-rubrica) ${
            esActual ? "font-medium text-(--sim-rubrica)" : "text-(--sim-ink-soft)"
          }`}
        >
          {s.texto}
        </a>
      </li>
    );
  };

  return (
    <>
      {/* < 1024px (o siempre, si va plegado): la barra, a sangre completa en móvil */}
      <div
        className={`-mx-4 border-b border-(--sim-rule) bg-(--sim-paper-deep) sm:-mx-6 ${
          plegado ? "lg:mx-0 lg:border-x lg:border-t" : "lg:hidden"
        }`}
      >
        <button
          type="button"
          aria-expanded={abierto}
          aria-controls={idMovil}
          onClick={() => setAbierto((a) => !a)}
          className="flex min-h-11 w-full cursor-pointer items-center justify-between px-4 text-left sm:px-6"
        >
          <span className="kk-label text-[0.6rem] tracking-[0.18em] text-(--sim-ink-soft)">
            En este artículo · {secciones.length}
          </span>
          <span aria-hidden="true" className="sim-mono text-[0.7rem] text-(--sim-rubrica)">
            {abierto ? "▴" : "▾"}
          </span>
        </button>
        <ol
          id={idMovil}
          hidden={!abierto}
          className={`kk-desplegable-cuerpo flex flex-col border-t border-(--sim-rule) px-4 py-2 text-[0.85rem] leading-snug sm:px-6 ${
            plegado ? "sm:grid sm:grid-cols-2 sm:gap-x-8" : ""
          }`}
        >
          {secciones.map((s) => entrada(s, () => setAbierto(false)))}
        </ol>
      </div>

      {/* ≥ 1024px: la columna (no en la obra de consulta) */}
      <div className={plegado ? "hidden" : "hidden flex-col gap-2.5 lg:flex"}>
        <p className="kk-label text-[0.58rem] tracking-[0.22em] text-(--sim-ink-soft)">
          En este artículo · {secciones.length}
        </p>
        <ol
          id={idLista}
          className="flex flex-col gap-[7px] border-l-2 border-(--sim-rule) pl-3.5 text-[0.76rem] leading-snug"
        >
          {(verTodas ? secciones : secciones.slice(0, VISIBLES)).map((s) => entrada(s))}
          {resto > 0 && !verTodas && (
            <li>
              <button
                type="button"
                aria-expanded={false}
                aria-controls={idLista}
                onClick={() => setTodas(true)}
                className="cursor-pointer text-left text-(--sim-ink-soft) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:text-(--sim-rubrica)"
              >
                … {resto} {resto === 1 ? "sección más" : "secciones más"}
              </button>
            </li>
          )}
        </ol>
        {children && <div className="mt-[18px]">{children}</div>}
      </div>
    </>
  );
}
