import Link from "next/link";
import { generoLegible, getBibliografia } from "@/lib/wiki";
import { obrasDelArticulo } from "@/lib/articulo";
import Desplegable from "@/components/kaketiana/Desplegable";

// El pie de un artículo del wiki, del manual de Kaketiana (Vistas §02): «sobre
// qué se sostiene este artículo» y la tarjeta de lo que sigue. Lo comparten el
// ensayo del pueblo y la obra de consulta de la lengua.

const OBRAS_VISIBLES = 6;

const plural = (n: number, uno: string, varios: string) => `${n} ${n === 1 ? uno : varios}`;

interface ObraCitada {
  slug: string;
  corto: string;
  genero: string | null;
}

/** Las obras del artículo, juntadas con la bibliografía: «Arcaya 1920 · crónica». */
export function obrasCitadas(cuerpo: string, fuentes: { slug: string; titulo: string }[]): ObraCitada[] {
  const biblio = new Map(getBibliografia().map((o) => [o.slug, o]));
  return obrasDelArticulo(cuerpo, fuentes).map((slug) => {
    const o = biblio.get(slug);
    const titulo = o?.titulo ?? fuentes.find((f) => f.slug === slug)?.titulo ?? slug;
    return { slug, corto: titulo.split(" — ")[0], genero: generoLegible(o?.genero ?? null) };
  });
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

/** Obra y disciplina, las primeras seis a la vista y el resto a un clic. */
export function SobreQueSeSostiene({ obras, className = "" }: { obras: ObraCitada[]; className?: string }) {
  if (obras.length === 0) return null;
  return (
    <section className={`border-t-2 border-(--sim-ink) pt-[22px] ${className}`}>
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
  );
}

/** La tarjeta de lo que sigue y, debajo, el enlace al anterior. */
export function SeguirLeyendo({
  siguiente,
  anterior,
  className = "",
}: {
  siguiente: { href: string; etiqueta: string; titulo: string };
  anterior?: { href: string; titulo: string } | null;
  className?: string;
}) {
  return (
    <nav aria-label="Seguir leyendo" className={`flex flex-col gap-3 ${className}`}>
      <Link
        href={siguiente.href}
        className="flex flex-col gap-2 rounded-2xl border border-(--sim-rule) px-5 py-4 transition-colors duration-300 hover:border-(--sim-rubrica) sm:flex-row sm:items-baseline sm:justify-between sm:gap-6 sm:px-[26px] sm:py-5"
      >
        <span className="kk-label shrink-0 text-[0.6rem] tracking-[0.2em] text-(--sim-ink-soft)">
          {siguiente.etiqueta}
        </span>
        <span className="sim-display text-[1.05rem] leading-snug text-(--sim-ink) sm:text-right sm:text-[1.15rem]">
          {siguiente.titulo} →
        </span>
      </Link>
      {anterior && (
        <Link
          href={anterior.href}
          className="kk-label inline-flex min-h-11 items-center self-start text-[0.6rem] tracking-[0.16em] text-(--sim-ink-soft) transition-colors hover:text-(--sim-rubrica)"
        >
          ← {anterior.titulo}
        </Link>
      )}
    </nav>
  );
}
