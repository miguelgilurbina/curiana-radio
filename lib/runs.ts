import fs from "fs";
import path from "path";

// Índice cross-run: la espina dorsal comparativa que permite contar la
// EVOLUCIÓN entre simulaciones (no un solo run). Lo genera
// curiana_sim/export_runs_index.py desde Supabase local; la página en
// producción solo lee este JSON estático. Ver MIGRACION_RUNS_EVOLUCION.md.
const INDEX_PATH = path.join(process.cwd(), "content", "simulador", "runs", "index.json");

export type RunCategoria = "insignia" | "koine" | "experimento" | "baseline";
/** Lectura de convergencia usada; "acumulada" infla — mostrar con reserva. */
export type LecturaConvergencia = "emergente" | "ventana" | "acumulada";

export interface Convergencia {
  lectura: LecturaConvergencia;
  inicio: number;
  fin: number;
  delta_pct: number | null;
  dias: number;
  /** Serie de la lectura elegida, para sparkline. */
  serie: number[];
}

export interface FormaFijada {
  concepto: string;
  /** Glosa del referente que la comunidad necesitaba nombrar. */
  descripcion: string | null;
  form: string;
  fijada_dia: number | null;
  n_variantes: number | null;
}

export interface Fijacion {
  conceptos_fijados: number;
  formas: FormaFijada[];
}

export interface RunIndexEntry {
  id8: string;
  seed_run_id: string;
  categoria: RunCategoria;
  /** Solo en categoría "experimento": qué brazo del par es. */
  rol: "normal" | "ablacion" | null;
  /** id8 del run apareado (el otro brazo del experimento). */
  pareja: string | null;
  hito: string;
  started_at: string;
  total_dias: number | null;
  total_turnos: number | null;
  agentes: number;
  respuestas: number;
  avg_score: number | null;
  pct_caquetio: number | null;
  neologismos_adoptados: number;
  convergencia: Convergencia | null;
  fijacion: Fijacion | null;
}

export interface RunsIndex {
  version: number;
  generado: string;
  runs: RunIndexEntry[];
}

export function getRunsIndex(): RunsIndex | null {
  try {
    const raw = fs.readFileSync(INDEX_PATH, "utf-8");
    return JSON.parse(raw) as RunsIndex;
  } catch {
    return null;
  }
}

/** Un run del índice por su prefijo id8. */
export function getRunIndexEntry(id8: string): RunIndexEntry | null {
  return getRunsIndex()?.runs.find((r) => r.id8 === id8) ?? null;
}

/** El par de un experimento (normal + ablación) por el id8 de cualquiera. */
export function getParejaExperimento(id8: string): {
  normal: RunIndexEntry;
  ablacion: RunIndexEntry;
} | null {
  const idx = getRunsIndex();
  if (!idx) return null;
  const a = idx.runs.find((r) => r.id8 === id8);
  if (!a?.pareja) return null;
  const b = idx.runs.find((r) => r.id8 === a.pareja);
  if (!b) return null;
  const normal = a.rol === "normal" ? a : b;
  const ablacion = a.rol === "ablacion" ? a : b;
  return { normal, ablacion };
}
