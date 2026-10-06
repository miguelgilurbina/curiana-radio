import type { Metadata } from "next";
import type { CSSProperties } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import MarcoWiki from "@/components/jai-sounds/wiki/MarcoWiki";
import { Datos, DosVoces, Generos, Riel, Rotulo, SiguePor, type Tarjeta } from "@/components/jai-sounds/wiki/piezas";
import { album, artista, cancion, conVozDeJai, duracion, estaciones, imagenSocial, nombreArtista, portada, vecinas } from "@/lib/jai-wiki";
import { metadatos, TARJETA_JAI } from "@/lib/seo";

// Una página por canción, generada la primera vez que alguien la visita y
// servida estática desde ahí (son ~2.000: no se arman todas en el build).
export const dynamicParams = true;
export function generateStaticParams() {
  return [];
}

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const c = cancion((await params).slug);
  // notFound() aquí y no solo en la página: la metadata se resuelve antes de
  // transmitir, así el 404 llega como 404 y no como 200 con el aviso.
  if (!c) notFound();
  const de = c.a.map(nombreArtista).join(", ");
  return metadatos({
    titulo: `${c.t} — ${de} | JAI Sounds`,
    tituloSocial: `${c.t} — ${de}`,
    descripcion: `${c.t}, de ${de}, en el dial de JAI Sounds: dónde suena, qué suena antes y después, y lo que se sabe de ella.`,
    ruta: `/jai-sounds/canciones/${(await params).slug}`,
    imagen: imagenSocial(c.img, `${c.t}, de ${de}`) ?? TARJETA_JAI,
    noIndex: !conVozDeJai(c),
  });
}

