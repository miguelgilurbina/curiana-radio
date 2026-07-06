import fs from "fs";
import path from "path";
import matter from "gray-matter";

// La voz de Manaure: fragmentos MDX curados en content/simulador/manaure/.
// Cada archivo trae dos voces — el narrador (frontmatter, 3ª persona) y
// Manaure (cuerpo, 1ª persona). El binding fragmento→sección lo decide
// content/simulador/editorial.json, no el fragmento.
const MANAURE_DIR = path.join(process.cwd(), "content", "simulador", "manaure");

export const TIPOS_VOZ = ["reconstruido", "hipotetico", "imaginado"] as const;
export type TipoVoz = (typeof TIPOS_VOZ)[number];

export interface ManaureFragment {
  id: string; // slug = nombre de archivo sin .mdx
  tipo: TipoVoz;
  narrador?: string; // marco en 3ª persona, sobrio
  caquetio?: string; // línea en caquetío reconstruido
  traduccion?: string;
  contexto?: string; // referencia en tiempo del mundo, nunca del proyecto
  body: string; // la voz de Manaure (MDX)
}

function parseFragment(filePath: string): ManaureFragment {
  const id = path.basename(filePath, ".mdx");
  const { data, content } = matter(fs.readFileSync(filePath, "utf-8"));

  // Un fragmento sin tipo válido rompe la marca de honestidad intelectual:
  // mejor fallar el build que publicar voz sin etiqueta.
  if (!TIPOS_VOZ.includes(data.tipo)) {
    throw new Error(
      `manaure/${id}.mdx: frontmatter "tipo" debe ser uno de ${TIPOS_VOZ.join(" | ")} (recibido: ${JSON.stringify(data.tipo)})`
    );
  }

  return {
    id,
    tipo: data.tipo,
    narrador: data.narrador,
    caquetio: data.caquetio,
    traduccion: data.traduccion,
    contexto: data.contexto,
    body: content.trim(),
  };
}

export function getAllManaureFragments(): ManaureFragment[] {
  let files: string[];
  try {
    files = fs.readdirSync(MANAURE_DIR).filter((f) => f.endsWith(".mdx"));
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw err;
  }
  return files.map((f) => parseFragment(path.join(MANAURE_DIR, f)));
}

export function getManaureFragment(id: string): ManaureFragment | null {
  return getAllManaureFragments().find((f) => f.id === id) ?? null;
}
