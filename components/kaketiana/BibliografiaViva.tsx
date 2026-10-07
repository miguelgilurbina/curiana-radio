"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, useSyncExternalStore } from "react";
import FormaCaquetia from "@/components/kaketiana/Forma";
import Desplegable from "@/components/kaketiana/Desplegable";

// La bibliografía del manual de Kaketiana (Vistas §04): el filtro por
// disciplina en la fila de controles de 44px, y cada obra como una entrada
// —el año en mono y en rúbrica, autor y título, «#ancla · disciplina», lo que
// aporta, y [ LEER → ] si se puede leer en línea—.
//
// El Ancla: la obra a la que se llega desde una cita
// (`/kaketiana/bibliografia#alvarado-1921`) queda resaltada y respira una vez
// (.kk-obra[data-ancla] en globals.css). El ancla es el id del <li>, el slug
// que generan los enlaces de export_wiki_seed.py: no se cambia sin romperlos.
// El hash se lee con useSyncExternalStore, como el filtro del diccionario: sin
// efectos que pongan estado.

export interface EntradaBiblio {
  slug: string;
  anio: string | null;
  autor: string;
  obra: string;
  genero: string | null;
  grupo: string;
  publicacion: string | null;
  aporta: string | null;
  acceso: string | null;
  lectura_url: string | null;
  voces: { slug: string; forma: string; capa: string }[];
}

export interface GrupoConCuenta {
  clave: string;
  label: string;
  n: number;
}

// Cuántas voces del diccionario se enlazan por obra antes del «y N más».
const VOCES_VISIBLES = 12;

// «Dónde está» corto va a la vista; el largo —en algunas obras es la nota de
// trabajo del vault, con pesos de archivo y derechos— queda a un clic.
const ACCESO_CORTO = 160;

function suscribir(cb: () => void) {
  window.addEventListener("hashchange", cb);
  return () => window.removeEventListener("hashchange", cb);
}

function anclaDeLaUrl(): string | null {
  try {
    return decodeURIComponent(window.location.hash.slice(1)) || null;
  } catch {
    return null;
  }
}

const CHIP =
  "sim-mono inline-flex min-h-11 cursor-pointer items-center rounded-[2px] border px-3.5 text-[0.62rem] uppercase tracking-[0.14em] transition-colors";
const CHIP_ACTIVO = "border-(--sim-ink) bg-(--sim-ink) text-(--sim-paper)";
const CHIP_INACTIVO = "border-(--sim-rule) text-(--sim-ink-soft) hover:border-(--sim-rubrica)";

function Voces({ voces }: { voces: EntradaBiblio["voces"] }) {
  const visibles = voces.slice(0, VOCES_VISIBLES);
  const resto = voces.length - visibles.length;
  return (
    <p className="mt-1 font-sans text-[0.8rem] leading-relaxed text-(--sim-ink-soft)">
      <span className="kk-label mr-1.5 text-[0.56rem] tracking-[0.16em]">
        {voces.length === 1 ? "Sostiene una voz" : `Sostiene ${voces.length} voces`}
      </span>
      {visibles.map((v, i) => (
        <span key={v.slug}>
          {i > 0 && <span aria-hidden="true"> · </span>}
          <Link href={`/kaketiana/lexicon/${v.slug}`} className="underline decoration-transparent underline-offset-2 hover:decoration-(--sim-fuego)">
            <FormaCaquetia forma={v.forma} capa={v.capa} />
          </Link>
        </span>
      ))}
      {resto > 0 && <span> y {resto} más</span>}
    </p>
  );
}

