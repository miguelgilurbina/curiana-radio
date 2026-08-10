/**
 * Semilla del orden del mosaico.
 *
 * La galería se baraja en cada visita, pero la página es estática: si el
 * servidor barajara, el orden quedaría congelado en el build. Y barajar
 * durante el render del cliente rompería la hidratación, porque el HTML que
 * llega y el que React calcula dirían cosas distintas.
 *
 * Así que la semilla se modela como lo que es: un dato externo a React que
 * vale `null` en el servidor y un número en el navegador. Ese es justo el caso
 * de `useSyncExternalStore` — React renderiza el orden canónico para hidratar
 * y acto seguido conmuta al barajado, sin efectos que escriban estado.
 */

let semilla: number | null = null;
const suscriptores = new Set<() => void>();

function nuevaSemilla(): number {
  return (Math.random() * 0x7fffffff) | 0;
}

export function suscribirse(alCambiar: () => void): () => void {
  suscriptores.add(alCambiar);
  return () => {
    suscriptores.delete(alCambiar);
  };
}

/**
 * Snapshot en cliente. Se siembra en la primera lectura y luego es estable:
 * `useSyncExternalStore` exige que devolver dos veces seguidas dé lo mismo o
 * entra en bucle de renders.
 */
export function leerSemilla(): number {
  if (semilla === null) semilla = nuevaSemilla();
  return semilla;
}

/** Snapshot en servidor: sin semilla, orden curatorial del manifest. */
export function leerSemillaServidor(): null {
  return null;
}

/** Vuelve a barajar a petición del visitante. */
export function rebarajar(): void {
  semilla = nuevaSemilla();
  for (const alCambiar of suscriptores) alCambiar();
}