export default async function CancionPage({ params }: Props) {
  const { slug } = await params;
  const c = cancion(slug);
  if (!c) notFound();

  const est = estaciones();
  const al = c.al ? album(c.al) : null;
  const mb = c.mb;
  // La fecha de MusicBrainz solo se afirma si es la MISMA grabación (por
  // ISRC). Por título puede ser otra edición: se muestra, pero se dice.
  const exacta = mb?.via === "isrc";
  const primera = exacta ? (mb?.f ?? null) : null;
  const difiere = primera && c.fecha && primera.slice(0, 4) !== c.fecha.slice(0, 4);
  // Si la grabación no trae géneros propios, los del primer artista (y se dice).
  const generosArtista = artista(c.a[0])?.mb?.g ?? [];
  const etiqueta = (s: string | null) => {
    const x = s ? cancion(s) : null;
    return x ? { t: x.t, a: x.a.map(nombreArtista).join(", "), href: `/jai-sounds/canciones/${s}` } : null;
  };

  const sigue: Tarjeta[] = [
    ...c.a.map((a) => ({ tipo: "artista", n: nombreArtista(a), sub: "quien la toca", href: `/jai-sounds/artistas/${a}` })),
    ...(al && c.al ? [{ tipo: "álbum", n: al.t, sub: [al.tipo, al.fecha?.slice(0, 4)].filter(Boolean).join(" · "), href: `/jai-sounds/albumes/${c.al}` }] : []),
    ...c.dial.map(([e]) => ({ tipo: `estación ${String(e + 1).padStart(2, "0")}`, n: est[e].nombre.toLowerCase(), sub: "la estación donde suena", href: `/jai-sounds#${String(e + 1).padStart(2, "0")}`, i: e })),
    ...(artista(c.a[0])?.cerca ?? []).slice(0, 3).map(([a, e]) => ({ tipo: "artista", n: nombreArtista(a), sub: `comparte ${est[e]?.nombre ?? "estación"}`, href: `/jai-sounds/artistas/${a}` })),
  ];
  const idPista = c.id;

  return (
    <MarcoWiki tipo="canción" punto={{ tipo: "cancion", slug, n: c.t }} color={c.dial[0]?.[0] ?? null}>
      <section className="grid items-end gap-x-12 gap-y-8 min-[820px]:grid-cols-[minmax(0,300px)_minmax(0,1fr)]">
        <div className="box-border aspect-square max-w-[220px] border-l-3 border-(--jai-senal) bg-(--jai-senal-tenue) min-[820px]:max-w-none">
          {c.img ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={portada(c.img, 640) ?? ""} alt={al ? `Portada de ${al.t}` : ""} className="block h-full w-full object-cover" />
          ) : null}
        </div>
        <div className="flex min-w-0 flex-col gap-[18px]">
          <span className="jai-dato text-[11px] text-(--jai-senal)">
            canción{c.n && al ? ` · pista ${c.n} de ${al.t.toLowerCase()}` : ""}
          </span>
          <h1 className="jai-titulo m-0 text-[clamp(36px,5vw,64px)] leading-[1.02] tracking-[-0.01em] text-balance text-(--jai-luz)">{c.t}</h1>
          <p className="jai-manifiesto m-0 flex flex-wrap items-baseline gap-x-3.5 gap-y-1 text-[22px]">
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">de</span>
            {c.a.map((a) => (
              <Link key={a} href={`/jai-sounds/artistas/${a}`} className="border-b border-(--jai-rule) text-(--jai-luz) transition-colors duration-300 hover:border-(--jai-senal)">
                {nombreArtista(a)}
              </Link>
            ))}
          </p>
          <Datos
            datos={[
              { k: "duración", v: duracion(c.ms) },
              { k: "primera edición", v: primera },
              { k: "álbum", v: al?.t ?? null, href: c.al ? `/jai-sounds/albumes/${c.al}` : undefined },
              { k: "spotify", v: c.fecha },
            ]}
          />
          {difiere ? (
            <p className="m-0 font-(family-name:--jai-mono) text-[11px] leading-[1.8] tracking-[0.12em] text-(--jai-luz-soft)">
              <span className="text-(--jai-senal)">≠</span> spotify dice {c.fecha}: es la fecha de la edición que tiene. musicbrainz guarda la primera, {primera}.
            </p>
          ) : null}
          {mb?.g.length ? <Generos generos={mb.g} /> : <Generos generos={generosArtista} de={`géneros de ${nombreArtista(c.a[0]).toLowerCase()}`} />}
          <div className="flex flex-col gap-3">
            <a
              href={c.spotify}
              target="_blank"
              rel="noopener noreferrer"
              className="self-start bg-(--jai-senal) px-[22px] py-[15px] font-sans text-[11px] font-semibold uppercase tracking-[0.2em] text-(--jai-noche) transition-colors duration-300 hover:bg-(--jai-luz)"
            >
              ▶ escuchar en spotify
            </a>
            <iframe
              title={`${c.t} en Spotify`}
              src={`https://open.spotify.com/embed/track/${idPista}?utm_source=generator&theme=0`}
              width="100%"
              height="80"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
              className="block max-w-[520px] border-0"
            />
          </div>
        </div>
      </section>

      <section aria-label="En el dial" className="flex flex-col gap-[18px]">
        <Rotulo derecha={`${c.dial.length} ${c.dial.length === 1 ? "estación" : "estaciones"} · la secuencia también es curaduría`}>en el dial</Rotulo>
        {c.dial.map(([e, pos, desde]) => {
          const es = est[e];
          const v = vecinas(e, pos);
          const antes = etiqueta(v.antes);
          const despues = etiqueta(v.despues);
          return (
            <div key={e} className="jai-estacion flex flex-col gap-3.5 border-b border-(--jai-rule) pb-[22px]" style={{ "--jai-i": e } as CSSProperties}>
              <Link href={`/jai-sounds#${String(e + 1).padStart(2, "0")}`} className="grid grid-cols-[56px_minmax(0,1fr)] items-center gap-4">
                {es.portada ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={es.portada} alt="" className="block aspect-square w-14 border-l-3 border-(--jai-senal) object-cover" />
                ) : (
                  <span className="block aspect-square w-14 border-l-3 border-(--jai-senal) bg-(--jai-senal-tenue)" />
                )}
                <span className="flex min-w-0 flex-col gap-[5px]">
                  <span className="jai-display text-2xl leading-none lowercase">{es.nombre}</span>
                  <span className="font-(family-name:--jai-mono) text-[11px] tracking-[0.2em] text-(--jai-luz-faint)">
                    <span className="text-(--jai-senal)">{String(e + 1).padStart(2, "0")}</span> · pista {String(pos).padStart(3, "0")} de {es.pistas.length}
                    {desde ? ` · en el dial desde ${desde}` : ""}
                  </span>
                </span>
              </Link>
              <div className="grid border border-(--jai-rule) min-[820px]:grid-cols-3">
                <Vecina dir="antes" v={antes} />
                <div className="flex min-w-0 flex-col gap-1 border-t-2 border-(--jai-senal) bg-(--jai-panel) px-3.5 py-3 min-[820px]:border-x min-[820px]:border-x-(--jai-rule)">
                  <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.3em] text-(--jai-senal)">esta · {String(pos).padStart(3, "0")}</span>
                  <span className="truncate text-sm font-medium">{c.t}</span>
                </div>
                <Vecina dir="despues" v={despues} />
              </div>
            </div>
          );
        })}
      </section>

      <DosVoces voces={c} cosa="esta canción" nombre={`${c.t} ${nombreArtista(c.a[0])}`} />

      <section aria-label="Ficha técnica" className="flex flex-col gap-[22px]">
        <Rotulo derecha={mb && !exacta ? "musicbrainz · por título" : "musicbrainz"}>ficha técnica</Rotulo>
        {mb && !exacta ? (
          <p className="m-0 max-w-[64ch] font-(family-name:--jai-mono) text-[11px] leading-[1.8] tracking-[0.12em] text-(--jai-luz-faint)">
            {"// musicbrainz no tiene el isrc de esta pista: la encontró por título, artista y duración. puede ser otra edición de la misma canción."}
          </p>
        ) : null}
        {mb === undefined ? (
          <Riel titulo="todavía no se le preguntó a musicbrainz">La próxima corrida del enriquecimiento la busca. Mientras, lo que hay es lo de Spotify.</Riel>
        ) : mb === null ? (
          <Riel titulo="musicbrainz no encontró esta grabación">
            Spotify sí la conoce: título, álbum, duración y fecha son todo lo que hay por ahora. El hilo sigue por el álbum y por quien la toca.
          </Riel>
        ) : (
          <div className="grid grid-cols-[repeat(auto-fit,minmax(min(100%,300px),1fr))] gap-x-12 gap-y-9">
            <div className="flex flex-col gap-3">
              <span className="jai-dato text-[10px] text-(--jai-luz-faint)">créditos</span>
              {mb.cr.length ? (
                mb.cr.map((cr, k) => (
                  <div key={`${cr.mbid}-${cr.rol}-${k}`} className="grid grid-cols-[96px_minmax(0,1fr)] items-baseline gap-3 border-b border-(--jai-rule) py-2">
                    <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.2em] text-(--jai-luz-faint)">{cr.rol}</span>
                    <span className="flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
                      {cr.a ? (
                        <Link href={`/jai-sounds/artistas/${cr.a}`} className="border-b border-(--jai-rule) text-[15px] transition-colors duration-300 hover:border-(--jai-senal)">
                          {cr.n}
                        </Link>
                      ) : (
                        <a href={`https://musicbrainz.org/artist/${cr.mbid}`} target="_blank" rel="noopener noreferrer" className="text-[15px] text-(--jai-luz-soft)" title="Fuera del dial: abre MusicBrainz">
                          {cr.n} <span className="text-[11px] text-(--jai-luz-faint)">↗</span>
                        </a>
                      )}
                      {cr.attrs.length ? <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.15em] text-(--jai-luz-faint)">{cr.attrs.join(", ")}</span> : null}
                    </span>
                  </div>
                ))
              ) : (
                <span className="text-sm text-(--jai-luz-faint)">MusicBrainz no trae créditos para esta grabación.</span>
              )}
            </div>
            <div className="flex flex-col gap-7">
              <div className="flex flex-col gap-2.5">
                <span className="jai-dato text-[10px] text-(--jai-luz-faint)">la obra</span>
                {mb.obras.length ? (
                  mb.obras.map((o) => (
                    <a key={o.mbid} href={`https://musicbrainz.org/work/${o.mbid}`} target="_blank" rel="noopener noreferrer" className="jai-titulo text-xl">
                      {o.titulo} <span className="font-sans text-xs text-(--jai-luz-faint)">↗</span>
                    </a>
                  ))
                ) : (
                  <span className="text-sm text-(--jai-luz-faint)">Sin obra enlazada.</span>
                )}
              </div>
              <div className="flex flex-col gap-0.5">
                <span className="jai-dato pb-2 text-[10px] text-(--jai-luz-faint)">ediciones</span>
                {mb.ed.length ? (
                  mb.ed.slice(0, 12).map((ed, k) => (
                    <div key={`${ed.t}-${ed.f}-${k}`} className="grid grid-cols-[96px_minmax(0,1fr)_auto] items-baseline gap-3 border-b border-(--jai-rule) py-2">
                      <span className={`font-(family-name:--jai-mono) text-[11px] tracking-[0.1em] ${k === 0 ? "text-(--jai-senal)" : "text-(--jai-luz-soft)"}`}>{ed.f ?? "—"}</span>
                      <span className="text-sm">{ed.t}</span>
                      <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.15em] text-(--jai-luz-faint)">{[ed.tipo, ...ed.sec].filter(Boolean).join(" · ").toLowerCase()}</span>
                    </div>
                  ))
                ) : (
                  <span className="text-sm text-(--jai-luz-faint)">Solo se conoce la edición de Spotify.</span>
                )}
              </div>
            </div>
          </div>
        )}
      </section>

      <SiguePor titulo="sigue por" tarjetas={sigue} />
    </MarcoWiki>
  );
}

function Vecina({ dir, v }: { dir: "antes" | "despues"; v: { t: string; a: string; href: string } | null }) {
  const rotulo = dir === "antes" ? "← suena antes" : "suena después →";
  const lado = dir === "antes" ? "" : "items-end text-right";
  if (!v) {
    return (
      <div className={`flex min-w-0 flex-col gap-1 px-3.5 py-3 opacity-40 ${lado}`}>
        <span className="jai-dato text-[10px] text-(--jai-luz-faint)">{rotulo}</span>
        <span className="text-sm">{dir === "antes" ? "abre la estación" : "cierra la estación"}</span>
      </div>
    );
  }
  return (
    <Link href={v.href} className={`flex min-w-0 flex-col gap-1 px-3.5 py-3 transition-colors duration-300 hover:bg-(--jai-panel) ${lado}`}>
      <span className="jai-dato text-[10px] text-(--jai-luz-faint)">{rotulo}</span>
      <span className="max-w-full truncate text-sm">{v.t}</span>
      <span className="max-w-full truncate text-xs text-(--jai-luz-soft)">{v.a}</span>
    </Link>
  );
}
