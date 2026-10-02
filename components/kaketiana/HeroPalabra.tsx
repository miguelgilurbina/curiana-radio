"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Etiqueta from "@/components/kaketiana/Etiqueta";
import { CLAVE_HERO, ID_ESTILO_HERO } from "@/lib/kaketiana-hero";

// Hero 1a del manual de Kaketiana — «la palabra se arma». La etimología ES el
// hero: tipografía pura, cero imagen. Secuencia, una vez por visita y con la
// curva única: las piezas atestiguadas amanecen (600ms, escalonadas 150ms),
// aparecen los signos (300ms), la palabra se escribe letra a letra con caret
// —la única excepción del wiki a la regla del caret: aquí la palabra se
// reconstruye ante el lector— y después amanecen la glosa, la bajada y las
// acciones. Sin JS, con prefers-reduced-motion o ya vista: todo compuesto.
//
// El canon manda sobre el handoff en dos marcas (2026-09-30): la glosa 'lugar
// de' de -ana se retiró del canon el 2026-09-07 (#109) y la palabra entera es
// un compuesto nuestro; una acuñación de trabajo es ◇ hipotética
// (fichas.json, capa «hipotético»), no ◆. Las piezas sí son ▮: las dos formas
// están documentadas.
//
// El arranque oculto lo decide un <script> en línea que la portada pone antes
// de este componente (lib/kaketiana-hero.ts): mete un <style> en <head> y así
// no hay un primer cuadro compuesto que parpadee, sin tocar ningún nodo que
// React hidrate. Este componente corre la secuencia y quita el <style>.

const PALABRA = "kaketiana";
const MS_LETRA = 60;

type Paso = "piezas" | "ana" | "signos" | "palabra" | "glosa" | "resto";

export default function HeroPalabra() {
  const [anima, setAnima] = useState(false);
  const [vistos, setVistos] = useState<Set<Paso>>(new Set());
  const [letras, setLetras] = useState(PALABRA.length);
  const [caret, setCaret] = useState(false);

  useEffect(() => {
    const estilo = document.getElementById(ID_ESTILO_HERO);
    if (!estilo) return;
    // La secuencia sólo existe si el script en línea la pidió: es el estado
    // de arranque, y no hay otra forma de saberlo que leer el DOM.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setAnima(true);
    setLetras(0);
    const timers: ReturnType<typeof setTimeout>[] = [];
    const en = (ms: number, fn: () => void) => timers.push(setTimeout(fn, ms));
    const ver = (p: Paso) => setVistos((v) => new Set(v).add(p));

    en(80, () => ver("piezas"));
    en(230, () => ver("ana"));
    en(830, () => ver("signos"));
    let t = 1130;
    en(t, () => {
      ver("palabra");
      setCaret(true);
    });
    for (let i = 1; i <= PALABRA.length; i++) {
      const n = i;
      en((t += MS_LETRA), () => setLetras(n));
    }
    en((t += 250), () => setCaret(false));
    en(t, () => ver("glosa"));
    en((t += 300), () => ver("resto"));
    en((t += 700), () => {
      try {
        sessionStorage.setItem(CLAVE_HERO, "visto");
      } catch {
        // modo privado estricto: la secuencia se repetirá, nada más
      }
      estilo.remove();
    });
    // La limpieza sólo cancela los tiempos: el <style> lo quita el final de la
    // secuencia. (En modo estricto React monta dos veces; si la limpieza lo
    // quitara, el segundo montaje ya no encontraría qué animar.)
    return () => timers.forEach(clearTimeout);
  }, []);

  const p = (paso: Paso) => ({ "data-paso": paso, "data-visto": !anima || vistos.has(paso) ? "" : undefined });

  return (
    <div className="kk-hero" data-corriendo={anima ? "" : undefined}>
      <p className="kk-label text-(--sim-ink-soft)">El nombre, como declaración de método</p>

      <div className="mt-5 flex flex-col items-start gap-3 sm:flex-row sm:flex-wrap sm:items-end sm:gap-x-5">
        <span {...p("piezas")} className="flex flex-col gap-1.5">
          <span className="kk-forma text-5xl leading-none md:text-6xl">kaketio</span>
          <span className="flex flex-col items-start gap-1">
            <span className="font-sans text-xs text-(--sim-ink-soft)">el nombre del pueblo</span>
            <Etiqueta grado="atest" corta />
          </span>
        </span>
        <span {...p("signos")} aria-hidden="true" className="sim-display text-4xl leading-none text-(--sim-ink-soft) sm:pb-11 md:text-5xl">
          +
        </span>
        <span {...p("ana")} className="flex flex-col gap-1.5">
          <span className="kk-forma text-5xl leading-none md:text-6xl">-ana</span>
          <span className="flex flex-col items-start gap-1">
            <span className="font-sans text-xs text-(--sim-ink-soft)">en Paraguaná, Curiana, Jayana…</span>
            <Etiqueta grado="atest" corta />
          </span>
        </span>
        {/* «= kaketiana» va junto: si la ecuación se parte, se parte antes del
            signo y no deja el = colgando al final de la línea */}
        <span className="flex items-end gap-x-5">
          <span {...p("signos")} aria-hidden="true" className="sim-display pb-6 text-4xl text-(--sim-ink-soft) md:text-5xl">
            =
          </span>
          <span {...p("palabra")} className="flex flex-col gap-1.5">
            <span className="relative kk-forma text-5xl leading-none md:text-6xl">
              {anima ? (
                <>
                  <span className="invisible" aria-hidden="true">
                    {PALABRA}
                  </span>
                  <span className="absolute inset-0" aria-hidden="true">
                    {PALABRA.slice(0, letras)}
                    {caret && <span className="sim-caret ml-0.5" />}
                  </span>
                  <span className="sr-only">{PALABRA}</span>
                </>
              ) : (
                PALABRA
              )}
            </span>
            <span {...p("glosa")} className="flex items-center gap-2">
              <span className="font-serif text-sm italic text-(--sim-ink)">&lsquo;el lugar de la gente&rsquo;</span>
              <Etiqueta grado="hip" corta />
            </span>
          </span>
        </span>
      </div>

      <div {...p("resto")}>
        <p className="mt-6 max-w-[34rem] font-sans text-xs leading-relaxed text-(--sim-ink-soft)">
          Oliver (1989) lee <em>kaketio</em> como &lsquo;ser viviente, gente&rsquo;, desde el lokono. El valor de{" "}
          <em>-ana</em> nadie lo anotó: &lsquo;lugar de&rsquo; es lectura nuestra, y por eso la palabra entera es
          hipotética, un compuesto que hicimos con piezas documentadas.
        </p>
        <p className="mt-6 max-w-[34rem] font-sans text-lg leading-relaxed text-(--sim-ink-soft)">
          La palabra que nombra este sitio no está documentada; sus piezas sí. Así funciona todo lo que vas a
          leer: el pueblo caquetío del Golfete de Coro y su lengua, reconstruidos sin fingir jamás saber más de lo
          que se sabe.
        </p>
        <div className="mt-7 flex flex-wrap gap-x-7 gap-y-4">
          <Link href="/kaketiana/pueblo" className="kk-accion text-[0.8rem]">
            [ ENTRAR AL PUEBLO → ]
          </Link>
          <Link href="/kaketiana/lengua" className="kk-accion text-[0.8rem] text-(--sim-ink-soft)">
            [ CONSULTAR LA LENGUA ]
          </Link>
        </div>
      </div>
    </div>
  );
}
