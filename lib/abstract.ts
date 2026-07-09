import fs from "fs";
import path from "path";
import { getLexicon } from "@/lib/lexicon";
import { getNeologismos, type Neologismo } from "@/lib/neologismos";
import { getRunsIndex } from "@/lib/runs";

// El abstract de disertación del Acto I: pitch, resumen formal, los conceptos
// del experimento explicados en teoría plana, y el pipeline. El copy vive en
// content/simulador/abstract.json; las CIFRAS se derivan aquí en build desde
// los seeds reales (lexicon.json, runs/index.json) — nunca copiadas a mano,
// para que el texto no mienta cuando entren runs nuevos.
const ABSTRACT_PATH = path.join(process.cwd(), "content", "simulador", "abstract.json");

export interface ConceptoAbstract {
  id: string;
  termino: string;
  /** Definición de una línea, en itálica bajo el término. */
  lema: string;
  cuerpo: string;
  /** El dato del proyecto que aterriza el concepto (opcional). */
  dato?: string;
}

export interface PasoPipeline {
  titulo: string;
  sub: string;
}

export interface AbstractContent {
  version: number;
  pitch: { overline: string; titulo: string; bajada: string };
  abstract: string[];
  conceptos: ConceptoAbstract[];
  pipeline: PasoPipeline[];
  /** Forma de neologismos.json que protagoniza "Vida de una palabra". */
  ejemplo_form: string;
  cierre: string;
  nota_honestidad: string;
}

function fail(msg: string): never {
  throw new Error(`abstract.json: ${msg}`);
}

export function getAbstract(): AbstractContent {
  const raw = fs.readFileSync(ABSTRACT_PATH, "utf-8");
  const content = JSON.parse(raw) as AbstractContent;

  if (!content.pitch?.titulo) fail("pitch.titulo es obligatorio");
  if (!content.abstract?.length) fail("abstract[] no puede estar vacío");
  if (!content.conceptos?.length) fail("conceptos[] no puede estar vacío");
  for (const c of content.conceptos) {
    if (!c.id || !c.termino || !c.lema || !c.cuerpo) {
      fail(`concepto incompleto: ${JSON.stringify(c.id ?? c.termino)}`);
    }
  }
  if (content.pipeline?.length !== 4) fail("pipeline[] debe tener 4 pasos");
  return content;
}

/** El neologismo protagonista de "Vida de una palabra" (validado en build). */
export function getEjemploVida(): Neologismo {
  const form = getAbstract().ejemplo_form;
  const neo = getNeologismos().find((n) => n.form === form);
  if (!neo) fail(`ejemplo_form "${form}" no existe en neologismos.json`);
  return neo;
}

// ── Cifras derivadas (la placa de métricas del laboratorio) ────────────
export interface CifrasLab {
  palabrasLexicon: number;
  atestiguadas: number;
  runsCurados: number;
  respuestasTotales: number;
  agentesRango: string;
  conceptosFijados: number;
  /** "2,7" — convergencia emergente normal / ablación del experimento. */
  factorExperimento: string | null;
  pctCaquetioMax: number | null;
}

export function getCifrasLab(): CifrasLab {
  const lexicon = getLexicon();
  const idx = getRunsIndex();
  const runs = idx?.runs ?? [];

  const agentes = runs.map((r) => r.agentes).filter((n) => n > 0);
  const agentesRango = agentes.length
    ? `${Math.min(...agentes)}–${Math.max(...agentes)}`
    : "—";

  const normal = runs.find((r) => r.rol === "normal");
  const ablacion = runs.find((r) => r.rol === "ablacion");
  let factorExperimento: string | null = null;
  if (normal?.convergencia?.delta_pct != null && ablacion?.convergencia?.delta_pct) {
    const factor = normal.convergencia.delta_pct / ablacion.convergencia.delta_pct;
    if (Number.isFinite(factor) && factor > 0) {
      factorExperimento = factor.toFixed(1).replace(".", ",");
    }
  }

  const pcts = runs.map((r) => r.pct_caquetio).filter((p): p is number => p != null);

  return {
    palabrasLexicon: lexicon.length,
    atestiguadas: lexicon.filter((p) => p.attested).length,
    runsCurados: runs.length,
    respuestasTotales: runs.reduce((acc, r) => acc + (r.respuestas ?? 0), 0),
    agentesRango,
    conceptosFijados: runs.reduce((acc, r) => acc + (r.fijacion?.conceptos_fijados ?? 0), 0),
    factorExperimento,
    pctCaquetioMax: pcts.length ? Math.max(...pcts) : null,
  };
}
