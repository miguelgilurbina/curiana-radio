import type { Metadata } from "next";
import Link from "next/link";
import { getAbstract } from "@/lib/abstract";
import { getFichasSeed } from "@/lib/fichas";
import { getSerie, brazo, SERIE_ACTUAL } from "@/lib/serie";
import { getEscenasParaElVisor } from "@/lib/escena";
import Umbral from "@/components/kaketiana/Umbral";
import Amanecer from "@/components/kaketiana/Amanecer";
import Etiqueta from "@/components/kaketiana/Etiqueta";
import Desplegable from "@/components/kaketiana/Desplegable";
import Glosario from "@/components/kaketiana/Glosario";
import { PortadaLab, AbstractCientifico, PipelineFlujo } from "@/components/simulador/laboratorio";
import SerieBrazosChart from "@/components/simulador/SerieBrazosChart";
import { HallazgosSerie, NombresDeLaSerie } from "@/components/simulador/serie";
import MapaDeEscena from "@/components/simulador/MapaDeEscena";
import { DataAside } from "@/components/simulador/prose";
import { Overline, EmptyState } from "@/components/simulador/ui";

export function generateMetadata(): Metadata {
  const { pitch } = getAbstract();
  return {
    title: "El experimento — una lengua hablada de nuevo | Kaketiana · Curiana Radio",
    description: pitch.bajada,
  };
}

const ANEXOS = [
  { href: "/kaketiana/lexicon", label: "El diccionario", desc: "Cada voz caquetía con su fuente y con cómo la sabemos." },
  { href: "/kaketiana/no-sabemos", label: "Lo que no sabemos", desc: "Las preguntas abiertas, con lo que se midió y lo que falta." },
  { href: "/kaketiana", label: "El mundo del kaketío", desc: "Cómo vivían, en qué creían, y cómo se reconstruye su lengua." },
];

// Capa 3, la madriguera: lo que el lector puede abrir si quiere todo. El repo
// es público; la bitácora y los datos de esta página se leen tal cual.
const REPO = "https://github.com/miguelgilurbina/curiana-radio/blob/main";
const MADRIGUERA = [
  {
    href: `${REPO}/proyecto-linguistico-caquet%C3%ADo/5-experimento/BITACORA_RUNS.md`,
    label: "La bitácora de la serie",
    desc: "Cómo se corrió, día por día, y lo que salió mal en el camino.",
  },
  {
    href: `${REPO}/content/simulador/series/era2-base.json`,
    label: "Los datos de esta página",
    desc: "Las dos curvas, las palabras fijadas y las disputas, tal como las exportó la base.",
  },
  {
    href: "https://github.com/miguelgilurbina/curiana-radio/tree/main/proyecto-linguistico-caquet%C3%ADo/5-experimento/analisis",
    label: "Los análisis",
    desc: "La competencia por los nombres y las treinta reflexiones del Director.",
  },
];

function H3({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
      {children}
    </h3>
  );
}

