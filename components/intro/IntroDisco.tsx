"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { arrancarDisco, type MotorDisco } from "./disco-motor";

// La intro v1 · El Disco. El visitante está obligado a interactuar: trazando
// círculos alrededor de un disco de arena, los surcos del viento se ordenan
// en la espiral del isotipo. Afinado, aparece [ SINTONIZAR → ], que lleva a
// la landing (/inicio). Se ve una vez por sesión en `/`; en /intro, siempre.
// Spec completa en BRAND_MVP.md §9.

export const CLAVE_INTRO = "curiana:intro-v1";
const DESTINO = "/inicio";
const LOGO = "/marca/isotipo-espiral.png";
const MARCAS_DIAL = Array.from({ length: 14 }, (_, i) => (i / 13) * 100);

function yaVista(): boolean {
  try {
    return sessionStorage.getItem(CLAVE_INTRO) === "visto";
  } catch {
    return false;
  }
}

function marcarVista() {
  try {
    sessionStorage.setItem(CLAVE_INTRO, "visto");
  } catch {
    // modo privado estricto: la intro se repetirá, nada más
  }
}

export default function IntroDisco({ siempre = false }: { siempre?: boolean }) {
  const router = useRouter();
  // "decide": el servidor y la hidratación todavía no saben si la sesión ya
  // la vio; mientras tanto solo se ve la noche (sin interfaz que parpadee).
  const [fase, setFase] = useState<"decide" | "lista">("decide");
  const [ok, setOk] = useState(false);
  const [sinGl, setSinGl] = useState(false);

  const raiz = useRef<HTMLDivElement>(null);
  const lienzo = useRef<HTMLCanvasElement>(null);
  const frecuencia = useRef<HTMLSpanElement>(null);
  const aguja = useRef<HTMLSpanElement>(null);
  const viento = useRef<HTMLSpanElement>(null);
  const patron = useRef<HTMLSpanElement>(null);
  const anillo = useRef<HTMLDivElement>(null);
  const velo = useRef<HTMLDivElement>(null);
  const saltar = useRef<HTMLButtonElement>(null);
  const sintonizar = useRef<HTMLButtonElement>(null);
  const motor = useRef<MotorDisco | null>(null);
  const saliendo = useRef(false);

  useEffect(() => {
    if (!siempre && yaVista()) {
      router.replace(DESTINO);
      return;
    }
    router.prefetch(DESTINO);
    const lento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const m = arrancarDisco(
      {
        raiz: raiz.current!,
        lienzo: lienzo.current!,
        frecuencia: frecuencia.current!,
        aguja: aguja.current!,
        viento: viento.current!,
        patron: patron.current!,
        anillo: anillo.current!,
        velo: velo.current!,
      },
      { lento, logo: LOGO, onAfinado: () => setOk(true) },
    );
    motor.current = m;
    // Es el estado inicial que decide el cliente al montar (qué ve y si hay
    // WebGL2): no hay otra forma de saberlo en el servidor.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setFase("lista");
    if (!m) {
      setSinGl(true);
      setOk(true);
    }
    return () => {
      m?.destruir();
      motor.current = null;
    };
  }, [siempre, router]);

  // Quien afinó con [ SALTAR ] sigue con el foco: pasa a SINTONIZAR, que es
  // lo único que queda por hacer (SALTAR desaparece).
  useEffect(() => {
    if (ok && document.activeElement === saltar.current) sintonizar.current?.focus();
  }, [ok]);

  function alSintonizar() {
    if (saliendo.current) return;
    saliendo.current = true;
    marcarVista();
    const ir = () => router.push(DESTINO);
    if (motor.current) motor.current.salir(ir);
    else ir();
  }

  return (
    <div
      ref={raiz}
      className="intro-disco"
      data-fase={fase}
      data-ok={ok ? "" : undefined}
    >
      <canvas ref={lienzo} className="intro-disco-lienzo" aria-hidden="true" />

      <div className="intro-disco-ui">
        {sinGl && (
          // eslint-disable-next-line @next/next/no-img-element -- el isotipo a tamaño de disco, sin optimizador
          <img className="intro-disco-plano" src="/marca/isotipo-hueso.png" alt="" />
        )}

        <div className="intro-disco-esq intro-disco-mono intro-disco-tl">
          v1 — <b>el disco</b>
          <br />
          transmisión 001
        </div>
        <div className="intro-disco-esq intro-disco-mono intro-disco-tr" aria-hidden="true">
          11°54′N · 70°00′O
          <br />
          viento <span ref={viento}>09 km/h NE</span>
          <br />
          patrón <span ref={patron}>surcos</span>
        </div>
        <h1 className="intro-disco-esq intro-disco-firma m-0">
          Curiana
          <br />
          Radio
        </h1>

        <div className="intro-disco-pie">
          <div className="intro-disco-pista" aria-hidden={ok}>
            <div className="intro-disco-mono">
              <i aria-hidden="true">◌</i>gira alrededor del disco
            </div>
            <div className="intro-disco-freq" aria-hidden="true">
              <span ref={frecuencia}>87.5</span>
              <small>FM</small>
            </div>
            <div className="intro-disco-dial" aria-hidden="true">
              {MARCAS_DIAL.map((x) => (
                <em key={x} style={{ left: `${x}%` }} />
              ))}
              <span ref={aguja} className="intro-disco-aguja" />
            </div>
          </div>
          <div className="intro-disco-final" inert={!ok}>
            <div className="intro-disco-mono" aria-live="polite">
              {ok && (
                <>
                  <span className="intro-disco-punto" aria-hidden="true" />
                  señal encontrada · 88.8 FM
                </>
              )}
            </div>
            <button ref={sintonizar} type="button" className="intro-disco-sintonizar" onClick={alSintonizar}>
              [ SINTONIZAR → ]
            </button>
            <p className="intro-disco-proverbio m-0">«El viento no borra, reescribe.»</p>
          </div>
        </div>

        <button
          ref={saltar}
          type="button"
          className="intro-disco-saltar"
          inert={ok}
          onClick={() => motor.current?.afinado()}
        >
          [ SALTAR → ]
        </button>
      </div>

      <div ref={anillo} className="intro-disco-anillo" aria-hidden="true" />
      <div ref={velo} className="intro-disco-velo" aria-hidden="true" />

      {/* Sin JS no hay disco ni botón que funcione: directo a la landing. */}
      <noscript>
        <div className="intro-disco-sin-js">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/marca/isotipo-hueso.png" alt="" width={220} height={220} />
          <a href={DESTINO}>[ SINTONIZAR → ]</a>
        </div>
      </noscript>
    </div>
  );
}