function Entrada({ o, anclada }: { o: EntradaBiblio; anclada: boolean }) {
  return (
    <li
      id={o.slug}
      data-ancla={anclada ? "" : undefined}
      className="kk-obra relative grid scroll-mt-24 grid-cols-[3.5rem_minmax(0,1fr)] gap-x-4 gap-y-3 border-b border-(--sim-rule) px-2 py-5 sm:grid-cols-[4rem_minmax(0,1fr)_auto] sm:gap-x-5"
    >
      <span className="sim-mono pt-0.5 text-[0.82rem] font-medium text-(--sim-rubrica)">{o.anio ?? "s. f."}</span>
      <div className="flex min-w-0 flex-col gap-1">
        <p className="font-serif text-[1.02rem] leading-snug text-(--sim-ink)">
          {o.autor} — <em>{o.obra}</em>
        </p>
        <p className="sim-mono text-[0.66rem] text-(--sim-ink-soft)">
          #{o.slug}
          {o.genero && <> · {o.genero}</>}
        </p>
        {o.publicacion && (
          <p className="font-sans text-[0.75rem] leading-snug text-(--sim-ink-soft)">{o.publicacion}</p>
        )}
        {o.aporta && (
          <p className="mt-1 max-w-reading font-sans text-[0.85rem] leading-relaxed text-(--sim-ink-soft)">{o.aporta}</p>
        )}
        {!o.lectura_url &&
          o.acceso &&
          (o.acceso.length <= ACCESO_CORTO ? (
            <p className="max-w-reading font-sans text-[0.75rem] leading-relaxed text-(--sim-ink-soft)">
              <span className="kk-label mr-1.5 text-[0.56rem] tracking-[0.16em]">Dónde está</span>
              {o.acceso}
            </p>
          ) : (
            <Desplegable abrir="[ DÓNDE ESTÁ ↓ ]" className="mt-1">
              <p className="max-w-reading font-sans text-[0.75rem] leading-relaxed text-(--sim-ink-soft)">{o.acceso}</p>
            </Desplegable>
          ))}
        {o.voces.length > 0 && <Voces voces={o.voces} />}
      </div>
      {o.lectura_url && (
        <a
          href={o.lectura_url}
          target="_blank"
          rel="noopener noreferrer"
          className="kk-accion col-start-2 self-start text-[0.64rem] sm:col-start-auto sm:self-center"
        >
          [ LEER → ]
        </a>
      )}
    </li>
  );
}

export default function BibliografiaViva({ obras, grupos }: { obras: EntradaBiblio[]; grupos: GrupoConCuenta[] }) {
  const ancla = useSyncExternalStore(suscribir, anclaDeLaUrl, () => null);
  const [grupo, setGrupo] = useState<string | null>(null);

  // Llegar a la obra: el sitio usa scroll-behavior: smooth y la hidratación
  // cortaba el desplazamiento del navegador a mitad de camino (quedaba arriba,
  // con la obra a 10.000 px). Se la trae a la vista al llegar, sin animación.
  useEffect(() => {
    if (ancla) document.getElementById(ancla)?.scrollIntoView({ block: "start", behavior: "instant" });
  }, [ancla]);

  // La obra anclada se ve aunque el filtro sea otro: se llegó a ella a propósito.
  const visibles = useMemo(
    () => (grupo ? obras.filter((o) => o.grupo === grupo || o.slug === ancla) : obras),
    [obras, grupo, ancla]
  );

  return (
    <div>
      <ul className="flex flex-wrap gap-2" aria-label="Filtrar por disciplina">
        <li>
          <button
            type="button"
            onClick={() => setGrupo(null)}
            aria-pressed={grupo === null}
            className={`${CHIP} ${grupo === null ? CHIP_ACTIVO : CHIP_INACTIVO}`}
          >
            Todas · {obras.length}
          </button>
        </li>
        {grupos.map((g) => (
          <li key={g.clave}>
            <button
              type="button"
              onClick={() => setGrupo(grupo === g.clave ? null : g.clave)}
              aria-pressed={grupo === g.clave}
              className={`${CHIP} ${grupo === g.clave ? CHIP_ACTIVO : CHIP_INACTIVO}`}
            >
              {g.label} · {g.n}
            </button>
          </li>
        ))}
      </ul>

      <p className="mt-4 sim-mono text-[0.66rem] text-(--sim-ink-soft)" aria-live="polite">
        {visibles.length === obras.length ? `${obras.length} obras` : `${visibles.length} de ${obras.length} obras`}
      </p>

      {/* wrap-anywhere: las notas de acceso traen URL y sha256 sin espacios,
          que en el móvil empujaban la página a lo ancho */}
      <ul className="mt-2 border-t border-(--sim-rule) wrap-anywhere">
        {visibles.map((o) => (
          <Entrada key={o.slug} o={o} anclada={o.slug === ancla} />
        ))}
      </ul>
    </div>
  );
}
