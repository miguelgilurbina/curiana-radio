"use client";

import { useEffect, useRef, useState, useSyncExternalStore, type CSSProperties, type KeyboardEvent, type PointerEvent } from "react";
import Link from "next/link";
import { Cartel } from "@/components/ui/Typography";
import { LIBERADA, type Seccion } from "@/lib/secciones";
import { medir, type AristaMedida } from "@/lib/analitica";

// 01 · Hero: el carrusel de aristas (BRAND_MVP §10). La intro ya obligó a
// interactuar, así que aquí no hay "gira la espiral": el hero arranca
// sintonizado y pasa solo de una arista a la otra (Miguel, 2026-10-08: en el
// móvil ocupa toda la pantalla y las otras aristas quedaban detrás de un
// gesto). Cada cambio es una vuelta del dial: la aguja barre la pista en el
// sentido del cambio, detrás de ella amanece la superficie de la arista que
// entra (la noche, la sal de Kaketiana, la noche de JAI) y su texto entra en
// tinta, línea por línea. El punto activo se llena con el tiempo que le queda
// al aire; cuando se llena, cambia.
//
// Se pausa con el ratón encima, con el foco de teclado dentro y con la
// pestaña oculta; tocarlo en el móvil o el botón PAUSA lo detienen hasta
// SEGUIR. Con movimiento reducido no avanza solo (el CSS no llena el punto) y
// el cambio es un fundido de 200 ms; flechas, puntos, teclado y deslizar
// siguen funcionando. La primera diapositiva llega en el HTML tal como se ve:
// sin barrido ni entrada.

// la mono del sistema (Tailwind: ui-monospace, Menlo, Consolas…), como el DS
const MONO = "font-mono";
/** lo que cada arista se queda al aire antes de pasar a la siguiente */
const CICLO_MS = 7000;

interface Cta {
  texto: string;
  /** null: la sección se anuncia pero no se abre (Buchibe) */
  href: string | null;
  clase: string;
}

interface Diapositiva {
  /** la sección que anuncia: sale sólo si está al aire (lib/secciones.ts) */
  seccion?: Seccion;
  /** a qué arista lleva su CTA: data-arista y el evento «arista» */
  arista: AristaMedida;
  nombre: string; // para la etiqueta "0X / 0N · NOMBRE"
  frecuencia: string;
  titulo: string;
  bajada: string;
  cta: Cta;
  /** superficie: tema de sección + fondo */
  tema: Record<string, string>;
  clase: string;
  estilo?: CSSProperties;
  claseFrecuencia: string;
  claseBajada: string;
}

