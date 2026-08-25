import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getWikiPagina, getWikiParams, getVecinos } from "@/lib/wiki";
import { SECCIONES_WIKI, type SeccionWiki } from "@/types/wiki";
import { Overline } from "@/components/simulador/ui";
import { WikiProse } from "@/components/simulador/wiki-mdx";

interface ArticuloProps {
  params: Promise<{ seccion: string; slug: string }>;
}

export async function generateStaticParams() {
  return getWikiParams();
}

export const dynamicParams = false;

function esSeccion(s: string): s is SeccionWiki {
  return s === "pueblo" || s === "lengua";
}

export async function generateMetadata({ params }: ArticuloProps): Promise<Metadata> {
  const { seccion, slug } = await params;
  if (!esSeccion(seccion)) return { title: "No encontrado | Curiana Radio" };
  const p = getWikiPagina(seccion, slug);
  if (!p) return { title: "No encontrado | Curiana Radio" };
  return {
    title: `${p.titulo} — Kaketiana | Curiana Radio`,
    description: p.resumen,
  };
}

export default async function ArticuloPage({ params }: ArticuloProps) {
  const { seccion, slug } = await params;
  if (!esSeccion(seccion)) notFound();
  const pagina = getWikiPagina(seccion, slug);
  if (!pagina) notFound();

  const info = SECCIONES_WIKI[seccion];
  const { anterior, siguiente } = getVecinos(seccion, slug);

  // `lengua` es material de referencia: 20% de sus líneas son tabla. `pueblo`
  // es prosa larga con citas de crónicas. Por ahora comparten plantilla y solo
  // cambia el ancho de la columna; separarlos de verdad es trabajo de diseño.
  const anchoColumna = seccion === "lengua" ? "max-w-[860px]" : "max-w-[720px]";

  return (
    <article className={`mx-auto ${anchoColumna}`}>
      <Link
        href="/kaketiana"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← Kaketiana
      </Link>

      <header className="mt-5">
        <Overline>{info.label}</Overline>
        <h1 className="mt-1 sim-display text-3xl font-bold tracking-tight text-(--sim-ink) md:text-4xl">
          {pagina.titulo}
        </h1>
      </header>

      <div className="mt-8">
        <WikiProse source={pagina.cuerpo} />
      </div>

      {/* Sobre qué se sostiene — rescatado del preámbulo del ensayo */}
      {pagina.fuentes.length > 0 && (
        <section className="mt-12 border-t border-(--sim-rule) pt-6">
          <Overline>Sobre qué se sostiene</Overline>
          <ul className="mt-3 flex flex-wrap gap-x-2 gap-y-1.5 font-sans text-sm">
            {pagina.fuentes.map((f, i) => (
              <li key={f.slug}>
                <Link
                  href={`/kaketiana/bibliografia#${f.slug}`}
                  className="text-(--sim-ink-soft) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:text-(--sim-fuego)"
                >
                  {f.titulo}
                </Link>
                {i < pagina.fuentes.length - 1 && (
                  <span aria-hidden="true" className="ml-2 text-(--sim-rule)">·</span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      <nav className="mt-14 flex items-start justify-between gap-6 border-t border-(--sim-rule) pt-6 font-sans text-sm">
        {anterior ? (
          <Link
            href={`/kaketiana/${seccion}/${anterior.slug}`}
            className="max-w-[45%] text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
          >
            ← {anterior.titulo}
          </Link>
        ) : (
          <span />
        )}
        {siguiente && (
          <Link
            href={`/kaketiana/${seccion}/${siguiente.slug}`}
            className="max-w-[45%] text-right text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
          >
            {siguiente.titulo} →
          </Link>
        )}
      </nav>
    </article>
  );
}
