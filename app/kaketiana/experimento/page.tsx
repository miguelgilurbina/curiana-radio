import type { Metadata } from "next";
import Link from "next/link";
import { getAbstract } from "@/lib/abstract";
import { getFichasSeed } from "@/lib/fichas";
import { getSerie, brazo, SERIE_ACTUAL } from "@/lib/serie";
import { getEscenasParaElVisor } from "@/lib/escena";
import Masthead from "@/components/simulador/Masthead";
import {
  PortadaLab,
  AbstractCientifico,
  Conceptos,
  PipelineFlujo,
} from "@/components/simulador/laboratorio";
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

function H3({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
      {children}
    </h3>
  );
}

// El experimento, era 2: la serie `era2-base`, dos brazos de treinta días.
// La página entera vive en el registro oscuro del laboratorio. Las cifras salen
// de los seeds (series/, escena/, wiki/fichas.json) y el texto del abstract las
// recibe por marcas: nada aquí se escribe a mano. La era 1 —cómo se construyó
// el motor— tiene su página aparte, con la advertencia de su bitácora.
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
    <div data-sim-acto="laboratorio" className="bg-(--sim-paper)">
      <div className="mx-auto max-w-6xl px-4 pb-20 pt-8 sm:px-6 lg:px-8">
        <Masthead />

        <div className="mx-auto max-w-[820px]">
          <PortadaLab pitch={abstract.pitch} />
          <p className="mt-4 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
            La frase del principio la dijo {frase.quien}, en {frase.lugar}, el día {frase.dia} de la
            simulación (run <code className="sim-mono">{frase.run}</code>). {frase.nota}
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

          <AbstractCientifico parrafos={abstract.abstract} />

          {serie && escena && control ? (
            <>
              <section id="resultados" className="mt-14 scroll-mt-24">
                <Overline>Lo que pasó</Overline>
                <H3>
                  {escena.dias} días, {serie.brazos.length} brazos
                </H3>
                <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                  La misma comunidad, dos veces: una con el mapa de Paraguaná y el Capubana cada{" "}
                  {serie.capubana.cada} días, y otra sin mapa, donde todos oyen a todos. La gráfica
                  mide la distancia entre las maneras de hablar de los {serie.elenco?.total} personajes,
                  día a día.
                </p>
                <figure className="mt-6">
                  <SerieBrazosChart escena={escena.serie} control={control.serie} capubana={serie.capubana.dias} />
                  <figcaption className="sim-mono mt-3 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
                    Fig. 1 · Distancia idiolectal media por día, serie {serie.serie}. Baja = las voces se
                    parecen más.
                  </figcaption>
                </figure>
                <HallazgosSerie seed={serie} />
              </section>

              <section id="nombres" className="mt-16 scroll-mt-24">
                <Overline>Lo que la comunidad nombró</Overline>
                <H3>La misma cosa, dos nombres</H3>
                <NombresDeLaSerie seed={serie} />
              </section>
            </>
          ) : (
            <div className="mt-14">
              <EmptyState
                title="Todavía no hay una serie exportada"
                hint="Corre export_serie_seed.py contra Supabase local al cerrar una serie."
              />
            </div>
          )}

          {/* La escena: el visor de repetición sobre el mapa real (decisión de
              Miguel 2026-09-17). Sólo los días exportados de ESTA serie. */}
          {escenas.length > 0 && (
            <section id="escena" className="mt-16 scroll-mt-24">
              <Overline>El mundo, turno a turno</Overline>
              <H3>Dónde estaba cada uno</H3>
              <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                Un personaje no vive en una etiqueta: está en un sitio, a una hora, con quien esté ahí.
                Esto no simula nada: lee la escena que el motor guardó, a cada uno en un lugar en cada
                momento del día, y la pone sobre Paraguaná. Lo que se dijo en un sitio se lee pinchando
                el sitio.
              </p>
              <MapaDeEscena seeds={escenas} />
            </section>
          )}

          <Conceptos conceptos={abstract.conceptos} />
          <PipelineFlujo pasos={abstract.pipeline} />

          <section id="limites" className="mt-14 scroll-mt-24">
            <Overline>Dicho con cuidado</Overline>
            <H3>Lo que esto no prueba</H3>
            <ul className="mt-5 max-w-reading list-disc space-y-2 pl-5 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
              {abstract.limites.map((l) => (
                <li key={l}>{l}</li>
              ))}
            </ul>
            <p className="sim-display mt-8 text-xl font-semibold text-(--sim-ink)">Lo que sigue</p>
            <ul className="mt-3 max-w-reading list-disc space-y-2 pl-5 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
              {abstract.siguiente.map((l) => (
                <li key={l}>{l}</li>
              ))}
            </ul>
          </section>

          <footer className="mt-16 border-t border-(--sim-rule) pt-8">
            <Link href="/kaketiana/experimento/era-1" className="group block max-w-reading">
              <Overline>Historia del motor</Overline>
              <span className="sim-display mt-1 block text-xl font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                La era 1: cómo se construyó el instrumento →
              </span>
              <span className="mt-1 block font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                Las simulaciones de junio y julio de 2026, su crónica y el primer experimento de control.
                Pruebas de desarrollo, no resultados.
              </span>
            </Link>

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
  );
}
