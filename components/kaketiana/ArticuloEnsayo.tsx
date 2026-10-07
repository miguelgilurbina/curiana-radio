import Link from "next/link";
import type { WikiPagina } from "@/types/wiki";
import { generoLegible, getBibliografia, getVecinos, getWikiPagina, getWikiPorSeccion } from "@/lib/wiki";
import { enlazarVoces } from "@/lib/fichas";
import { abreConCursiva, medidasDe, obrasDelArticulo, pieDeCitaAparte, seccionesDe } from "@/lib/articulo";
import { Overline } from "@/components/simulador/ui";
import { WikiProse } from "@/components/simulador/wiki-mdx";
import Sumario from "@/components/kaketiana/Sumario";
import Desplegable from "@/components/kaketiana/Desplegable";
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

const OBRAS_VISIBLES = 6;

const dos = (n: number) => String(n).padStart(2, "0");
const plural = (n: number, uno: string, varios: string) => `${n} ${n === 1 ? uno : varios}`;

const TIPOS: Record<string, string> = { articulo: "artículo" };

/** La pregunta del ensayo (frontmatter `pregunta`), si la tiene. */
function preguntaDe(p: Pick<WikiPagina, "frontmatter"> | null): string | null {
  const q = p?.frontmatter.pregunta;
  return typeof q === "string" && q.trim() ? q.trim() : null;
}

interface ObraCitada {
  slug: string;
  corto: string;
  genero: string | null;
}

function ListaDeObras({ obras }: { obras: ObraCitada[] }) {
  return (
    <ul className="grid gap-x-6 gap-y-2.5 font-sans text-[0.8rem] leading-snug text-(--sim-ink-soft) sm:grid-cols-2">
      {obras.map((o) => (
        <li key={o.slug}>
          <Link
            href={`/kaketiana/bibliografia#${o.slug}`}
            className="text-(--kk-extra) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:decoration-(--kk-extra)"
          >
            {o.corto}
          </Link>
          {o.genero && <span> · {o.genero}</span>}
        </li>
      ))}
    </ul>
  );
}

export default function ArticuloEnsayo({ pagina }: { pagina: WikiPagina }) {
  const lista = getWikiPorSeccion("pueblo");
  const posicion = lista.findIndex((p) => p.slug === pagina.slug) + 1;
  const { anterior, siguiente } = getVecinos("pueblo", pagina.slug);

  // Las voces que nombra enlazan a su ficha; la atribución de una cita, a su pie.
  const cuerpo = pieDeCitaAparte(enlazarVoces(pagina.cuerpo));
  const secciones = seccionesDe(cuerpo);
  const medidas = medidasDe(cuerpo);

  const biblio = new Map(getBibliografia().map((o) => [o.slug, o]));
  const obras: ObraCitada[] = obrasDelArticulo(cuerpo, pagina.fuentes).map((slug) => {
    const o = biblio.get(slug);
    const titulo = o?.titulo ?? pagina.fuentes.find((f) => f.slug === slug)?.titulo ?? slug;
    return { slug, corto: titulo.split(" — ")[0], genero: generoLegible(o?.genero ?? null) };
  });

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
      {/* La miga, pegada a la nav de la sección: anula el pt-10 de la columna,
          y en móvil va a sangre completa, como la barra del sumario de abajo */}
      <nav
        aria-label="Dónde estás"
        className="-mx-4 -mt-10 flex items-center gap-4 border-b border-(--sim-rule) px-4 py-0.5 sm:mx-0 sm:px-0 sm:py-3.5"
      >
        <ol className="kk-label hidden min-w-0 items-center gap-2 text-[0.62rem] tracking-[0.16em] text-(--sim-ink-soft) sm:flex">
          <li>
            <Link href="/kaketiana" className="transition-colors hover:text-(--sim-rubrica)">
              Kaketiana
            </Link>
          </li>
          <li aria-hidden="true" className="text-(--sim-ink-faint)">
            /
          </li>
          <li>
            <Link href="/kaketiana/pueblo" className="whitespace-nowrap transition-colors hover:text-(--sim-rubrica)">
              El pueblo
            </Link>
          </li>
          <li aria-hidden="true" className="text-(--sim-ink-faint)">
            /
          </li>
          <li aria-current="page" className="min-w-0 truncate text-(--sim-ink)">
            {pagina.titulo}
          </li>
        </ol>
        <Link
          href="/kaketiana/pueblo"
          className="kk-label inline-flex min-h-11 items-center text-[0.6rem] tracking-[0.12em] text-(--sim-ink-soft) sm:hidden"
        >
          ← El pueblo
        </Link>
        <span className="flex-1" />
        <span className="kk-label shrink-0 text-[0.6rem] tracking-[0.16em] text-(--sim-ink-soft) sm:text-[0.62rem]">
          <span className="sr-only">Artículo </span>
          {dos(posicion)} / {dos(lista.length)}
        </span>
      </nav>

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
          </header>

          <WikiProse
            source={cuerpo}
            variante="ensayo"
            className={`mt-10 ${abreConCursiva(cuerpo) ? "kk-capitular-2" : "kk-capitular"}`}
          />
          <FinDeLectura pagina={`/kaketiana/pueblo/${pagina.slug}`} />

          {obras.length > 0 && (
            <section className="mt-16 border-t-2 border-(--sim-ink) pt-[22px]">
              <h2 className="kk-label text-[0.6rem] tracking-[0.22em] text-(--sim-ink-soft)">
                Sobre qué se sostiene este artículo
              </h2>
              <div className="mt-3.5">
                <ListaDeObras obras={obras.slice(0, OBRAS_VISIBLES)} />
              </div>
              {obras.length > OBRAS_VISIBLES && (
                <Desplegable
                  abrir={`[ y ${plural(obras.length - OBRAS_VISIBLES, "obra más", "obras más")} ↓ ]`}
                  className="mt-4"
                >
                  <ListaDeObras obras={obras.slice(OBRAS_VISIBLES)} />
                </Desplegable>
              )}
              <Link href="/kaketiana/bibliografia" className="kk-accion mt-5 text-[0.66rem]">
                [ toda la bibliografía → ]
              </Link>
            </section>
          )}

          <nav aria-label="Seguir leyendo" className="mt-14 flex flex-col gap-3">
            <Link
              href={siguiente ? `/kaketiana/pueblo/${siguiente.slug}` : "/kaketiana/lengua"}
              className="flex flex-col gap-2 rounded-2xl border border-(--sim-rule) px-5 py-4 transition-colors duration-300 hover:border-(--sim-rubrica) sm:flex-row sm:items-baseline sm:justify-between sm:gap-6 sm:px-[26px] sm:py-5"
            >
              <span className="kk-label shrink-0 text-[0.6rem] tracking-[0.2em] text-(--sim-ink-soft)">
                {siguiente ? "Siguiente pregunta" : "Sigue con"}
              </span>
              <span className="sim-display text-[1.05rem] leading-snug text-(--sim-ink) sm:text-right sm:text-[1.15rem]">
                {preguntaSiguiente ?? "La lengua"} →
              </span>
            </Link>
            {anterior && (
              <Link
                href={`/kaketiana/pueblo/${anterior.slug}`}
                className="kk-label inline-flex min-h-11 items-center self-start text-[0.6rem] tracking-[0.16em] text-(--sim-ink-soft) transition-colors hover:text-(--sim-rubrica)"
              >
                ← {anterior.titulo}
              </Link>
            )}
          </nav>
        </article>
      </div>
    </>
  );
}
