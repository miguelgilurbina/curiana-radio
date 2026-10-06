import type { CSSProperties, ReactNode } from "react";
import Link from "next/link";
import type { PuntoRastro } from "@/lib/jai-rastro";
import { cuentas } from "@/lib/jai-wiki";
import JA from "../JA";
import Rastro from "./Rastro";

const fmt = (n: number) => n.toLocaleString("es");

/**
 * El marco de toda página del wiki: la consola, el rastro (fijo), el cuerpo
 * y el pie. La página toma el color de una estación (`color`): la canción
 * el de la primera donde suena, el álbum el de su primera canción, el
 * artista el de la estación donde más suena. Sin estación, sin color.
 */
export default function MarcoWiki({
  tipo,
  punto,
  color,
  children,
}: {
  tipo: string;
  punto: PuntoRastro | null;
  color: number | null;
  children: ReactNode;
}) {
  const c = cuentas();
  return (
    <div
      className={color !== null ? "jai-estacion" : ""}
      style={
        color !== null
          ? ({ "--jai-i": color } as CSSProperties)
          : ({ "--jai-senal": "var(--jai-luz-soft)", "--jai-senal-tenue": "var(--jai-panel)" } as CSSProperties)
      }
    >
      <header className="border-b border-(--jai-rule)">
        <div className="mx-auto flex max-w-[1120px] flex-wrap items-center gap-x-7 gap-y-3 px-[clamp(16px,4vw,32px)] py-3.5">
          <Link href="/jai-sounds" className="flex items-center gap-3">
            <JA tamano={30} />
            <span className="jai-display text-2xl leading-none lowercase text-(--jai-luz)">jai sounds</span>
          </Link>
          <span className="jai-dato text-[11px] text-(--jai-luz-faint)">el wiki · {tipo}</span>
          <span className="flex-1" />
          <span className="jai-dato hidden text-[11px] text-(--jai-luz-faint) md:inline">
            {fmt(c.canciones)} canciones · {fmt(c.albumes)} álbumes · {fmt(c.artistas)} artistas
          </span>
        </div>
      </header>
      {punto ? <Rastro punto={punto} /> : null}
      <main className="mx-auto flex max-w-[1120px] flex-col gap-[clamp(56px,7vw,88px)] px-[clamp(16px,4vw,32px)] pb-24 pt-12">{children}</main>
      <footer className="mx-auto flex max-w-[1120px] flex-wrap justify-between gap-5 border-t border-(--jai-rule) px-[clamp(16px,4vw,32px)] pb-[72px] pt-10">
        <span className="jai-dato text-[11px] text-(--jai-luz-faint)">datos · spotify · musicbrainz · wikipedia (cc by-sa)</span>
        <Link href="/jai-sounds" className="font-sans text-xs uppercase tracking-[0.2em] text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)">
          ← la batea
        </Link>
      </footer>
    </div>
  );
}