function diapositivas(edicion: { numero: string; slug: string }): Diapositiva[] {
  const enlaceMono = `${MONO} text-[0.72rem] tracking-[0.16em] transition-colors duration-300 hover:text-(--noche-acento)`;
  // el orden alterna las superficies: la noche → la sal → la noche de JAI
  const todas: Diapositiva[] = [
    {
      arista: "radio",
      nombre: "LA RADIO",
      frecuencia: "88.8 · EL MARCO",
      titulo: "La Radio",
      bajada: "Emitimos desde una Paraguaná paralela, después del Renacimiento de La Curiana.",
      // con el archivo en el taller, sintonizar es entrar a la radio (el
      // manifiesto), no a una edición
      cta: {
        texto: LIBERADA.archivo ? `Sintonizar #${edicion.numero} →` : "Sintonizar →",
        href: LIBERADA.archivo ? `/${edicion.slug}` : "#manifiesto",
        clase:
          "mt-1.5 self-start rounded-[2px] bg-(--noche-acento) px-7 py-[15px] text-[0.78rem] font-semibold uppercase tracking-[0.2em] whitespace-nowrap text-(--noche-fondo) transition-colors duration-300 hover:bg-(--noche-hueso) hover:text-(--noche-fondo)",
      },
      tema: {},
      clase: "noche-gradiente",
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--noche-hueso-2)`,
      claseBajada: "font-serif italic text-lg leading-relaxed text-(--noche-hueso-2) max-w-[44ch]",
    },
    {
      seccion: "kaketiana",
      arista: "kaketiana",
      nombre: "KAKETIANA",
      frecuencia: "88.3 · Golfete de Coro · s. XIV–XV",
      titulo: "Kaketiana",
      bajada: "El pueblo caquetío del Golfete de Coro y su lengua, reconstruidos con cada fuente a la vista.",
      cta: { texto: "ENTRAR A KAKETIANA →", href: "/kaketiana", clase: `${enlaceMono} text-(--sim-ink)` },
      // la placa 6b «Sal y almagre» de Kaketiana (BRAND_MVP §11), no el pergamino del Simulador
      tema: { "data-sim-theme": "cronista", "data-kk-dir": "sal" },
      clase: "bg-(--sim-paper)",
      claseFrecuencia: "text-[0.64rem] font-medium uppercase tracking-[0.2em] text-(--sim-rubrica)",
      claseBajada: "text-base leading-relaxed text-(--sim-ink-soft) max-w-[46ch]",
    },
    {
      seccion: "jai-sounds",
      arista: "jai-sounds",
      nombre: "JAI SOUNDS",
      frecuencia: "88.1 · jai · caquetío · oír, escuchar",
      titulo: "JAI Sounds",
      bajada: "La cabina de noche. Cinco pistas por emisión, reseñadas al oído; el dial rota su matiz con cada visita.",
      cta: { texto: "ENTRAR AL DIAL →", href: "/jai-sounds", clase: `${enlaceMono} text-(--jai-luz)` },
      tema: { "data-jai-theme": "dial" },
      clase: "bg-(--jai-noche)",
      estilo: { "--jai-hue": "212" } as CSSProperties,
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--jai-luz-soft)`,
      claseBajada: "text-base leading-relaxed text-(--jai-luz-soft) max-w-[46ch]",
    },
    {
      seccion: "galeria",
      arista: "galeria",
      nombre: "GALERÍA",
      frecuencia: "88.5 · LA SALA NEUTRA",
      titulo: "Galería · Prompt Maker",
      bajada: "Cientos de visiones curadas. El prompt es código y se publica a la vista.",
      cta: { texto: "RECORRER LA SALA →", href: "/galeria", clase: `${enlaceMono} text-(--gal-luz)` },
      tema: { "data-galeria-theme": "sala" },
      clase: "bg-(--gal-sala)",
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--gal-luz-soft)`,
      claseBajada: "text-base leading-relaxed text-(--gal-luz-soft) max-w-[46ch]",
    },
    {
      seccion: "buchibe",
      arista: "buchibe",
      nombre: "BUCHIBE",
      frecuencia: "88.6 · EL TELÓN",
      titulo: "Cuentos de Buchibe",
      bajada: "Narrativa oral del Príncipe Cayerúa: cuentos que se leen — o se escuchan — bajo un cielo ultramar.",
      // La sección aún no existe: el telón se anuncia, no se abre.
      cta: {
        texto: "CORRER EL TELÓN · PRONTO",
        href: null,
        clase: `${MONO} text-[0.72rem] tracking-[0.16em] text-(--buc-luz)`,
      },
      tema: { "data-buchibe-theme": "telon" },
      clase: "bg-(--buc-telon)",
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--buc-luz)`,
      claseBajada: "text-base leading-relaxed text-(--buc-luz) max-w-[46ch]",
    },
  ];
  return todas.filter((d) => !d.seccion || LIBERADA[d.seccion]);
}

// La pestaña oculta pausa el avance; el servidor no tiene pestaña.
function alCambiarVisibilidad(avisar: () => void) {
  document.addEventListener("visibilitychange", avisar);
  return () => document.removeEventListener("visibilitychange", avisar);
}
const estaOculta = () => document.visibilityState === "hidden";
const nunca = () => () => {};

/** el foco llegó por teclado (un clic en un botón no cuenta) */
function focoDeTeclado(el: Element): boolean {
  try {
    return el.matches(":focus-visible");
  } catch {
    return false; // navegadores sin :focus-visible: sólo pausa el ratón
  }
}

type Origen = "auto" | "manual";

