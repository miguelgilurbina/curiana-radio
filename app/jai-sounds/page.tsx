import type { CSSProperties } from "react";
import { getCenso, getPlaylists, hueDeSlug } from "@/lib/jai-sounds";
import type { FichaPlaylist } from "@/types/jai-sounds";

// El catálogo cambia cuando corre la ingesta, no cuando entra una visita.
export const revalidate = 3600;

function Estacion({ ficha }: { ficha: FichaPlaylist }) {
  return (
    <li
      style={{ "--jai-hue": hueDeSlug(ficha.slug) } as CSSProperties}
      className="jai-estacion group relative bg-(--jai-panel) overflow-hidden"
    >
      {/* Mientras no haya portada propia, la placa de color hace de arte:
          estable por slug, así cada lista tiene identidad desde hoy. */}
      <div className="aspect-square relative">
        {ficha.portada ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={ficha.portada}
            alt=""
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <div className="absolute inset-0 bg-(--jai-senal-tenue) flex items-end p-4">
            <span
              aria-hidden
              className="font-(family-name:--jai-display) text-6xl leading-none text-(--jai-senal) opacity-40 select-none"
            >
              {ficha.nombre.trim().charAt(0)}
            </span>
          </div>
        )}
        <span
          aria-hidden
          className="absolute left-0 top-0 bottom-0 w-[3px] bg-(--jai-senal) opacity-60 transition-opacity group-hover:opacity-100"
        />
      </div>

      <div className="p-4">
        <h3 className="font-(family-name:--jai-display) text-lg leading-tight">
          {ficha.nombre}
        </h3>
        {ficha.descripcion ? (
          <p className="mt-2 text-sm text-(--jai-luz-soft)">
            {ficha.descripcion}
          </p>
        ) : null}
        <p className="mt-3 font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest tabular-nums text-(--jai-luz-faint)">
          {ficha.pistas} pistas
        </p>
        <a
          href={`https://open.spotify.com/playlist/${ficha.spotify_id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-block font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-luz-faint) hover:text-(--jai-senal) transition-colors"
        >
          Escuchar ↗
        </a>
      </div>
    </li>
  );
}

export default async function JaiSoundsPage() {
  const playlists = getPlaylists();
  const censo = await getCenso();
  const totalPistas = playlists.reduce((s, p) => s + (p.pistas ?? 0), 0);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
      {/* ── Quiénes somos ──────────────────────────────────────────── */}
      <header className="border-b border-(--jai-rule) pb-12">
        <p className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.3em] text-(--jai-luz-faint)">
          88.8 FM · Curaduría
        </p>
        <h1 className="font-(family-name:--jai-display) text-5xl md:text-7xl mt-4 leading-[1.05]">
          JAI Sounds
        </h1>
        <p className="mt-5 font-(family-name:--jai-mono) text-sm text-(--jai-senal)">
          jay · caquetío · ruido, sonido
        </p>
        <p className="mt-6 max-w-reading text-body text-(--jai-luz-soft)">
          Una curaduría sin fronteras de género. Ninguna canción entra por lo
          que es; entra por lo que describe — la experiencia viva que la trajo
          al mundo, y el sentimiento que la sostiene.
        </p>
      </header>

      {/* ── Las playlists: lo principal ────────────────────────────── */}
      <section className="mt-16">
        <div className="flex flex-wrap items-baseline justify-between gap-4 mb-8">
          <h2 className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.3em] text-(--jai-luz-faint)">
            El dial · {playlists.length} estaciones
          </h2>
          <p className="font-(family-name:--jai-mono) text-[0.7rem] tabular-nums text-(--jai-luz-faint)">
            {totalPistas.toLocaleString("es")} pistas curadas
            {censo.artistas > 0 &&
              ` · ${censo.artistas.toLocaleString("es")} artistas en el archivo`}
          </p>
        </div>

        {playlists.length === 0 ? (
          <p className="text-(--jai-luz-faint)">
            Todavía no hay playlists en{" "}
            <span className="font-(family-name:--jai-mono)">
              content/jai-sounds/playlists.json
            </span>
            .
          </p>
        ) : (
          <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {playlists.map((p) => (
              <Estacion key={p.slug} ficha={p} />
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
