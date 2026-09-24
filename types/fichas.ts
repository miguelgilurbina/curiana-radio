/**
 * Las fichas de palabra y «Lo que no sabemos».
 *
 * Los dos JSON los generan los exportadores del vault
 * (`curiana_sim/export_fichas_seed.py` y `export_no_sabemos_seed.py`) desde
 * el lexicón y las mediciones. No se editan a mano, y el front no escribe
 * ninguna cifra: todas vienen de aquí.
 */

/** Las cuatro capas epistémicas del caquetío — la marca de la casa. */
export type Capa = "atestiguado" | "reconstruido" | "retroabstraido" | "hipotetico";

export interface CapaInfo {
  fuente: string;
  etiqueta: string;
  /** Qué es, en una frase. */
  que_es: string;
  /** Qué es lo incierto de una voz de esta capa. */
  incierto: string;
}

export interface CitaFicha {
  /** Slug de la obra en la bibliografía; null si el vault no la tiene. */
  obra: string | null;
  titulo: string;
  /** true si la obra tiene ancla en /kaketiana/bibliografia. */
  enlace: boolean;
  /** «p. 74», «#273 (AM)», «pliego 32 izq.»… */
  localizadores: string[];
}

export interface HermanaFicha {
  lengua: string;
  /** false = «cognado en X» sin obra: se muestra y se dice. */
  citada: boolean;
}

export interface Ficha {
  slug: string;
  forma: string;
  /** La grafía de la fuente, si difiere del lema («cazi» para kasi). */
  forma_fuente: string | null;
  glosa: string;
  /** La glosa tal como la escribe la fuente, si dice algo más. */
  glosa_fuente: string | null;
  categoria: string | null;
  capa: Capa;
  citas: CitaFicha[];
  hermanas: HermanaFicha[];
  /** compuesto = del proyecto sobre piezas con fuente; acunacion = sin cita. */
  origen: "compuesto" | "acunacion" | null;
  /** La nota dice que ninguna hermana le da pareja. */
  sin_pareja: boolean;
  /** La voz retirada en cuyo lugar entró. */
  sustituye: { forma: string; ancla: string | null; glosa: string | null }[];
  /** Hueco declarado: lo llena la corrida base. */
  en_la_simulacion: null;
}

export interface Retirada {
  forma: string;
  ancla: string;
  glosa: string;
  /** Su capa, intacta: archivar no es degradar. null si no era caquetía. */
  capa: Capa | null;
  lengua: string | null;
  fecha: string | null;
  motivo: string;
  motivo_texto: string;
  sustitutas: { forma: string; slug: string | null }[];
}

export interface FichasSeed {
  generado: string;
  fuente_de_verdad: string;
  n: number;
  por_capa: Record<Capa, number>;
  con_cita: number;
  capas: Record<Capa, CapaInfo>;
  /** Siglas del glosario de Zavala Reyes 2015 → quién aportó la voz. */
  siglas_zavala: Record<string, string>;
  pendiente_de_la_corrida_base: string[];
  fichas: Ficha[];
  retiradas: Retirada[];
}

/** Lo mínimo de una ficha para el índice del diccionario (viaja al cliente). */
export type FichaIndice = Pick<Ficha, "slug" | "forma" | "glosa" | "capa">;

// ── Lo que no sabemos ────────────────────────────────────────────────

export interface FuenteMedida {
  /** Ruta dentro del repo del proyecto. */
  ruta: string;
  que: string;
  fecha: string | null;
}

export interface PreguntaAbierta {
  slug: string;
  pregunta: string;
  planteamiento: string;
  /** Frases con las cifras ya puestas por el exportador. */
  medido: string[];
  barras?: {
    titulo: string;
    filas: { etiqueta: string; valor: number; detalle: string; n: number }[];
  };
  lo_que_falta: string;
  estado: "abierta" | "espera-la-corrida-base";
  fuentes: FuenteMedida[];
  enlaces: { href: string; texto: string }[];
}

export interface NoSabemosSeed {
  generado: string;
  n: number;
  preguntas: PreguntaAbierta[];
  /** Preguntas que no salieron porque su fuente cambió. */
  faltan: string[];
}
