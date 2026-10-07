import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import MarcoWiki from "@/components/jai-sounds/wiki/MarcoWiki";
import { ChipEstacion, Datos, DosVoces, Generos, Riel, Rotulo, SiguePor, type Tarjeta } from "@/components/jai-sounds/wiki/piezas";
import { album, anio, artista, cancion, conVozDeJai, estacionDeColor, estaciones, estacionesDeArtista, imagenSocial, nombreArtista, portada } from "@/lib/jai-wiki";
import { metadatos, TARJETA_JAI } from "@/lib/seo";
import type { PersonaMB } from "@/types/jai-wiki";

export const dynamicParams = true;
export function generateStaticParams() {
  return [];
}

type Props = { params: Promise<{ slug: string }> };

const TIPOS: Record<string, string> = { Person: "persona", Group: "grupo", Orchestra: "orquesta", Choir: "coro", Character: "personaje", Other: "otro" };
const paises = new Intl.DisplayNames(["es"], { type: "region" });
const pais = (codigo: string | null) => {
  if (!codigo) return null;
  try {
    return paises.of(codigo) ?? codigo;
  } catch {
    return codigo;
  }
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const ar = artista((await params).slug);
  // notFound() aquí y no solo en la página: la metadata se resuelve antes de
  // transmitir, así el 404 llega como 404 y no como 200 con el aviso.
  if (!ar) notFound();
  // Los artistas no traen foto: la tarjeta es la portada de su primer álbum.
  const disco = ar.albumes.map(album).find((x) => x?.img);
  return metadatos({
    titulo: `${ar.n} | JAI Sounds`,
    tituloSocial: `${ar.n} en JAI Sounds`,
    descripcion: `${ar.n} en el dial de JAI Sounds: sus canciones, dónde suena y al lado de quién.`,
    ruta: `/jai-sounds/artistas/${(await params).slug}`,
    imagen: (disco && imagenSocial(disco.img, `Portada de ${disco.t}, de ${ar.n}`)) ?? TARJETA_JAI,
    noIndex: !conVozDeJai(ar),
  });
}

