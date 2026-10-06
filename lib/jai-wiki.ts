import fs from "fs";
import path from "path";
import type {
  AlbumWiki,
  ArtistaWiki,
  CancionWiki,
  DatosEstacion,
  EstacionWiki,
  FilaPista,
} from "@/types/jai-wiki";

/**
 * El wiki de JAI Sounds se lee de content/jai-sounds/wiki/, que deja
 * `npm run jai:exportar`. La base (curiana-produccion) es la fuente pero no
 * se consulta en vivo: es plan gratis y se pausa sola. Así las páginas se
 * arman de un archivo y el sitio no depende de que la base esté despierta.
 */
const DIR = path.join(process.cwd(), "content", "jai-sounds", "wiki");

export const N_ESTACIONES = 23;

type Wiki = {
  estaciones: EstacionWiki[];
  canciones: Record<string, CancionWiki>;
  albumes: Record<string, AlbumWiki>;
  artistas: Record<string, ArtistaWiki>;
};

let memo: Wiki | null = null;

function leer<T>(archivo: string, vacio: T): T {
  try {
    return JSON.parse(fs.readFileSync(path.join(DIR, archivo), "utf-8")) as T;
  } catch (err) {
    // Sin export todavía (clon nuevo): el wiki existe vacío, no rompe.
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return vacio;
    throw err;
  }
}

export function wiki(): Wiki {
  memo ??= {
    estaciones: leer<EstacionWiki[]>("estaciones.json", []),
    canciones: leer<Record<string, CancionWiki>>("canciones.json", {}),
    albumes: leer<Record<string, AlbumWiki>>("albumes.json", {}),
    artistas: leer<Record<string, ArtistaWiki>>("artistas.json", {}),
  };
  return memo;
}

// ── Formatos ─────────────────────────────────────────────────────────

export function duracion(ms: number | null | undefined): string {
  if (!ms) return "—";
  const s = Math.round(ms / 1000);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

export function horas(ms: number): string {
  const m = Math.round(ms / 60000);
  return m >= 60 ? `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")}` : `${m} min`;
}

export const anio = (f: string | null | undefined) => (f ? f.slice(0, 4) : null);

const TAMANOS = { 64: "ab67616d00004851", 300: "ab67616d00001e02", 640: "ab67616d0000b273" } as const;

/** La portada de álbum de Spotify al tamaño pedido (la misma imagen, otro prefijo). */
export function portada(url: string | null, tam: 64 | 300 | 640): string | null {
  if (!url) return null;
  for (const p of Object.values(TAMANOS)) if (url.includes(p)) return url.replace(p, TAMANOS[tam]);
  return url;
}

export const num = (i: number) => String(i + 1).padStart(2, "0");

// ── Consultas ────────────────────────────────────────────────────────

export const estaciones = () => wiki().estaciones;
export const cancion = (slug: string) => wiki().canciones[slug] ?? null;
export const album = (slug: string) => wiki().albumes[slug] ?? null;
export const artista = (slug: string) => wiki().artistas[slug] ?? null;
export const nombreArtista = (slug: string) => wiki().artistas[slug]?.n ?? slug;

/** La canción que suena antes y después en una estación. */
export function vecinas(e: number, pos: number) {
  const p = wiki().estaciones[e]?.pistas ?? [];
  return { antes: p[pos - 2] ?? null, despues: p[pos] ?? null };
}

/** El tracklist de una estación, listo para la batea. */
export function datosEstacion(i: number): DatosEstacion | null {
  const w = wiki();
  const e = w.estaciones[i];
  if (!e) return null;
  const filas: FilaPista[] = e.pistas.map((s) => {
    const c = w.canciones[s];
    const al = c.al ? w.albumes[c.al] : null;
    const enEsta = c.dial.find((d) => d[0] === i);
    return {
      s,
      t: c.t,
      a: c.a.map((x) => ({ s: x, n: nombreArtista(x) })),
      al: al && c.al ? { s: c.al, n: al.t } : null,
      y: (c.mb?.via === "isrc" ? anio(c.mb.f) : null) ?? anio(c.fecha),
      ys: c.fecha,
      // Solo la fecha de la misma grabación: una coincidencia por título
      // puede ser otra edición.
      f: c.mb?.via === "isrc" ? c.mb.f : null,
      d: duracion(c.ms),
      img: c.img,
      desde: enEsta?.[2] ?? null,
      tambien: c.dial.map((d) => d[0]).filter((x) => x !== i),
      r: c.resena?.cuerpo ?? null,
      spotify: c.spotify,
    };
  });
  return { i, filas };
}

/** Lo que el wiki muestra de una estación sin cargar su tracklist. */
export function resumenEstaciones() {
  return wiki().estaciones.map((e) => ({
    i: e.i,
    slug: e.slug,
    nombre: e.nombre,
    portada: e.portada,
    spotify_id: e.spotify_id,
    censo: {
      ...e.censo,
      presentes: e.censo.presentes.map(([s, n]) => ({ s, n: nombreArtista(s), veces: n })),
    },
  }));
}

export type ResumenEstacion = ReturnType<typeof resumenEstaciones>[number];

/** Estaciones donde suena un artista, de más a menos. */
export function estacionesDeArtista(slug: string): number[] {
  const w = wiki();
  const cuenta = new Map<number, number>();
  for (const c of w.artistas[slug]?.canciones ?? []) {
    for (const [e] of w.canciones[c]?.dial ?? []) cuenta.set(e, (cuenta.get(e) ?? 0) + 1);
  }
  return [...cuenta].sort((a, b) => b[1] - a[1] || a[0] - b[0]).map(([e]) => e);
}

/** La estación que le da color a una página del wiki (o null: sin color). */
export function estacionDeColor(tipo: "cancion" | "album" | "artista", slug: string): number | null {
  const w = wiki();
  if (tipo === "cancion") return w.canciones[slug]?.dial[0]?.[0] ?? null;
  if (tipo === "album") {
    const c = w.albumes[slug]?.canciones[0];
    return c ? (w.canciones[c]?.dial[0]?.[0] ?? null) : null;
  }
  const propias = estacionesDeArtista(slug);
  if (propias.length) return propias[0];
  return w.estaciones.find((e) => e.censo.presentes.some(([s]) => s === slug))?.i ?? null;
}

export const cuentas = () => {
  const w = wiki();
  return {
    canciones: Object.keys(w.canciones).length,
    albumes: Object.keys(w.albumes).length,
    artistas: Object.keys(w.artistas).length,
  };
};
