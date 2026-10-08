import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { AUTOR, fechaCorta, getSenal, getSenales, vecinas } from "@/lib/senales";
import { PORTAFOLIO, REDES } from "@/lib/redes";
import SenalMdx from "@/components/senales/senal-mdx";
import Etiquetas from "@/components/senales/Etiquetas";
import InterruptorLuz from "@/components/senales/InterruptorLuz";
import { PIELES } from "@/components/senales/pieles";
import { VOZ } from "@/components/senales/voces";
import FinDeLectura from "@/components/analitica/FinDeLectura";

interface Props {
  params: Promise<{ slug: string }>;
}

export function generateStaticParams() {
  return getSenales().map((s) => ({ slug: s.slug }));
}

export const dynamicParams = false;

// La imagen para compartir la pone opengraph-image.tsx (la tarjeta con el
// título): es lo que se ve cuando la señal se enlaza en LinkedIn o WhatsApp.
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const senal = getSenal(slug);
  if (!senal) return {};
  return {
    title: `${senal.titulo} — Señales · Curiana Radio`,
    description: senal.sumario,
    authors: [{ name: senal.autor }],
    alternates: { canonical: `/senales/${senal.slug}` },
    robots: senal.borrador ? { index: false, follow: false } : undefined,
    openGraph: {
      title: senal.titulo,
      description: senal.sumario,
      type: "article",
      publishedTime: senal.fecha,
      authors: [senal.autor],
      siteName: "Curiana Radio",
      locale: "es",
    },
    twitter: { card: "summary_large_image", title: senal.titulo, description: senal.sumario },
  };
}

