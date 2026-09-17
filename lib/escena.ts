import fs from "fs";
import path from "path";

// LA ESCENA — dónde estaba cada uno, turno a turno, sobre el mapa real.
//
// Lo genera `curiana_sim/export_escena_seed.py` desde Supabase LOCAL leyendo la
// tabla `presencias` (los 63 agentes en un lugar cada momento del día, no sólo
// los 12 que hablan) y `agent_responses` (qué dijo cada uno, y dónde). La página
// en producción sólo lee este JSON estático: cero egress, como el resto de
// `content/simulador/`.
//
// Diseño y decisión: 6-fusion/issues-pendientes/
// existir-en-el-mundo-escena-por-lugar-2026-09-17.md §5b y la decisión 10 de
// Miguel del 2026-09-17 («el visor de repetición sobre el mapa real»).
const ESCENA_DIR = path.join(process.cwd(), "content", "simulador", "escena");

/** El nodo al que pertenece un lugar: el de quien lo trabaja. `compartido` si
 *  lo tocan los dos — no hay ninguna frontera declarada en ninguna parte. */
export type NodoEscena = "GUARANAO" | "AMUAY" | "compartido";

/** Cómo se sitúa un lugar en el mapa. `heredado` = se dibuja sobre su aldea
 *  porque el canon no le da punto propio; `sin-coordenada` = la escena lo usó y
 *  la tabla derivada no lo conoce (sale en los avisos). */
export type TipoLugar = "propio" | "heredado" | "zona" | "camino" | "sin-coordenada";

export interface LugarEscena {
  id: string;
  nombre: string;
  sitio: string;
  locacion: string | null;
  nodo: NodoEscena | null;
  tipo: TipoLugar;
  lat: number | null;
  lon: number | null;
  /** Zona: los puntos del área. Camino: los dos extremos, si el canon nombra el par. */
  puntos: [number, number][] | null;
  /** Declarado compartido entre nodos (el Capubana; el camino Moruy–Caseto). */
  compartido: boolean;
  /** Qué lo declara compartido. */
  por_que: string | null;
}

export interface DichoEscena {
  agente: string;
  nodo: NodoEscena | null;
  /** Recortado al `tope_texto` del seed: el texto entero vive en la base. */
  texto: string;
  recortado: boolean;
}

export interface PresenteEscena {
  agente: string;
  nodo: NodoEscena | null;
  hablo: boolean;
}

export interface EscenaDeLugar {
  lugar: string;
  /** Cuánta gente hay aquí ahora — el tamaño del punto en el mapa. */
  n: number;
  por_nodo: Record<string, number>;
  /** Los DOS nodos aquí, a la vez. */
  contacto: boolean;
  presentes: PresenteEscena[];
  dichos: DichoEscena[];
}

export interface TurnoEscena {
  i: number;
  run: string;
  dia: number | null;
  turno: number | null;
  momento: string;
  n_presencias: number;
  escenas: EscenaDeLugar[];
}

export interface EscenaSeed {
  version: number;
  generado: string;
  /** Ni una fila en `presencias`: el mapa se dibuja, no hay nadie encima. */
  vacio: boolean;
  tope_texto: number;
  run: {
    id8: string | null;
    run_id: string | null;
    /** id8 de la cadena, raíz→hoja. */
    cadena: string[];
    started_at: string | null;
    dias: number[];
    n_turnos: number;
    n_agentes: number;
    n_presencias: number;
  };
  lugares: LugarEscena[];
  turnos: TurnoEscena[];
  /** Lo que no cuadra, dicho y no tapado (el visor es también un guardián). */
  avisos: string[];
}

/** Todos los seeds de escena exportados, del más reciente al más viejo. */
export function getEscenas(): EscenaSeed[] {
  let archivos: string[];
  try {
    archivos = fs.readdirSync(ESCENA_DIR).filter((f) => f.endsWith(".json"));
  } catch {
    return [];
  }
  const seeds: EscenaSeed[] = [];
  for (const archivo of archivos) {
    try {
      seeds.push(JSON.parse(fs.readFileSync(path.join(ESCENA_DIR, archivo), "utf-8")));
    } catch {
      // Un JSON roto no debe tumbar el build del sitio entero.
    }
  }
  return seeds.sort((a, b) => (a.generado < b.generado ? 1 : -1));
}

/**
 * El seed a mostrar. Con `id8`, ese run; sin él, el más reciente que TENGA
 * escena — y sólo si no hay ninguno, el seed vacío (el catálogo de lugares sin
 * nadie encima, que es el estado mientras ningún run haya corrido con escena).
 */
export function getEscena(id8?: string): EscenaSeed | null {
  const seeds = getEscenas();
  if (id8) return seeds.find((s) => s.run.id8 === id8) ?? null;
  return seeds.find((s) => !s.vacio) ?? seeds[0] ?? null;
}
