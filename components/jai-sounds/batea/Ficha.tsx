"use client";

import Link from "next/link";
import { useEffect, type CSSProperties } from "react";
import { empezarEn } from "@/lib/jai-rastro";
import type { ResumenEstacion } from "@/lib/jai-wiki";
import type { FilaPista } from "@/types/jai-wiki";
import Markdown from "../wiki/Markdown";

const DT = "border-b border-(--jai-rule) py-[11px] pr-4 font-(family-name:--jai-mono) text-[10px] tracking-[0.3em] text-(--jai-luz-faint) whitespace-nowrap";
const DD = "m-0 border-b border-(--jai-rule) py-2.5 text-sm";
const ENLACE = "border-b border-(--jai-rule) transition-colors duration-300 hover:border-(--jai-senal)";

/** El id de Spotify de una pista, desde su URL. */
const idSpotify = (url: string) => url.match(/track\/([A-Za-z0-9]{22})/)?.[1] ?? null;

/**
 * La ficha de pista: la antesala del wiki. Panel a la derecha (pantalla
 * completa en el móvil) sobre un velo; Esc o el velo la cierran. Todo
 * enlace de aquí empieza el rastro en la estación.
 */
export default function Ficha({
  fila,
  pos,
  total,
  estacion,
  estaciones,
  antes,
  despues,
  abrir,
  cerrar,
  irEstacion,
}: {
  fila: FilaPista;
  pos: number;
  total: number;
  estacion: ResumenEstacion;
  estaciones: ResumenEstacion[];
  antes: FilaPista | null;
  despues: FilaPista | null;
  abrir: (slug: string) => void;
  cerrar: () => void;
  irEstacion: (k: number) => void;
}) {
  useEffect(() => {
    const tecla = (e: KeyboardEvent) => e.key === "Escape" && cerrar();
    addEventListener("keydown", tecla);
    return () => removeEventListener("keydown", tecla);
  }, [cerrar]);

  const marcar = () => empezarEn({ tipo: "estacion", slug: estacion.slug, n: estacion.nombre, e: estacion.i });
  const otra = fila.ys && fila.f && fila.f.slice(0, 4) !== fila.ys.slice(0, 4);
  const pista = idSpotify(fila.spotify);
  const nombreMin = estacion.nombre.toLowerCase();

  return (
    <>
      <div onClick={cerrar} className="fixed inset-0 z-[60] bg-[rgba(11,17,25,0.72)]" />
      <aside
        role="dialog"
        aria-label={`Ficha de ${fila.t}`}
        className="jai-entra fixed inset-y-0 right-0 z-[61] flex w-full flex-col overflow-y-auto border-l border-(--jai-rule) bg-(--jai-panel) min-[900px]:w-[min(480px,100%)]"
      >
        <div className="sticky top-0 z-[1] flex items-center justify-between gap-3 border-b border-(--jai-rule) bg-(--jai-panel) px-5 py-3.5 font-(family-name:--jai-mono) text-[10px] tracking-[0.3em] text-(--jai-luz-faint)">
          <span>
            ficha de pista · <span className="text-(--jai-senal)">{String(pos).padStart(2, "0")} / {total}</span> · {nombreMin}
          </span>
          <button onClick={cerrar} className="py-1.5 text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)">
            cerrar · esc
          </button>
        </div>

        <div className="flex flex-col gap-[26px] px-5 pb-8 pt-6">
          <div className="grid grid-cols-[112px_minmax(0,1fr)] items-end gap-[18px]">
            <div className="box-border aspect-square border-l-3 border-(--jai-senal) bg-(--jai-senal-tenue)">
              {fila.img ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={fila.img.replace("ab67616d0000b273", "ab67616d00001e02")} alt="" className="block h-full w-full object-cover" />
              ) : null}
            </div>
            <div className="flex min-w-0 flex-col gap-2">
              <h2 className="jai-titulo m-0 text-[28px] leading-[1.08] text-balance text-(--jai-luz)">{fila.t}</h2>
              <div className="flex flex-wrap gap-x-2.5 gap-y-1 text-[15px]">
                {fila.a.map((a) => (
                  <Link key={a.s} href={`/jai-sounds/artistas/${a.s}`} onClick={marcar} className={`text-(--jai-luz-soft) hover:text-(--jai-luz) ${ENLACE}`}>
                    {a.n}
                  </Link>
                ))}
              </div>
            </div>
          </div>

          <dl className="m-0 grid grid-cols-[auto_minmax(0,1fr)] border-t border-(--jai-rule)">
            <dt className={DT}>álbum</dt>
            <dd className={DD}>
              {fila.al ? (
                <Link href={`/jai-sounds/albumes/${fila.al.s}`} onClick={marcar} className={ENLACE}>
                  {fila.al.n}
                </Link>
              ) : (
                "—"
              )}
            </dd>
            <dt className={DT}>año</dt>
            <dd className={DD}>
              {fila.y ?? "—"}{" "}
              <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.2em] text-(--jai-luz-faint)">
                {otra ? `primera edición · spotify dice ${fila.ys}` : fila.f ? "" : "según spotify"}
              </span>
            </dd>
            <dt className={DT}>duración</dt>
            <dd className={DD}>{fila.d}</dd>
            <dt className={DT}>en el dial desde</dt>
            <dd className={`${DD} font-(family-name:--jai-mono) text-xs tracking-[0.1em]`}>{fila.desde ?? "—"}</dd>
            <dt className={DT}>también en</dt>
            <dd className={`${DD} flex flex-wrap gap-1.5 py-2`}>
              {fila.tambien.length ? (
                fila.tambien.map((k) => (
                  <button
                    key={k}
                    onClick={() => irEstacion(k)}
                    className="jai-estacion border-l-3 border-(--jai-senal) bg-(--jai-noche) py-[3px] pl-1.5 pr-2 text-left"
                    style={{ "--jai-i": k } as CSSProperties}
                  >
                    {estaciones[k]?.nombre}
                  </button>
                ))
              ) : (
                <span className="text-(--jai-luz-faint)">solo en esta estación</span>
              )}
            </dd>
          </dl>

          <div className="flex flex-col gap-2.5">
            <span className="jai-dato text-[10px] text-(--jai-senal)">jai</span>
            {fila.r ? (
              <>
                <div className="flex flex-col gap-3">
                  <Markdown texto={fila.r} tam="ficha" />
                </div>
                <span className="jai-dato text-[10px] text-(--jai-luz-faint)">— miguel</span>
              </>
            ) : (
              <p className="jai-manifiesto m-0 text-xl leading-[1.45] text-(--jai-luz-faint)">JAI Sounds aún no le hace review.</p>
            )}
          </div>

          {pista ? (
            <iframe
              key={pista}
              title={`${fila.t} en Spotify`}
              src={`https://open.spotify.com/embed/track/${pista}?utm_source=generator&theme=0`}
              width="100%"
              height="80"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
              className="block border-0"
            />
          ) : null}

          <div className="grid grid-cols-2 border-t border-(--jai-rule)">
            <button
              onClick={() => antes && abrir(antes.s)}
              disabled={!antes}
              className="flex flex-col gap-1 border-b border-r border-(--jai-rule) py-3 pr-3 text-left text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz) disabled:opacity-40"
            >
              <span className="jai-dato text-[10px] text-(--jai-luz-faint)">↑ suena antes</span>
              <span className="truncate text-[13px]">{antes ? `${antes.t} — ${antes.a.map((a) => a.n).join(", ")}` : "es la primera"}</span>
            </button>
            <button
              onClick={() => despues && abrir(despues.s)}
              disabled={!despues}
              className="flex flex-col items-end gap-1 border-b border-(--jai-rule) py-3 pl-3 text-right text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz) disabled:opacity-40"
            >
              <span className="jai-dato text-[10px] text-(--jai-luz-faint)">suena después ↓</span>
              <span className="max-w-full truncate text-[13px]">{despues ? `${despues.t} — ${despues.a.map((a) => a.n).join(", ")}` : "es la última"}</span>
            </button>
          </div>

          <Link
            href={`/jai-sounds/canciones/${fila.s}`}
            onClick={marcar}
            className="flex items-center justify-between gap-4 bg-(--jai-senal) px-5 py-[18px] text-(--jai-noche) transition-colors duration-300 hover:bg-(--jai-luz)"
          >
            <span className="flex flex-col gap-1">
              <span className="font-(family-name:--jai-mono) text-[10px] tracking-[0.3em]">el wiki</span>
              <span className="jai-titulo text-xl leading-[1.1]">entra a la canción</span>
            </span>
            <span aria-hidden className="text-[22px]">→</span>
          </Link>
        </div>
      </aside>
    </>
  );
}
