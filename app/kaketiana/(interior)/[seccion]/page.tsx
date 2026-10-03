import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getWikiPorSeccion } from "@/lib/wiki";
import CompendioLengua from "@/components/kaketiana/CompendioLengua";
import { SECCIONES_WIKI, type SeccionWiki } from "@/types/wiki";
import { Overline } from "@/components/simulador/ui";

// Las dos puertas de la portada (manual de Kaketiana): el pueblo es ensayo,
// la lengua es obra de consulta. La portada ya no lista los artículos — los
// lista aquí, cada sección con su densidad. La lengua es además el compendio:
// el diccionario y los topónimos entran por su puerta (CompendioLengua).

interface SeccionProps {
  params: Promise<{ seccion: string }>;
}

const PUERTA: Record<SeccionWiki, { overline: string; titulo: string }> = {
  pueblo: { overline: "El pueblo · ensayo", titulo: "Preguntas de fondo" },
  lengua: { overline: "La lengua · referencia", titulo: "Obra de consulta" },
};

function esSeccion(s: string): s is SeccionWiki {
  return s === "pueblo" || s === "lengua";
}

export function generateStaticParams() {
  return [{ seccion: "pueblo" }, { seccion: "lengua" }];
}

export const dynamicParams = false;

export async function generateMetadata({ params }: SeccionProps): Promise<Metadata> {
  const { seccion } = await params;
  if (!esSeccion(seccion)) return { title: "No encontrado | Curiana Radio" };
  return {
    title: `${SECCIONES_WIKI[seccion].label} — Kaketiana | Curiana Radio`,
    description: SECCIONES_WIKI[seccion].desc,
  };
}

export default async function SeccionPage({ params }: SeccionProps) {
  const { seccion } = await params;
  if (!esSeccion(seccion)) notFound();
  const lista = getWikiPorSeccion(seccion);
  if (seccion === "lengua") return <CompendioLengua articulos={lista} />;
  const info = SECCIONES_WIKI[seccion];

  return (
    <article className="mx-auto max-w-[760px]">
      <Link
        href="/kaketiana"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← Kaketiana
      </Link>
      <header className="mt-6">
        <Overline>
          {PUERTA[seccion].overline} · {lista.length} artículos
        </Overline>
        <h2 className="mt-2 sim-display text-4xl font-semibold leading-tight text-(--sim-ink)">
          {PUERTA[seccion].titulo}
        </h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">{info.desc}</p>
      </header>

      <ul className="mt-8">
        {lista.map((p) => (
          <li key={p.slug} className="border-t border-(--sim-rule) first:border-t-0">
            <Link href={`/kaketiana/${seccion}/${p.slug}`} className="group block py-4">
              <h3 className="sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                {p.titulo}
              </h3>
              <p className="mt-0.5 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{p.resumen}</p>
            </Link>
          </li>
        ))}
      </ul>

      <p className="mt-10 font-sans text-sm text-(--sim-ink-soft)">
        <Link href="/kaketiana/no-sabemos" className="font-medium text-(--sim-fuego) hover:text-(--sim-rubrica)">
          Lo que no sabemos →
        </Link>
      </p>
    </article>
  );
}
