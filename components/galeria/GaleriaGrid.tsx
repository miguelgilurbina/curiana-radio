"use client";

import { useMemo, useState, useSyncExternalStore } from "react";
import Mosaico from "./Mosaico";
import Lightbox from "./Lightbox";
import { mezclar, separarHermanas } from "@/lib/mosaico";
import {
  leerSemilla,
  leerSemillaServidor,
  rebarajar,
  suscribirse,
} from "@/lib/semilla-orden";
import type { ObraGrid, Serie } from "@/types/galeria";

interface GaleriaGridProps {
  obras: ObraGrid[];
  blobBase: string | null;
  series: Serie[];
  tags: { tag: string; total: number }[];
}

export default function GaleriaGrid({
  obras,
  blobBase,
  series,
  tags,
}: GaleriaGridProps) {
  const [serieActiva, setSerieActiva] = useState<string | null>(null);
  const [tagsActivos, setTagsActivos] = useState<string[]>([]);
  const [abierta, setAbierta] = useState<number | null>(null);

  // `null` en servidor (orden curatorial, el que se prerenderiza) y un número
  // en el navegador. Ver lib/semilla-orden.ts.
  const semilla = useSyncExternalStore(
    suscribirse,
    leerSemilla,
    leerSemillaServidor
  );

  const barajadas = useMemo(() => {
    if (semilla === null) return obras;
    // Barajar y luego apartar las obras que salieron de la misma parrilla de
    // Midjourney: se parecen mucho y el azar las junta cada tanto.
    return separarHermanas(mezclar(obras, semilla), (o) => o.generacion);
  }, [obras, semilla]);

  const visibles = useMemo(
    () =>
      barajadas.filter((obra) => {
        if (serieActiva && obra.serie !== serieActiva) return false;
        // Dentro de la faceta de tags la lógica es OR: sumar un tag amplía la
        // selección en vez de estrangularla hasta el estado vacío.
        if (tagsActivos.length > 0) {
          return tagsActivos.some((t) => obra.tags.includes(t));
        }
        return true;
      }),
    [barajadas, serieActiva, tagsActivos]
  );

  const hayFiltros = serieActiva !== null || tagsActivos.length > 0;

  // Cambiar el filtro reordena `visibles`, y el índice del lightbox apunta a
  // esa lista: cerrarlo evita quedar mirando otra obra de la que se abrió.
  const alternarTag = (tag: string) => {
    setAbierta(null);
    setTagsActivos((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const elegirSerie = (id: string | null) => {
    setAbierta(null);
    setSerieActiva(id);
  };

  const limpiar = () => {
    setAbierta(null);
    setSerieActiva(null);
    setTagsActivos([]);
  };

  const barajar = () => {
    setAbierta(null);
    rebarajar();
  };

  // Remonta el mosaico cuando cambia lo que muestra, para que la ventana de
  // piezas pintadas vuelva a empezar por la primera tanda.
  const firma = `${serieActiva ?? ""}|${tagsActivos.join(",")}|${semilla ?? ""}`;

  return (
    <div>
      {/* ── Filtros ─────────────────────────────────────────────── */}
      <div className="mb-8 space-y-4 border-y border-earth-200 py-6">
        {series.length > 1 && (
          <Faceta etiqueta="Serie">
            <Pill activo={serieActiva === null} onClick={() => elegirSerie(null)}>
              Todas
            </Pill>
            {series.map((serie) => (
              <Pill
                key={serie.id}
                activo={serieActiva === serie.id}
                onClick={() => elegirSerie(serie.id)}
              >
                {serie.titulo}
              </Pill>
            ))}
          </Faceta>
        )}

        {tags.length > 0 && (
          <Faceta etiqueta="Motivos">
            {tags.map(({ tag, total }) => (
              <Pill
                key={tag}
                activo={tagsActivos.includes(tag)}
                onClick={() => alternarTag(tag)}
              >
                {tag}
                <span className="ml-1.5 opacity-50">{total}</span>
              </Pill>
            ))}
          </Faceta>
        )}

        <div
          className="flex flex-wrap items-center gap-4 font-sans text-sm text-earth-600"
          aria-live="polite"
        >
          <span>
            {visibles.length} {visibles.length === 1 ? "obra" : "obras"}
          </span>
          <button
            type="button"
            onClick={barajar}
            className="border-b border-earth-400 transition-colors hover:border-frequency hover:text-frequency"
          >
            Barajar
          </button>
          {hayFiltros && (
            <button
              type="button"
              onClick={limpiar}
              className="border-b border-earth-400 transition-colors hover:border-frequency hover:text-frequency"
            >
              Limpiar filtros
            </button>
          )}
        </div>
      </div>

      {/* ── Mosaico ─────────────────────────────────────────────── */}
      {visibles.length > 0 ? (
        <Mosaico
          key={firma}
          obras={visibles}
          blobBase={blobBase}
          onAmpliar={setAbierta}
        />
      ) : (
        <p className="py-16 text-center font-sans text-earth-600">
          Ninguna obra coincide con esos filtros.
        </p>
      )}

      {abierta !== null && (
        <Lightbox
          obras={visibles}
          blobBase={blobBase}
          indice={abierta}
          onCerrar={() => setAbierta(null)}
          onIr={setAbierta}
        />
      )}
    </div>
  );
}

function Faceta({
  etiqueta,
  children,
}: {
  etiqueta: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="mr-1 font-sans text-xs tracking-[0.2em] uppercase text-earth-500">
        {etiqueta}
      </span>
      {children}
    </div>
  );
}

function Pill({
  activo,
  onClick,
  children,
}: {
  activo: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={activo}
      className={`border px-3 py-1 font-sans text-sm transition-colors ${
        activo
          ? "border-frequency bg-frequency text-white"
          : "border-earth-300 text-earth-700 hover:border-frequency hover:text-frequency"
      }`}
    >
      {children}
    </button>
  );
}
