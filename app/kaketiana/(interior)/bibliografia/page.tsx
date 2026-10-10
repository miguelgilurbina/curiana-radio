import Link from "next/link";
import type { Metadata } from "next";
import { anioDe, autorCortoDe, generoLegible, getBibliografia, grupoDeGenero, GRUPOS_BIBLIO } from "@/lib/wiki";
import { getFichasPorObra } from "@/lib/fichas";
import { EmptyState } from "@/components/simulador/ui";
import BibliografiaViva, { type EntradaBiblio } from "@/components/kaketiana/BibliografiaViva";
import { metadatos, tarjeta } from "@/lib/seo";

export const metadata: Metadata = metadatos({
  titulo: "Bibliografía — Kaketiana | Curiana Radio",
  descripcion:
    "Las obras sobre las que se sostiene todo lo demás: crónicas del siglo XVI, glosarios, arqueología y lingüística comparada, con dónde leer cada una.",
  ruta: "/kaketiana/bibliografia",
  imagen: tarjeta("kaketiana/bibliografia", "Kaketiana · bibliografía"),
});

// La bibliografía del manual de Kaketiana (Vistas §04): de la crónica a hoy,
// en orden de año, con el filtro por disciplina y el Ancla para quien llega
// desde una cita (components/kaketiana/BibliografiaViva.tsx). Todo sale de
// content/wiki/bibliografia.json (export_wiki_seed.py): ninguna cifra a mano.

const orden = (anio: string | null) => (anio ? Number(anio.slice(0, 4)) : Number.POSITIVE_INFINITY);

export default function BibliografiaPage() {
  const obras = getBibliografia();

  if (obras.length === 0) {
    return (
      <EmptyState
        title="Aún no hay bibliografía"
        hint="Corre export_wiki_seed.py en proyecto-linguistico-caquetío/curiana_sim/."
      />
    );
  }

  const conLectura = obras.filter((o) => o.lectura_url).length;
  // Qué voces del diccionario cita cada obra: el enlace de vuelta a las fichas.
  const porObra = getFichasPorObra();

  const entradas: EntradaBiblio[] = obras
    .map((o) => ({
      slug: o.slug,
      anio: anioDe(o),
      autor: autorCortoDe(o),
      obra: o.obra,
      genero: generoLegible(o.genero),
      grupo: grupoDeGenero(o.genero),
      publicacion: o.publicacion,
      aporta: o.aporta || null,
      acceso: o.acceso,
      lectura_url: o.lectura_url,
      voces: (porObra.get(o.slug) ?? []).map(({ slug, forma, capa }) => ({ slug, forma, capa })),
    }))
    .sort((a, b) => orden(a.anio) - orden(b.anio) || a.autor.localeCompare(b.autor, "es"));

  const grupos = GRUPOS_BIBLIO.map((g) => ({
    clave: g.clave,
    label: g.label,
    n: entradas.filter((e) => e.grupo === g.clave).length,
  })).filter((g) => g.n > 0);

  return (
    // Un <div> y no un <article>: la bibliografía no es un artículo, y la regla
    // base `article p` le metía 1,5rem bajo cada línea de cada obra.
    <div className="mx-auto max-w-[78ch]">
      <Link
        href="/kaketiana"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-rubrica)"
      >
        ← Kaketiana
      </Link>

      <header className="mt-6 flex flex-wrap items-baseline gap-x-5 gap-y-2">
        <h1 className="sim-display text-[2rem] font-semibold leading-none tracking-tight text-(--sim-ink) sm:text-[2.4rem]">
          Bibliografía
        </h1>
        <p className="kk-label text-[0.62rem] tracking-[0.16em] text-(--sim-ink-soft)">
          {obras.length} obras · {conLectura} con lectura en línea · el resto dice dónde está
        </p>
      </header>
      <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
        Las obras sobre las que se sostiene todo lo demás, de la crónica del siglo XVI a la arqueología de
        hoy. Cada cita de los artículos llega aquí, a su obra.
      </p>

      <div className="mt-8">
        <BibliografiaViva obras={entradas} grupos={grupos} />
      </div>
    </div>
  );
}
