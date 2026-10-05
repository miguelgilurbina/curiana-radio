"use client";

import Link from "next/link";
import {
  useCallback,
  useEffect,
  useRef,
  useState,
  useSyncExternalStore,
  type CSSProperties,
} from "react";
import { hueDeEstacion, semillaDeSesion } from "@/lib/jai-rotacion";
import { empezarEn } from "@/lib/jai-rastro";
import type { ResumenEstacion } from "@/lib/jai-wiki";
import type { DatosEstacion } from "@/types/jai-wiki";
import JA from "../JA";
import Ficha from "./Ficha";
import Pila from "./Pila";

const num = (i: number) => String(i + 1).padStart(2, "0");
const sinCambios = () => () => {};
// La estación vive en el hash (#09): se lee como un store externo, y pasar
// de disco lo reescribe y avisa con un evento propio (replaceState no
// dispara hashchange).
const EVENTO = "jai:estacion";
const suscribirHash = (cb: () => void) => {
  addEventListener("hashchange", cb);
  addEventListener(EVENTO, cb);
  return () => {
    removeEventListener("hashchange", cb);
    removeEventListener(EVENTO, cb);
  };
};
const sinMovimiento = (cb: () => void) => {
  const m = matchMedia("(prefers-reduced-motion: reduce)");
  m.addEventListener("change", cb);
  return () => m.removeEventListener("change", cb);
};

function horas(ms: number) {
  const m = Math.round(ms / 60000);
  return m >= 60 ? `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")}` : `${m} min`;
}

/**
 * /jai-sounds: la batea. Una sola pieza de cliente porque todo cuelga de
 * la estación actual: la consola, el disco de frente, la contraportada y la
 * ficha. La estación vive en el hash (#09) para compartir y volver.
 */
