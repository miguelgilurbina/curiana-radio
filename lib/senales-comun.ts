// Lo de Señales que no toca el disco: las aristas, los tipos y el formato
// de fecha. Vive aparte de lib/senales.ts (que lee content/ con fs) para que
// los componentes de cliente —el filtro del índice— puedan importarlo.

export const ARISTAS = {
  kaketiana: { nombre: "Kaketiana", corto: "Kaketiana", href: "/kaketiana" },
  "jai-sounds": { nombre: "JAI Sounds", corto: "JAI Sounds", href: "/jai-sounds" },
  galeria: { nombre: "Galería", corto: "Galería", href: "/galeria" },
  // Buchibe todavía no tiene sección: la etiqueta existe, el enlace no.
  buchibe: { nombre: "Cuentos de Buchibe", corto: "Buchibe", href: null },
} as const satisfies Record<string, { nombre: string; corto: string; href: string | null }>;

export type Arista = keyof typeof ARISTAS;

export const esArista = (id: string): id is Arista => Object.prototype.hasOwnProperty.call(ARISTAS, id);

// El motor de pieles (components/senales/pieles/). La arista dice DÓNDE
// aparece una señal; la piel, CÓMO se ve. Cada arista trae su piel por
// defecto y una señal puede pedir otra en el frontmatter (`piel:`). Ésta es
// la lista de pieles registradas: una piel nueva se nombra aquí primero, y el
// registro no compila hasta que tenga su definición.
export const PIELES_IDS = ["radio", "kaketiana", "jai-sounds", "galeria", "buchibe"] as const;

export type PielId = (typeof PIELES_IDS)[number];

export const esPiel = (id: string): id is PielId => (PIELES_IDS as readonly string[]).includes(id);

/** La piel que trae cada arista si la señal no pide otra. */
export const PIEL_DE_ARISTA: Record<Arista, PielId> = {
  kaketiana: "kaketiana",
  "jai-sounds": "jai-sounds",
  galeria: "galeria",
  buchibe: "buchibe",
};

export interface Portada {
  src: string;
  alt: string;
  pie?: string;
}

export interface SenalResumen {
  slug: string;
  titulo: string;
  /** YYYY-MM-DD */
  fecha: string;
  sumario: string;
  aristas: Arista[];
  /** la piel resuelta: la pedida en el frontmatter, o la de su primera arista, o la radio */
  piel: PielId;
  portada: Portada | null;
  autor: string;
  minutos: number;
  borrador: boolean;
}

export interface Senal extends SenalResumen {
  cuerpo: string;
}

/** «3 oct 2026»: la fecha del dato, en listas y cabeceras. */
export function fechaCorta(iso: string): string {
  return new Intl.DateTimeFormat("es", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" })
    .format(new Date(`${iso}T00:00:00Z`))
    .replace(/\./g, "");
}

/** «3 de octubre de 2026», sin que el huso horario corra el día. */
export function fechaLarga(iso: string): string {
  return new Intl.DateTimeFormat("es", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }).format(
    new Date(`${iso}T00:00:00Z`),
  );
}
