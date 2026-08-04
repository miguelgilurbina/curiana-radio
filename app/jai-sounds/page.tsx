import type { CSSProperties } from "react";
import {
  contarMood,
  getCenso,
  getMoods,
  hayTaxonomiaEnBorrador,
} from "@/lib/jai-sounds";

// El catálogo cambia cuando corre la ingesta, no cuando entra una visita.
export const revalidate = 3600;

function Cifra({ valor, etiqueta }: { valor: number; etiqueta: string }) {
  return (
    <div>
      <div className="font-(family-name:--jai-mono) text-2xl md:text-3xl tabular-nums text-(--jai-luz)">
        {valor > 0 ? valor.toLocaleString("es") : "—"}
      </div>
      <div className="font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-[0.2em] text-(--jai-luz-faint) mt-1">
        {etiqueta}
      </div>
    </div>
  );
}

export default async function JaiSoundsPage() {
  const moods = getMoods();
  const censo = await getCenso();
  const enBorrador = hayTaxonomiaEnBorrador(moods);

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
      {/* ── Cabecera: la banda ─────────────────────────────────────── */}
      <header className="border-b border-(--jai-rule) pb-10">
        <p className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.3em] text-(--jai-luz-faint)">
          88.8 FM · Curaduría
        </p>
        <h1 className="font-(family-name:--jai-display) text-5xl md:text-7xl mt-4 leading-[1.05]">
          JAI Sounds
        </h1>
        <p className="mt-6 max-w-reading text-body text-(--jai-luz-soft)">
          Un dial, no un catálogo. Cada estación es un{" "}
          <em>mood</em> — un estado, no un género — y lo que la sintoniza es
          que cruza fronteras que la industria dibujó por conveniencia.
        </p>
        <p className="mt-4 max-w-reading text-sm text-(--jai-luz-faint)">
          En noviembre de 2024 Spotify apagó el acceso público a sus medidas de{" "}
          <span className="font-(family-name:--jai-mono)">valence</span> y{" "}
          <span className="font-(family-name:--jai-mono)">energy</span>. Aquí
          eso no es una pérdida: el mood nunca fue un número. Lo decide el
          oído, y queda escrito.
        </p>
      </header>

      {/* ── Censo del catálogo ─────────────────────────────────────── */}
      <section className="grid grid-cols-3 gap-6 py-10 border-b border-(--jai-rule)">
        <Cifra valor={censo.tracks} etiqueta="Pistas" />
        <Cifra valor={censo.artistas} etiqueta="Artistas" />
        <Cifra valor={censo.playlists} etiqueta="Playlists" />
      </section>

      {censo.tracks === 0 && (
        <p className="mt-8 font-(family-name:--jai-mono) text-xs leading-relaxed text-(--jai-luz-faint) border-l-2 border-(--jai-rule) pl-4">
          Catálogo vacío: la migración de Supabase y la ingesta desde Spotify
          todavía no han corrido. Ver{" "}
          <span className="text-(--jai-luz-soft)">jai-sounds/README.md</span>.
        </p>
      )}

      {enBorrador && (
        <p className="mt-4 font-(family-name:--jai-mono) text-xs leading-relaxed text-(--jai-luz-faint) border-l-2 border-(--jai-senal) pl-4">
          Taxonomía en borrador: los moods de abajo son andamio para que el
          dial exista, no curaduría. Se reemplazan por los reales al derivarlos
          de las playlists.
        </p>
      )}

      {/* ── El dial ────────────────────────────────────────────────── */}
      <section className="mt-16">
        <h2 className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.3em] text-(--jai-luz-faint) mb-8">
          El dial · {moods.length} estaciones
        </h2>

        {moods.length === 0 ? (
          <p className="text-(--jai-luz-faint)">
            No hay taxonomía todavía. Falta{" "}
            <span className="font-(family-name:--jai-mono)">
              content/jai-sounds/moods.json
            </span>
            .
          </p>
        ) : (
          <ol className="space-y-px">
            {moods.map((mood) => {
              const total = contarMood(mood, censo);
              return (
                <li
                  key={mood.slug}
                  style={{ "--jai-hue": mood.hue } as CSSProperties}
                  className="jai-estacion group relative bg-(--jai-panel) px-5 py-6 md:px-8 md:py-8 transition-colors hover:bg-(--jai-senal-tenue)"
                >
                  {/* La aguja: el matiz del mood, encendido al pasar */}
                  <span
                    aria-hidden
                    className="absolute left-0 top-0 bottom-0 w-[3px] bg-(--jai-senal) opacity-40 transition-opacity group-hover:opacity-100"
                  />
                  <div className="md:flex md:items-baseline md:gap-8">
                    <div className="font-(family-name:--jai-mono) text-sm tabular-nums text-(--jai-senal) shrink-0 md:w-20">
                      {mood.frecuencia}
                    </div>
                    <div className="mt-2 md:mt-0 flex-1">
                      <h3 className="font-(family-name:--jai-display) text-2xl md:text-3xl">
                        {mood.nombre}
                      </h3>
                      <p className="mt-2 max-w-reading text-(--jai-luz-soft)">
                        {mood.bajada}
                      </p>
                      <ul className="mt-4 flex flex-wrap gap-2">
                        {mood.cruces.map((cruce) => (
                          <li
                            key={cruce}
                            className="font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-luz-faint) border border-(--jai-rule) rounded-full px-3 py-1"
                          >
                            {cruce}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="mt-4 md:mt-0 font-(family-name:--jai-mono) text-xs tabular-nums text-(--jai-luz-faint) shrink-0 md:text-right md:w-24">
                      {total > 0 ? `${total.toLocaleString("es")} pistas` : "sin pistas"}
                    </div>
                  </div>
                </li>
              );
            })}
          </ol>
        )}
      </section>
    </div>
  );
}