// El experimento, era 2: la serie `era2-base`, dos brazos de treinta días.
// En tres capas (Miguel, 2026-10-01: que no sobrecargue y que el lector
// decida hasta dónde baja): a la vista lo esencial —el resultado, la gráfica,
// los hallazgos en una línea, el mapa, cuatro nombres, los límites—; plegado
// el dato y el método (Desplegable, Glosario); y al final, la madriguera.
// Diseño: el manual de Kaketiana (design_handoff_kaketiana). Se entra por el
// umbral —la placa clara del wiki que anochece— y del otro lado todo es el
// Acto I en tinta profunda: lo que dice la simulación lleva ◉ canon-simulación
// y sólo la voz simulada se escribe con caret. Las cifras salen de los seeds
// (series/, escena/, wiki/fichas.json) y el texto del abstract las recibe por
// marcas: nada aquí se escribe a mano. La era 1 —cómo se construyó el motor—
// tiene su página aparte, con la advertencia de su bitácora.
export default function ExperimentoPage() {
  const abstract = getAbstract();
  const serie = getSerie();
  const fichas = getFichasSeed();
  const escenas = getEscenasParaElVisor(SERIE_ACTUAL);
  const escena = serie ? brazo(serie, "escena") : undefined;
  const control = serie ? brazo(serie, "control") : undefined;
  const { frase } = abstract;
  const nf = (n: number) => n.toLocaleString("es-VE");

  return (
    <div data-kk>
      <Umbral umbral={abstract.umbral} destino="#laboratorio" />

      <div id="laboratorio" data-sim-acto="laboratorio" className="scroll-mt-0 bg-(--sim-paper)">
        <div className="mx-auto max-w-6xl px-4 pb-20 pt-12 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-[820px]">
            <PortadaLab pitch={abstract.pitch} />
            {/* El pie de la cita, como lo pide el manual: quién, dónde, cuándo y
                la etiqueta. Es una voz simulada: ◉. */}
            <p className="mt-4 flex max-w-reading flex-wrap items-center gap-x-2 gap-y-1.5">
              <span className="sim-mono text-[0.7rem] tracking-[0.08em] text-(--sim-ink-soft)">
                — {frase.quien} · {frase.lugar} · día {frase.dia} · run {frase.run}
              </span>
              <Etiqueta grado="canon" corta />
            </p>
            <p className="mt-2 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-soft)">
              {frase.nota}
            </p>

            {serie?.elenco && escena && control && (
              <DataAside
                items={[
                  {
                    label: "Voces",
                    value: nf(serie.elenco.total),
                    sub: Object.entries(serie.elenco.por_nodo)
                      .map(([nodo, n]) => `${nodo.charAt(0)}${nodo.slice(1).toLowerCase()} ${n}`)
                      .join(" · "),
                  },
                  { label: "Días", value: `${escena.dias} × ${serie.brazos.length}`, sub: "con escena y de control" },
                  {
                    label: "Intervenciones",
                    value: nf(escena.respuestas + control.respuestas),
                    sub: "todas guardadas, todas citables",
                  },
                  {
                    label: "Diccionario",
                    value: nf(fichas.n),
                    sub: `${nf(fichas.por_capa.atestiguado)} voces atestiguadas`,
                  },
                ]}
              />
            )}

            {serie && escena && control ? (
              <>
                <Amanecer as="section" id="resultados" className="mt-14 scroll-mt-24">
                  <Overline>Lo que pasó</Overline>
                  <H3>
                    {escena.dias} días, {serie.brazos.length} brazos
                  </H3>
                  <p className="mt-4 max-w-reading font-serif text-lg leading-relaxed text-(--sim-ink)">
                    {abstract.resultado}
                  </p>
                  <p className="mt-3 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                    La gráfica mide cuánto se parecen las maneras de hablar de los {serie.elenco?.total}{" "}
                    personajes, día a día: cuanto más baja, más parecido hablan.
                  </p>
                  <figure className="mt-6">
                    <SerieBrazosChart escena={escena.serie} control={control.serie} capubana={serie.capubana.dias} />
                    <figcaption className="sim-mono mt-3 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
                      Fig. 1 · Distancia idiolectal media por día, serie {serie.serie}. Baja = las voces se
                      parecen más.
                    </figcaption>
                  </figure>
                  <HallazgosSerie seed={serie} />
                </Amanecer>

              {/* La escena: el visor de repetición sobre el mapa real (decisión de
                  Miguel 2026-09-17). Sólo los días exportados de ESTA serie. */}
              {escenas.length > 0 && (
                <Amanecer as="section" id="escena" className="mt-16 scroll-mt-24">
                  <Overline>El mundo, turno a turno</Overline>
                  <H3>Dónde estaba cada uno</H3>
                  <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                    Cada personaje está en un sitio, a una hora, con quien esté ahí. Pincha un lugar para leer
                    lo que se dijo en él.
                  </p>
                  <MapaDeEscena seeds={escenas} />
                </Amanecer>
              )}

                <Amanecer as="section" id="nombres" className="mt-16 scroll-mt-24">
                  <Overline>Lo que la comunidad nombró</Overline>
                  <H3>La misma cosa, dos nombres</H3>
                  <NombresDeLaSerie seed={serie} />
                </Amanecer>
              </>
            ) : (
              <div className="mt-14">
                <EmptyState
                  title="Todavía no hay una serie exportada"
                  hint="Corre export_serie_seed.py contra Supabase local al cerrar una serie."
                />
              </div>
            )}

            <Amanecer as="section" id="como-se-hizo" className="scroll-mt-24">
              <PipelineFlujo pasos={abstract.pipeline} />
              <Desplegable abrir="[ el método, término a término ↓ ]" className="mt-6">
                <AbstractCientifico parrafos={abstract.abstract} />
                <div className="mt-10">
                  <Glosario conceptos={abstract.conceptos} />
                </div>
              </Desplegable>
            </Amanecer>

            <Amanecer as="section" id="limites" className="mt-14 scroll-mt-24">
              <Overline>Dicho con cuidado</Overline>
              <H3>Lo que esto no prueba</H3>
              <ul className="mt-5 max-w-reading list-disc space-y-2 pl-5 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                {abstract.limites.map((l) => (
                  <li key={l}>{l}</li>
                ))}
              </ul>
              <Desplegable abrir="[ lo que sigue ↓ ]" className="mt-6">
                <ul className="max-w-reading list-disc space-y-2 pl-5 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                  {abstract.siguiente.map((l) => (
                    <li key={l}>{l}</li>
                  ))}
                </ul>
              </Desplegable>
            </Amanecer>

            <footer className="mt-16 border-t border-(--sim-rule) pt-8">
              <Overline>Más hondo</Overline>
              <ul className="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-3">
                {MADRIGUERA.map((m) => (
                  <li key={m.href}>
                    <a href={m.href} className="group block" target="_blank" rel="noopener noreferrer">
                      <span className="sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                        {m.label} ↗
                      </span>
                      <span className="mt-1 block font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{m.desc}</span>
                    </a>
                  </li>
                ))}
              </ul>

              <div className="mt-12 max-w-reading">
                <Overline>Historia del motor</Overline>
                <p className="sim-display mt-1 text-xl font-semibold text-(--sim-ink)">
                  La era 1: cómo se construyó el instrumento
                </p>
                <p className="mt-1 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                  Las simulaciones de junio y julio de 2026, su crónica y el primer experimento de control.
                  Pruebas de desarrollo, no resultados.
                </p>
                <Link href="/kaketiana/experimento/era-1" className="kk-accion mt-3 text-[0.75rem]">
                  [ LEER LA ERA 1 → ]
                </Link>
              </div>

              <ul className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-3">
                {ANEXOS.map((a) => (
                  <li key={a.href}>
                    <Link href={a.href} className="group block">
                      <span className="sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                        {a.label} →
                      </span>
                      <span className="mt-1 block font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{a.desc}</span>
                    </Link>
                  </li>
                ))}
              </ul>

              <p className="mt-10 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
                {abstract.nota_honestidad}
              </p>
              {serie && escena && control && (
                <p className="sim-mono mt-3 max-w-reading text-[0.65rem] leading-relaxed text-(--sim-ink-faint)">
                  Serie {serie.serie} · con escena {escena.runs.primero}→{escena.runs.ultimo} · control{" "}
                  {control.runs.primero}→{control.runs.ultimo} · motor {serie.motor.join(", ")} ·{" "}
                  {escena.motor.modelos.join(", ")} · exportado {serie.generado.slice(0, 10)}
                </p>
              )}
            </footer>
          </div>
        </div>
      </div>
    </div>
  );
}
