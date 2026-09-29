"use client";

import {
  useRef,
  useState,
  useSyncExternalStore,
  type CSSProperties,
  type ReactNode,
} from "react";
import { hueDeEstacion, semillaDeSesion } from "@/lib/jai-rotacion";
import type { EdicionSintonizada, PistaResenada } from "@/types/jai-sounds";
import EstacionCard from "./EstacionCard";
import JA from "./JA";
import { CAJA, CTA } from "./estilos";

export interface EstacionDial {
  slug: string;
  nombre: string;
  descripcion: string;
  pistas: number;
  portada: string | null;
  spotify_id: string;
}

/** Lo que el dial sabe sintonizar: una edición con sus cinco, o una playlist. */
interface Sintonia {
  clave: string;
  numero: string;
  /** Rótulo del "sintonizado · …" */
  rotulo: string;
  nombre: string;
  descripcion: string;
  dato: string;
  marca?: string;
  portada: string | null;
  spotify_id: string | null;
  /** Pistas en la playlist; null si no se sabe (edición sin estación). */
  total: number | null;
  cinco: PistaResenada[] | null;
}

const pad = (n: number, largo = 2) => String(n).padStart(largo, "0");
// La semilla no cambia en la vida de la página: no hay nada a qué suscribirse.
const sinCambios = () => () => {};
const fmt = (n: number) => n.toLocaleString("es");

/**
 * El dial y la estación sintonizada. Abre sintonizada la estación que tiene
 * cinco pistas reseñadas (las de la edición); tocar otra la sintoniza con su
 * playlist entera en el reproductor, hasta que tenga cinco propias.
 */