// La plantilla del motor de pieles (design_handoff_senales_luces): la misma
// estructura para toda señal —miga e interruptor, borrador, título, sumario,
// dato, portada, cuerpo a 65ch, firma, nota y pie— y ninguna clase que nombre
// una piel. La piel sólo pone sus atributos de tema y `data-piel`; la tinta y
// las voces salen de los alias --e-* (globals.css, «El motor de pieles»).
export default async function SenalPagina({ params }: Props) {
  const { slug } = await params;
  const senal = getSenal(slug);
  if (!senal) notFound();
  const { anterior, siguiente } = vecinas(slug);
  const piel = PIELES[senal.piel];
  const { Antetitulo } = piel;
  const datoCabecera = `${VOZ.dato} text-(--e-cabecera-texto-2)`;
  const dato = `${VOZ.dato} text-(--e-texto-2)`;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    headline: senal.titulo,
    description: senal.sumario,
    datePublished: senal.fecha,
    author: {
      "@type": "Person",
      name: senal.autor,
      ...(senal.autor === AUTOR ? { url: PORTAFOLIO.url } : {}),
    },
    publisher: { "@type": "Organization", name: "Curiana Radio", url: "https://curianaradio.com" },
    mainEntityOfPage: `https://curianaradio.com/senales/${senal.slug}`,
    ...(senal.portada ? { image: senal.portada.src } : {}),
  };

  return (
    <article {...piel.atributos} data-piel={piel.id} className={`min-h-screen animate-fade-in ${piel.raiz ?? ""}`}>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      {/* lo que la piel necesita antes del primer pintado (la semilla del dial) */}
      {piel.script && <script dangerouslySetInnerHTML={{ __html: piel.script }} />}

      <header className={`bg-(--e-cabecera-fondo) ${piel.cabecera ?? ""}`}>
        {Antetitulo && <Antetitulo />}
        <div className="mx-auto flex max-w-[65ch] flex-col gap-[18px] px-6 pt-10 pb-12 sm:pt-14 sm:pb-14">
          <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-1">
            <nav aria-label="Miga" className={`flex flex-wrap items-center gap-x-3 ${datoCabecera}`}>
              <Link href="/senales" className={VOZ.accion}>
                Señales
              </Link>
              <span aria-hidden="true">/</span>
              <Etiquetas aristas={senal.aristas} clase={datoCabecera} hover={VOZ.accion} />
            </nav>
            <InterruptorLuz
              nativo={piel.nativo}
              alterno={piel.alterno}
              activo="text-(--e-cabecera-texto)"
              className={datoCabecera}
            />
          </div>
          {senal.borrador && (
            <span className={`self-start border border-dashed border-current px-2.5 py-1.5 ${datoCabecera}`}>
              Borrador · vista previa
            </span>
          )}
          <h1
            className={`m-0 max-w-[20ch] text-[clamp(2.2rem,5.4vw,3.5rem)] leading-[1.08] text-balance text-(--e-titulo) ${VOZ.titulo}`}
          >
            {senal.titulo}
          </h1>
          <p
            className={`m-0 max-w-[46ch] text-[clamp(1.1rem,2.2vw,1.35rem)] leading-[1.5] [text-wrap:pretty] text-(--e-cabecera-texto-2) ${VOZ.sumario}`}
          >
            {senal.sumario}
          </p>
          <p className={`m-0 ${datoCabecera}`}>
            {senal.autor} · <time dateTime={senal.fecha}>{fechaCorta(senal.fecha)}</time> · {senal.minutos} min
          </p>
        </div>
      </header>

      {senal.portada && (
        <figure className="mx-auto mt-12 flex max-w-[72rem] flex-col gap-2.5 px-6 sm:mt-14">
          {/* eslint-disable-next-line @next/next/no-img-element -- Vercel Blob tal cual, como la galería */}
          <img
            src={senal.portada.src}
            alt={senal.portada.alt}
            className="block h-auto max-h-[80vh] w-full rounded-(--e-radio) bg-(--e-placa) object-cover"
          />
          {senal.portada.pie && (
            <figcaption className="mx-auto w-full max-w-[65ch] font-mono text-xs leading-relaxed tracking-[0.06em] text-(--e-texto-2)">
              {senal.portada.pie}
            </figcaption>
          )}
        </figure>
      )}

      <div className="px-6 pt-12 sm:pt-14">
        <SenalMdx source={senal.cuerpo} capitular={piel.capitular} />
        {/* el final del cuerpo: aquí cuenta la lectura completa (MEDICION.md) */}
        <FinDeLectura pagina={`/senales/${senal.slug}`} />

        <div className={`mx-auto mt-[22px] flex max-w-[65ch] flex-col gap-[22px] ${VOZ.cuerpo}`}>
          {/* la firma de Miguel lleva a «Quién transmite» */}
          <p className={`m-0 text-[1.1em] text-(--e-texto) ${VOZ.sumario}`}>
            —{" "}
            {senal.autor === AUTOR ? (
              <Link href="/sobre" className={VOZ.accion}>
                {senal.autor}
              </Link>
            ) : (
              senal.autor
            )}
          </p>

          {/* Lo que una señal diga de los caquetíos es la voz de su autor, no
              el canon: la investigación, con sus fuentes, vive en Kaketiana. */}
          {senal.aristas.includes("kaketiana") && (
            <p className="m-0 border-t border-(--e-filete) pt-3.5 text-[0.85em] leading-[1.6] text-(--e-texto-2)">
              Esta señal es la voz de su autor. Lo que la investigación sostiene sobre los caquetíos, con cada fuente a
              la vista, está en{" "}
              <Link href="/kaketiana" className={VOZ.enlace}>
                Kaketiana
              </Link>
              .
            </p>
          )}
        </div>
      </div>

      <footer className="mt-14 border-t border-(--e-filete) px-6 pt-6 pb-10 sm:mt-16">
        <div className={`mx-auto flex max-w-[65ch] flex-col gap-[18px] ${dato}`}>
          {(anterior || siguiente) && (
            <nav aria-label="Otras señales" className="flex flex-wrap justify-between gap-4">
              {anterior ? (
                <Link href={`/senales/${anterior.slug}`} className={`text-(--e-texto) ${VOZ.accion}`}>
                  ← Anterior · {anterior.titulo}
                </Link>
              ) : (
                <span />
              )}
              {siguiente && (
                <Link href={`/senales/${siguiente.slug}`} className={`text-(--e-texto) ${VOZ.accion}`}>
                  Siguiente · {siguiente.titulo} →
                </Link>
              )}
            </nav>
          )}
          <div className="flex flex-wrap items-center justify-between gap-4">
            <Link href="/senales" className={VOZ.accion}>
              ← Todas las señales
            </Link>
            <span className="flex flex-wrap items-center gap-4">
              {REDES.map((r) => (
                <a key={r.nombre} href={r.url} target="_blank" rel="noopener noreferrer" className={VOZ.accion}>
                  {r.nombre}
                </a>
              ))}
              <span className="normal-case">@curianaradio</span>
            </span>
          </div>
        </div>
      </footer>
    </article>
  );
}
