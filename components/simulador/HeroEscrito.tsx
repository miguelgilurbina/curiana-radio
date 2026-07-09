"use client";

import { useEffect, useState } from "react";

// "El cronista escribe": el hero del laboratorio tipea primero la frase
// caquetía, respira, y entonces escribe el titular en español — la máquina
// que redacta la crónica, elevada a primer segundo de la experiencia.
//
// Progressive enhancement estricto: el servidor (y el primer paint) rinden
// el texto completo; la animación solo arranca tras montar, y nunca con
// prefers-reduced-motion. El layout no salta: mientras tipea, el texto
// completo queda invisible reservando su espacio y la capa tipeada se
// superpone. Para lectores de pantalla el contenido real está siempre
// (sr-only durante la animación).

const MS_LETRA_CAQUETIO = 46; // el caquetío se escribe despacio, letra a letra
const MS_PALABRA_TITULO = 85; // el español llega rápido, palabra a palabra
const PAUSA_TRADUCCION = 750; // el respiro entre lengua y lengua
const CARET_DESPEDIDA = 2600; // cuánto sigue parpadeando el caret al terminar

type Fase = "caquetio" | "pausa" | "titulo" | "fin";

function Caret({ visible }: { visible: boolean }) {
  return (
    <span
      aria-hidden="true"
      className={`sim-caret ml-0.5 transition-opacity duration-700 ${visible ? "opacity-100" : "opacity-0"}`}
    />
  );
}

export default function HeroEscrito({
  caquetio,
  traduccion,
  titulo,
}: {
  caquetio: string;
  traduccion: string;
  titulo: string;
}) {
  const [animando, setAnimando] = useState(false);
  const [fase, setFase] = useState<Fase>("caquetio");
  const [letras, setLetras] = useState(0);
  const [palabras, setPalabras] = useState(0);
  const [caretVivo, setCaretVivo] = useState(true);

  const tituloPalabras = titulo.split(" ");

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    setAnimando(true);
    const timers: ReturnType<typeof setTimeout>[] = [];
    const en = (ms: number, fn: () => void) => timers.push(setTimeout(fn, ms));

    let t = 300; // beat inicial: la página aparece, el cronista se sienta
    for (let i = 1; i <= caquetio.length; i++) {
      const n = i;
      en((t += MS_LETRA_CAQUETIO), () => setLetras(n));
    }
    en((t += 80), () => setFase("pausa"));
    en((t += PAUSA_TRADUCCION), () => setFase("titulo"));
    const nPalabras = titulo.split(" ").length;
    for (let i = 1; i <= nPalabras; i++) {
      const n = i;
      en((t += MS_PALABRA_TITULO), () => setPalabras(n));
    }
    en((t += 120), () => setFase("fin"));
    en((t += CARET_DESPEDIDA), () => setCaretVivo(false));

    return () => timers.forEach(clearTimeout);
    // El contenido es estático por render del server; solo corre al montar.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      {/* La frase caquetía: la lengua habla primero */}
      <p className="relative mt-4 sim-display text-2xl italic leading-snug text-(--sim-fuego) md:text-3xl">
        {animando ? (
          <>
            <span className="invisible" aria-hidden="true">
              {caquetio}
            </span>
            <span className="absolute inset-0" aria-hidden="true">
              {caquetio.slice(0, letras)}
              <Caret visible={caretVivo && fase === "caquetio"} />
            </span>
            <span className="sr-only">{caquetio}</span>
          </>
        ) : (
          caquetio
        )}
      </p>
      <p
        className={`mt-1.5 font-sans text-sm text-(--sim-ink-faint) transition-opacity duration-700 ${
          animando && fase === "caquetio" ? "opacity-0" : "opacity-100"
        }`}
      >
        {traduccion}
      </p>

      {/* El titular: el cronista lo reescribe en español */}
      <h2 className="relative mt-6 sim-display text-4xl font-semibold leading-[1.02] tracking-tight text-(--sim-ink) sm:text-5xl md:text-6xl">
        {animando ? (
          <>
            <span className="invisible" aria-hidden="true">
              {titulo}
            </span>
            <span className="absolute inset-0" aria-hidden="true">
              {tituloPalabras.slice(0, palabras).join(" ")}
              {(fase === "titulo" || fase === "fin") && <Caret visible={caretVivo} />}
            </span>
            <span className="sr-only">{titulo}</span>
          </>
        ) : (
          titulo
        )}
      </h2>
    </div>
  );
}
