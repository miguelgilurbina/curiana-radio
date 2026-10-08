/**
 * Simulador — la forma de las tablas de Supabase donde el experimento de
 * Kaketiana registra cada run.
 *
 * El sitio ya no le habla a Supabase: es 100 % estático y lee los JSON que el
 * exportador deja en content/simulador/ (lib/resumen.ts, lib/runs.ts…). Estos
 * tipos describen esas filas tal como salen de la base. Vivían en
 * lib/supabase.ts junto a un cliente que ninguna página usaba; el cliente se
 * borró en la segunda revisión de seguridad (2026-10-08).
 */

export interface SimulationRun {
  id: string;
  started_at: string;
  ended_at: string | null;
  total_turns: number;
  total_days: number;
  model: string;
  langsmith_project: string | null;
  config: Record<string, unknown>;
}

export interface Turn {
  id: string;
  run_id: string;
  day: number;
  turn_num: number;
  moment: string;
  season: string;
  event_description: string | null;
  created_at: string;
}

export interface AgentResponse {
  id: string;
  turn_id: string;
  run_id: string;
  agent_name: string;
  ethnicity: string;
  tier: number;
  response_text: string;
  score: number;
  pct_caquetio: number;
  pct_wayunaiki: number;
  pct_lokono: number;
  pct_taino: number;
  pct_proto_arahuaco: number;
  aspects_used: string[];
  words_used: string[];
  neologisms_proposed: number;
  langsmith_trace_url: string | null;
  created_at: string;
}

export interface Neologism {
  id: string;
  run_id: string;
  form: string;
  components: string;
  meaning: string;
  morphological_rule: string;
  proposed_by: string;
  proposed_day: number;
  status: "propuesto" | "adoptado" | "rechazado" | "ignorado";
  adopted_by: string[];
  created_at: string;
}

export interface LexiconEntry {
  id: string;
  word: string;
  meaning: string;
  category: string;
  source_language: string;
  attested: boolean;
  source_ref: string;
}

export interface LanguageDriftRow {
  run_id: string;
  day: number;
  turn_num: number;
  moment: string;
  season: string;
  avg_caquetio: number;
  avg_wayunaiki: number;
  avg_lokono: number;
  avg_taino: number;
  avg_proto_arahuaco: number;
  avg_score: number;
  agents_active: number;
}
