import type { WikiPagina } from "@/types/wiki";
import { getVecinos, getWikiPagina, getWikiPorSeccion } from "@/lib/wiki";
import { enlazarVoces } from "@/lib/fichas";
import { abreConCursiva, medidasDe, pieDeCitaAparte, preguntaDe, seccionesDe } from "@/lib/articulo";
import { Overline } from "@/components/simulador/ui";
import { WikiProse } from "@/components/simulador/wiki-mdx";
import Sumario from "@/components/kaketiana/Sumario";
import MigaArticulo from "@/components/kaketiana/MigaArticulo";
import { obrasCitadas, SeguirLeyendo, SobreQueSeSostiene } from "@/components/kaketiana/PieDeArticulo";
import FinDeLectura from "@/components/analitica/FinDeLectura";

// El artículo de fondo del pueblo, del manual de Kaketiana (design_handoff_
// kaketiana, Vistas §02; móvil en Sistema §06): la miga con el progreso, el
// sumario lateral con lo que el artículo mide de sí mismo, la pregunta como
// título, la prosa a 65ch con capitular, «sobre qué se sostiene» y la
// siguiente pregunta. Todo lo que lleva número sale del cuerpo
// (lib/articulo.ts) o de la bibliografía.
//
// El índice de certeza de la cabecera queda fuera: el manual lo calcula de
// las etiquetas de cada afirmación, y los ensayos no las llevan. Se probó con
// las voces que nombran (lib/fichas.ts) y dan de 0 a 5 por ensayo, porque las
// formas van en cursiva y no en código: un índice así diría más del formato
// que de la certeza.

const dos = (n: number) => String(n).padStart(2, "0");
const plural = (n: number, uno: string, varios: string) => `${n} ${n === 1 ? uno : varios}`;

const TIPOS: Record<string, string> = { articulo: "artículo" };

export default function ArticuloEnsayo({ pagina }: { pagina: WikiPagina }) {
  const lista = getWikiPorSeccion("pueblo");
  const posicion = lista.findIndex((p) => p.slug === pagina.slug) + 1;
  const { anterior, siguiente } = getVecinos("pueblo", pagina.slug);

  // Las voces que nombra enlazan a su ficha; la atribución de una cita, a su pie.
  const cuerpo = pieDeCitaAparte(enlazarVoces(pagina.cuerpo));
  const secciones = seccionesDe(cuerpo);
  const medidas = medidasDe(cuerpo);
  const obras = obrasCitadas(cuerpo, pagina.fuentes);

  const pregunta = preguntaDe(pagina);
  const preguntaSiguiente = siguiente
    ? (preguntaDe(getWikiPagina("pueblo", siguiente.slug)) ?? siguiente.titulo)
    : null;

  const esteArticulo = [
    medidas.citas > 0 ? plural(medidas.citas, "cita de fuente", "citas de fuente") : null,
    [
      medidas.tablas > 0 ? plural(medidas.tablas, "tabla", "tablas") : null,
      obras.length > 0 ? plural(obras.length, "obra", "obras") : null,
    ]
      .filter(Boolean)
      .join(" · ") || null,
  ].filter((l): l is string => Boolean(l));

  return (
    <>
      <MigaArticulo
        seccion={{ label: "El pueblo", href: "/kaketiana/pueblo" }}
        titulo={pagina.titulo}
        derecha={
          <>
            <span className="sr-only">Artículo </span>
            {dos(posicion)} / {dos(lista.length)}
          </>
        }
      />

      <div className="lg:mt-14 lg:grid lg:grid-cols-[230px_minmax(0,1fr)] lg:gap-14">
        <aside
          aria-label="En este artículo"
          className="lg:sticky lg:top-8 lg:max-h-[calc(100vh-4rem)] lg:self-start lg:overflow-y-auto"
        >
          <Sumario secciones={secciones}>
            {esteArticulo.length > 0 && (
              <div className="flex flex-col gap-2">
                <p className="kk-label text-[0.58rem] tracking-[0.22em] text-(--sim-ink-soft)">Este artículo</p>
                {esteArticulo.map((l) => (
                  <p key={l} className="sim-mono text-[0.66rem] text-(--sim-ink-soft)">
                    {l}
                  </p>
                ))}
              </div>
            )}
          </Sumario>
        </aside>

        <article className="mt-10 max-w-[65ch] lg:mt-0">
          <header>
            <Overline>
              El pueblo · {TIPOS[pagina.tipo] ?? pagina.tipo}
            </Overline>
            <h1 className="sim-display mt-4 text-[1.9rem] font-semibold leading-[1.08] tracking-tight text-(--sim-ink) sm:text-[2.9rem] sm:leading-[1.05]">
              {pregunta ?? pagina.titulo}
            </h1>
            {pagina.descripcion && (
              <p className="mt-5 max-w-reading font-sans text-base leading-relaxed text-(--sim-ink-soft) md:text-lg">
                {pagina.descripcion}
              </p>
            )}
          </header>

          <WikiProse
            source={cuerpo}
            variante="ensayo"
            className={`mt-10 ${abreConCursiva(cuerpo) ? "kk-capitular-2" : "kk-capitular"}`}
          />
          <FinDeLectura pagina={`/kaketiana/pueblo/${pagina.slug}`} />

          <SobreQueSeSostiene obras={obras} className="mt-16" />

          <SeguirLeyendo
            className="mt-14"
            siguiente={
              siguiente
                ? { href: `/kaketiana/pueblo/${siguiente.slug}`, etiqueta: "Siguiente pregunta", titulo: preguntaSiguiente ?? siguiente.titulo }
                : { href: "/kaketiana/lengua", etiqueta: "Sigue con", titulo: "La lengua" }
            }
            anterior={anterior ? { href: `/kaketiana/pueblo/${anterior.slug}`, titulo: anterior.titulo } : null}
          />
        </article>
      </div>
    </>
  );
}
