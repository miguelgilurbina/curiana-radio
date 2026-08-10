/**
 * Motor del mosaico de la galería.
 *
 * Reparte las obras en filas justificadas: cada fila ocupa el ancho exacto del
 * contenedor y su altura sale de las proporciones reales de las imágenes que
 * le tocaron. Es lo que hace que la grilla se lea como un tejido y no como una
 * cuadrícula — el tamaño de cada pieza lo decide su forma, no una celda fija.
 *
 * Módulo puro: sin DOM, sin `fs`. Lo importan tanto el servidor como el
 * cliente, y se puede probar llamándolo con números.
 */

import type { ObraGrid } from "@/types/galeria";

// ── Aleatoriedad reproducible ─────────────────────────────────────────

/** djb2. Determinista y estable entre servidor y cliente. */
export function hashTexto(texto: string): number {
  let h = 5381;
  for (let i = 0; i < texto.length; i++) {
    h = (h * 33) ^ texto.charCodeAt(i);
  }
  return Math.abs(h);
}

/** mulberry32: PRNG de 32 bits, suficiente para barajar y sembrable. */
function generador(semilla: number): () => number {
  let a = semilla >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Fisher-Yates sembrado. Con semilla explícita porque el orden tiene que ser
 * el mismo dentro de una visita (filtrar no debe rebarajar la galería) y
 * distinto entre visitas.
 */
export function mezclar<T>(items: readonly T[], semilla: number): T[] {
  const azar = generador(semilla);
  const copia = [...items];
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(azar() * (i + 1));
    [copia[i], copia[j]] = [copia[j], copia[i]];
  }
  return copia;
}

// ── Proporciones ──────────────────────────────────────────────────────

/**
 * Proporciones plausibles para obras que todavía no tienen render. El mosaico
 * necesita un aspecto para colocar la pieza; usar 4:5 en todas dejaría una
 * franja de huecos idénticos que delata el estado pendiente como un bug.
 * Se elige por hash del slug: la misma obra ocupa siempre la misma forma.
 */
const ASPECTOS_PENDIENTE = [16 / 9, 4 / 5, 1, 3 / 2, 21 / 9, 4 / 3];

export function aspectoDeObra(obra: ObraGrid): number {
  if (obra.w && obra.h) return obra.w / obra.h;
  return ASPECTOS_PENDIENTE[hashTexto(obra.slug) % ASPECTOS_PENDIENTE.length];
}

/**
 * Aparta las variantes hermanas de una misma generación.
 *
 * Midjourney devuelve cuatro imágenes casi idénticas por prompt. Publicadas
 * las cuatro, un barajado normal las deja caer contiguas cada tanto y el
 * mosaico parece un error de repetición. Esto recorre el orden ya barajado y,
 * cuando una pieza choca con una hermana dentro de las `distancia` anteriores,
 * la intercambia por la primera de más adelante que no choque.
 *
 * Es una reparación, no una reordenación: el azar del barajado se conserva
 * salvo en los pocos puntos donde hacía falta. Si no hay candidato limpio, se
 * deja como está — mejor una repetición que un orden retorcido.
 */
export function separarHermanas<T>(
  items: readonly T[],
  claveDe: (item: T) => string | undefined,
  distancia = 6
): T[] {
  const salida = [...items];
  const chocaConVentana = (clave: string | undefined, hasta: number) => {
    if (!clave) return false;
    for (let k = Math.max(0, hasta - distancia); k < hasta; k++) {
      if (claveDe(salida[k]) === clave) return true;
    }
    return false;
  };

  for (let i = 0; i < salida.length; i++) {
    if (!chocaConVentana(claveDe(salida[i]), i)) continue;
    for (let j = i + 1; j < salida.length; j++) {
      if (!chocaConVentana(claveDe(salida[j]), i)) {
        [salida[i], salida[j]] = [salida[j], salida[i]];
        break;
      }
    }
  }
  return salida;
}

// ── Composición en filas justificadas ─────────────────────────────────

export interface Celda<T> {
  item: T;
  ancho: number;
  alto: number;
}

export interface Fila<T> {
  celdas: Celda<T>[];
  alto: number;
  /** La última fila puede quedar corta: no se estira para no inflar piezas. */
  completa: boolean;
}

export interface OpcionesMosaico {
  /** Altura a la que tienden las filas. El motor se desvía para justificar. */
  alturaObjetivo: number;
  /** Separación entre piezas. Pequeña a propósito: el tejido es el punto. */
  gap: number;
}

/**
 * Reparte `items` en filas que ocupan `ancho` exacto.
 *
 * Greedy: se van sumando piezas a la fila hasta que estirarla al ancho del
 * contenedor la dejaría más baja que `alturaObjetivo`; ahí se cierra. Es el
 * mismo criterio de las galerías justificadas clásicas, y basta: el óptimo
 * global (partición lineal) no se nota a simple vista y cuesta O(n²).
 */
export function componerFilas<T>(
  items: readonly T[],
  ancho: number,
  aspectoDe: (item: T) => number,
  { alturaObjetivo, gap }: OpcionesMosaico
): Fila<T>[] {
  if (ancho <= 0 || items.length === 0) return [];

  const filas: Fila<T>[] = [];
  let actual: T[] = [];
  let sumaAspectos = 0;

  const cerrar = (completa: boolean) => {
    if (actual.length === 0) return;
    const anchoUtil = ancho - gap * (actual.length - 1);
    // Altura que justifica la fila. Si la fila quedó corta (la última), no se
    // estira: se respeta alturaObjetivo y se deja el borde derecho irregular.
    const alto = completa
      ? anchoUtil / sumaAspectos
      : Math.min(alturaObjetivo, anchoUtil / sumaAspectos);

    let acumulado = 0;
    const celdas = actual.map((item, i) => {
      const esUltima = i === actual.length - 1;
      // El redondeo se salda en la última pieza para que la suma dé el ancho
      // exacto; si no, quedan hilos de fondo de 1px entre columnas.
      const anchoCelda =
        completa && esUltima
          ? anchoUtil - acumulado
          : Math.round(alto * aspectoDe(item));
      acumulado += anchoCelda;
      return { item, ancho: anchoCelda, alto };
    });

    filas.push({ celdas, alto, completa });
    actual = [];
    sumaAspectos = 0;
  };

  for (const item of items) {
    actual.push(item);
    sumaAspectos += aspectoDe(item);
    const anchoUtil = ancho - gap * (actual.length - 1);
    if (anchoUtil / sumaAspectos <= alturaObjetivo) cerrar(true);
  }
  cerrar(false);

  return filas;
}

/**
 * Altura objetivo por ancho de viewport. En móvil una fila justificada de
 * varias piezas las dejaría diminutas, así que las filas se hacen altas: el
 * motor acaba poniendo una o dos por fila sin necesidad de un caso especial.
 */
export function alturaObjetivoPara(ancho: number): number {
  if (ancho < 480) return 260;
  if (ancho < 768) return 240;
  if (ancho < 1280) return 300;
  return 340;
}
