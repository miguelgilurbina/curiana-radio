/**
 * La rotación del dial de JAI Sounds (manual de marca, pág. 05).
 *
 * 1. La semilla vive en sessionStorage: estable mientras se navega, distinta
 *    al volver otro día. Nunca aleatoria por render — el dial parpadearía.
 * 2. El círculo se parte en N sectores iguales y la semilla gira el conjunto:
 *    hue(i) = (semilla + i · 360/N) mod 360. Dos estaciones vecinas nunca
 *    caen en matices casi idénticos.
 * 3. El hue NO se guarda en playlists.json. El color no es propiedad de la
 *    estación; es su turno en el dial.
 *
 * El cálculo de verdad lo hace el CSS (`.jai-estacion` en globals.css) con
 * --jai-semilla; aquí solo se elige la semilla y se publica en la página.
 */

export const CLAVE_SEMILLA = "jai:semilla";
const ID_ESTILO = "jai-semilla";

/** Matiz de la estación `i` de `n`, en grados enteros (0-359). */
export function hueDeEstacion(semilla: number, i: number, n: number): number {
  return Math.round((semilla + (i * 360) / n) % 360);
}

/**
 * Escribe la semilla como regla CSS en <head>. Va por <style> y no por un
 * atributo de <html> porque React no toca los nodos que no renderizó en el
 * head — un atributo en <html> sí rompería la hidratación.
 */
function publicarSemilla(semilla: number) {
  let estilo = document.getElementById(ID_ESTILO);
  if (!estilo) {
    estilo = document.createElement("style");
    estilo.id = ID_ESTILO;
    document.head.appendChild(estilo);
  }
  estilo.textContent = `html [data-jai-theme]{--jai-semilla:${semilla}}`;
}

// La semilla no cambia mientras la página vive: se lee una vez.
let enMemoria: number | null = null;

/**
 * Lee la semilla de la sesión, o la sortea si es la primera visita, y la
 * publica en la página. Sirve de getSnapshot de useSyncExternalStore: tras
 * la primera llamada devuelve siempre el mismo número.
 */
export function semillaDeSesion(): number {
  if (enMemoria !== null) return enMemoria;
  let semilla = NaN;
  try {
    semilla = Number.parseInt(sessionStorage.getItem(CLAVE_SEMILLA) ?? "", 10);
    if (!(semilla >= 0 && semilla < 360)) {
      semilla = Math.floor(Math.random() * 360);
      sessionStorage.setItem(CLAVE_SEMILLA, String(semilla));
    }
  } catch {
    // sessionStorage bloqueado (modo privado estricto): el dial gira igual,
    // solo que no recuerda la vuelta al navegar.
    if (Number.isNaN(semilla)) semilla = Math.floor(Math.random() * 360);
  }
  publicarSemilla(semilla);
  enMemoria = semilla;
  return semilla;
}

/**
 * La misma lógica como script en línea, para que corra ANTES del primer
 * pintado en la carga inicial y el dial no nazca en el matiz de reserva y
 * salte después. En navegación de cliente el script no se re-ejecuta; ahí
 * lo cubre semillaDeSesion(), que el dial lee al renderizar.
 */
export const SCRIPT_SEMILLA = `(function(){try{var k=${JSON.stringify(
  CLAVE_SEMILLA
)},s=parseInt(sessionStorage.getItem(k),10);if(!(s>=0&&s<360)){s=Math.floor(Math.random()*360);sessionStorage.setItem(k,String(s))}var e=document.getElementById(${JSON.stringify(
  ID_ESTILO
)});if(!e){e=document.createElement("style");e.id=${JSON.stringify(
  ID_ESTILO
)};document.head.appendChild(e)}e.textContent="html [data-jai-theme]{--jai-semilla:"+s+"}"}catch(_){}})();`;
