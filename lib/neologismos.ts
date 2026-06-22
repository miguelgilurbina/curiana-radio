import fs from "fs";
import path from "path";

const SEED_PATH = path.join(process.cwd(), "content", "simulador", "neologismos.json");

export interface NeologismoDestacado {
  quote: string;
  traduccion: string;
  impacto_score: number;
  agente: string;
  agente_slug: string;
}

export interface Neologismo {
  id: string;
  form: string;
  components: string;
  meaning: string;
  morphological_rule: string;
  proposed_by: string;
  proposed_day: number;
  status: "propuesto" | "adoptado" | "rechazado" | "ignorado";
  adopted_by: string[] | null;
  destacado: NeologismoDestacado | null;
}

export function getNeologismos(): Neologismo[] {
  try {
    const raw = fs.readFileSync(SEED_PATH, "utf-8");
    return (JSON.parse(raw).neologismos as Neologismo[]) ?? [];
  } catch {
    return [];
  }
}
