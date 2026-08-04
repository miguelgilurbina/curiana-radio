import type { CSSProperties } from "react";
import type {
  AlbumMuestra,
  ArtistaResuelto,
} from "@/lib/jai-sounds-muestra/tipos";

/**
 * PROPUESTA C · "Fichas y cruces" — gestión de artistas y álbumes.
 *
 * Tesis: un directorio alfabético de artistas no dice nada que Spotify no
 * diga ya. Lo que este proyecto puede mostrar y Spotify no es DÓNDE SE
 * CRUZAN: qué géneros comparte cada artista con los demás del catálogo. Por
 * eso la ficha no lleva biografía — lleva sus géneros y sus vecinos, con lo
 * común resaltado. El cruce es el contenido.
 *
 * Los álbumes van debajo como estantería, agrupados por década: es la vista
 * que permite ver de un golpe si el catálogo está sesgado a un periodo.
 */

function Genero({ nombre, comun }: { nombre: string; comun?: boolean }) {
  return (
    <span
      className={`font-(family-name:--jai-mono) text-[0.6rem] uppercase tracking-widest rounded-full px-2 py-0.5 border ${
        comun
          ? "border-(--jai-senal) text-(--jai-senal)"
          : "border-(--jai-rule) text-(--jai-luz-faint)"
      }`}
    >
      {nombre}
    </span>
  );
}

function Ficha({ artista }: { artista: ArtistaResuelto }) {
  const vecinos = artista.vecinos.slice(0, 3);
  return (
    <article
      style={{ "--jai-hue": artista.hue } as CSSProperties}
      className="jai-estacion bg-(--jai-panel) border-l-2 border-(--jai-senal) p-5"
    >
      <header className="flex items-baseline justify-between gap-3">
        <h4 className="font-(family-name:--jai-display) text-xl">
          {artista.nombre}
        </h4>
        <span className="font-(family-name:--jai-mono) text-[0.65rem] tabular-nums text-(--jai-luz-faint) shrink-0">
          {artista.totalPistas} {artista.totalPistas === 1 ? "pista" : "pistas"}
          {artista.albums.length > 0 && ` · ${artista.albums.length} álb.`}
        </span>
      </header>

      <ul className="mt-3 flex flex-wrap gap-1.5">
        {artista.generos.map((g) => (
          <li key={g}>
            <Genero nombre={g} />
          </li>
        ))}
      </ul>

      {artista.moods.length > 0 && (
        <p className="mt-3 font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-luz-faint)">
          Suena en: {artista.moods.map((m) => m.nombre).join(" · ")}
        </p>
      )}

      {vecinos.length > 0 && (
        <div className="mt-4 pt-3 border-t border-(--jai-rule)">
          <p className="font-(family-name:--jai-mono) text-[0.6rem] uppercase tracking-[0.2em] text-(--jai-luz-faint)">
            Cruza con
          </p>
          <ul className="mt-2 space-y-1.5">
            {vecinos.map(({ artista: otro, comunes }) => (
              <li key={otro.id} className="flex flex-wrap items-baseline gap-2">
                <span className="text-sm text-(--jai-luz-soft)">
                  {otro.nombre}
                </span>
                {comunes.map((g) => (
                  <Genero key={g} nombre={g} comun />
                ))}
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}

function Estanteria({
  albums,
  artistas,
}: {
  albums: AlbumMuestra[];
  artistas: ArtistaResuelto[];
}) {
  const nombreDe = new Map(artistas.map((a) => [a.id, a.nombre]));
  const hueDe = new Map(artistas.map((a) => [a.id, a.hue]));

  // Agrupar por década: revela de un vistazo si el catálogo está sesgado.
  const decadas = new Map<number, AlbumMuestra[]>();
  for (const d of [...albums].sort((a, b) => a.anio - b.anio)) {
    const dec = Math.floor(d.anio / 10) * 10;
    decadas.set(dec, [...(decadas.get(dec) ?? []), d]);
  }

  return (
    <div className="space-y-8">
      {[...decadas.entries()].map(([dec, discos]) => (
        <div key={dec}>
          <h4 className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.25em] text-(--jai-luz-faint) border-b border-(--jai-rule) pb-2">
            {dec}s · {discos.length}
          </h4>
          <ul className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {discos.map((d) => (
              <li
                key={d.id}
                style={{ "--jai-hue": hueDe.get(d.artista_id) ?? 40 } as CSSProperties}
                className="jai-estacion bg-(--jai-panel) p-4 flex gap-3 items-start"
              >
                {/* Sin carátulas: la muestra no depende de imágenes externas.
                    El bloque de color hereda el matiz del artista. */}
                <span
                  aria-hidden
                  className="w-10 h-10 shrink-0 bg-(--jai-senal) opacity-70"
                />
                <div className="min-w-0">
                  <p className="text-(--jai-luz) truncate">{d.nombre}</p>
                  <p className="text-xs text-(--jai-luz-faint) truncate">
                    {nombreDe.get(d.artista_id)}
                  </p>
                  <p className="font-(family-name:--jai-mono) text-[0.65rem] tabular-nums text-(--jai-luz-faint) mt-1">
                    {d.anio}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default function PropuestaFichas({
  artistas,
  albums,
}: {
  artistas: ArtistaResuelto[];
  albums: AlbumMuestra[];
}) {
  const ordenados = [...artistas].sort(
    (a, b) => b.vecinos.length - a.vecinos.length || b.totalPistas - a.totalPistas
  );

  return (
    <div className="space-y-12">
      <div>
        <p className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.25em] text-(--jai-luz-faint) mb-4">
          Artistas · ordenados por cuánto cruzan
        </p>
        <div className="grid gap-3 md:grid-cols-2">
          {ordenados.map((a) => (
            <Ficha key={a.id} artista={a} />
          ))}
        </div>
      </div>

      <div>
        <p className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.25em] text-(--jai-luz-faint) mb-4">
          Álbumes · por década
        </p>
        <Estanteria albums={albums} artistas={artistas} />
      </div>
    </div>
  );
}
