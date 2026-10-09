import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";
import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";
import { idYouTube } from "@/lib/youtube";
import { VOZ } from "./voces";

// La prosa de una señal. Ninguna clase nombra una piel: todo sale de los
// alias --e-* (globals.css, «El motor de pieles»), así que el mismo cuerpo
// se lee en la noche, en la sal, en el dial, en la sala o en el telón.
// El contenedor es .senal-cuerpo: cada bloque a 65ch, las figuras hasta lo
// que diga la piel (--e-figura-max) y la capitular si la piel la tiene.
//
// Además del markdown, una señal puede usar:
//   <Figura src="…" alt="…" pie="…" />   una imagen con su pie (Vercel Blob)
//   <Video id="…" titulo="…" />          un video de YouTube (id o URL)

const externo = (href: string) => /^https?:\/\//.test(href);

function Enlace({ href = "", children }: ComponentProps<"a">) {
  return externo(href) ? (
    <a href={href} target="_blank" rel="noopener noreferrer" className={VOZ.enlace}>
      {children}
    </a>
  ) : (
    <Link href={href} className={VOZ.enlace}>
      {children}
    </Link>
  );
}

export function Figura({ src, alt, pie }: { src: string; alt: string; pie?: ReactNode }) {
  return (
    <figure className="m-0 flex w-full flex-col gap-2.5">
      {/* eslint-disable-next-line @next/next/no-img-element -- archivos de Vercel Blob servidos tal cual, como la galería */}
      <img
        src={src}
        alt={alt}
        loading="lazy"
        decoding="async"
        className="block h-auto w-full rounded-(--e-radio) bg-(--e-placa)"
      />
      {pie && (
        <figcaption className="max-w-[65ch] font-mono text-xs leading-relaxed tracking-[0.06em] text-(--e-texto-2)">
          {pie}
        </figcaption>
      )}
    </figure>
  );
}

// El aviso de un <Video> que no es de YouTube se ve en local y en las vistas
// previas del PR, donde Miguel revisa la señal; en producción la señal sale
// sin esa figura.
const AVISAR = process.env.NODE_ENV !== "production" || process.env.VERCEL_ENV === "preview";

export function Video({ id, titulo = "Video de Curiana Radio" }: { id: string; titulo?: string }) {
  const video = idYouTube(id);
  if (!video) {
    console.warn(`<Video>: «${String(id)}» no es un id ni una URL de YouTube; la señal sale sin el video`);
    return AVISAR ? (
      <div
        role="note"
        className="w-full rounded-(--e-radio) border border-dashed border-(--e-filete) bg-(--e-placa) px-4 py-3 font-mono text-xs leading-relaxed text-(--e-texto-2)"
      >
        &lt;Video&gt;: «{String(id)}» no es un id ni una URL de YouTube. Así no se incrusta: en producción esta
        figura no sale.
      </div>
    ) : null;
  }
  return (
    <figure className="m-0 w-full">
      <div className="relative aspect-video overflow-hidden rounded-(--e-radio) border border-(--e-filete) bg-(--e-placa)">
        {/* youtube-nocookie: el video no deja cookies hasta que alguien le da play */}
        <iframe
          src={`https://www.youtube-nocookie.com/embed/${video}`}
          title={titulo}
          loading="lazy"
          allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
          className="absolute inset-0 h-full w-full border-0"
        />
      </div>
    </figure>
  );
}

const h2 = ({ children }: ComponentProps<"h2">) => (
  <h2 className={`m-0 mt-2.5 text-[1.55em] leading-[1.2] text-(--e-texto) ${VOZ.h2}`}>{children}</h2>
);

const componentes = {
  // el h1 es el título de la señal: en el cuerpo, un # baja a h2
  h1: h2,
  h2,
  // el h3 habla en la voz del cuerpo, no en la display
  h3: ({ children }: ComponentProps<"h3">) => (
    <h3 className="m-0 mt-1 text-[1.05em] font-semibold leading-[1.3] text-(--e-texto)">{children}</h3>
  ),
  // [line-height:inherit]: la regla base `article p` (globals.css) le pondría 1.75 a toda piel
  p: ({ children }: ComponentProps<"p">) => <p className="m-0 [line-height:inherit] [text-wrap:pretty]">{children}</p>,
  a: Enlace,
  blockquote: ({ children }: ComponentProps<"blockquote">) => (
    <blockquote
      className={`my-2 bg-(--e-cita-fondo) px-[22px] py-[18px] text-[1.2em] leading-[1.5] text-(--e-texto) [border-left:var(--e-cita-ancho)_solid_var(--e-riel)] [border-radius:var(--e-radio-cita)] ${VOZ.cita} [&_p+p]:mt-3`}
    >
      {children}
    </blockquote>
  ),
  ul: ({ children }: ComponentProps<"ul">) => (
    <ul className="m-0 flex list-disc flex-col gap-2 pl-[1.2em] marker:text-(--e-texto-2)">{children}</ul>
  ),
  ol: ({ children }: ComponentProps<"ol">) => (
    <ol className="m-0 flex list-decimal flex-col gap-2 pl-[1.2em] marker:text-(--e-texto-2)">{children}</ol>
  ),
  li: ({ children }: ComponentProps<"li">) => <li className="pl-1">{children}</li>,
  hr: () => (
    <div aria-hidden="true" className="text-center tracking-[0.6em] text-(--e-texto-2)">
      · · ·
    </div>
  ),
  img: ({ src, alt }: ComponentProps<"img">) => <Figura src={String(src ?? "")} alt={alt ?? ""} />,
  Figura,
  Video,
};

export default function SenalMdx({ source, capitular }: { source: string; capitular: boolean }) {
  return (
    <div
      className={`senal-cuerpo flex flex-col gap-[22px] break-words text-(--e-texto) ${VOZ.cuerpo}`}
      data-capitular={capitular || undefined}
    >
      <MDXRemote source={source} components={componentes} options={{ mdxOptions: { remarkPlugins: [remarkGfm] } }} />
    </div>
  );
}
