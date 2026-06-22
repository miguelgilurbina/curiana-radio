import fs from "fs";
import path from "path";
import type { LanguageDriftRow } from "@/lib/supabase";

const SEED_PATH = path.join(process.cwd(), "content", "simulador", "resumen.json");

export interface ResumenSeed {
  run_id: string;
  started_at: string;
  ended_at: string | null;
  total_days: number | null;
  total_turns: number | null;
  model: string;
  avg_score: number | null;
  pct_caquetio_final: number | null;
  total_neologismos: number;
  total_adoptados: number;
  drift: LanguageDriftRow[];
}

export function getResumen(): ResumenSeed | null {
  try {
    const raw = fs.readFileSync(SEED_PATH, "utf-8");
    return JSON.parse(raw) as ResumenSeed;
  } catch {
    return null;
  }
}
