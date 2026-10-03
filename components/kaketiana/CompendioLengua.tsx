import Link from "next/link";
import type { WikiIndiceEntry } from "@/types/wiki";
import type { Capa } from "@/types/fichas";
import { getFichasSeed, getRetiradas } from "@/lib/fichas";
import { getMapa } from "@/lib/mapa";
import { SECCIONES_WIKI } from "@/types/wiki";
import { Overline } from "@/components/simulador/ui";
import Etiqueta, { GRADO_DE_CAPA } from "@/components/kaketiana/Etiqueta";

// La puerta de la lengua como compendio (Miguel, 2026-10-02: «el tema de las
// lenguas es muy importante, tiene que estar en su compendio»): el diccionario,
// los topónimos y los artículos de referencia, juntos y fuera de la portada.
// Cada cifra sale de su seed —fichas.json, mapa.json, el índice del wiki—;
// ninguna se escribe a mano.

// El orden de la escala del manual: ▮ ◆ ◇ ~.
const ESCALA: Capa[] = ["atestiguado", "reconstruido", "hipotetico", "retroabstraido"];

function Cifra({ n, de }: { n: number; de: string }) {
  return (
    <p className="mt-3 flex flex-wrap items-baseline gap-x-3">
      <span className="sim-display text-[2.6rem] font-semibold leading-none text-(--sim-ink)">{n}</span>
      <span className="sim-display text-xl text-(--sim-ink-soft)">{de}</span>
    </p>
  );
}

export default function CompendioLengua({ articulos }: { articulos: WikiIndiceEntry[] }) {
  const fichas = getFichasSeed();
  const retiradas = getRetiradas();
  const mapa = getMapa();

  return (
    <div>
      <Link
        href="/kaketiana"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-rubrica)"
      >
        ← Kaketiana
      </Link>
      <header className="mt-6 max-w-[760px]">
        <Overline>La lengua · obra de consulta</Overline>
        <h1 className="sim-display mt-2 text-4xl font-semibold leading-tight text-(--sim-ink) sm:text-[2.6rem]">
          La lengua
        </h1>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          {SECCIONES_WIKI.lengua.desc} Se consulta, no se lee de corrido: cada voz y cada nombre de lugar llevan
          la marca de cómo los sabemos.
        </p>
      </header>

      <div className="mt-10 grid gap-6 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)]">
        {fichas.n > 0 && (
          <section className="border border-(--sim-rule) bg-(--sim-paper-deep) p-6 sm:p-8">
            <h2 className="kk-label text-[0.6rem] tracking-[0.2em] text-(--sim-ink-soft)">El diccionario</h2>
            <Cifra n={fichas.n} de="voces caquetías" />
            <ul className="mt-5 flex flex-wrap gap-2" aria-label="Por cómo las sabemos">
              {ESCALA.filter((c) => (fichas.por_capa[c] ?? 0) > 0).map((c) => (
                <li key={c}>
                  <Link
                    href={`/kaketiana/lexicon?capa=${c}`}
                    className="inline-flex min-h-11 items-center gap-2 rounded-[2px] border border-(--sim-rule) bg-(--sim-paper) px-3 transition-colors hover:border-(--sim-rubrica)"
                  >
                    <Etiqueta grado={GRADO_DE_CAPA[c]} corta />
                    <span className="sim-mono text-xs tabular-nums text-(--sim-ink)">{fichas.por_capa[c]}</span>
                  </Link>
                </li>
              ))}
            </ul>
            <p className="mt-4 max-w-[52ch] font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              Cada voz con su fuente y su página. Las palabras de las lenguas hermanas que sirvieron para
              reconstruir no están: son el andamio, no la lengua.
            </p>
            <div className="mt-6 flex flex-wrap gap-x-6 gap-y-3">
              <Link href="/kaketiana/lexicon" className="kk-accion text-[0.7rem]">
                [ ABRIR EL DICCIONARIO → ]
              </Link>
              {retiradas.length > 0 && (
                <Link href="/kaketiana/lexicon/retiradas" className="kk-accion text-[0.7rem]">
                  [ LAS {retiradas.length} RETIRADAS → ]
                </Link>
              )}
            </div>
          </section>
        )}

        {mapa && mapa.resumen.toponimos_canon > 0 && (
          <section className="border border-(--sim-rule) p-6 sm:p-8">
            <h2 className="kk-label text-[0.6rem] tracking-[0.2em] text-(--sim-ink-soft)">Los topónimos</h2>
            <Cifra n={mapa.resumen.toponimos_canon} de="nombres de lugar" />
            <p className="mt-4 max-w-[46ch] font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              {mapa.resumen.toponimos_con_lugar} están ubicados en el mapa. Los nombres vienen con su traducción
              dentro: de ellos salen morfemas que ninguna otra fuente da.
            </p>
            <div className="mt-6 flex flex-wrap gap-x-6 gap-y-3">
              <Link href="/kaketiana#mapa" className="kk-accion text-[0.7rem]">
                [ VER EL MAPA → ]
              </Link>
              <Link href="/kaketiana/lengua/toponimia" className="kk-accion text-[0.7rem]">
                [ CÓMO SE LEEN → ]
              </Link>
            </div>
          </section>
        )}
      </div>

      {articulos.length > 0 && (
        <section className="mt-14">
          <h2 className="kk-label text-[0.6rem] tracking-[0.2em] text-(--sim-ink-soft)">
            Los artículos de referencia · {articulos.length}
          </h2>
          <ul className="mt-3 grid gap-x-10 border-t-2 border-(--sim-ink) sm:grid-cols-2">
            {articulos.map((p) => (
              <li key={p.slug} className="border-b border-(--sim-rule)">
                <Link
                  href={`/kaketiana/lengua/${p.slug}`}
                  className="group flex min-h-11 items-baseline justify-between gap-4 py-3.5"
                >
                  <span className="sim-display text-lg font-semibold leading-snug text-(--sim-ink) transition-colors group-hover:text-(--sim-rubrica)">
                    {p.titulo}
                  </span>
                  <span aria-hidden="true" className="text-(--sim-ink-soft) transition-colors group-hover:text-(--sim-rubrica)">
                    →
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      <p className="mt-12">
        <Link href="/kaketiana/no-sabemos" className="kk-accion text-[0.7rem]">
          [ LO QUE NO SABEMOS → ]
        </Link>
      </p>
    </div>
  );
}
