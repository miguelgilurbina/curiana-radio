// El arranque del hero 1a de Kaketiana («la palabra se arma»). Vive aparte
// porque lo leen el script en línea de la portada (servidor) y HeroPalabra
// (cliente): una constante exportada desde un módulo "use client" llega al
// servidor como referencia de cliente, no como texto.

/** sessionStorage: la secuencia corre una vez por visita. */
export const CLAVE_HERO = "kk-hero-1a";

/** El <style> que el script mete en <head> mientras la secuencia corre. */
export const ID_ESTILO_HERO = "kk-hero-oculto";

// Lo que se oculta mientras la secuencia corre: todo, hasta que React arranca
// (y a los 4 s se destapa igual, por si no arranca); después, sólo lo que
// todavía no amaneció.
const CSS_OCULTO =
  ".kk-hero:not([data-corriendo]) [data-paso]{opacity:0;animation:kk-hero-seguro 0s linear 4s forwards}" +
  ".kk-hero[data-corriendo] [data-paso]:not([data-visto]){opacity:0;transform:translateY(14px)}" +
  '.kk-hero[data-corriendo] [data-paso="signos"]:not([data-visto]){transform:none}';

/** Corre antes de pintar el hero. Inyecta el estilo en <head> —no toca nodos
 *  que React hidrata— sólo si toca: primera vez en la visita y sin
 *  prefers-reduced-motion. */
export const SCRIPT_HERO =
  "try{" +
  `if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&sessionStorage.getItem(${JSON.stringify(CLAVE_HERO)})!=="visto"){` +
  `var s=document.createElement("style");s.id=${JSON.stringify(ID_ESTILO_HERO)};` +
  `s.textContent=${JSON.stringify(CSS_OCULTO)};document.head.appendChild(s)}` +
  "}catch(e){}";
