import fs from "fs";
import path from "path";
import { getFichasSeed } from "@/lib/fichas";
import { getSerie, brazo, type SerieSeed } from "@/lib/serie";

// El abstract de disertación del experimento: pitch, resumen formal, los
// conceptos explicados en teoría plana, el flujo y los límites. El copy vive en
// content/simulador/abstract.json; las CIFRAS no se escriben ahí: el texto
// lleva marcas como {agentes} o {voces} que se rellenan aquí, en build, desde
// los seeds reales (la serie de la era 2 y las fichas del diccionario). Una
// marca que no tenga valor rompe el build: el texto no puede mentir en silencio
// cuando cambie un seed.
const ABSTRACT_PATH = path.join(process.cwd(), "content", "simulador", "abstract.json");

export interface ConceptoAbstract {
  id: string;
  termino: string;
  /** Definición de una línea, en itálica bajo el término. */
  lema: string;
  cuerpo: string;
  /** El dato del proyecto que aterriza el concepto (opcional). */
  dato?: string;
}

export interface PasoPipeline {
  titulo: string;
  sub: string;
}

/** Una frase dicha en la simulación, citada con su procedencia. La traducción
 *  es la glosa del propio personaje, no una nuestra. */
export interface FraseCitada {
  caquetio: string;
  traduccion: string;
  quien: string;
  lugar: string;
  run: string;
  dia: number;
  nota?: string;
}

export interface AbstractContent {
  version: number;
  pitch: {
    overline: string;
    /** La frase que el cronista tipea antes del titular. No se escribe en el
     *  JSON: es `frase`, una frase DICHA en la serie. */
    caquetio: string;
    traduccion: string;
    titulo: string;
    bajada: string;
  };
  frase: FraseCitada;
  abstract: string[];
  conceptos: ConceptoAbstract[];
  pipeline: PasoPipeline[];
  limites: string[];
  siguiente: string[];
  nota_honestidad: string;
}

function fail(msg: string): never {
  throw new Error(`abstract.json: ${msg}`);
}

/** Los valores de las marcas: todos medidos. */
export function valoresDelExperimento(serie: SerieSeed | null = getSerie()): Record<string, string> {
  const fichas = getFichasSeed();
  const escena = serie ? brazo(serie, "escena") : undefined;
  const control = serie ? brazo(serie, "control") : undefined;
  const nf = (n: number) => n.toLocaleString("es-VE");
  const v: Record<string, string> = {
    voces: nf(fichas.n),
    atestiguadas: nf(fichas.por_capa.atestiguado),
    reconstruidas: nf(fichas.por_capa.reconstruido),
    retroabstraidas: nf(fichas.por_capa.retroabstraido),
    hipoteticas: nf(fichas.por_capa.hipotetico),
  };
  if (serie?.elenco) {
    v.agentes = nf(serie.elenco.total);
    for (const [nodo, n] of Object.entries(serie.elenco.por_nodo)) v[`agentes_${nodo.toLowerCase()}`] = nf(n);
  }
  if (serie) {
    v.capubana_cada = String(serie.capubana.cada);
    v.brazos = String(serie.brazos.length);
  }
  if (escena) {
    v.dias = String(escena.dias);
    v.fijadas_escena = String(escena.fijadas.length);
    if (escena.competencia) {
      v.referentes = String(escena.competencia.referentes);
      if (escena.competencia.umbral != null) v.umbral_pct = String(Math.round(escena.competencia.umbral * 100));
    }
  }
  if (control) v.fijadas_control = String(control.fijadas.length);
  if (escena && control) v.respuestas = nf(escena.respuestas + control.respuestas);
  return v;
}

function rellenar(texto: string, valores: Record<string, string>, donde: string): string {
  return texto.replace(/\{([a-z_]+)\}/g, (_, clave: string) => {
    if (!(clave in valores)) fail(`la marca {${clave}} de ${donde} no tiene valor medido`);
    return valores[clave];
  });
}

/** Rellena todas las cadenas de un objeto JSON, recursivamente. */
function rellenarTodo<T>(obj: T, valores: Record<string, string>, donde = "abstract"): T {
  if (typeof obj === "string") return rellenar(obj, valores, donde) as T;
  if (Array.isArray(obj)) return obj.map((x, i) => rellenarTodo(x, valores, `${donde}[${i}]`)) as T;
  if (obj && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([k, x]) => [k, rellenarTodo(x, valores, `${donde}.${k}`)]),
    ) as T;
  }
  return obj;
}

export function getAbstract(): AbstractContent {
  const raw = JSON.parse(fs.readFileSync(ABSTRACT_PATH, "utf-8")) as AbstractContent;
  const content = rellenarTodo(raw, valoresDelExperimento());

  if (!content.frase?.caquetio || !content.frase.traduccion) {
    fail("frase.caquetio y frase.traduccion son obligatorios (los tipea el cronista)");
  }
  if (!content.frase.run || !content.frase.quien || !content.frase.dia) {
    fail("frase: hace falta quién la dijo, en qué run y qué día");
  }
  content.pitch = { ...content.pitch, caquetio: content.frase.caquetio, traduccion: content.frase.traduccion };
  if (!content.pitch?.titulo) fail("pitch.titulo es obligatorio");
  if (!content.abstract?.length) fail("abstract[] no puede estar vacío");
  if (!content.conceptos?.length) fail("conceptos[] no puede estar vacío");
  for (const c of content.conceptos) {
    if (!c.id || !c.termino || !c.lema || !c.cuerpo) {
      fail(`concepto incompleto: ${JSON.stringify(c.id ?? c.termino)}`);
    }
  }
  if (content.pipeline?.length !== 4) fail("pipeline[] debe tener 4 pasos");
  return content;
}
