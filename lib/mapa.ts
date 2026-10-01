import fs from "fs";
import path from "path";

// EL MAPA DE LA PORTADA — los topónimos del canon con lugar en el mapa vivo.
// Lo genera `curiana_sim/export_mapa_seed.py` cruzando `2-lengua/toponimos.yaml`
// con `6-fusion/toponimos_mapa_kaketiana.yaml` (OpenStreetMap). La página sólo
// lee este JSON.
const MAPA_PATH = path.join(process.cwd(), "content", "wiki", "mapa.json");

/** La lectura del nombre, no su existencia: A cierra con morfemas
 *  atestiguados, B exige un morfema despejado, C es plausible, «sin» no tiene
 *  lectura (el «descartado» del canon: se descartó la lectura, no el lugar). */
export type NivelLectura = "A" | "B" | "C" | "sin";

export interface PuntoMapa {
  id: string;
  forma: string;
  nombre_en_el_mapa: string;
  tipo: string | null;
  lat: number;
  lon: number;
  region: string;
  nivel: NivelLectura;
  cruce: "exacto" | "forma-viva" | "parcial";
  glosa: string | null;
  /** Sólo en «sin»: por qué no hay lectura, dicho desde la razón del canon. */
  motivo: string | null;
  obra: string | null;
}

export interface MapaSeed {
  version: number;
  generado: string;
  fuente_mapa: string | null;
  licencia: string | null;
  resumen: {
    puntos: number;
    toponimos_con_lugar: number;
    toponimos_canon: number;
    por_nivel: Record<NivelLectura, number>;
    puntos_por_region: Record<string, number>;
  };
  puntos: PuntoMapa[];
}

export function getMapa(): MapaSeed | null {
  if (!fs.existsSync(MAPA_PATH)) return null;
  const seed = JSON.parse(fs.readFileSync(MAPA_PATH, "utf-8")) as MapaSeed;
  if (seed.version !== 1) throw new Error(`mapa.json: versión ${seed.version} desconocida`);
  return seed;
}
