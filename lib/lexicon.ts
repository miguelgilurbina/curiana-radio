import fs from "fs";
import path from "path";

const SEED_PATH = path.join(process.cwd(), "content", "simulador", "lexicon.json");

export interface PalabraLexicon {
  id: string;
  word: string;
  meaning: string;
  category: string | null;
  source_language: string;
  attested: boolean;
  source_ref: string | null;
}

export function getLexicon(): PalabraLexicon[] {
  let raw: string;
  try {
    raw = fs.readFileSync(SEED_PATH, "utf-8");
  } catch (err) {
    // Seed no generado todavía (ej. clon nuevo del repo, antes de correr
    // export_lexicon_seed.py) -- estado vacío legítimo, no un bug.
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw err;
  }
  // JSON malformado SÍ debe fallar el build -- no disfrazarlo de "sin datos".
  return (JSON.parse(raw).palabras as PalabraLexicon[]) ?? [];
}
