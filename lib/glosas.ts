import fs from "fs";
import path from "path";
import { getAllManaureFragments } from "@/lib/manaure";
import { getNeologismos } from "@/lib/neologismos";

// Las glosas del cronista: el cruce entre la lengua ATESTIGUADA (crónicas
// reales, ver curiana_lexicon.py::notas) y la narrativa que la simulación
// produjo. Curaduría a mano, deliberadamente pequeña — cada glosa cita una
// palabra real con su fuente y señala, sin inventar etimología donde no la
// hay, un eco verificable en los datos del run (una raíz reusada, una forma
// heredada). Ver content/simulador/glosas.json.
const GLOSAS_PATH = path.join(process.cwd(), "content", "simulador", "glosas.json");

export interface AnclaGlosa {
  /** El fragmento de Manaure junto al que aparece (content/simulador/manaure/) */
  manaure?: string;
  /** La forma del neologismo junto al que aparece (neologismos.json) */
  evento_forma?: string;
}

export interface Glosa {
  id: string;
  palabra_real: string;
  significado_real: string;
  /** Autor(es) y año de la fuente académica/crónica que atestigua la palabra. */
  cita: string;
  ancla: AnclaGlosa;
  nota: string;
}

function fail(msg: string): never {
  throw new Error(`glosas.json: ${msg}`);
}

function validate(glosas: Glosa[]): void {
  const manaureIds = new Set(getAllManaureFragments().map((f) => f.id));
  const neologismoFormas = new Set(getNeologismos().map((n) => n.form));

  for (const g of glosas) {
    if (!g.ancla.manaure && !g.ancla.evento_forma) {
      fail(`glosa "${g.id}" no tiene ancla (ni manaure ni evento_forma)`);
    }
    if (g.ancla.manaure && !manaureIds.has(g.ancla.manaure)) {
      fail(`glosa "${g.id}" referencia el fragmento de Manaure "${g.ancla.manaure}", que no existe`);
    }
    if (g.ancla.evento_forma && !neologismoFormas.has(g.ancla.evento_forma)) {
      fail(`glosa "${g.id}" referencia el neologismo "${g.ancla.evento_forma}", que no existe`);
    }
  }
}

export function getGlosas(): Glosa[] {
  let raw: string;
  try {
    raw = fs.readFileSync(GLOSAS_PATH, "utf-8");
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw err;
  }
  const glosas = (JSON.parse(raw).glosas as Glosa[]) ?? [];
  validate(glosas);
  return glosas;
}

/** Las glosas ancladas a un fragmento de Manaure específico. */
export function getGlosasPorManaure(fragmentoId: string): Glosa[] {
  return getGlosas().filter((g) => g.ancla.manaure === fragmentoId);
}

/** Las glosas ancladas a la forma de un neologismo específico. */
export function getGlosasPorEvento(forma: string): Glosa[] {
  return getGlosas().filter((g) => g.ancla.evento_forma === forma);
}
