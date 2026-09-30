import fs from "fs";
import path from "path";

// UNA SERIE DE LA ERA 2 — dos brazos, treinta días cada uno, mismas semillas.
//
// Lo genera `curiana_sim/export_serie_seed.py` desde Supabase LOCAL: la serie
// de la cadena y su veredicto (`curiana_cadena`), la brecha entre pueblos y las
// formas que cruzan (`analizar_nodos`), las palabras fijadas (`koine_lexicon`)
// y las disputas abiertas (el estado guardado al cerrar cada brazo). La página
// sólo lee este JSON: ninguna cifra del experimento se escribe a mano.
const SERIES_DIR = path.join(process.cwd(), "content", "simulador", "series");

/** La serie que la página del experimento cuenta hoy. */
export const SERIE_ACTUAL = "era2-base";

export interface DiaSerie {
  dia: number;
  /** Las tres lecturas de la distancia idiolectal media (0 = todos hablan igual). */
  acumulada: number | null;
  ventana: number | null;
  /** Sólo las formas nacidas en la simulación: la lectura del veredicto. */
  emergente: number | null;
  /** Distancia entre pueblos menos distancia dentro de cada pueblo
   *  (acumulada-emergente). Positiva = cada pueblo habla más parecido por dentro. */
  brecha: number | null;
  /** La emergente de SÓLO ese día, reconstruida de lo dicho (analizar_nodos):
   *  la que separa un día suelto, como el de Capubana. */
  emergente_dia: number | null;
  brecha_dia: number | null;
}

export interface FijadaSerie {
  concepto: string;
  descripcion: string;
  /** Tal como la guardó el motor (puede traer asteriscos: ver `formaLimpia`). */
  forma: string;
  dia: number | null;
  n_variantes: number | null;
  soporte: number | null;
}

export interface DisputaSerie {
  concepto: string;
  orden: number | null;
  descripcion: string;
  fijada: string | null;
  fijada_dia: number | null;
  n_variantes: number;
  rivales: { forma: string; soporte: number }[];
}

export interface BrazoSerie {
  clave: "escena" | "control";
  escena: boolean;
  capubana_cada: number;
  runs: { primero: string; ultimo: string; n: number };
  dias: number;
  semillas: (string | null)[];
  motor: { modelos: string[]; commits: string[]; sucios: number; sin_huella: number };
  respuestas: number;
  agentes: number;
  serie: DiaSerie[];
  veredicto: {
    lectura: string | null;
    codigo: string;
    mensaje: string;
    inicio: number | null;
    fin: number | null;
  };
  emergente_min: { dia: number; valor: number } | null;
  formas: {
    emergentes: number;
    clasificables: number;
    cruzaron: number;
    no_cruzaron: number;
    nacidas_en_los_dos: number;
  };
  fijadas: FijadaSerie[];
  competencia: {
    umbral: number | null;
    soporte_minimo: number | null;
    referentes: number;
    fijados: number;
    /** Todos los referentes, en el orden en que el mundo los presentó. */
    lista: DisputaSerie[];
  } | null;
}

interface PartidoCapubana {
  capubana: number | null;
  resto: number | null;
  n_capubana: number;
}

export interface SerieSeed {
  version: number;
  generado: string;
  serie: string;
  elenco: { total: number; por_nodo: Record<string, number> } | null;
  motor: string[];
  brazos: BrazoSerie[];
  capubana: {
    cada: number;
    dias: number[];
    emergente_dia: Partial<Record<"escena" | "control", PartidoCapubana>>;
    brecha_dia: Partial<Record<"escena" | "control", PartidoCapubana>>;
    /** De los días de Capubana, cuántos quedaron por debajo del día anterior. */
    bajan: Partial<Record<"escena" | "control", { bajan: number; de: number }>>;
  };
  avisos: string[];
}

export function getSerie(nombre: string = SERIE_ACTUAL): SerieSeed | null {
  const archivo = path.join(SERIES_DIR, `${nombre}.json`);
  if (!fs.existsSync(archivo)) return null;
  const seed = JSON.parse(fs.readFileSync(archivo, "utf-8")) as SerieSeed;
  if (seed.version !== 1) throw new Error(`${nombre}.json: versión ${seed.version} desconocida`);
  if (!seed.brazos?.length) throw new Error(`${nombre}.json: sin brazos`);
  return seed;
}

export function brazo(seed: SerieSeed, clave: "escena" | "control"): BrazoSerie | undefined {
  return seed.brazos.find((b) => b.clave === clave);
}

/** Los asteriscos de markdown que el modelo a veces pega a una forma son un
 *  defecto anotado del instrumento (`**x` y `x` reparten soporte). Se limpian
 *  SOLO al mostrar; el dato del seed queda como lo guardó el motor. */
export function formaLimpia(forma: string): string {
  return forma.replace(/\*/g, "").trim();
}

// Los ids del catálogo (6-fusion/referentes_era2.yaml) van sin tildes ni
// espacios. Esto es sólo cómo se escriben en castellano para el lector; lo que
// no esté aquí se muestra con los guiones bajos cambiados por espacios.
const NOMBRE_CASTELLANO: Record<string, string> = {
  tarantula_azul: "tarántula azul",
  delfin: "delfín",
  colibri: "colibrí",
};

/** «Tarántula azul» desde `tarantula_azul`. */
export function nombreDeConcepto(concepto: string): string {
  const n = NOMBRE_CASTELLANO[concepto] ?? concepto.replace(/_/g, " ");
  return n.charAt(0).toUpperCase() + n.slice(1);
}

/** Cuántos días la emergente del brazo con escena quedó por encima del control,
 *  y la diferencia media — la lectura de «la geografía sostiene la variación». */
export function ventajaEscena(seed: SerieSeed): { dias: number; de: number; media: number } | null {
  const e = brazo(seed, "escena");
  const c = brazo(seed, "control");
  if (!e || !c) return null;
  const control = new Map(c.serie.map((p) => [p.dia, p.emergente]));
  const pares = e.serie
    .map((p) => [p.emergente, control.get(p.dia)] as const)
    .filter((x): x is readonly [number, number] => x[0] != null && x[1] != null);
  if (!pares.length) return null;
  return {
    dias: pares.filter(([a, b]) => a > b).length,
    de: pares.length,
    media: pares.reduce((acc, [a, b]) => acc + (a - b), 0) / pares.length,
  };
}

/** Formato de cifra decimal a la venezolana: 0,1619. */
export function dec(x: number | null | undefined, n = 4): string {
  if (x == null) return "—";
  return x.toFixed(n).replace(".", ",");
}

/** Con signo: +0,0356 / −0,0027. */
export function decConSigno(x: number | null | undefined, n = 4): string {
  if (x == null) return "—";
  return `${x >= 0 ? "+" : "−"}${Math.abs(x).toFixed(n).replace(".", ",")}`;
}
