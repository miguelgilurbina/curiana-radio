"use client";

import { useCallback, useEffect, useRef, useState, type CSSProperties, type ReactNode } from "react";
import Link from "next/link";
import { Cartel } from "@/components/ui/Typography";

// 01 · Hero: el carrusel de aristas (opción 2a del handoff, fase 2). La intro
// ya obligó a interactuar, así que aquí no hay "gira la espiral": el hero
// arranca sintonizado. Cinco diapositivas a pantalla completa, cada una en su
// superficie; auto-avance cada 5 s que se pausa con hover o foco y se detiene
// en cuanto alguien toca los controles.

// la mono del sistema (Tailwind: ui-monospace, Menlo, Consolas…), como el DS
const MONO = "font-mono";
const AUTO_MS = 5000;

interface Diapositiva {
  nombre: string; // para la etiqueta "0X / 05 · NOMBRE"
  frecuencia: string;
  titulo: string;
  bajada: string;
  cta: ReactNode;
  /** superficie: tema de sección + fondo */
  tema: Record<string, string>;
  clase: string;
  estilo?: CSSProperties;
  claseFrecuencia: string;
  claseBajada: string;
}

function diapositivas(edicion: { numero: string; slug: string }): Diapositiva[] {
  const enlaceMono = `${MONO} text-[0.72rem] tracking-[0.16em] transition-colors duration-300 hover:text-frequency`;
  return [
    {
      nombre: "LA RADIO",
      frecuencia: "88.8 · EL MARCO",
      titulo: "La Radio",
      bajada: "Emitimos desde una Paraguaná paralela, después del Renacimiento de La Curiana.",
      cta: (
        <Link
          href={`/${edicion.slug}`}
          className="mt-1.5 self-start rounded-[2px] bg-frequency px-7 py-[15px] text-[0.78rem] font-semibold uppercase tracking-[0.2em] whitespace-nowrap text-white transition-all duration-300 hover:bg-(--noche-hueso) hover:text-(--noche-fondo)"
        >
          Sintonizar #{edicion.numero} →
        </Link>
      ),
      tema: {},
      clase: "noche-gradiente",
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--noche-hueso-2)`,
      claseBajada: "font-serif italic text-lg leading-relaxed text-(--noche-hueso-2) max-w-[44ch]",
    },
    {
      nombre: "JAI SOUNDS",
      frecuencia: "88.1 · jay · caquetío · oír, escuchar",
      titulo: "Jai Sounds",
      bajada: "La cabina de noche. Cinco pistas por emisión, reseñadas al oído; el dial rota su matiz con cada visita.",
      cta: (
        <Link href="/jai-sounds" className={`${enlaceMono} text-(--jai-luz)`}>
          ENTRAR AL DIAL →
        </Link>
      ),
      tema: { "data-jai-theme": "dial" },
      clase: "bg-(--jai-noche)",
      estilo: { "--jai-hue": "212" } as CSSProperties,
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--jai-luz-soft)`,
      claseBajada: "text-base leading-relaxed text-(--jai-luz-soft) max-w-[46ch]",
    },
    {
      nombre: "SIMULADOR",
      frecuencia: "88.3 · La crónica de Indias",
      titulo: "Simulador Caquetío",
      bajada: "Sobre pergamino y rúbrica, una lengua del golfo se reconstruye palabra a palabra.",
      cta: (
        <Link href="/kaketiana" className={`${enlaceMono} text-(--sim-ink)`}>
          ABRIR EL CÓDICE →
        </Link>
      ),
      tema: { "data-sim-theme": "cronista" },
      clase: "bg-(--sim-paper)",
      claseFrecuencia: "text-[0.64rem] font-medium uppercase tracking-[0.2em] text-(--sim-rubrica)",
      claseBajada: "text-base leading-relaxed text-(--sim-ink-soft) max-w-[46ch]",
    },
    {
      nombre: "GALERÍA",
      frecuencia: "88.5 · LA SALA NEUTRA",
      titulo: "Galería · Prompt Maker",
      bajada: "Cientos de visiones curadas. El prompt es código y se publica a la vista.",
      cta: (
        <Link href="/galeria" className={`${enlaceMono} text-(--gal-luz)`}>
          RECORRER LA SALA →
        </Link>
      ),
      tema: { "data-galeria-theme": "sala" },
      clase: "bg-(--gal-sala)",
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--gal-luz-soft)`,
      claseBajada: "text-base leading-relaxed text-(--gal-luz-soft) max-w-[46ch]",
    },
    {
      nombre: "BUCHIBE",
      frecuencia: "88.6 · EL TELÓN",
      titulo: "Cuentos de Buchibe",
      bajada: "Narrativa oral del Príncipe Cayerúa: cuentos que se leen — o se escuchan — bajo un cielo ultramar.",
      // La sección aún no existe: el telón se anuncia, no se abre.
      cta: <span className={`${MONO} text-[0.72rem] tracking-[0.16em] text-(--buc-luz)`}>CORRER EL TELÓN · PRONTO</span>,
      tema: { "data-buchibe-theme": "telon" },
      clase: "bg-(--buc-telon)",
      claseFrecuencia: `${MONO} text-[0.64rem] tracking-[0.3em] text-(--buc-luz)`,
      claseBajada: "text-base leading-relaxed text-(--buc-luz) max-w-[46ch]",
    },
  ];
}

export default function HeroAristas({ edicion }: { edicion: { numero: string; slug: string } }) {
  const lista = diapositivas(edicion);
  const total = lista.length;
  const [activa, setActiva] = useState(0);
  const [pausado, setPausado] = useState(false); // hover o foco dentro
  const [detenido, setDetenido] = useState(false); // alguien tocó los controles
  const [lento, setLento] = useState(false);
  const toque = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    // eslint-disable-next-line react-hooks/set-state-in-effect -- preferencia del cliente, no existe en el servidor
    setLento(mq.matches);
    const alCambiar = () => setLento(mq.matches);
    mq.addEventListener("change", alCambiar);
    return () => mq.removeEventListener("change", alCambiar);
  }, []);

  useEffect(() => {
    if (pausado || detenido || lento) return;
    const t = setInterval(() => setActiva((i) => (i + 1) % total), AUTO_MS);
    return () => clearInterval(t);
  }, [pausado, detenido, lento, total]);

  const ir = useCallback(
    (i: number) => {
      setDetenido(true);
      setActiva(((i % total) + total) % total);
    },
    [total],
  );

  function alTeclear(e: React.KeyboardEvent) {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      ir(activa + 1);
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      ir(activa - 1);
    }
  }

  // Swipe en táctil: un gesto horizontal de más de 50 px cambia de arista.
  function alBajar(e: React.PointerEvent) {
    if (e.pointerType !== "mouse") toque.current = { x: e.clientX, y: e.clientY };
  }
  function alSubir(e: React.PointerEvent) {
    const t = toque.current;
    toque.current = null;
    if (!t) return;
    const dx = e.clientX - t.x, dy = e.clientY - t.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) ir(activa + (dx < 0 ? 1 : -1));
  }

  const actual = lista[activa];
  const etiqueta = `${String(activa + 1).padStart(2, "0")} / ${String(total).padStart(2, "0")} · ${actual.nombre}`;
  const flecha =
    "hidden sm:inline-block cursor-pointer rounded-[2px] border border-(--noche-filete-fuerte) px-4 py-[9px] text-[0.8rem] text-(--noche-hueso) transition-colors duration-300 hover:border-frequency hover:text-frequency";

  return (
    <section id="hero" aria-label="Curiana Radio y sus aristas" className="flex h-[min(100svh,760px)] flex-col bg-(--noche-fondo)">
      {/* Barra superior: isotipo + lockup en hueso, y la señal en vivo */}
      <div className="flex items-center gap-[18px] border-b border-(--noche-filete) px-6 py-5 sm:px-11">
        {/* eslint-disable-next-line @next/next/no-img-element -- los PNG de marca van tal cual */}
        <img src="/marca/isotipo-hueso.png" alt="" width={44} height={44} className="h-11 w-11" />
        <h1 className="m-0">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/marca/lockup-hueso.png" alt="Curiana Radio" width={130} height={130} className="h-auto w-24 sm:w-[130px]" />
        </h1>
        <span className="flex-1" />
        <span className={`${MONO} flex items-center gap-2 text-[0.66rem] tracking-[0.26em] text-(--noche-hueso-2)`}>
          <span aria-hidden="true" className="noche-pulso inline-block h-[7px] w-[7px] rounded-full bg-frequency" />
          88.8 FM<span className="hidden sm:inline"> · SINTONIZADO</span>
        </span>
      </div>

      {/* La pista */}
      <div
        role="region"
        aria-roledescription="carrusel"
        aria-label="Las aristas — usa las flechas del teclado para cambiar"
        tabIndex={0}
        onKeyDown={alTeclear}
        onMouseEnter={() => setPausado(true)}
        onMouseLeave={() => setPausado(false)}
        onFocus={() => setPausado(true)}
        onBlur={(e) => {
          if (!e.currentTarget.contains(e.relatedTarget as Node | null)) setPausado(false);
        }}
        onPointerDown={alBajar}
        onPointerUp={alSubir}
        className="relative flex-1 touch-pan-y overflow-hidden focus-visible:outline-offset-[-2px]"
      >
        <div className="hero-pista" style={{ transform: `translateX(-${activa * 100}%)` }}>
          {lista.map((d, i) => (
            <div
              key={d.nombre}
              role="group"
              aria-roledescription="diapositiva"
              aria-label={`${i + 1} de ${total}: ${d.titulo}`}
              inert={i !== activa}
              data-activa={i === activa ? "" : undefined}
              {...d.tema}
              style={d.estilo}
              className={`hero-diapositiva ${d.clase}`}
            >
              <div className="flex h-full flex-col justify-center gap-3.5 px-6 py-10 sm:px-[88px] sm:py-14">
                <span className={d.claseFrecuencia}>{d.frecuencia}</span>
                <Cartel as="h2" className="text-[1.9rem] leading-none whitespace-normal sm:text-[2.4rem] sm:whitespace-nowrap">
                  {d.titulo}
                </Cartel>
                <p className={`m-0 ${d.claseBajada}`}>{d.bajada}</p>
                {d.cta}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Controles: flechas (desde sm), puntos y la etiqueta */}
      <div className="flex items-center gap-5 border-t border-(--noche-filete) px-6 py-[18px] sm:px-11">
        <button type="button" className={`${MONO} ${flecha}`} aria-label="Arista anterior" onClick={() => ir(activa - 1)}>
          ←
        </button>
        <button type="button" className={`${MONO} ${flecha}`} aria-label="Arista siguiente" onClick={() => ir(activa + 1)}>
          →
        </button>
        <div className="flex items-center gap-2.5">
          {lista.map((d, i) => (
            <button
              key={d.nombre}
              type="button"
              aria-label={`Ir a ${d.titulo}`}
              aria-current={i === activa ? "true" : undefined}
              onClick={() => ir(i)}
              className="flex h-6 cursor-pointer items-center"
            >
              <span
                aria-hidden="true"
                className={`block h-2 rounded-full transition-all duration-300 ${
                  i === activa ? "w-7 bg-frequency" : "w-2 bg-(--noche-filete-fuerte)"
                }`}
              />
            </button>
          ))}
        </div>
        <span className="flex-1" />
        <span
          className={`${MONO} text-[0.64rem] tracking-[0.24em] text-(--noche-hueso-2)`}
          aria-live={pausado || detenido || lento ? "polite" : "off"}
        >
          {etiqueta}
        </span>
      </div>
    </section>
  );
}
