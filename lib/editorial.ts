import fs from "fs";
import path from "path";
import { getAllManaureFragments } from "@/lib/manaure";
import { getAllPersonajes } from "@/lib/personajes";
import { getNeologismos } from "@/lib/neologismos";

// Capa editorial del simulador — el "guion" que decide qué cuenta cada run:
// épocas, eventos significativos y qué fragmento de Manaure acompaña cada
// sección. Multi-run desde el inicio: hoy hay un run publicado, pero cada
// corrida futura es una edición nueva con su propia historia.
//
// La validación corre en build (server components): una referencia rota en
// editorial.json — fragmento inexistente, slug desconocido, día fuera de
// rango — rompe el build con mensaje claro. Misma filosofía que lib/lexicon.ts:
// no disfrazar datos rotos de "sin datos".
const EDITORIAL_PATH = path.join(process.cwd(), "content", "simulador", "editorial.json");

export type RunEstado = "publicado" | "borrador" | "archivado";

export const EVENTO_TIPOS_IDS = [
  "neologismo_adoptado",
  "neologismo_propuesto",
  "hito_deriva",
  "momento",
] as const;
export type EventoTipo = (typeof EVENTO_TIPOS_IDS)[number];

export interface EventoEditorial {
  dia: number;
  tipo: EventoTipo;
  /** Forma del neologismo — obligatoria en eventos neologismo_* */
  forma?: string;
  /** Slug del personaje protagonista (content/simulador/personajes.json) */
  personaje?: string;
  nota?: string;
}

export interface EpocaEditorial {
  id: string;
  titulo: string;
  dias: [number, number];
  hito?: string;
  resumen: string;
  /** Fragmento de Manaure embebido en la época (opcional) */
  manaure?: string;
  eventos: EventoEditorial[];
}

export interface RunEditorial {
  id: string;
  /** run_id del seed exportado por curiana_sim (para trazabilidad) */
  seed_run_id?: string;
  titulo: string;
  subtitulo?: string;
  fecha: string;
  estado: RunEstado;
  dias: number;
  manaure_hero?: string;
  manaure_cierre?: string;
  deriva?: { manaure?: string; nota?: string };
  epocas: EpocaEditorial[];
}

export interface Editorial {
  version: number;
  run_activo: string;
  runs: RunEditorial[];
}

function fail(msg: string): never {
  throw new Error(`editorial.json: ${msg}`);
}

function validate(editorial: Editorial): void {
  const manaureIds = new Set(getAllManaureFragments().map((f) => f.id));
  const personajeSlugs = new Set(getAllPersonajes().map((p) => p.slug));
  const neologismoFormas = new Set(getNeologismos().map((n) => n.form));

  const checkManaure = (id: string | undefined, donde: string) => {
    if (id != null && !manaureIds.has(id)) {
      fail(`${donde} referencia el fragmento de Manaure "${id}", que no existe en content/simulador/manaure/`);
    }
  };

  if (!editorial.runs.some((r) => r.id === editorial.run_activo)) {
    fail(`run_activo "${editorial.run_activo}" no está en runs[]`);
  }

  const ids = new Set<string>();
  for (const run of editorial.runs) {
    if (ids.has(run.id)) fail(`run id duplicado: "${run.id}"`);
    ids.add(run.id);

    checkManaure(run.manaure_hero, `runs.${run.id}.manaure_hero`);
    checkManaure(run.manaure_cierre, `runs.${run.id}.manaure_cierre`);
    checkManaure(run.deriva?.manaure, `runs.${run.id}.deriva.manaure`);

    for (const epoca of run.epocas) {
      const donde = `runs.${run.id}.epocas.${epoca.id}`;
      const [desde, hasta] = epoca.dias;
      if (desde < 1 || hasta > run.dias || desde > hasta) {
        fail(`${donde}.dias [${desde}, ${hasta}] fuera del rango del run (1–${run.dias})`);
      }
      checkManaure(epoca.manaure, `${donde}.manaure`);

      for (const ev of epoca.eventos) {
        if (!EVENTO_TIPOS_IDS.includes(ev.tipo)) {
          fail(`${donde}: tipo de evento desconocido "${ev.tipo}"`);
        }
        if (ev.dia < desde || ev.dia > hasta) {
          fail(`${donde}: evento del día ${ev.dia} fuera del rango de la época [${desde}, ${hasta}]`);
        }
        if (ev.tipo.startsWith("neologismo")) {
          if (!ev.forma) fail(`${donde}: evento ${ev.tipo} del día ${ev.dia} sin "forma"`);
          // Solo validamos contra el seed en el run que lo generó — los seeds
          // actuales son del run activo; runs futuros traerán los suyos.
          if (run.id === editorial.run_activo && !neologismoFormas.has(ev.forma)) {
            fail(`${donde}: la forma "${ev.forma}" no existe en neologismos.json`);
          }
        }
        if (ev.personaje && run.id === editorial.run_activo && !personajeSlugs.has(ev.personaje)) {
          fail(`${donde}: el personaje "${ev.personaje}" no existe en personajes.json`);
        }
      }
    }
  }
}

export function getEditorial(): Editorial {
  const raw = fs.readFileSync(EDITORIAL_PATH, "utf-8");
  const editorial = JSON.parse(raw) as Editorial;
  validate(editorial);
  return editorial;
}

export function getRunsPublicados(): RunEditorial[] {
  return getEditorial().runs.filter((r) => r.estado === "publicado");
}

export function getRunActivo(): RunEditorial {
  const editorial = getEditorial();
  const run = editorial.runs.find((r) => r.id === editorial.run_activo);
  // validate() ya garantiza que existe
  return run!;
}
