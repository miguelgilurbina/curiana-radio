"use client";

import { useMemo, useState, type CSSProperties } from "react";
import {
  formatearDuracion,
  type TrackResuelto,
} from "@/lib/jai-sounds-muestra/tipos";
import type { Mood } from "@/types/jai-sounds";

/**
 * PROPUESTA B · "Mesa de curaduría" — gestión de canciones.
 *
 * Tesis: con 12.000 pistas, una herramienta que solo LISTA no sirve de nada
 * — nadie navega 12.000 filas. Lo que sirve es una que muestre el HUECO:
 * qué falta por asignar, qué falta por anotar, dónde está la deuda
 * curatorial. Por eso lo primero de la pantalla es la cobertura, y el filtro
 * más importante es "sin nota", no "buscar".
 *
 * Es una maqueta: los controles filtran de verdad, pero editar todavía no
 * escribe en ningún lado (haría falta la tabla jai_curation y una acción de
 * servidor).
 */

type Orden = "curatorial" | "nombre" | "artista" | "anio" | "popularidad";

const ORDENES: { valor: Orden; etiqueta: string }[] = [
  { valor: "curatorial", etiqueta: "Deuda curatorial" },
  { valor: "nombre", etiqueta: "Título" },
  { valor: "artista", etiqueta: "Artista" },
  { valor: "anio", etiqueta: "Año" },
  { valor: "popularidad", etiqueta: "Popularidad" },
];

function Barra({
  hecho,
  total,
  etiqueta,
}: {
  hecho: number;
  total: number;
  etiqueta: string;
}) {
  const pct = total === 0 ? 0 : Math.round((hecho / total) * 100);
  return (
    <div className="flex-1 min-w-[9rem]">
      <div className="flex justify-between font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-luz-faint)">
        <span>{etiqueta}</span>
        <span className="tabular-nums text-(--jai-luz-soft)">{pct}%</span>
      </div>
      <div className="mt-2 h-1 bg-(--jai-rule)">
        <div className="h-full bg-(--jai-senal)" style={{ width: `${pct}%` }} />
      </div>
      <div className="mt-1 font-(family-name:--jai-mono) text-[0.65rem] tabular-nums text-(--jai-luz-faint)">
        {hecho} / {total}
      </div>
    </div>
  );
}

