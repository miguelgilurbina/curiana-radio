// La luz del lector: claro u oscuro. Cada vista tiene su modo nativo (la
// identidad de su manual: Kaketiana es la placa clara, JAI la cabina de
// noche) y, cuando su otro modo está diseñado, el lector puede cambiarla.
// La elección es del lector y vale para todo el sitio: se guarda en
// localStorage y se publica como `html[data-luz]`. Sin elección, cada vista
// en su modo nativo. Los tokens del otro modo viven en globals.css, bajo
// `html[data-luz="…"] [data-piel="…"]`. BRAND_MVP §12.

export type Luz = "claro" | "oscuro";

export const CLAVE_LUZ = "curiana:luz";
const EVENTO = "curiana:luz";

export const opuesta = (l: Luz): Luz => (l === "claro" ? "oscuro" : "claro");

/** La elección guardada, o null si el lector no eligió. */
export function luzElegida(): Luz | null {
  if (typeof document === "undefined") return null;
  const l = document.documentElement.dataset.luz;
  return l === "claro" || l === "oscuro" ? l : null;
}

export function elegirLuz(l: Luz) {
  document.documentElement.dataset.luz = l;
  try {
    localStorage.setItem(CLAVE_LUZ, l);
  } catch {
    // almacenamiento bloqueado: la luz cambia igual, sólo que no se recuerda
  }
  window.dispatchEvent(new Event(EVENTO));
}

/** Vuelve a la luz de cada sección: borra la elección del lector. */
export function olvidarLuz() {
  delete document.documentElement.dataset.luz;
  try {
    localStorage.removeItem(CLAVE_LUZ);
  } catch {
    // almacenamiento bloqueado: igual vuelve a la luz nativa en esta visita
  }
  window.dispatchEvent(new Event(EVENTO));
}

export function alCambiarLuz(avisar: () => void): () => void {
  window.addEventListener(EVENTO, avisar);
  return () => window.removeEventListener(EVENTO, avisar);
}

/** En línea en el <head>: publica la elección antes del primer pintado, para
 *  que una vista no nazca en su modo nativo y salte después. */
export const SCRIPT_LUZ = `(function(){try{var l=localStorage.getItem(${JSON.stringify(
  CLAVE_LUZ,
)});if(l==="claro"||l==="oscuro")document.documentElement.dataset.luz=l}catch(_){}})();`;