export default function Batea({
  estaciones,
  inicial,
}: {
  estaciones: ResumenEstacion[];
  inicial: DatosEstacion | null;
}) {
  const N = estaciones.length;
  const leerHash = useCallback(() => {
    const n = Number.parseInt(location.hash.slice(1), 10);
    return n >= 1 && n <= N ? n - 1 : 0;
  }, [N]);
  const actual = useSyncExternalStore(suscribirHash, leerHash, () => 0);
  const [ficha, setFicha] = useState<string | null>(null);
  const [embed, setEmbed] = useState(false);
  const [datos, setDatos] = useState<Record<number, DatosEstacion>>(() => (inicial ? { [inicial.i]: inicial } : {}));
  // Qué estaciones ya se pidieron: solo se lee en callbacks, nunca al renderizar.
  const pedidas = useRef(new Set<number>(inicial && !inicial.parcial ? [inicial.i] : []));

  const semilla = useSyncExternalStore(sinCambios, semillaDeSesion, () => null);
  const quieto = useSyncExternalStore(
    sinMovimiento,
    () => matchMedia("(prefers-reduced-motion: reduce)").matches,
    () => false
  );

  const pedir = useCallback((k: number) => {
    if (pedidas.current.has(k)) return;
    pedidas.current.add(k);
    fetch(`/jai-sounds/datos/${num(k)}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d: DatosEstacion | null) => {
        if (d) setDatos((prev) => ({ ...prev, [k]: d }));
        else pedidas.current.delete(k);
      })
      .catch(() => pedidas.current.delete(k));
  }, []);

  const ir = useCallback(
    (k: number) => {
      const n = ((k % N) + N) % N;
      setFicha(null);
      setEmbed(false);
      try {
        history.replaceState(null, "", `#${num(n)}`);
      } catch {}
      dispatchEvent(new Event(EVENTO));
    },
    [N]
  );

  // La actual y sus vecinas: pasar de disco no espera la red.
  useEffect(() => {
    pedir(actual);
    pedir((actual + 1) % N);
    pedir((actual - 1 + N) % N);
  }, [actual, N, pedir]);

  useEffect(() => {
    const tecla = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (ficha || t?.closest?.("input, textarea, select, iframe")) return;
      if (e.key === "ArrowRight") ir(actual + 1);
      if (e.key === "ArrowLeft") ir(actual - 1);
    };
    addEventListener("keydown", tecla);
    return () => removeEventListener("keydown", tecla);
  }, [actual, ficha, ir]);

  const e = estaciones[actual];
  const d = datos[actual] ?? null;
  const hue = semilla === null ? null : hueDeEstacion(semilla, actual, N);
  const filaFicha = d && ficha ? d.filas.findIndex((f) => f.s === ficha) : -1;
  const marcar = () => empezarEn({ tipo: "estacion", slug: e.slug, n: e.nombre, e: e.i });
  const cz = e.censo;
  const stats: [string, string | null][] = [
    ["pistas", String(cz.pistas)],
    ["duración", cz.ms ? horas(cz.ms) : null],
    ["años", cz.desde ? (cz.desde === cz.hasta ? String(cz.desde) : `${cz.desde}–${cz.hasta}`) : null],
    ["artistas", cz.artistas ? String(cz.artistas) : null],
  ];
  const vecina = (k: number) => estaciones[((k % N) + N) % N];

  return (
    <div className="jai-estacion" style={{ "--jai-i": actual } as CSSProperties}>
      {/* ── la consola ── */}
      <header className="border-b border-(--jai-rule)">
        <div className="mx-auto flex max-w-[1280px] flex-wrap items-center gap-x-7 gap-y-3.5 px-[clamp(16px,4vw,32px)] py-3.5">
          <Link href="/jai-sounds" className="flex items-center gap-3">
            <JA tamano={30} />
            <span className="jai-display text-2xl leading-none lowercase text-(--jai-luz)">jai sounds</span>
          </Link>
          <span className="jai-dato text-[11px] text-(--jai-luz-faint)">jai · caquetío · oír, escuchar</span>
          <div className="flex h-[22px] min-w-[200px] flex-[1_1_240px] items-end gap-0.5" aria-label="el dial">
            {estaciones.map((x, k) => (
              <button
                key={x.slug}
                onClick={() => ir(k)}
                title={`${num(k)} · ${x.nombre}`}
                aria-label={`${num(k)} · ${x.nombre}`}
                className="jai-estacion flex h-full flex-1 items-end justify-center"
                style={{ "--jai-i": k } as CSSProperties}
              >
                <span
                  className="block transition-[background-color,height] duration-300"
                  style={{
                    width: k === actual ? 3 : 1,
                    height: k === actual ? "100%" : k % 5 === 0 ? "55%" : "35%",
                    background: k === actual ? "var(--jai-senal)" : "var(--jai-luz-faint)",
                  }}
                />
              </button>
            ))}
          </div>
          <span className="jai-dato whitespace-nowrap text-[11px] text-(--jai-senal)">
            estación {num(actual)} / {N} · hue {hue === null ? "···" : String(hue).padStart(3, "0")}
          </span>
        </div>
      </header>

      <main className="mx-auto grid max-w-[1280px] items-start gap-x-[clamp(32px,5vw,72px)] gap-y-10 px-[clamp(16px,4vw,32px)] pb-24 pt-10 min-[900px]:grid-cols-[minmax(0,520px)_minmax(0,1fr)]">
        {/* ── la batea ── */}
        <section aria-label="La batea" className="flex min-w-0 flex-col gap-[18px] min-[900px]:sticky min-[900px]:top-6">
          <div className="jai-dato flex justify-between gap-3 text-[11px] lowercase text-(--jai-luz-faint)">
            <span>la batea · {N} discos</span>
            <span className="truncate text-(--jai-luz-soft)">
              {num(actual)} · {e.nombre.toLowerCase()}
            </span>
          </div>
          <Pila estaciones={estaciones} actual={actual} ir={ir} quieto={quieto} />
          <div className="h-px bg-(--jai-rule)" />
          <div className="flex justify-between gap-3">
            {[-1, 1].map((paso) => (
              <button
                key={paso}
                onClick={() => ir(actual + paso)}
                className={`jai-dato max-w-[48%] truncate py-1.5 text-[11px] lowercase text-(--jai-luz-faint) transition-colors duration-300 hover:text-(--jai-luz) ${paso > 0 ? "text-right" : "text-left"}`}
              >
                {paso < 0 ? `← ${num(actual - 1 < 0 ? N - 1 : actual - 1)} · ${vecina(actual - 1).nombre.toLowerCase()}` : `${num((actual + 1) % N)} · ${vecina(actual + 1).nombre.toLowerCase()} →`}
              </button>
            ))}
          </div>
          <div className="flex flex-col gap-2">
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">
              separadores · <span className="min-[900px]:hidden">desliza el disco a los lados</span>
              <span className="hidden min-[900px]:inline">← → o rueda para pasar discos</span>
            </span>
            <div className="grid grid-cols-[repeat(23,44px)] gap-[3px] overflow-x-auto pb-1 [scrollbar-width:none] min-[900px]:grid-cols-[repeat(23,minmax(0,1fr))]">
              {estaciones.map((x, k) => (
                <button
                  key={x.slug}
                  onClick={() => ir(k)}
                  title={`${num(k)} · ${x.nombre}`}
                  aria-label={`${num(k)} · ${x.nombre}`}
                  aria-current={k === actual || undefined}
                  className="jai-estacion flex flex-col gap-[3px] transition-opacity duration-300 hover:opacity-100"
                  style={{ "--jai-i": k, opacity: k === actual ? 1 : 0.62 } as CSSProperties}
                >
                  {x.portada ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={x.portada}
                      alt=""
                      loading="lazy"
                      className="block aspect-square w-full object-cover outline-offset-1"
                      style={{ outline: k === actual ? "1px solid var(--jai-luz)" : "1px solid transparent" }}
                    />
                  ) : (
                    <span className="block aspect-square w-full bg-(--jai-senal-tenue)" />
                  )}
                  <span className="block h-[3px] bg-(--jai-senal)" />
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* ── la contraportada ── */}
        <section aria-label="Contraportada" aria-live="polite" className="flex min-w-0 flex-col gap-7">
          <div className="flex flex-col gap-3.5">
            <span className="jai-dato text-[11px] text-(--jai-senal)">contraportada · estación {num(actual)}</span>
            <h1 className="jai-display m-0 text-[clamp(44px,5.4vw,76px)] leading-[0.92] lowercase text-balance text-(--jai-luz)">
              {e.nombre}
            </h1>
          </div>

          <dl className="m-0 grid grid-cols-[repeat(auto-fit,minmax(118px,1fr))] border-l border-t border-(--jai-rule)">
            {stats.map(([k, v]) => (
              <div key={k} className="flex flex-col gap-2 border-b border-r border-(--jai-rule) px-4 pb-4 pt-3.5">
                <dt className="jai-dato text-[10px] text-(--jai-luz-faint)">{k}</dt>
                <dd className={`jai-titulo m-0 text-[28px] leading-none ${v ? "text-(--jai-luz)" : "text-(--jai-luz-faint)"}`}>{v ?? "—"}</dd>
              </div>
            ))}
          </dl>

          <div className="grid gap-2.5">
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">más presentes</span>
            <ol className="m-0 flex list-none flex-wrap gap-2 p-0">
              {cz.presentes.map((p) => (
                <li key={p.s}>
                  <Link
                    href={`/jai-sounds/artistas/${p.s}`}
                    onClick={marcar}
                    className="flex items-baseline gap-2.5 border border-(--jai-rule) px-3 py-[9px] transition-colors duration-300 hover:border-(--jai-senal)"
                  >
                    <span className="text-[15px] font-medium">{p.n}</span>
                    <span className="font-(family-name:--jai-mono) text-[11px] tracking-[0.2em] text-(--jai-senal)">×{p.veces}</span>
                  </Link>
                </li>
              ))}
            </ol>
          </div>

          <div className="grid gap-2.5 border-y border-(--jai-rule) py-[18px]">
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">nota de curaduría</span>
            <p className="jai-manifiesto m-0 max-w-[44ch] text-xl leading-[1.4] text-(--jai-luz-faint)">
              JAI Sounds aún no le escribe nota a esta estación.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            <div className="flex flex-wrap items-center gap-x-5 gap-y-3">
              <button
                onClick={() => setEmbed(!embed)}
                className="bg-(--jai-senal) px-[22px] py-[15px] font-sans text-[11px] font-semibold uppercase tracking-[0.2em] text-(--jai-noche) transition-colors duration-300 hover:bg-(--jai-luz)"
              >
                {embed ? "■ cerrar el reproductor" : "▶ escuchar en spotify"}
              </button>
              <a
                href={`https://open.spotify.com/playlist/${e.spotify_id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="jai-dato text-[11px] text-(--jai-luz-faint) transition-colors duration-300 hover:text-(--jai-luz)"
              >
                abrir la playlist ↗
              </a>
            </div>
            {embed ? (
              <div className="border border-(--jai-rule) bg-(--jai-panel) p-2">
                <iframe
                  title={`${e.nombre} en Spotify`}
                  src={`https://open.spotify.com/embed/playlist/${e.spotify_id}?utm_source=generator&theme=0`}
                  width="100%"
                  height="152"
                  allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                  loading="lazy"
                  className="block border-0"
                />
              </div>
            ) : null}
          </div>

          <div className="flex flex-col">
            <div className="jai-dato flex justify-between gap-3 border-b border-(--jai-rule) pb-2.5 text-[10px] text-(--jai-luz-faint)">
              <span>tracklist · {cz.pistas} pistas</span>
              <span className="hidden sm:inline">toca una pista para ver su ficha</span>
            </div>
            {d ? (
              d.filas.map((f, k) => {
                const activa = ficha === f.s;
                return (
                  <button
                    key={f.s}
                    onClick={() => setFicha(f.s)}
                    className="grid w-full grid-cols-[34px_40px_minmax(0,1fr)_auto] items-center gap-3.5 border-b border-l-3 border-b-(--jai-rule) py-3 pl-[9px] pr-3 text-left transition-colors duration-300 hover:border-l-(--jai-senal) hover:bg-(--jai-panel) sm:grid-cols-[40px_40px_minmax(0,1fr)_auto]"
                    style={{
                      borderLeftColor: activa ? "var(--jai-senal)" : "transparent",
                      background: activa ? "var(--jai-panel)" : undefined,
                    }}
                  >
                    <span className="font-(family-name:--jai-mono) text-[11px] tracking-[0.1em] text-(--jai-luz-faint)">{String(k + 1).padStart(3, "0")}</span>
                    <span className="box-border block aspect-square w-10 border border-(--jai-rule) bg-(--jai-senal-tenue)">
                      {f.img ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={f.img.replace("ab67616d0000b273", "ab67616d00004851")} alt="" loading="lazy" className="block h-full w-full object-cover" />
                      ) : null}
                    </span>
                    <span className="flex min-w-0 flex-col gap-[3px]">
                      <span className="truncate text-[15px] font-medium leading-[1.3]">{f.t}</span>
                      <span className="truncate text-[13px] text-(--jai-luz-soft)">{f.a.map((a) => a.n).join(", ")}</span>
                    </span>
                    <span className="flex items-center gap-3.5 font-(family-name:--jai-mono) text-[11px] tracking-[0.1em] text-(--jai-luz-soft)">
                      {f.r ? <span className="tracking-[0.3em] text-(--jai-senal)">reseña</span> : null}
                      <span className="hidden text-(--jai-luz-faint) sm:inline">{f.y}</span>
                      <span>{f.d}</span>
                    </span>
                  </button>
                );
              })
            ) : null}
            {d?.parcial ? (
              <p className="jai-dato m-0 mt-3.5 text-[10px] leading-[1.9] text-(--jai-luz-faint)">sintonizando el resto del tracklist…</p>
            ) : null}
            {!d ? (
              ["62%", "48%", "70%", "40%", "56%"].map((ancho) => (
                <div key={ancho} className="jai-latido grid grid-cols-[40px_40px_minmax(0,1fr)_64px] items-center gap-3.5 border-b border-(--jai-rule) p-3">
                  <span className="h-2 bg-(--jai-panel)" />
                  <span className="aspect-square w-10 bg-(--jai-panel)" />
                  <span className="flex flex-col gap-1.5">
                    <span className="h-2.5 bg-(--jai-panel)" style={{ width: ancho }} />
                    <span className="h-2 w-[36%] bg-(--jai-panel)" />
                  </span>
                  <span className="h-2 bg-(--jai-panel)" />
                </div>
              ))
            ) : null}
          </div>
        </section>
      </main>

      {d && filaFicha >= 0 ? (
        <Ficha
          fila={d.filas[filaFicha]}
          pos={filaFicha + 1}
          total={d.filas.length}
          estacion={e}
          estaciones={estaciones}
          antes={d.filas[filaFicha - 1] ?? null}
          despues={d.filas[filaFicha + 1] ?? null}
          abrir={setFicha}
          cerrar={() => setFicha(null)}
          irEstacion={ir}
        />
      ) : null}
    </div>
  );
}