export default async function ArtistaPage({ params }: Props) {
  const { slug } = await params;
  const ar = artista(slug);
  if (!ar) notFound();

  const est = estaciones();
  const m = ar.mb;
  const tipo = m?.tipo ? (TIPOS[m.tipo] ?? m.tipo.toLowerCase()) : null;
  const grupo = m?.tipo === "Group" || m?.tipo === "Orchestra" || m?.tipo === "Choir";
  const temas = ar.canciones.map((s) => ({ s, c: cancion(s)! })).filter((x) => x.c);
  const ests = estacionesDeArtista(slug);
  const anios = temas.map((x) => Number(anio(x.c.mb?.f) ?? anio(x.c.fecha))).filter(Boolean).sort((a, b) => a - b);
  const rango = anios.length ? (anios[0] === anios.at(-1) ? String(anios[0]) : `${anios[0]}–${anios.at(-1)}`) : null;
  const vida = m?.inicio ? (grupo ? `${m.inicio.slice(0, 4)} – ${m.fin?.slice(0, 4) ?? "hoy"}` : m.fin ? `${m.inicio.slice(0, 4)} – ${m.fin.slice(0, 4)}` : `nació ${m.inicio.slice(0, 4)}`) : null;
  const gente: PersonaMB[] = grupo ? (m?.miembros ?? []) : (m?.de ?? []);
  const enlaces = Object.entries(m?.links ?? {}).filter(([k]) => k !== "wikidata");
  const nombreMin = ar.n.toLowerCase();

  const sigue: Tarjeta[] = [
    ...ar.cerca.slice(0, 6).map(([a, e]) => ({ tipo: "artista", n: nombreArtista(a), sub: `comparte ${est[e]?.nombre ?? "estación"}`, href: `/jai-sounds/artistas/${a}` })),
    ...ests.map((e) => ({ tipo: `estación ${String(e + 1).padStart(2, "0")}`, n: est[e].nombre.toLowerCase(), sub: "donde suena", href: `/jai-sounds#${String(e + 1).padStart(2, "0")}`, i: e })),
  ];

  return (
    <MarcoWiki tipo="artista" punto={{ tipo: "artista", slug, n: ar.n }} color={estacionDeColor("artista", slug)}>
      <section className="flex min-w-0 flex-col gap-[18px]">
        <span className="jai-dato text-[11px] text-(--jai-senal)">
          artista{tipo ? ` · ${tipo}` : ""}
          {m?.pais ? ` · ${(pais(m.pais) ?? "").toLowerCase()}` : ""}
        </span>
        <h1 className="jai-display m-0 text-[clamp(52px,8.4vw,120px)] leading-[0.9] tracking-[-0.02em] lowercase text-balance text-(--jai-luz) [overflow-wrap:anywhere]">{ar.n}</h1>
        {m?.desamb ? <span className="font-(family-name:--jai-mono) text-[11px] tracking-[0.15em] text-(--jai-luz-faint)">{m.desamb}</span> : null}
        <Datos
          datos={[
            { k: "tipo", v: tipo },
            { k: "país", v: pais(m?.pais ?? null) ?? m?.area ?? null },
            { k: grupo ? "se formó en" : m?.tipo === "Person" ? "nació en" : "origen", v: m?.origen ?? null },
            { k: grupo ? "años" : "vida", v: vida },
            { k: "lo suyo que suena", v: rango },
            { k: "en el dial", v: `${temas.length} ${temas.length === 1 ? "canción" : "canciones"} · ${ests.length} ${ests.length === 1 ? "estación" : "estaciones"}` },
          ]}
        />
        <Generos generos={m?.g ?? []} />
      </section>

      {!m ? (
        <Riel titulo={`musicbrainz aún no sabe quién es ${nombreMin}`}>
          Llegó al dial por sus canciones. Lo que sí se sabe es dónde suena y con quién: el hilo sigue por ahí.
        </Riel>
      ) : !ar.internet && !enlaces.length ? (
        <Riel titulo={`el internet sabe poco de ${nombreMin}`}>
          Sin Wikipedia ni Discogs. Lo que cuenta de {ar.n} lo cuenta el dial: dónde suena y al lado de quién.
        </Riel>
      ) : null}

      {temas.length ? (
        <section aria-label="Sus canciones en el dial" className="flex flex-col">
          <Rotulo derecha={rango ?? undefined}>sus canciones en el dial</Rotulo>
          {temas.map(({ s, c }) => {
            const al = c.al ? album(c.al) : null;
            return (
              <div key={s} className="grid items-center gap-x-[18px] gap-y-2 border-b border-(--jai-rule) py-[13px] min-[820px]:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)_72px]">
                <span className="flex min-w-0 flex-col gap-[3px]">
                  <Link href={`/jai-sounds/canciones/${s}`} className="text-[15px] font-medium leading-[1.3] transition-colors duration-300 hover:text-(--jai-senal)">
                    {c.t}
                  </Link>
                  {al && c.al ? (
                    <Link href={`/jai-sounds/albumes/${c.al}`} className="text-[13px] text-(--jai-luz-soft)">
                      {al.t}
                    </Link>
                  ) : null}
                </span>
                <span className="flex flex-wrap gap-1.5">
                  {c.dial.map(([e, pos]) => (
                    <ChipEstacion key={e} i={e} nombre={est[e].nombre} pos={pos} />
                  ))}
                </span>
                <span className="hidden text-right font-(family-name:--jai-mono) text-[11px] tracking-[0.1em] text-(--jai-luz-faint) min-[820px]:block">
                  {anio(c.mb?.f) ?? anio(c.fecha) ?? "—"}
                </span>
              </div>
            );
          })}
        </section>
      ) : null}

      {ar.albumes.length ? (
        <section aria-label="Sus álbumes en el dial" className="flex flex-col gap-[18px]">
          <Rotulo>sus álbumes en el dial</Rotulo>
          <div className="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-5">
            {ar.albumes.map((a) => {
              const x = album(a);
              if (!x) return null;
              return (
                <Link key={a} href={`/jai-sounds/albumes/${a}`} className="group flex flex-col gap-2.5">
                  <span className="box-border block aspect-square border border-(--jai-rule) bg-(--jai-senal-tenue) transition-colors duration-300 group-hover:border-(--jai-senal)">
                    {x.img ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={portada(x.img, 300) ?? ""} alt="" loading="lazy" className="block h-full w-full object-cover" />
                    ) : null}
                  </span>
                  <span className="text-sm font-medium leading-[1.3]">{x.t}</span>
                  <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.2em] text-(--jai-luz-faint)">
                    {[x.fecha?.slice(0, 4), x.tipo].filter(Boolean).join(" · ")}
                  </span>
                </Link>
              );
            })}
          </div>
        </section>
      ) : null}

      {m ? (
        <section className="grid grid-cols-[repeat(auto-fit,minmax(min(100%,300px),1fr))] gap-x-12 gap-y-9">
          <div className="flex flex-col gap-0.5">
            <span className="jai-dato border-b border-(--jai-rule) pb-2.5 text-[10px] text-(--jai-luz-faint)">{grupo ? "miembros" : "grupos de los que fue parte"}</span>
            {gente.length ? (
              gente.map((g) =>
                g.a ? (
                  <Link key={g.mbid} href={`/jai-sounds/artistas/${g.a}`} className="flex justify-between gap-3 border-b border-(--jai-rule) py-[11px] text-[15px] transition-colors duration-300 hover:text-(--jai-senal)">
                    <span>{g.nombre}</span>
                    <span className="text-(--jai-luz-faint)">→</span>
                  </Link>
                ) : (
                  <a key={g.mbid} href={`https://musicbrainz.org/artist/${g.mbid}`} target="_blank" rel="noopener noreferrer" className="flex justify-between gap-3 border-b border-(--jai-rule) py-[11px] text-[15px] text-(--jai-luz-soft)">
                    <span>
                      {g.nombre}
                      {g.desde ? <span className="ml-2 font-(family-name:--jai-mono) text-[10px] tracking-[0.15em] text-(--jai-luz-faint)">{g.desde.slice(0, 4)}–{g.hasta?.slice(0, 4) ?? ""}</span> : null}
                    </span>
                    <span className="text-(--jai-luz-faint)">↗</span>
                  </a>
                )
              )
            ) : (
              <span className="py-[11px] text-sm text-(--jai-luz-faint)">MusicBrainz no registra {grupo ? "sus miembros" : "grupos"}.</span>
            )}
          </div>
          <div className="flex flex-col gap-0.5">
            <span className="jai-dato border-b border-(--jai-rule) pb-2.5 text-[10px] text-(--jai-luz-faint)">enlaces</span>
            {enlaces.length ? (
              enlaces.map(([k, url]) => (
                <a key={k} href={url} target="_blank" rel="noopener noreferrer" className="flex justify-between gap-3 border-b border-(--jai-rule) py-[11px] font-(family-name:--jai-mono) text-xs tracking-[0.2em] text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)">
                  <span>{k === "web" ? "web oficial" : k}</span>
                  <span>↗</span>
                </a>
              ))
            ) : (
              <span className="py-[11px] text-sm text-(--jai-luz-faint)">Sin Wikipedia, Discogs ni web oficial registrados.</span>
            )}
          </div>
        </section>
      ) : null}

      <DosVoces voces={ar} cosa={ar.n} nombre={ar.n} />

      <SiguePor titulo="suena cerca de" tarjetas={sigue} />
    </MarcoWiki>
  );
}
