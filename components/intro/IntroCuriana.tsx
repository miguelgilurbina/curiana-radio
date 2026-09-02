"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import FrequencyBadge from "@/components/ui/FrequencyBadge";
import type { Escena, EstadoIntro } from "./escena";

// La intro oficial de Curiana Radio: el visitante llega a un remolino
// psicodélico serigráfico — el registro de ARTE de la marca a máxima
// saturación — con la espiral 3D del logo flotando al frente y un túnel de
// ecos detrás. Al pulsar [ SINTONIZAR → ] el remolino acelera, la cámara
// entra por el centro y un velo pergamino amanece hacia la landing. La
// intro es lo saturado; lo que sigue es lo sobrio.
//
// Progressive enhancement: el servidor rinde la cáscara (fondo índigo, UI,
// botón) y solo al montar con `activa` se carga three.js en su propio chunk
// y se calca el isotipo. Sin WebGL la intro sigue siendo usable. Con
// prefers-reduced-motion el shader se congela y el botón entra directo.
// Estilos en globals.css (.intro-*), valores 1:1 del prototipo del handoff.

export const URL_ISOTIPO = "/marca/isotipo-calco.png";

const DURACION_SINTONIZAR = 1600; // ms: el remolino se traga la cámara
const VELO_DESDE = 0.45; // el velo pergamino empieza a fundir al 45 %
const VELOCIDAD_MAX = 27;
const DOLLY_MAX = 2.35;
const AMANECER_MS = 900; // el velo se disuelve y la landing aparece debajo

type Fase = "espera" | "sintonizando" | "amanece";

interface IntroCurianaProps {
  /** Mientras es false solo se ve la cáscara (server / hidratando). */
  activa?: boolean;
  /** Si el velo se disuelve al final (gate sobre la landing) o queda opaco
   *  para que quien llama navegue (ruta /intro). */
  amanecer?: boolean;
  onFin: () => void;
}

export default function IntroCuriana({
  activa = true,
  amanecer = true,
  onFin,
}: IntroCurianaProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const veloRef = useRef<HTMLDivElement>(null);
  const botonRef = useRef<HTMLButtonElement>(null);
  const estado = useRef<EstadoIntro>({ velocidad: 1, dolly: 0, mx: 0, my: 0, lento: false });
  const rafRef = useRef(0);
  const terminado = useRef(false);

  const [fase, setFase] = useState<Fase>("espera");
  const [listo, setListo] = useState(false); // ¿la escena ya pinta?

  const terminar = useCallback(() => {
    if (terminado.current) return;
    terminado.current = true;
    onFin();
  }, [onFin]);

  // La escena vive desde que la intro se activa hasta que amanece.
  const escenaViva = activa && fase !== "amanece";
  useEffect(() => {
    if (!escenaViva) return;
    const canvas = canvasRef.current;
    if (!canvas) return;

    const e = estado.current;
    e.lento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    e.velocidad = e.lento ? 0 : 1;
    e.dolly = 0;

    let cancelado = false;
    let escena: Escena | null = null;
    import("./escena")
      .then((m) => m.prepararEscena(URL_ISOTIPO))
      .then((montar) => {
        if (cancelado) return;
        escena = montar(canvas, e);
        setListo(true);
      })
      .catch((err: unknown) => {
        // Sin WebGL (o sin el PNG) la intro degrada a índigo + UI: el botón
        // sigue llevando a la landing.
        console.warn("[intro] la escena 3D no pudo montarse:", err);
      });

    const mover = (ev: PointerEvent) => {
      e.mx = (ev.clientX / window.innerWidth - 0.5) * 2;
      e.my = (ev.clientY / window.innerHeight - 0.5) * 2;
    };
    window.addEventListener("pointermove", mover);

    // La landing sigue debajo: que la rueda no la desplace mientras tanto.
    const html = document.documentElement;
    const overflowPrevio = html.style.overflow;
    html.style.overflow = "hidden";
    botonRef.current?.focus({ preventScroll: true });

    return () => {
      cancelado = true;
      window.removeEventListener("pointermove", mover);
      escena?.dispose();
      html.style.overflow = overflowPrevio;
    };
  }, [escenaViva]);

  // Si el componente se va a mitad del viaje, el rAF no debe seguir.
  useEffect(() => () => cancelAnimationFrame(rafRef.current), []);

  const sintonizar = () => {
    if (fase !== "espera") return;
    const e = estado.current;
    if (e.lento) {
      // reduced motion: sin viaje, directo a la landing
      terminar();
      return;
    }
    setFase("sintonizando");
    const velo = veloRef.current;
    const ini = performance.now();
    const paso = (ahora: number) => {
      const k = Math.min((ahora - ini) / DURACION_SINTONIZAR, 1);
      const s = 1 - Math.pow(1 - k, 3); // ease-out-cubic
      e.velocidad = 1 + s * (VELOCIDAD_MAX - 1);
      e.dolly = s * DOLLY_MAX;
      if (velo && k > VELO_DESDE) {
        velo.style.opacity = String((k - VELO_DESDE) / (1 - VELO_DESDE));
      }
      if (k < 1) rafRef.current = requestAnimationFrame(paso);
      else setFase("amanece");
    };
    rafRef.current = requestAnimationFrame(paso);
  };

  // Amanecer: la escena ya se fue y el velo está opaco. Se disuelve y la
  // landing aparece debajo. transitionend con timeout de respaldo.
  useEffect(() => {
    if (fase !== "amanece") return;
    const velo = veloRef.current;
    if (!amanecer || !velo) {
      terminar();
      return;
    }
    const raf = requestAnimationFrame(() => {
      velo.classList.add("intro-velo-amanece");
      velo.style.opacity = "0";
    });
    velo.addEventListener("transitionend", terminar, { once: true });
    const respaldo = setTimeout(terminar, AMANECER_MS + 300);
    return () => {
      cancelAnimationFrame(raf);
      clearTimeout(respaldo);
      velo.removeEventListener("transitionend", terminar);
    };
  }, [fase, amanecer, terminar]);

  return (
    <div
      className="intro-curiana"
      data-fase={fase}
      data-listo={listo || undefined}
      role="dialog"
      aria-modal="true"
      aria-label="Bienvenida a Curiana Radio"
    >
      {fase !== "amanece" && (
        <>
          <canvas ref={canvasRef} className="intro-lienzo" aria-hidden="true" />
          <div className="intro-trama" aria-hidden="true" />
          <div className="intro-scan" aria-hidden="true" />
          <div className="intro-ui">
            <div className="intro-marca">
              <p className="intro-nombre">Curiana Radio</p>
              <FrequencyBadge size="sm" />
            </div>
            <div className="intro-pie">
              <p className="intro-estado">
                <span className="intro-punto" aria-hidden="true" />
                Interferencia · señal de otro tiempo
              </p>
              <button
                ref={botonRef}
                type="button"
                className="intro-sintonizar"
                onClick={sintonizar}
              >
                [ SINTONIZAR → ]
              </button>
              <p className="intro-proverbio">
                «No es propaganda para el cambio — es propaganda desde después.»
              </p>
            </div>
          </div>
        </>
      )}
      <div ref={veloRef} className="intro-velo" aria-hidden="true" />
    </div>
  );
}
