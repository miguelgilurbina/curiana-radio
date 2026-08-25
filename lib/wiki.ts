import fs from "fs";
import path from "path";
import type {
  WikiManifest,
  WikiPagina,
  WikiIndiceEntry,
  SeccionWiki,
  Bibliografia,
  ObraBiblio,
} from "@/types/wiki";

const WIKI_DIR = path.join(process.cwd(), "content", "wiki");

// Mismo criterio que lib/galeria.ts: cachear en producción (el build no debe
// releer los mismos archivos por cada página que los referencia), no cachear
// en desarrollo — el contenido se regenera corriendo export_wiki_seed.py con
// el server vivo, y cachearlo obligaría a reiniciar para ver cada cambio.
const CACHEAR = process.env.NODE_ENV === "production";

let cacheManifest: WikiManifest | null = null;
let cacheBiblio: Bibliografia | null = null;
const cachePaginas = new Map<string, WikiPagina>();

const MANIFEST_VACIO: WikiManifest = { generado: "", n: 0, n_biblio: 0, paginas: [] };
const BIBLIO_VACIA: Bibliografia = { n: 0, obras: [] };

/** Lee un JSON del wiki. `null` si no existe — ausencia = wiki sin generar,
 *  que es un estado legítimo (clon nuevo, rama sin contenido). */
function leerJSON<T>(...segmentos: string[]): T | null {
  try {
    return JSON.parse(fs.readFileSync(path.join(WIKI_DIR, ...segmentos), "utf-8")) as T;
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw err; // JSON roto SÍ debe romper el build: es contenido curado
  }
}

function leerManifest(): WikiManifest {
  if (CACHEAR && cacheManifest) return cacheManifest;
  cacheManifest = leerJSON<WikiManifest>("index.json") ?? MANIFEST_VACIO;
  return cacheManifest;
}

/** Todos los artículos, en orden editorial. */
export function getWikiIndice(): WikiIndiceEntry[] {
  return leerManifest().paginas;
}

export function getWikiPorSeccion(seccion: SeccionWiki): WikiIndiceEntry[] {
  return leerManifest()
    .paginas.filter((p) => p.seccion === seccion)
    .sort((a, b) => a.orden - b.orden);
}

export function getWikiPagina(seccion: SeccionWiki, slug: string): WikiPagina | null {
  const clave = `${seccion}/${slug}`;
  if (CACHEAR && cachePaginas.has(clave)) return cachePaginas.get(clave)!;
  const pagina = leerJSON<WikiPagina>(seccion, `${slug}.json`);
  if (pagina && CACHEAR) cachePaginas.set(clave, pagina);
  return pagina;
}

/** Anterior y siguiente en el orden editorial de la sección. */
export function getVecinos(seccion: SeccionWiki, slug: string): {
  anterior: WikiIndiceEntry | null;
  siguiente: WikiIndiceEntry | null;
} {
  const lista = getWikiPorSeccion(seccion);
  const i = lista.findIndex((p) => p.slug === slug);
  if (i === -1) return { anterior: null, siguiente: null };
  return { anterior: lista[i - 1] ?? null, siguiente: lista[i + 1] ?? null };
}

/** Params de todas las combinaciones sección/slug, para generateStaticParams. */
export function getWikiParams(seccion?: SeccionWiki): { seccion: SeccionWiki; slug: string }[] {
  const paginas = seccion ? getWikiPorSeccion(seccion) : getWikiIndice();
  return paginas.map((p) => ({ seccion: p.seccion, slug: p.slug }));
}

export function getBibliografia(): ObraBiblio[] {
  if (!CACHEAR || !cacheBiblio) {
    cacheBiblio = leerJSON<Bibliografia>("bibliografia.json") ?? BIBLIO_VACIA;
  }
  return cacheBiblio.obras;
}

/** Cifras medidas para la portada. Ninguna se escribe a mano (regla 1). */
export function getCifrasWiki(): { articulos: number; obras: number; conLectura: number } {
  const obras = getBibliografia();
  return {
    articulos: leerManifest().n,
    obras: obras.length,
    conLectura: obras.filter((o) => o.lectura_url).length,
  };
}