export default function PropuestaMesa({
  pistas,
  moods,
}: {
  pistas: TrackResuelto[];
  moods: Mood[];
}) {
  const [busqueda, setBusqueda] = useState("");
  const [moodFiltro, setMoodFiltro] = useState<string | null>(null);
  const [soloSinNota, setSoloSinNota] = useState(false);
  const [orden, setOrden] = useState<Orden>("curatorial");

  const conMood = pistas.filter((p) => p.mood).length;
  const conNota = pistas.filter((p) => p.nota).length;

  const visibles = useMemo(() => {
    const q = busqueda.trim().toLowerCase();
    const filtradas = pistas.filter((p) => {
      if (soloSinNota && p.nota) return false;
      if (moodFiltro && p.mood_slug !== moodFiltro) return false;
      if (!q) return true;
      return (
        p.nombre.toLowerCase().includes(q) ||
        p.album?.nombre.toLowerCase().includes(q) ||
        p.artistasResueltos.some((a) => a.nombre.toLowerCase().includes(q)) ||
        p.generos.some((g) => g.includes(q))
      );
    });

    const peso = (p: TrackResuelto) => (p.nota ? 0 : 1) + (p.mood ? 0 : 2);
    const cmp: Record<Orden, (a: TrackResuelto, b: TrackResuelto) => number> = {
      // Lo no curado primero: la lista se ordena por lo que falta hacer.
      curatorial: (a, b) => peso(b) - peso(a) || b.popularidad - a.popularidad,
      nombre: (a, b) => a.nombre.localeCompare(b.nombre, "es"),
      artista: (a, b) =>
        (a.artistasResueltos[0]?.nombre ?? "").localeCompare(
          b.artistasResueltos[0]?.nombre ?? "",
          "es"
        ),
      anio: (a, b) => (b.album?.anio ?? 0) - (a.album?.anio ?? 0),
      popularidad: (a, b) => b.popularidad - a.popularidad,
    };
    return [...filtradas].sort(cmp[orden]);
  }, [pistas, busqueda, moodFiltro, soloSinNota, orden]);

  return (
    <div className="bg-(--jai-panel)">
      {/* Lo primero de la pantalla: la deuda, no el catálogo. */}
      <div className="px-6 py-6 md:px-8 border-b border-(--jai-rule) flex flex-wrap gap-6">
        <Barra hecho={conMood} total={pistas.length} etiqueta="Con mood" />
        <Barra hecho={conNota} total={pistas.length} etiqueta="Con nota" />
      </div>

      {/* Controles */}
      <div className="px-6 py-5 md:px-8 border-b border-(--jai-rule) space-y-4">
        <div className="flex flex-wrap gap-3">
          <input
            type="search"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            placeholder="Título, artista, álbum o género…"
            aria-label="Buscar pistas"
            className="flex-1 min-w-[14rem] bg-(--jai-noche) border border-(--jai-rule) px-4 py-2 text-sm text-(--jai-luz) placeholder:text-(--jai-luz-faint) focus:outline-none focus:border-(--jai-senal)"
          />
          <label className="flex items-center gap-2 font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-widest text-(--jai-luz-soft) cursor-pointer">
            <input
              type="checkbox"
              checked={soloSinNota}
              onChange={(e) => setSoloSinNota(e.target.checked)}
              className="accent-(--jai-senal)"
            />
            Solo sin nota
          </label>
          <label className="flex items-center gap-2 font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-widest text-(--jai-luz-faint)">
            Orden
            <select
              value={orden}
              onChange={(e) => setOrden(e.target.value as Orden)}
              className="bg-(--jai-noche) border border-(--jai-rule) px-2 py-1 text-(--jai-luz) focus:outline-none focus:border-(--jai-senal)"
            >
              {ORDENES.map((o) => (
                <option key={o.valor} value={o.valor}>
                  {o.etiqueta}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setMoodFiltro(null)}
            className={`font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest border rounded-full px-3 py-1 transition-colors ${
              moodFiltro === null
                ? "border-(--jai-luz) text-(--jai-luz)"
                : "border-(--jai-rule) text-(--jai-luz-faint) hover:text-(--jai-luz-soft)"
            }`}
          >
            Todos
          </button>
          {moods.map((m) => (
            <button
              key={m.slug}
              style={{ "--jai-hue": m.hue } as CSSProperties}
              onClick={() =>
                setMoodFiltro(moodFiltro === m.slug ? null : m.slug)
              }
              className={`jai-estacion font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest border rounded-full px-3 py-1 transition-colors ${
                moodFiltro === m.slug
                  ? "border-(--jai-senal) text-(--jai-senal)"
                  : "border-(--jai-rule) text-(--jai-luz-faint) hover:text-(--jai-senal)"
              }`}
            >
              {m.nombre}
            </button>
          ))}
        </div>
      </div>

      {/* Tabla */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <caption className="sr-only">
            Pistas del catálogo con su estado de curaduría
          </caption>
          <thead>
            <tr className="font-(family-name:--jai-mono) text-[0.6rem] uppercase tracking-widest text-(--jai-luz-faint) text-left">
              <th scope="col" className="px-6 md:px-8 py-3 font-normal">Pista</th>
              <th scope="col" className="px-3 py-3 font-normal">Álbum</th>
              <th scope="col" className="px-3 py-3 font-normal">Mood</th>
              <th scope="col" className="px-3 py-3 font-normal">Nota</th>
              <th scope="col" className="px-3 py-3 font-normal text-right">Dur.</th>
              <th scope="col" className="px-6 md:px-8 py-3 font-normal text-right">Pop.</th>
            </tr>
          </thead>
          <tbody>
            {visibles.map((p) => (
              <tr
                key={p.id}
                style={{ "--jai-hue": p.mood?.hue ?? 40 } as CSSProperties}
                className="jai-estacion border-t border-(--jai-rule) hover:bg-(--jai-senal-tenue)"
              >
                <th scope="row" className="px-6 md:px-8 py-3 font-normal text-left">
                  <div className="flex items-center gap-2">
                    {p.destacado && (
                      <span
                        title="Destacada"
                        className="text-(--jai-senal) text-xs"
                      >
                        ★
                      </span>
                    )}
                    <span className="text-(--jai-luz)">{p.nombre}</span>
                  </div>
                  <div className="text-xs text-(--jai-luz-faint) mt-0.5">
                    {p.artistasResueltos.map((a) => a.nombre).join(" · ")}
                  </div>
                </th>
                <td className="px-3 py-3 text-(--jai-luz-faint) whitespace-nowrap">
                  {p.album?.nombre}{" "}
                  <span className="tabular-nums">({p.album?.anio})</span>
                </td>
                <td className="px-3 py-3 whitespace-nowrap">
                  {p.mood ? (
                    <span className="font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-senal)">
                      {p.mood.nombre}
                    </span>
                  ) : (
                    <span className="font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-luz-faint)">
                      sin asignar
                    </span>
                  )}
                </td>
                <td className="px-3 py-3 max-w-xs">
                  {p.nota ? (
                    <span className="text-(--jai-luz-soft) text-xs line-clamp-2">
                      {p.nota}
                    </span>
                  ) : (
                    <span className="font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-widest text-(--jai-luz-faint) border border-dashed border-(--jai-rule) rounded px-2 py-0.5">
                      falta
                    </span>
                  )}
                </td>
                <td className="px-3 py-3 text-right font-(family-name:--jai-mono) text-xs tabular-nums text-(--jai-luz-faint)">
                  {formatearDuracion(p.duracion_ms)}
                </td>
                <td className="px-6 md:px-8 py-3 text-right font-(family-name:--jai-mono) text-xs tabular-nums text-(--jai-luz-faint)">
                  {p.popularidad}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {visibles.length === 0 && (
          <p className="px-6 md:px-8 py-10 text-center text-(--jai-luz-faint)">
            Ninguna pista coincide con el filtro.
          </p>
        )}
      </div>

      <div className="px-6 md:px-8 py-4 border-t border-(--jai-rule) font-(family-name:--jai-mono) text-[0.7rem] tabular-nums text-(--jai-luz-faint)">
        {visibles.length} de {pistas.length} pistas
      </div>
    </div>
  );
}
