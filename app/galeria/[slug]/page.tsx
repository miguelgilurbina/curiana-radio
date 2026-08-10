import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import ImagenObra from "@/components/galeria/ImagenObra";
import {
  getBlobBase,
  getObra,
  getSeries,
  getSlugs,
  getVecinas,
} from "@/lib/galeria";
import { urlVariante } from "@/types/galeria";

interface ObraPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getSlugs().map((slug) => ({ slug }));
}

export const dynamicParams = false;

export async function generateMetadata({
  params,
}: ObraPageProps): Promise<Metadata> {
  const { slug } = await params;
  const obra = getObra(slug);
  if (!obra) return { title: "Obra no encontrada | Curiana Radio" };
  const blobBase = getBlobBase();
  const mayor = obra.anchos[obra.anchos.length - 1];
  const og = mayor ? urlVariante(blobBase, obra.slug, mayor) : null;
  const descripcion = (obra.concepto || obra.alt).slice(0, 160);
  return {
    title: `${obra.titulo} — Galería | Curiana Radio`,
    description: descripcion,
    openGraph: {
      title: `${obra.titulo} — Galería | Curiana Radio`,
      description: descripcion,
      images: og ? [{ url: og, alt: obra.alt }] : undefined,
    },
  };
}

export default async function ObraPage({ params }: ObraPageProps) {
  const { slug } = await params;
  const obra = getObra(slug);
  if (!obra) notFound();

  const blobBase = getBlobBase();
  const serie = getSeries().find((s) => s.id === obra.serie);
  const { anterior, siguiente } = getVecinas(slug);
  const proporcion = obra.w && obra.h ? obra.w / obra.h : 4 / 5;

  return (
    <article className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      <Link
        href="/galeria"
        className="font-sans text-sm text-earth-600 transition-colors hover:text-frequency"
      >
        ← Galería
      </Link>

      <div
        className="relative mt-6 w-full overflow-hidden rounded-sm"
        style={{ aspectRatio: `${proporcion}`, backgroundColor: obra.color }}
      >
        <ImagenObra
          obra={obra}
          blobBase={blobBase}
          prioridad
          sizes="(max-width: 1024px) 100vw, 1024px"
          className="h-full w-full object-contain"
        />
      </div>

      <div className="mt-10 grid gap-10 lg:grid-cols-[1fr_18rem]">
        {/* Lectura principal */}
        <div>
          {serie && (
            <div className="mb-3 font-sans text-xs tracking-[0.2em] uppercase text-earth-600">
              {serie.titulo}
            </div>
          )}
          <h1 className="mb-5 font-serif text-4xl leading-tight text-deep-900 md:text-5xl">
            {obra.titulo}
          </h1>
          {obra.concepto && (
            <p className="max-w-reading font-sans text-lg leading-relaxed text-earth-800">
              {obra.concepto}
            </p>
          )}

          {/* El prompt ya no se publica. 72 de las 821 obras nombran a un
              artista en el suyo ("in the style of…"), y apoyar la ficha en el
              nombre de otro no es describir la obra. El texto de arriba sale
              de mirar la imagen — ver scripts/galeria-describir.mjs. */}

          {obra.procedencia.posproceso && (
            <section className="mt-8">
              <h2 className="mb-2 font-sans text-xs tracking-[0.2em] uppercase text-earth-600">
                Proceso
              </h2>
              <p className="max-w-reading font-sans text-sm leading-relaxed text-earth-700">
                {obra.procedencia.posproceso}
              </p>
            </section>
          )}
        </div>

        {/* Ficha técnica */}
        <aside className="space-y-6 border-t border-earth-200 pt-6 lg:border-l lg:border-t-0 lg:pl-8 lg:pt-0">
          <Dato etiqueta="Herramienta">{obra.procedencia.herramienta}</Dato>
          <Dato etiqueta="Año">{obra.anio}</Dato>
          {obra.w && obra.h && (
            <Dato etiqueta="Dimensiones">
              {obra.w} × {obra.h}
            </Dato>
          )}
          {obra.estado === "pendiente" && (
            <Dato etiqueta="Estado">Concepto sin render</Dato>
          )}
          {obra.edicion && (
            <Dato etiqueta="Edición">
              <Link
                href={`/${obra.edicion}`}
                className="border-b border-earth-300 transition-colors hover:border-frequency hover:text-frequency"
              >
                #{obra.edicion}
              </Link>
            </Dato>
          )}

          {/* La licencia vive en el manifest pero no se muestra todavía: la
              galería es, por ahora, un sitio donde enseñar el trabajo. Cuando
              haya algo que ofrecer, el dato ya está etiquetado obra por obra. */}

          {obra.tags.length > 0 && (
            <div>
              <div className="mb-2 font-sans text-xs tracking-[0.2em] uppercase text-earth-500">
                Motivos
              </div>
              <div className="flex flex-wrap gap-2">
                {obra.tags.map((tag) => (
                  <span
                    key={tag}
                    className="border border-earth-200 px-2 py-0.5 font-sans text-xs text-earth-700"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </aside>
      </div>

      <nav className="mt-14 flex items-center justify-between gap-4 border-t border-earth-200 pt-6 font-sans text-sm">
        {anterior ? (
          <Link
            href={`/galeria/${anterior.slug}`}
            className="text-earth-700 transition-colors hover:text-frequency"
          >
            ← {anterior.titulo}
          </Link>
        ) : (
          <span />
        )}
        {siguiente ? (
          <Link
            href={`/galeria/${siguiente.slug}`}
            className="text-right text-earth-700 transition-colors hover:text-frequency"
          >
            {siguiente.titulo} →
          </Link>
        ) : (
          <span />
        )}
      </nav>
    </article>
  );
}

function Dato({
  etiqueta,
  children,
}: {
  etiqueta: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <div className="mb-1 font-sans text-xs tracking-[0.2em] uppercase text-earth-500">
        {etiqueta}
      </div>
      <div className="font-sans text-sm text-earth-800">{children}</div>
    </div>
  );
}
