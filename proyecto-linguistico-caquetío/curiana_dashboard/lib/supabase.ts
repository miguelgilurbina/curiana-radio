import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// ── Tipos de las tablas Supabase ───────────────────────────────────────

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

// ── Colores canónicos por lengua ──────────────────────────────────────

export const LANG_COLORS: Record<string, string> = {
  caquetío:   "#C47A2B",
  wayunaiki:  "#2E7D4F",
  lokono:     "#5B4FCF",
  taíno:      "#B04040",
  "proto-arahuaco": "#6D8A9E",
};