export default function HeroAristas({ edicion }: { edicion: { numero: string; slug: string } }) {
  const lista = diapositivas(edicion);
  const total = lista.length;

  const [activa, setActiva] = useState(0);
  // la que se va mientras la nueva amanece encima; null en reposo
  const [saliente, setSaliente] = useState<number | null>(null);
  // la aguja barre hacia la derecha al ir a la siguiente y al revés al volver
  const [sentido, setSentido] = useState<"adelante" | "atras">("adelante");
  // cuántos cambios van: con 0, la primera está quieta (como vino en el HTML)
  const [cambios, setCambios] = useState(0);
  // lo que oye un lector de pantalla: sólo los cambios que pidió él
  const [anuncio, setAnuncio] = useState("");

  // las pausas: el ratón encima, el foco de teclado dentro, la pestaña
  // oculta; y la detención, que dura hasta SEGUIR (el botón o un toque)
  const [encima, setEncima] = useState(false);
  const [foco, setFoco] = useState(false);
  const [detenido, setDetenido] = useState(false);
  const oculta = useSyncExternalStore(alCambiarVisibilidad, estaOculta, () => false);
  // hidratado: hasta entonces el punto no se llena (y sin JS, nunca)
  const listo = useSyncExternalStore(nunca, () => true, () => false);
  const pausa = encima || foco || oculta || detenido;

  const carrusel = useRef<HTMLDivElement>(null);
  const pista = useRef<HTMLDivElement>(null);
  const toque = useRef<{ x: number; y: number } | null>(null);
  const llevarFoco = useRef(false);

  function ir(destino: number, origen: Origen, haciaDonde: "adelante" | "atras") {
    const i = ((destino % total) + total) % total;
    if (i === activa) return;
    // si el foco estaba en la diapositiva que se va (que pasa a inert), lo
    // llevamos a la que entra para que el teclado no lo pierda
    const fuera = pista.current?.querySelector(`[data-indice="${activa}"]`);
    llevarFoco.current = !!fuera?.contains(document.activeElement);
    setSentido(haciaDonde);
    setSaliente(activa);
    setActiva(i);
    setCambios((c) => c + 1);
    setAnuncio(origen === "manual" ? `${lista[i].titulo}, ${i + 1} de ${total}` : "");
  }
  const siguiente = (origen: Origen) => ir(activa + 1, origen, "adelante");
  const anterior = () => ir(activa - 1, "manual", "atras");

  useEffect(() => {
    if (!llevarFoco.current) return;
    llevarFoco.current = false;
    const destino =
      pista.current?.querySelector<HTMLElement>(`[data-indice="${activa}"] a`) ?? carrusel.current;
    destino?.focus();
  }, [activa]);

  function alTeclear(e: KeyboardEvent) {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      siguiente("manual");
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      anterior();
    }
  }

  // Tocar en el móvil detiene el avance: quien toca está leyendo. Un gesto
  // horizontal de más de 50 px sobre la pista cambia de arista.
  function alTocar(e: PointerEvent) {
    if (e.pointerType === "mouse") return;
    // el botón PAUSA/SEGUIR decide solo (si no, el toque lo detendría y su
    // clic lo volvería a soltar)
    if ((e.target as Element).closest("[data-control-pausa]")) return;
    setDetenido(true);
    if (pista.current?.contains(e.target as Node)) toque.current = { x: e.clientX, y: e.clientY };
  }
  function alSoltar(e: PointerEvent) {
    const t = toque.current;
    toque.current = null;
    if (!t) return;
    const dx = e.clientX - t.x;
    const dy = e.clientY - t.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
      if (dx < 0) siguiente("manual");
      else anterior();
    }
  }

  const actual = lista[activa];
  const numero = (n: number) => String(n).padStart(2, "0");
  const flecha = `${MONO} hidden min-h-11 min-w-11 cursor-pointer items-center justify-center rounded-[2px] border border-(--noche-filete-fuerte) px-4 text-[0.8rem] text-(--noche-hueso) transition-colors duration-300 hover:border-(--noche-acento) hover:text-(--noche-acento) sm:flex`;

  return (
    // la cabecera de la noche (72px en móvil, 92px desde lg) va encima: el hero ocupa el resto
    <section
      id="hero"
      aria-label="Curiana Radio y sus aristas"
      className="flex h-[min(calc(100svh-72px),680px)] flex-col bg-(--noche-fondo) lg:h-[min(calc(100svh-92px),668px)]"
    >
      {/* La barra de arriba (sello, nombre, 88.8 en vivo) es la cabecera común
          de la noche, CabeceraNoche (shell 1a, BRAND_MVP §13). El h1 de la
          página queda aquí, para lectores de pantalla. */}
      <h1 className="sr-only">Curiana Radio · 88.8 FM</h1>

      <div
        ref={carrusel}
        role="region"
        aria-roledescription="carrusel"
        aria-label="Las aristas — usa las flechas del teclado para cambiar"
        tabIndex={0}
        data-listo={listo ? "" : undefined}
        data-pausa={pausa ? "" : undefined}
        style={{ "--hero-ciclo": `${CICLO_MS}ms` } as CSSProperties}
        onKeyDown={alTeclear}
        onMouseEnter={() => setEncima(true)}
        onMouseLeave={() => setEncima(false)}
        onFocus={(e) => {
          // sólo el foco de teclado pausa: un clic en un punto no deja el
          // carrusel quieto después de que el ratón se va
          if (focoDeTeclado(e.target)) setFoco(true);
        }}
        onBlur={(e) => {
          if (!e.currentTarget.contains(e.relatedTarget as Node | null)) setFoco(false);
        }}
        onPointerDown={alTocar}
        onPointerUp={alSoltar}
        onPointerCancel={() => {
          toque.current = null;
        }}
        className="hero-carrusel flex min-h-0 flex-1 flex-col focus-visible:outline-offset-[-2px]"
      >
        {/* La pista: las diapositivas apiladas en la misma celda */}
        <div
          ref={pista}
          data-sentido={sentido}
          className="hero-pista relative min-h-0 flex-1 touch-pan-y overflow-hidden"
        >
          {lista.map((d, i) => {
            const estado = i === activa ? (cambios ? "entra" : "quieta") : i === saliente ? "sale" : undefined;
            return (
              <div
                key={d.nombre}
                role="group"
                aria-roledescription="diapositiva"
                aria-label={`${i + 1} de ${total}: ${d.titulo}`}
                inert={i !== activa}
                data-indice={i}
                data-estado={estado}
                onAnimationEnd={(e) => {
                  // terminó de amanecer: la que se iba ya no hace falta debajo
                  if (e.target === e.currentTarget && i === activa) setSaliente(null);
                }}
                {...d.tema}
                style={d.estilo}
                className="hero-diapositiva"
              >
                {/* el lienzo lleva la superficie y el texto: al entrar, la
                    ventana se corre y el lienzo la compensa, así queda quieto */}
                <div
                  className={`hero-lienzo hero-texto flex h-full flex-col justify-center gap-3.5 px-6 py-10 sm:px-[88px] sm:py-14 ${d.clase}`}
                >
                  <span className={d.claseFrecuencia}>{d.frecuencia}</span>
                  <Cartel
                    as="h2"
                    className="text-[1.9rem] leading-none whitespace-normal sm:text-[2.4rem] sm:whitespace-nowrap"
                  >
                    {d.titulo}
                  </Cartel>
                  <p className={`m-0 ${d.claseBajada}`}>{d.bajada}</p>
                  {d.cta.href ? (
                    <Link
                      href={d.cta.href}
                      data-arista={d.arista}
                      data-desde="landing"
                      onClick={() => medir("arista", { arista: d.arista, desde: "landing" })}
                      className={`self-start ${d.cta.clase}`}
                    >
                      {d.cta.texto}
                    </Link>
                  ) : (
                    <span className={`self-start ${d.cta.clase}`}>{d.cta.texto}</span>
                  )}
                </div>
              </div>
            );
          })}
          {/* la aguja del dial: cruza la pista en cada cambio (decoración) */}
          {cambios > 0 && <span key={cambios} aria-hidden="true" className="hero-aguja" />}
        </div>

        {/* Controles: flechas (desde sm), puntos con el tiempo, pausa y la etiqueta */}
        <div className="flex items-center gap-3 border-t border-(--noche-filete) px-4 py-1.5 sm:gap-5 sm:px-11 sm:py-3">
          <button type="button" className={flecha} aria-label="Arista anterior" onClick={anterior}>
            ←
          </button>
          <button type="button" className={flecha} aria-label="Arista siguiente" onClick={() => siguiente("manual")}>
            →
          </button>
          {total > 1 && (
            <div className="flex items-center">
              {lista.map((d, i) => (
                <button
                  key={d.nombre}
                  type="button"
                  aria-label={`Ir a ${d.titulo}`}
                  aria-current={i === activa ? "true" : undefined}
                  onClick={() => ir(i, "manual", i > activa ? "adelante" : "atras")}
                  className="group flex h-11 cursor-pointer items-center px-[5px]"
                >
                  <span
                    aria-hidden="true"
                    className={`relative block h-2 overflow-hidden rounded-full bg-(--noche-filete-fuerte) transition-[width] duration-300 ${
                      i === activa ? "w-10" : "w-2 group-hover:bg-(--noche-hueso-2)"
                    }`}
                  >
                    {/* el tiempo que le queda al aire: se llena y cambia */}
                    {i === activa && (
                      <span
                        key={cambios}
                        className="hero-relleno absolute inset-0 bg-(--noche-acento)"
                        onAnimationEnd={(e) => {
                          if (e.animationName === "hero-llenar") siguiente("auto");
                        }}
                      />
                    )}
                  </span>
                </button>
              ))}
            </div>
          )}
          <span className="flex-1" />
          {total > 1 && (
            <button
              type="button"
              data-control-pausa=""
              onClick={() => setDetenido((d) => !d)}
              className={`${MONO} flex min-h-11 cursor-pointer items-center text-[0.64rem] tracking-[0.24em] whitespace-nowrap text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-acento) motion-reduce:hidden`}
            >
              <span aria-hidden="true">[&nbsp;</span>
              {detenido ? "SEGUIR" : "PAUSA"}
              <span className="sr-only"> el avance de las aristas</span>
              <span aria-hidden="true">&nbsp;]</span>
            </button>
          )}
          <span aria-hidden="true" className={`${MONO} text-[0.64rem] tracking-[0.24em] whitespace-nowrap text-(--noche-hueso-2)`}>
            {numero(activa + 1)} / {numero(total)}
            <span className="hidden sm:inline"> · {actual.nombre}</span>
          </span>
        </div>

        {/* sólo los cambios que pidió el lector; el avance solo no se anuncia */}
        <p aria-live="polite" aria-atomic="true" className="sr-only">
          {anuncio}
        </p>
      </div>
    </section>
  );
}
