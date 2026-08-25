import Link from "next/link";
import type { Metadata } from "next";
import { getBibliografia } from "@/lib/wiki";
import type { ObraBiblio } from "@/types/wiki";
import { Overline, EmptyState } from "@/components/simulador/ui";

export const metadata: Metadata = {
  title: "Bibliografía — Kaketiana | Curiana Radio",
  description:
    "Las obras sobre las que se sostiene todo lo demás: crónicas del siglo XVI, glosarios, arqueología y lingüística comparada, con dónde leer cada una.",
};

// ⚠️ ANDAMIO — funcional, sin diseñar. Ver el brief de secciones.
// El id del <li> es el ancla a la que llegan las citas de los artículos
// (`/kaketiana/bibliografia#alvarado-1921`), así que no se puede cambiar sin
// romper los enlaces que genera export_wiki_seed.py.
function Obra({ obra }: { obra: ObraBiblio }) {
  const ficha = [obra.autor, obra.anio, obra.publicacion].filter(Boolean).join(" · ");
  return (
    <li id={obra.slug} className="scroll-mt-24 border-t border-(--sim-rule) py-5 first:border-t-0">
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
        <h3 className="sim-display text-lg font-semibold text-(--sim-ink)">{obra.obra}</h3>
        {obra.genero && (
          <span className="font-sans text-[0.65rem] uppercase tracking-[0.1em] text-(--sim-ink-faint)">
            {obra.genero}
          </span>
        )}
      </div>
      {ficha && <p className="mt-0.5 font-sans text-sm text-(--sim-ink-faint)">{ficha}</p>}
      {obra.aporta && (
        <p className="mt-2 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          {obra.aporta}
        </p>
      )}
      {obra.lectura_url ? (
        <a
          href={obra.lectura_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-flex items-center gap-1.5 font-sans text-sm font-semibold text-(--sim-fuego) transition-colors hover:text-(--sim-rubrica)"
        >
          Leer la fuente <span aria-hidden="true">↗</span>
        </a>
      ) : (
        obra.acceso && (
          <p className="mt-2 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
            {obra.acceso}
          </p>
        )
      )}
    </li>
  );
}

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

  return (
    <article className="mx-auto max-w-[760px]">
      <Link
        href="/kaketiana"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← Kaketiana
      </Link>

      <header className="mt-5">
        <Overline>De dónde lo sabemos</Overline>
        <h1 className="mt-1 sim-display text-3xl font-bold tracking-tight text-(--sim-ink) md:text-4xl">
          Bibliografía
        </h1>
        <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          Las <strong className="text-(--sim-ink)">{obras.length} obras</strong> sobre las que
          se sostiene todo lo demás: crónicas del siglo XVI, glosarios del XIX y XX,
          arqueología y lingüística comparada. <strong className="text-(--sim-ink)">{conLectura}</strong>{" "}
          se pueden leer en línea; el resto está en papel o tras el muro de un editor,
          y se dice cuál es cuál.
        </p>
      </header>

      <ul className="mt-8">
        {obras.map((o) => (
          <Obra key={o.slug} obra={o} />
        ))}
      </ul>
    </article>
  );
}
