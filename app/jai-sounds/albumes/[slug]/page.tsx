import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import MarcoWiki from "@/components/jai-sounds/wiki/MarcoWiki";
import { ChipEstacion, Datos, DosVoces, Riel, Rotulo, SiguePor, type Tarjeta } from "@/components/jai-sounds/wiki/piezas";
import { album, artista, cancion, duracion, estacionDeColor, estaciones, nombreArtista, portada } from "@/lib/jai-wiki";

export const dynamicParams = true;
export function generateStaticParams() {
  return [];
}

type Props = { params: Promise<{ slug: string }> };

const TIPOS: Record<string, string> = { album: "álbum", single: "single", compilation: "compilación" };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const al = album((await params).slug);
  // notFound() aquí y no solo en la página: la metadata se resuelve antes de
  // transmitir, así el 404 llega como 404 y no como 200 con el aviso.
  if (!al) notFound();
  const de = al.a.map(nombreArtista).join(", ");
  return { title: `${al.t} — ${de} | JAI Sounds`, description: `${al.t}, de ${de}: lo que suena de este álbum en el dial de JAI Sounds.` };
}

export default async function AlbumPage({ params }: Props) {
  const { slug } = await params;
  const al = album(slug);
  if (!al) notFound();

  const est = estaciones();
  const temas = al.canciones.map((s) => ({ s, c: cancion(s)! })).filter((x) => x.c).sort((a, b) => (a.c.n ?? 0) - (b.c.n ?? 0));
  const ests = [...new Set(temas.flatMap((x) => x.c.dial.map((d) => d[0])))];
  const otros = [...new Set(al.a.flatMap((a) => artista(a)?.albumes ?? []))].filter((x) => x !== slug);
  const tipo = TIPOS[al.tipo ?? ""] ?? al.tipo ?? "álbum";
  const escaso = !al.internet && !al.resena && temas.length <= 1;

  const sigue: Tarjeta[] = [
    ...al.a.map((a) => ({ tipo: "artista", n: nombreArtista(a), sub: "quien lo firma", href: `/jai-sounds/artistas/${a}` })),
    ...otros.slice(0, 6).map((o) => {
      const x = album(o);
      return { tipo: "otro álbum", n: x?.t ?? o, sub: x?.fecha?.slice(0, 4) ?? "", href: `/jai-sounds/albumes/${o}` };
    }),
    ...ests.map((e) => ({ tipo: `estación ${String(e + 1).padStart(2, "0")}`, n: est[e].nombre.toLowerCase(), sub: "donde suena", href: `/jai-sounds#${String(e + 1).padStart(2, "0")}`, i: e })),
  ];

  return (
    <MarcoWiki tipo="álbum" punto={{ tipo: "album", slug, n: al.t }} color={estacionDeColor("album", slug)}>
      <section className="grid items-end gap-x-12 gap-y-8 min-[820px]:grid-cols-[minmax(0,300px)_minmax(0,1fr)]">
        <div className="box-border aspect-square max-w-[220px] border-l-3 border-(--jai-senal) bg-(--jai-senal-tenue) min-[820px]:max-w-none">
          {al.img ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={portada(al.img, 640) ?? ""} alt={`Portada de ${al.t}`} className="block h-full w-full object-cover" />
          ) : null}
        </div>
        <div className="flex min-w-0 flex-col gap-[18px]">
          <span className="jai-dato text-[11px] text-(--jai-senal)">
            {tipo === "álbum" ? "álbum" : `álbum · ${tipo}`}
            {al.fecha ? ` · ${al.fecha.slice(0, 4)}` : ""}
          </span>
          <h1 className="jai-titulo m-0 text-[clamp(36px,5vw,64px)] leading-[1.02] tracking-[-0.01em] text-balance text-(--jai-luz)">{al.t}</h1>
          {al.a.length ? (
            <p className="jai-manifiesto m-0 flex flex-wrap items-baseline gap-x-3.5 gap-y-1 text-[22px]">
              <span className="jai-dato text-[10px] text-(--jai-luz-faint)">de</span>
              {al.a.map((a) => (
                <Link key={a} href={`/jai-sounds/artistas/${a}`} className="border-b border-(--jai-rule) text-(--jai-luz) transition-colors duration-300 hover:border-(--jai-senal)">
                  {nombreArtista(a)}
                </Link>
              ))}
            </p>
          ) : null}
          <Datos
            datos={[
              { k: "tipo", v: tipo },
              { k: "fecha", v: al.fecha },
              { k: "en el dial", v: `${temas.length} ${temas.length === 1 ? "canción" : "canciones"}` },
              { k: "estaciones", v: String(ests.length) },
            ]}
          />
          <a
            href={`https://open.spotify.com/album/${al.id}`}
            target="_blank"
            rel="noopener noreferrer"
            className="self-start bg-(--jai-senal) px-[22px] py-[15px] font-sans text-[11px] font-semibold uppercase tracking-[0.2em] text-(--jai-noche) transition-colors duration-300 hover:bg-(--jai-luz)"
          >
            ▶ escuchar en spotify
          </a>
        </div>
      </section>

      {escaso ? (
        <Riel titulo="este álbum entra al dial por una sola puerta">Una canción, una estación. Poco para un álbum, suficiente para un hilo: sigue por quien lo firma.</Riel>
      ) : null}

      <section aria-label="Lo que suena de este álbum" className="flex flex-col">
        <Rotulo derecha={`${temas.length} de sus pistas · en ${ests.length} ${ests.length === 1 ? "estación" : "estaciones"}`}>lo que suena de este álbum</Rotulo>
        {temas.map(({ s, c }) => (
          <div key={s} className="grid grid-cols-[32px_minmax(0,1fr)] items-center gap-x-[18px] gap-y-2 border-b border-(--jai-rule) py-[13px] min-[820px]:grid-cols-[40px_minmax(0,1.3fr)_minmax(0,1fr)_72px]">
            <span className="font-(family-name:--jai-mono) text-[11px] tracking-[0.1em] text-(--jai-luz-faint)">{c.n ? String(c.n).padStart(2, "0") : "—"}</span>
            <span className="flex min-w-0 flex-col gap-[3px]">
              <Link href={`/jai-sounds/canciones/${s}`} className="text-[15px] font-medium leading-[1.3] transition-colors duration-300 hover:text-(--jai-senal)">
                {c.t}
              </Link>
              <Link href={`/jai-sounds/artistas/${c.a[0]}`} className="text-[13px] text-(--jai-luz-soft)">
                {c.a.map(nombreArtista).join(", ")}
              </Link>
            </span>
            <span className="col-start-2 flex flex-wrap gap-1.5 min-[820px]:col-start-auto">
              {c.dial.map(([e, pos]) => (
                <ChipEstacion key={e} i={e} nombre={est[e].nombre} pos={pos} />
              ))}
            </span>
            <span className="hidden text-right font-(family-name:--jai-mono) text-[11px] tracking-[0.1em] text-(--jai-luz-faint) min-[820px]:block">{duracion(c.ms)}</span>
          </div>
        ))}
      </section>

      <DosVoces voces={al} cosa="este álbum" nombre={`${al.t} ${al.a.map(nombreArtista)[0] ?? ""}`} />

      <SiguePor titulo="sigue por" tarjetas={sigue} />
    </MarcoWiki>
  );
}
