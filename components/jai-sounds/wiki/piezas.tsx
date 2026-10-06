import type { CSSProperties, ReactNode } from "react";
import Link from "next/link";
import type { Voces } from "@/types/jai-wiki";
import Markdown from "./Markdown";

/** El rótulo mono de una sección del wiki, con su contraparte a la derecha. */
export function Rotulo({ children, derecha }: { children: ReactNode; derecha?: ReactNode }) {
  return (
    <div className="jai-dato flex justify-between gap-3 border-b border-(--jai-rule) pb-2.5 text-[10px] text-(--jai-luz-faint)">
      <span>{children}</span>
      {derecha ? <span className="text-right">{derecha}</span> : null}
    </div>
  );
}

/**
 * El riel liminal: el patrón del dato ausente. Filete gris, un rótulo
 * `// …` y una frase. Una página con poco nunca es un callejón.
 */
export function Riel({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <section className="flex max-w-[64ch] flex-col gap-2.5 border-l-3 border-(--jai-luz-faint) py-1 pl-[22px]">
      <span className="jai-dato text-[11px] text-(--jai-luz-faint)">{`// ${titulo}`}</span>
      <p className="m-0 text-base leading-[1.7] text-(--jai-luz-soft)">{children}</p>
    </section>
  );
}

/** Los datos de cabecera: una grilla de pares con filetes. El que falta es «—». */
export function Datos({ datos }: { datos: { k: string; v: ReactNode | null; href?: string }[] }) {
  return (
    <dl className="m-0 grid grid-cols-[repeat(auto-fit,minmax(140px,1fr))] border-l border-t border-(--jai-rule)">
      {datos.map((x) => (
        <div key={x.k} className="flex min-w-0 flex-col gap-[7px] border-b border-r border-(--jai-rule) px-3.5 pb-3.5 pt-3">
          <dt className="jai-dato text-[10px] text-(--jai-luz-faint)">{x.k}</dt>
          <dd className={`m-0 text-[15px] leading-[1.35] [overflow-wrap:anywhere] ${x.v ? "text-(--jai-luz)" : "text-(--jai-luz-faint)"}`}>
            {x.v && x.href ? (
              <Link href={x.href} className="border-b border-(--jai-rule) transition-colors duration-300 hover:border-(--jai-senal)">
                {x.v}
              </Link>
            ) : (
              (x.v ?? "—")
            )}
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function Generos({ generos, de }: { generos: string[]; de?: string }) {
  if (!generos.length) return null;
  return (
    <div className="flex flex-col gap-2">
      {de ? <span className="jai-dato text-[10px] text-(--jai-luz-faint)">{de}</span> : null}
      <ul className="m-0 flex list-none flex-wrap gap-1.5 p-0">
        {generos.slice(0, 10).map((g) => (
          <li key={g} className="border border-(--jai-rule) px-[9px] py-[5px] font-(family-name:--jai-mono) text-[11px] tracking-[0.15em] text-(--jai-luz-soft)">
            {g}
          </li>
        ))}
      </ul>
    </div>
  );
}

/** Una estación como chip: filete de su señal, nombre y (si se da) el puesto. */
export function ChipEstacion({ i, nombre, pos }: { i: number; nombre: string; pos?: number }) {
  return (
    <Link
      href={`/jai-sounds#${String(i + 1).padStart(2, "0")}`}
      className="jai-estacion whitespace-nowrap border-l-3 border-(--jai-senal) bg-(--jai-panel) py-[3px] pl-1.5 pr-2 text-xs"
      style={{ "--jai-i": i } as CSSProperties}
    >
      {nombre}
      {pos ? <span className="font-(family-name:--jai-mono) text-[10px] text-(--jai-luz-faint)"> · {String(pos).padStart(3, "0")}</span> : null}
    </Link>
  );
}

/**
 * Las dos voces, que nunca se confunden: la reseña JAI (la de Miguel) y lo
 * que dice el internet (otra superficie, otra letra, siempre citado).
 */
export function DosVoces({ voces, cosa, nombre }: { voces: Voces; cosa: string; nombre: string }) {
  const w = voces.internet;
  return (
    <section aria-label="Las dos voces" className="grid items-start gap-x-14 gap-y-10 min-[820px]:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]">
      <div className="flex min-w-0 flex-col gap-[18px]">
        <div className="flex items-baseline justify-between gap-3 border-b border-(--jai-senal) pb-2.5">
          <span className="jai-dato text-[11px] text-(--jai-senal)">jai</span>
          <span className="jai-dato text-[10px] text-(--jai-luz-faint)">la reseña</span>
        </div>
        {voces.resena ? (
          <>
            <div className="flex max-w-[60ch] flex-col gap-5">
              <Markdown texto={voces.resena.cuerpo} />
            </div>
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">
              — miguel{voces.resena.publicada_en ? ` · ${voces.resena.publicada_en.slice(0, 10)}` : ""}
            </span>
          </>
        ) : (
          // El silencio también se compone: mismo cuerpo, sin caja.
          <p className="jai-manifiesto m-0 text-[clamp(22px,2.4vw,28px)] leading-[1.35] text-(--jai-luz-faint)">JAI Sounds aún no le hace review.</p>
        )}
      </div>
      <figure className="relative m-0 flex min-w-0 flex-col gap-4 bg-(--jai-panel) px-6 pt-[26px]">
        <span className="jai-dato text-[11px] text-(--jai-luz-soft)">esto dice el internet</span>
        {w ? (
          <>
            <blockquote lang={w.idioma ?? undefined} className="relative m-0 pl-7">
              <span aria-hidden className="absolute -left-1 -top-3.5 font-(family-name:--jai-display) text-[56px] leading-none text-(--jai-rule)">
                «
              </span>
              <p className="m-0 max-w-[60ch] text-[15px] leading-[1.7] text-pretty text-(--jai-luz-soft)">{w.extracto}</p>
            </blockquote>
            <figcaption className="-mx-6 flex flex-wrap gap-x-3.5 gap-y-1.5 border-t border-(--jai-rule) px-6 py-3 font-(family-name:--jai-mono) text-[10px] tracking-[0.2em] text-(--jai-luz-faint)">
              <span>wikipedia · «{w.titulo}»</span>
              <span>{(w.licencia ?? "cc by-sa 4.0").toLowerCase()}</span>
              <a href={w.url} target="_blank" rel="noopener noreferrer" className="text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)">
                leer el artículo ↗
              </a>
            </figcaption>
          </>
        ) : (
          <>
            <p className="m-0 text-[15px] leading-[1.7] text-(--jai-luz-faint)">El internet todavía no tiene un extracto para {cosa}.</p>
            <figcaption className="-mx-6 border-t border-(--jai-rule) px-6 py-3 font-(family-name:--jai-mono) text-[10px] tracking-[0.2em]">
              <a
                href={`https://es.wikipedia.org/w/index.php?search=${encodeURIComponent(nombre)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)"
              >
                buscarlo en wikipedia ↗
              </a>
            </figcaption>
          </>
        )}
      </figure>
    </section>
  );
}

export interface Tarjeta {
  tipo: string;
  n: string;
  sub: string;
  href: string;
  /** Estación que le da color al filete; sin ella, filete neutro. */
  i?: number;
}

/** «Sigue por» / «suena cerca de»: toda página termina con salidas. */
export function SiguePor({ titulo, tarjetas }: { titulo: string; tarjetas: Tarjeta[] }) {
  if (!tarjetas.length) return null;
  return (
    <section className="flex flex-col gap-[18px]">
      <Rotulo derecha="el hoyo sigue">{titulo}</Rotulo>
      <div className="grid grid-cols-[repeat(auto-fill,minmax(min(100%,230px),1fr))] gap-3">
        {tarjetas.map((t) => (
          <Link
            key={`${t.tipo}:${t.href}`}
            href={t.href}
            className={`flex min-w-0 flex-col gap-2 border border-l-3 border-(--jai-rule) pb-[18px] pl-3.5 pr-4 pt-4 transition-colors duration-300 hover:bg-(--jai-panel) ${t.i !== undefined ? "jai-estacion border-l-(--jai-senal)" : ""}`}
            style={t.i !== undefined ? ({ "--jai-i": t.i } as CSSProperties) : undefined}
          >
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">{t.tipo}</span>
            <span className="jai-titulo text-xl leading-[1.15] [overflow-wrap:anywhere]">{t.n}</span>
            <span className="text-[13px] text-(--jai-luz-soft)">{t.sub}</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
