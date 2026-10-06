"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import type { ResumenEstacion } from "@/lib/jai-wiki";

/** Cuántos discos asoman detrás del de frente. */
const ATRAS = 6;
/** Cada disco de atrás sube un 9% y se achica un 3.5%: asoma un lomo de 5.5%. */
const PASO = 9;
const ESC = 0.035;
/** Alto de la batea respecto del ancho: el disco + los lomos (+2%). */
export const PROPORCION = 1 + ATRAS * (PASO / 100) - ATRAS * ESC + 0.02;

/**
 * La batea: los 23 discos apilados, el de frente entero y seis de atrás
 * asomando el lomo. Pasar → hace caer el de frente hacia adelante con
 * aceleración de gravedad; ← lo levanta. El dedo arrastra el disco.
 */
export default function Pila({
  estaciones,
  actual,
  ir,
  quieto,
}: {
  estaciones: ResumenEstacion[];
  actual: number;
  ir: (k: number) => void;
  quieto: boolean;
}) {
  const N = estaciones.length;
  const caja = useRef<HTMLDivElement>(null);
  const [encima, setEncima] = useState<number | null>(null);
  const [dx, setDx] = useState<number | null>(null);
  const gesto = useRef<{ x: number; y: number; id: number; decidido: boolean } | null>(null);
  const reciente = useRef(0);

  // La rueda pasa discos solo sobre la batea, y solo ahí se le quita el
  // scroll a la página. Acumula hasta 40 y se bloquea 420 ms: un giro, un disco.
  useEffect(() => {
    const el = caja.current;
    if (!el) return;
    let acumulado = 0;
    let bloqueo = 0;
    const rueda = (e: WheelEvent) => {
      e.preventDefault();
      const ahora = Date.now();
      if (ahora < bloqueo) return;
      acumulado += Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (Math.abs(acumulado) > 40) {
        ir(actual + Math.sign(acumulado));
        acumulado = 0;
        bloqueo = ahora + 420;
      }
    };
    el.addEventListener("wheel", rueda, { passive: false });
    return () => el.removeEventListener("wheel", rueda);
  }, [actual, ir]);

  const bajar = (e: React.PointerEvent) => {
    gesto.current = { x: e.clientX, y: e.clientY, id: e.pointerId, decidido: false };
  };
  const mover = (e: React.PointerEvent) => {
    const g = gesto.current;
    if (!g) return;
    const ddx = e.clientX - g.x;
    const ddy = e.clientY - g.y;
    if (!g.decidido) {
      // 8 px para decidir el eje: lo vertical es del scroll de la página.
      if (Math.abs(ddx) > 8 && Math.abs(ddx) > Math.abs(ddy)) {
        g.decidido = true;
        try {
          (e.currentTarget as HTMLElement).setPointerCapture(g.id);
        } catch {}
      } else if (Math.abs(ddy) > 8) {
        gesto.current = null;
        return;
      } else return;
    }
    setDx(ddx);
  };
  const soltar = () => {
    gesto.current = null;
    if (dx === null) return;
    reciente.current = Date.now();
    if (dx < -60) ir(actual + 1);
    else if (dx > 60) ir(actual - 1);
    setDx(null);
  };

  return (
    <div
      ref={caja}
      onPointerDown={bajar}
      onPointerMove={mover}
      onPointerUp={soltar}
      onPointerCancel={soltar}
      className="relative w-full select-none [perspective:1600px] [perspective-origin:50%_0%] [touch-action:pan-y]"
      style={{ aspectRatio: `1 / ${PROPORCION.toFixed(3)}` }}
    >
      {estaciones.map((e, k) => {
        const d = (k - actual + N) % N;
        // -1: el que acaba de caer; 0: el de frente; 1-6: lomos; 7: fuera.
        const puesto = d <= ATRAS ? d : d === N - 1 ? -1 : ATRAS + 1;
        const lomo = puesto > 0 && puesto <= ATRAS;
        let transform: string;
        let transition: string;
        let opacity = 1;
        let brillo = 1;
        if (puesto === -1) {
          transform = "translateY(3%) rotateX(-86deg)";
          opacity = 0;
          transition = "transform 420ms cubic-bezier(.55,0,.9,.45), opacity 420ms cubic-bezier(.8,0,1,1)";
        } else {
          const sube = encima === k && lomo ? 2.4 : 0;
          transform = `translateY(${-(puesto * PASO + sube)}%) scale(${1 - puesto * ESC})`;
          if (puesto > ATRAS) opacity = 0;
          brillo = 1 - puesto * 0.1 + (sube ? 0.12 : 0);
          transition = "transform 460ms cubic-bezier(.3,.7,.2,1), opacity 300ms ease, filter 300ms ease";
        }
        if (puesto === 0 && dx !== null) {
          transform = `translateX(${dx}px) rotate(${dx * 0.012}deg)`;
          transition = "none";
        }
        if (quieto) transition = "none";
        return (
          <div
            key={e.slug}
            aria-hidden={puesto !== 0 || undefined}
            onClick={lomo ? () => Date.now() - reciente.current > 250 && ir(k) : undefined}
            onMouseEnter={lomo ? () => setEncima(k) : undefined}
            onMouseLeave={lomo ? () => setEncima(null) : undefined}
            className="jai-estacion absolute inset-x-0 bottom-0 box-border aspect-square border-l-3 border-t border-l-(--jai-senal) border-t-[rgba(241,236,226,0.3)] bg-(--jai-senal-tenue) will-change-transform"
            style={
              {
                "--jai-i": k,
                transformOrigin: "50% 100%",
                transform,
                transition,
                opacity,
                zIndex: puesto === -1 ? 40 : 30 - puesto,
                filter: `brightness(${brillo})`,
                cursor: lomo ? "pointer" : puesto === 0 ? (dx !== null ? "grabbing" : "grab") : "default",
                pointerEvents: puesto < 0 || puesto > ATRAS ? "none" : "auto",
              } as CSSProperties
            }
          >
            {e.portada ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={e.portada}
                alt={puesto === 0 ? `Portada de ${e.nombre}` : ""}
                draggable={false}
                loading={Math.abs(d) <= ATRAS + 1 || d === N - 1 ? "eager" : "lazy"}
                className="pointer-events-none absolute inset-0 block h-full w-full object-cover"
              />
            ) : null}
            {lomo ? (
              <div
                className="absolute inset-x-0 top-0 box-border flex items-center gap-2.5 overflow-hidden whitespace-nowrap bg-[rgba(11,17,25,0.8)] px-3 font-(family-name:--jai-mono) text-[11px] lowercase tracking-[0.18em]"
                style={{ height: `${(PASO - ESC * 100) / (1 - puesto * ESC)}%` }}
              >
                <span className="text-(--jai-senal)">{String(k + 1).padStart(2, "0")}</span>
                <span className="overflow-hidden text-ellipsis text-(--jai-luz-soft)">{e.nombre}</span>
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
