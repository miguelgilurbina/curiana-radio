import fs from "fs";
import path from "path";

// Seed curado de personajes para la sección evergreen /simulador/personajes.
// Generado por curiana_sim/export_personajes_seed.py desde Supabase (perfiles +
// citas curadas por el Observer) y curiana_agents.py (biografía estática).
// No es una conexión en vivo: re-correr el script actualiza este JSON.
const SEED_PATH = path.join(process.cwd(), "content", "simulador", "personajes.json");

export interface PersonajeQuote {
  quote: string;
  traduccion: string;
  justificacion: string;
  impacto_score: number | null;
  day: number | null;
  turn_num: number | null;
}

export interface Personaje {
  slug: string;
  nombre: string;
  tier: number | null;
  genero: string | null;
  edad: number | null;
  etnia: string;
  ubicacion_default: string | null;
  descripcion: string;
  rol_comunidad: string;
  resumen_arco: string;
  total_respuestas: number;
  avg_score: number | null;
  neologismos_propuestos: number;
  neologismos_adoptados: number;
  quotes: PersonajeQuote[];
}

export interface PersonajesSeed {
  run_id: string;
  run_started_at: string | null;
  total_days: number | null;
  total_turns: number | null;
  personajes: Personaje[];
}

export function getPersonajesSeed(): PersonajesSeed {
  try {
    const raw = fs.readFileSync(SEED_PATH, "utf-8");
    return JSON.parse(raw) as PersonajesSeed;
  } catch {
    return { run_id: "", run_started_at: null, total_days: null, total_turns: null, personajes: [] };
  }
}

export function getAllPersonajes(): Personaje[] {
  return getPersonajesSeed().personajes;
}

export function getPersonajeBySlug(slug: string): Personaje | null {
  return getAllPersonajes().find((p) => p.slug === slug) ?? null;
}