export default function Dial({
  estaciones,
  edicion,
  totalPistas,
  artistas,
  interludio,
}: {
  estaciones: EstacionDial[];
  edicion: EdicionSintonizada | null;
  totalPistas: number;
  artistas: number;
  /** Lo que va entre la parrilla y la estación sintonizada. */
  interludio?: ReactNode;
}) {
  // Las cinco reseñadas de la edición van con la estación cuya playlist ES
  // la de la edición (la #01 se escuchaba en Ruido de Chocolate). Si ninguna
  // coincide, la edición entra como placa propia al principio del dial.
  const ed = edicion && edicion.pistas.length > 0 ? edicion : null;
  const deLaEdicion = ed
    ? estaciones.findIndex((e) => e.spotify_id === ed.spotify_id)
    : -1;

  const sintonias: Sintonia[] = [
    ...(ed && deLaEdicion === -1
      ? [
          {
            clave: `edicion-${ed.numero}`,
            numero: `ed·${ed.numero}`,
            rotulo: `edición #${ed.numero}`,
            nombre: ed.titulo,
            descripcion: `${ed.tema}. Cinco pistas para sintonizar, cada una con su reseña.`,
            dato: `edición #${ed.numero} · cinco pistas`,
            portada: null,
            spotify_id: ed.spotify_id,
            total: null,
            cinco: ed.pistas,
          },
        ]
      : []),
    ...estaciones.map((e, i): Sintonia => {
      const esLaEdicion = ed !== null && i === deLaEdicion;
      return {
        clave: e.slug,
        numero: pad(i + 1),
        rotulo: esLaEdicion ? `edición #${ed.numero}` : `estación ${pad(i + 1)}`,
        nombre: e.nombre,
        descripcion:
          e.descripcion ||
          (esLaEdicion
            ? `De la edición #${ed.numero}, «${ed.titulo}»: cinco pistas para sintonizar, cada una con su reseña.`
            : ""),
        dato: `${fmt(e.pistas)} pistas`,
        marca: esLaEdicion ? `edición #${ed.numero}` : undefined,
        portada: e.portada,
        spotify_id: e.spotify_id,
        total: e.pistas,
        cinco: esLaEdicion ? ed.pistas : null,
      };
    }),
  ];
  const n = sintonias.length;
  const sector = n > 0 ? 360 / n : 0;

  const conCinco = sintonias.findIndex((x) => x.cinco !== null);
  const [activa, setActiva] = useState(Math.max(0, conCinco));
  const sintonizada = useRef<HTMLElement>(null);
  // En el servidor no hay sesión (null: se pinta «···»). En el cliente se lee
  // al renderizar, así que en navegación de cliente — donde el script del
  // layout no corre — la semilla también llega antes del pintado.
  const semilla = useSyncExternalStore(sinCambios, semillaDeSesion, () => null);

  if (n === 0) {
    return (
      <section className={`${CAJA} py-16`}>
        <p className="text-(--jai-luz-faint)">
          Todavía no hay playlists en{" "}
          <span className="font-(family-name:--jai-mono)">
            content/jai-sounds/playlists.json
          </span>
          .
        </p>
      </section>
    );
  }

  const s = sintonias[Math.min(activa, n - 1)];
  const hue = semilla === null ? null : hueDeEstacion(semilla, activa, n);

  function sintonizar(i: number) {
    setActiva(i);
    const destino = sintonizada.current;
    if (!destino) return;
    // Con la parrilla entera la estación sintonizada queda abajo: sin
    // moverse hasta ella, el click no tendría respuesta visible.
    const quieto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    destino.scrollIntoView({ behavior: quieto ? "auto" : "smooth", block: "start" });
  }

  return (
    // La raíz lleva el turno de la estación activa: el punto de señal, la
    // estación sintonizada y el reproductor pintan con su matiz. Cada placa
    // redeclara el suyo.
    <div
      className="jai-estacion"
      style={{ "--jai-i": activa, "--jai-sector": sector } as CSSProperties}
    >
      {/* ── El dial ─────────────────────────────────────────────────── */}
      <section id="dial" className="scroll-mt-16">
        <header className={`${CAJA} flex flex-col gap-[18px] pb-10 pt-6`}>
          <p className="jai-dato text-[11px] text-(--jai-senal)">
            el dial · jai sounds
          </p>
          <h2 className="jai-display text-[clamp(40px,6vw,80px)] leading-[0.95] tracking-[-0.01em] text-balance text-(--jai-luz)">
            el dial de la noche
          </h2>
          <p className="max-w-[56ch] text-[17px] leading-[1.65] text-(--jai-luz-soft)">
            cada estación gira su propio matiz. vuelve mañana y el dial habrá
            cambiado de color, no de canciones.
          </p>
          <p className="jai-dato flex items-center gap-3 text-[11px] text-(--jai-luz-faint)">
            <span
              aria-hidden
              className="inline-block size-2 shrink-0 rounded-full bg-(--jai-senal) shadow-[0_0_12px_var(--jai-senal)]"
            />
            <span className="tabular-nums">
              al aire · sesión {semilla === null ? "···" : pad(semilla, 3)} ·
              hue {hue === null ? "···" : pad(hue, 3)}
            </span>
          </p>
        </header>

        <div className={`${CAJA} flex flex-col gap-5 pb-16`}>
          <div className="jai-dato flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1 border-b border-(--jai-rule) pb-2.5 text-[11px] text-(--jai-luz-faint)">
            <span>estaciones · {pad(n)}</span>
            <span>reparto angular · {Math.round(sector)}° por estación</span>
          </div>
          <ul className="grid grid-cols-2 gap-3 sm:grid-cols-[repeat(auto-fill,240px)] sm:gap-4">
            {sintonias.map((e, i) => (
              <EstacionCard
                key={e.clave}
                numero={e.numero}
                nombre={e.nombre}
                descripcion={e.cinco ? undefined : e.descripcion}
                dato={e.dato}
                marca={e.marca}
                portada={e.portada}
                i={i}
                sector={sector}
                activa={i === activa}
                onSintonizar={() => sintonizar(i)}
              />
            ))}
          </ul>
          <p className="jai-dato text-[10px] tabular-nums text-(--jai-luz-faint)">
            {fmt(totalPistas)} pistas curadas
            {artistas > 0 && ` · ${fmt(artistas)} artistas en el archivo`}
          </p>
        </div>
      </section>

      {interludio}

      {/* ── Estación sintonizada ────────────────────────────────────── */}
      <section
        ref={sintonizada}
        id="sintonizado"
        aria-labelledby="sintonizado-titulo"
        className="scroll-mt-16 border-y border-(--jai-rule) bg-(--jai-panel)"
      >
        <div
          className={`${CAJA} grid items-start gap-10 py-16 lg:grid-cols-[minmax(0,1fr)_minmax(280px,360px)] lg:gap-14`}
        >
          <div className="flex min-w-0 flex-col gap-9">
            <div className="flex flex-col gap-2.5" aria-live="polite">
              <span className="jai-dato text-[11px] text-(--jai-senal)">
                sintonizado · {s.rotulo}
              </span>
              <h2
                id="sintonizado-titulo"
                className="jai-titulo text-[clamp(30px,4vw,48px)] leading-[1.05] text-(--jai-luz)"
              >
                {s.nombre}
              </h2>
              {s.descripcion ? (
                <p className="max-w-[60ch] text-base leading-[1.6] text-(--jai-luz-soft)">
                  {s.descripcion}
                </p>
              ) : null}
            </div>

            {s.cinco ? (
              <ol className="flex flex-col gap-0.5">
                {s.cinco.map((p, i) => (
                  <li
                    key={`${p.artista}-${p.titulo}`}
                    className={`grid grid-cols-[40px_minmax(0,1fr)] gap-4 border-b border-l-3 border-b-(--jai-rule) py-[22px] pl-4 transition-colors duration-300 hover:border-l-(--jai-senal) sm:grid-cols-[56px_minmax(0,1fr)] sm:gap-5 sm:pl-5 ${
                      i === 0 ? "border-l-(--jai-senal)" : "border-l-(--jai-rule)"
                    }`}
                  >
                    <span className="jai-dato pt-1.5 text-xs text-(--jai-senal)">
                      {pad(i + 1)}
                    </span>
                    <div className="flex min-w-0 flex-col gap-2">
                      <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1.5">
                        <h3 className="jai-pista text-2xl leading-[1.15] text-(--jai-luz)">
                          {p.titulo}
                        </h3>
                        <span className="font-(family-name:--jai-mono) text-[11px] tracking-[0.15em] text-(--jai-luz-faint)">
                          {p.artista}
                        </span>
                      </div>
                      <p className="max-w-[65ch] text-[15px] leading-[1.7] text-(--jai-luz-soft)">
                        {p.resena}
                      </p>
                    </div>
                  </li>
                ))}
              </ol>
            ) : (
              <div className="flex flex-col gap-4 border-l-3 border-(--jai-rule) py-2 pl-5">
                <p className="font-(family-name:--jai-mono) text-[11px] leading-[1.9] tracking-[0.15em] text-(--jai-luz-faint)">
                  {"// las cinco de esta estación todavía no están escritas."}
                  <br />
                  {"// mientras tanto suena entera en el reproductor."}
                </p>
                {ed && conCinco !== -1 ? (
                  <button
                    type="button"
                    onClick={() => sintonizar(conCinco)}
                    className="jai-dato self-start text-[11px] text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)"
                  >
                    ↺ volver a la edición #{ed.numero}
                  </button>
                ) : null}
              </div>
            )}
          </div>

          {/* reproductor: arriba en móvil, fijo a la derecha en escritorio */}
          <aside className="order-first flex flex-col gap-3.5 lg:sticky lg:top-[84px] lg:order-none">
            <div className="jai-ja-gatillo relative hidden aspect-square overflow-hidden bg-(--jai-senal-tenue) lg:block">
              <span
                aria-hidden
                className="absolute inset-y-0 left-0 w-[3px] bg-(--jai-senal) opacity-60"
              />
              <JA tamano="64%" className="absolute left-[18%] top-[18%]" />
            </div>
            <div className="flex flex-col gap-3 border border-(--jai-rule) bg-(--jai-noche) px-[18px] py-4">
              <div className="jai-dato flex justify-between gap-4 text-[11px] text-(--jai-luz-faint)">
                <span>spotify · embed</span>
                <span className="tabular-nums">
                  {s.total !== null ? `${fmt(s.total)} pistas` : "cinco pistas"}
                </span>
              </div>
              {s.spotify_id ? (
                <>
                  <iframe
                    key={s.spotify_id}
                    title={`${s.nombre} en Spotify`}
                    src={`https://open.spotify.com/embed/playlist/${s.spotify_id}?utm_source=generator&theme=0`}
                    width="100%"
                    height="152"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                    className="block border-0"
                  />
                  <a
                    href={`https://open.spotify.com/playlist/${s.spotify_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`${CTA} bg-(--jai-senal) text-center text-(--jai-noche) hover:bg-(--jai-luz)`}
                  >
                    escuchar →
                  </a>
                </>
              ) : null}
            </div>
            <p className="font-(family-name:--jai-mono) text-[10px] leading-[1.7] tracking-[0.15em] text-(--jai-luz-faint)">
              {"// el matiz no se guarda. la semilla vive en sessionStorage; al volver, el dial gira."}
            </p>
          </aside>
        </div>
      </section>
    </div>
  );
}
