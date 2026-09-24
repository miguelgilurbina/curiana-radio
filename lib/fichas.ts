import fs from "fs";
import path from "path";
import type { Capa, Ficha, FichasSeed, FichaIndice, NoSabemosSeed, Retirada } from "@/types/fichas";

// Las fichas de palabra y «Lo que no sabemos», leídas del JSON que generan
// export_fichas_seed.py y export_no_sabemos_seed.py (content/wiki/). Mismo
// criterio que lib/wiki.ts: cachear en producción, releer en desarrollo.
const WIKI_DIR = path.join(process.cwd(), "content", "wiki");
const CACHEAR = process.env.NODE_ENV === "production";

let cacheFichas: FichasSeed | null = null;
let cachePorSlug: Map<string, Ficha> | null = null;
let cacheNoSabemos: NoSabemosSeed | null = null;

const FICHAS_VACIAS: FichasSeed = {
  generado: "",
  fuente_de_verdad: "",
  n: 0,
  por_capa: { atestiguado: 0, reconstruido: 0, retroabstraido: 0, hipotetico: 0 },
  con_cita: 0,
  capas: {} as FichasSeed["capas"],
  siglas_zavala: {},
  pendiente_de_la_corrida_base: [],
  fichas: [],
  retiradas: [],
};

const NO_SABEMOS_VACIO: NoSabemosSeed = { generado: "", n: 0, preguntas: [], faltan: [] };

/** `null` si no existe — semilla sin generar es un estado legítimo. JSON roto
 *  sí rompe el build: es contenido curado. */
function leerJSON<T>(archivo: string): T | null {
  try {
    return JSON.parse(fs.readFileSync(path.join(WIKI_DIR, archivo), "utf-8")) as T;
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw err;
  }
}

export function getFichasSeed(): FichasSeed {
  if (CACHEAR && cacheFichas) return cacheFichas;
  cacheFichas = leerJSON<FichasSeed>("fichas.json") ?? FICHAS_VACIAS;
  cachePorSlug = null;
  return cacheFichas;
}

export function getFichas(): Ficha[] {
  return getFichasSeed().fichas;
}

export function getFicha(slug: string): Ficha | null {
  if (!CACHEAR || !cachePorSlug) {
    cachePorSlug = new Map(getFichas().map((f) => [f.slug, f]));
  }
  return cachePorSlug.get(slug) ?? null;
}

/** Lo que viaja al cliente para el índice: forma, glosa, capa y slug. */
export function getIndiceFichas(): FichaIndice[] {
  return getFichas().map(({ slug, forma, glosa, capa }) => ({ slug, forma, glosa, capa }));
}

export function getRetiradas(): Retirada[] {
  return getFichasSeed().retiradas;
}

/** Anterior y siguiente en el orden del diccionario (el del exportador). */
export function getVecinasFicha(slug: string): { anterior: Ficha | null; siguiente: Ficha | null } {
  const lista = getFichas();
  const i = lista.findIndex((f) => f.slug === slug);
  if (i === -1) return { anterior: null, siguiente: null };
  return { anterior: lista[i - 1] ?? null, siguiente: lista[i + 1] ?? null };
}

/** forma → dónde vive: la ficha si está en el habla, el archivo si se retiró.
 *  Es lo que usa el wiki para enlazar las voces que nombra. */
export function getMapaDeVoces(): Record<string, { href: string; capa: Capa | null; retirada: boolean }> {
  const mapa: Record<string, { href: string; capa: Capa | null; retirada: boolean }> = {};
  for (const r of getRetiradas()) {
    mapa[r.forma] = { href: `/kaketiana/lexicon/retiradas#${r.ancla}`, capa: r.capa, retirada: true };
  }
  for (const f of getFichas()) {
    mapa[f.forma] = { href: `/kaketiana/lexicon/${f.slug}`, capa: f.capa, retirada: false };
  }
  return mapa;
}

/**
 * El wiki nombra las voces caquetías en código (`kasi`, `ebo`). Esto las
 * convierte en enlaces a su ficha —o a su lugar en el archivo, si se
 * retiraron— con un título que el componente `a` del wiki reconoce
 * («voz:capa» / «retirada:capa») para pintarlas con el glifo de su capa.
 * Sólo el código en línea cuyo contenido es EXACTAMENTE una voz: los afijos
 * (`-bana`), las rutas y los nombres de campo quedan como estaban, y los
 * bloques de código no se tocan.
 */
export function enlazarVoces(md: string): string {
  const voces = getMapaDeVoces();
  if (Object.keys(voces).length === 0) return md;
  return md
    .split(/(```[\s\S]*?```)/)
    .map((trozo) =>
      trozo.startsWith("```")
        ? trozo
        : trozo.replace(/(\[?)`([^`\n]+)`(\]\()?/g, (todo, antes: string, forma: string, despues?: string) => {
            // Ya es el texto de un enlace: no se anida otro.
            if (antes || despues) return todo;
            const voz = voces[forma];
            if (!voz) return todo;
            const titulo = `${voz.retirada ? "retirada" : "voz"}:${voz.capa ?? ""}`;
            return `[${forma}](${voz.href} "${titulo}")`;
          })
    )
    .join("");
}

/** obra → las fichas que la citan, para que la bibliografía devuelva el enlace. */
export function getFichasPorObra(): Map<string, Ficha[]> {
  const mapa = new Map<string, Ficha[]>();
  for (const f of getFichas()) {
    for (const c of f.citas) {
      if (!c.obra) continue;
      const lista = mapa.get(c.obra) ?? [];
      lista.push(f);
      mapa.set(c.obra, lista);
    }
  }
  return mapa;
}

export function getNoSabemos(): NoSabemosSeed {
  if (CACHEAR && cacheNoSabemos) return cacheNoSabemos;
  cacheNoSabemos = leerJSON<NoSabemosSeed>("no-sabemos.json") ?? NO_SABEMOS_VACIO;
  return cacheNoSabemos;
}
